#!/usr/bin/env python3
"""Descobre, valida e registra fontes específicas para toda a central."""

from __future__ import annotations

import argparse
import html
import json
import math
import re
import ssl
import time
import unicodedata
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, quote_plus, unquote, urlparse, urlunparse
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from prune_weak_indexed_sources import source_is_specific


ROOT = Path(__file__).resolve().parents[1]
AGENDA_PATH = ROOT / "content/events/agenda-comunitaria-2026.json"
CALENDAR_PATH = ROOT / "content/calendar/cbm-2026.json"
COMPETITIONS_DIR = ROOT / "content/competitions"
CACHE_PATH = ROOT / "content/research/source-discovery-2026.json"
USER_AGENT = "Mozilla/5.0 (compatible; TVDUASRODAS-EditorialAudit/1.0; +https://tvduasrodas.com/)"
STOP = {
    "anos", "ano", "dos", "das", "do", "da", "de", "em", "the", "2026",
}
EXCLUDED_DOMAINS = {
    "tvduasrodas.com", "search.brave.com", "google.com", "bing.com", "youtube.com",
    "youtu.be", "pinterest.com", "tiktok.com",
}
GENERIC_SINGLETONS = {
    "beneficente", "evento", "encontro", "motofest", "motorock", "motofesta",
    "motocafe", "missa", "passeio", "aniversario", "confraternizacao", "festa",
}
NEWS_MARKERS = ("noticias", "news", "jornal", "portal", "gazeta", "diario")
PRIMARY_MARKERS = (
    "cbm.esp.br", "cbc.esp.br", "uci.org", "fim-moto.com", "motogp.com", "worldsbk.com",
    "instagram.com", "facebook.com", "sympla.com.br", "ticket", "inscri", "agendaoffroad.com.br",
)


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[dict[str, str]] = []
        self.href = ""
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "a":
            self.href = dict(attrs).get("href") or ""
            self.parts = []

    def handle_data(self, data: str) -> None:
        if self.href:
            self.parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self.href:
            self.links.append({"url": html.unescape(self.href), "label": " ".join(self.parts).strip()})
            self.href = ""
            self.parts = []


class TextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style", "noscript", "svg"}:
            self.skip += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript", "svg"} and self.skip:
            self.skip -= 1

    def handle_data(self, data: str) -> None:
        if not self.skip:
            value = " ".join(data.split())
            if value:
                self.parts.append(value)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFKD", str(value or ""))
    value = "".join(char for char in value if not unicodedata.combining(char))
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def tokens(value: str) -> set[str]:
    return {token for token in normalize(value).split() if len(token) >= 3 and token not in STOP}


def indexed_result_is_specific(data: dict[str, Any], source: dict[str, Any]) -> bool:
    """Exige identidade no título/URL; não aceita coincidência escondida no snippet."""
    title_tokens = tokens(data.get("title", ""))
    if not title_tokens:
        return False
    identity_words = set(normalize(f"{source.get('label', '')} {source.get('url', '')}").split())
    matched = sum(token in identity_words for token in title_tokens)
    city_words = set(normalize(data.get("city", "")).split())
    city_match = bool(city_words and city_words <= identity_words)
    year_match = "2026" in identity_words
    start_date = str(data.get("start_date") or "")
    date_digits = re.sub(r"\D", "", start_date)
    date_parts = start_date.split("-")
    date_dmy = "".join(reversed(date_parts)) if len(date_parts) == 3 else ""
    indexed_digits = re.sub(r"\D", "", f"{source.get('label', '')} {source.get('url', '')}")
    date_match = bool(
        (date_digits and date_digits in indexed_digits)
        or (date_dmy and date_dmy in indexed_digits)
    )
    identity_threshold = (
        len(title_tokens)
        if len(title_tokens) <= 3
        else max(3, math.ceil(len(title_tokens) * 0.7))
    )
    identity_match = matched >= identity_threshold
    contact_numbers = [
        re.sub(r"\D", "", number)
        for number in re.findall(
            r"(?:\(?\d{2}\)?\s*)?(?:9\s*)?\d{4}[\s.-]*\d{4}",
            str(data.get("contact") or ""),
        )
    ]
    contact_numbers = [number for number in contact_numbers if len(number) >= 8]
    phone_match = any(number in indexed_digits for number in contact_numbers)
    if len(title_tokens) == 1 and next(iter(title_tokens)) in GENERIC_SINGLETONS:
        return identity_match and city_match and (date_match or phone_match)
    return identity_match and (city_match or date_match or phone_match)


def domain(url: str) -> str:
    return urlparse(str(url or "")).netloc.lower().removeprefix("www.")


def excluded_domain(host: str) -> bool:
    return (
        host in EXCLUDED_DOMAINS
        or host == "yahoo.com"
        or host.endswith(".yahoo.com")
    )


def clean_url(url: str) -> str:
    parsed = urlparse(html.unescape(url))
    if parsed.scheme not in {"http", "https"}:
        return ""
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path.rstrip("/") or "/", "", parsed.query, ""))


def fetch(url: str, timeout: int = 18, retries: int = 0) -> str:
    for attempt in range(retries + 1):
        request = Request(url, headers={"User-Agent": USER_AGENT, "Accept-Language": "pt-BR,pt;q=0.9"})
        context = ssl.create_default_context()
        try:
            with urlopen(request, timeout=timeout, context=context) as response:
                content_type = response.headers.get("Content-Type", "")
                if "text" not in content_type and "html" not in content_type and "xml" not in content_type:
                    return ""
                raw = response.read(1_500_000)
                charset = response.headers.get_content_charset() or "utf-8"
                return raw.decode(charset, errors="replace")
        except HTTPError as exc:
            if exc.code != 429 or attempt >= retries:
                raise
            retry_after = exc.headers.get("Retry-After")
            wait = float(retry_after) if retry_after and retry_after.isdigit() else (6.0 * (attempt + 1))
            time.sleep(wait)
    return ""


def search(query: str) -> list[dict[str, str]]:
    """Consulta a saída HTML do Yahoo e devolve os destinos, não os redirecionadores."""
    url = f"https://search.yahoo.com/search?p={quote_plus(query)}"
    parser = LinkParser()
    parser.feed(fetch(url, retries=1))
    results: list[dict[str, str]] = []
    seen: set[str] = set()
    for link in parser.links:
        raw_url = link["url"]
        match = re.search(r"/RU=([^/]+)", raw_url)
        if match:
            raw_url = unquote(match.group(1))
        elif raw_url.startswith("/"):
            continue
        url = clean_url(raw_url)
        host = domain(url)
        if not url or excluded_domain(host) or url in seen:
            continue
        if any(url.lower().endswith(ext) for ext in (".jpg", ".jpeg", ".png", ".webp", ".svg")):
            continue
        seen.add(url)
        results.append({"url": url, "label": link["label"] or host})
    return results


def page_text(url: str) -> str:
    try:
        parser = TextParser()
        parser.feed(fetch(url))
        return " ".join(parser.parts)[:120_000]
    except Exception:
        return ""


def relevance(data: dict[str, Any], candidate: dict[str, str], text: str) -> int:
    title_tokens = tokens(data.get("title", ""))
    haystack = normalize(f"{candidate.get('label', '')} {candidate.get('url', '')} {text[:30000]}")
    haystack_words = set(haystack.split())
    matched = sum(token in haystack_words for token in title_tokens)
    city = normalize(data.get("city", ""))
    state = normalize(data.get("state", ""))
    score = matched * 5
    score += 3 if city and city in haystack else 0
    score += 1 if state and re.search(rf"\b{re.escape(state)}\b", haystack) else 0
    score += 2 if "2026" in haystack else 0
    score += 2 if str(data.get("start_date", ""))[:4] in haystack else 0
    if title_tokens and matched == len(title_tokens):
        score += 5
    return score


def supports(text: str, url: str) -> str:
    normalized = normalize(text)
    facts: list[str] = []
    patterns = (
        ("data e edição", r"\b2026\b|janeiro|fevereiro|marco|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro"),
        ("local", r"\bendereco\b|\blocal\b|\bcidade\b|\barena\b|\bparque\b|\bpraca\b"),
        ("horários e programação", r"\bhorario\b|\bprogramacao\b|\blargada\b|\bshow\b|\bcongresso tecnico\b"),
        ("inscrições e acesso", r"\binscri|\bingresso|\bentrada\b|\blote\b"),
        ("categorias, percurso ou regulamento", r"\bcategoria|\bpercurso|\bkm\b|\bregulamento\b"),
        ("resultados ou classificação", r"\bresultado|\bclassificacao|\branking\b|\bpontuacao\b"),
        ("organização e contatos", r"\borganiza|\brealiza|\bcontato\b|\bwhatsapp\b"),
    )
    for label, pattern in patterns:
        if re.search(pattern, normalized):
            facts.append(label)
    if not facts and any(marker in domain(url) for marker in ("instagram.com", "facebook.com")):
        facts.append("divulgação do organizador e material visual")
    return ", ".join(facts[:5]) or "existência e identificação específica do evento"


def source_type(url: str) -> str:
    host = domain(url)
    if host.endswith(".gov.br") or ".gov." in host:
        return "fonte institucional pública"
    if any(marker in host for marker in PRIMARY_MARKERS):
        return "fonte primária ou canal oficial"
    if any(marker in host for marker in NEWS_MARKERS):
        return "cobertura jornalística"
    return "fonte específica independente"


def seed_sources(data: dict[str, Any]) -> list[dict[str, str]]:
    seeded: list[dict[str, str]] = []
    for key, label in (
        ("official_url", "Canal oficial ou página indicada pela entidade"),
        ("results_url", "Resultados oficiais"),
        ("source_url", "Fonte original do registro"),
    ):
        url = clean_url(str(data.get(key) or ""))
        if url:
            is_specific_flyer = (
                domain(url) == "jb-rider.com.br"
                and ("/evento/" in url or ("/eventos/" in url and not url.endswith("/eventos.php")))
            )
            seeded.append({
                "url": url,
                "label": "Flyer ou página específica original do evento" if is_specific_flyer else label,
                "type": "evidência visual primária" if is_specific_flyer else source_type(url),
                "supports": (
                    "data, cidade, identidade e informações legíveis no flyer específico"
                    if is_specific_flyer else "dados de agenda, identificação e situação do evento"
                ),
            })
    visual = data.get("visual_verification") or {}
    for key in ("detail_url", "source_url"):
        url = clean_url(str(visual.get(key) or ""))
        if url:
            seeded.append({
                "url": url,
                "label": "Flyer ou página visual inspecionada",
                "type": "evidência visual primária",
                "supports": "dados legíveis no material visual associado ao evento",
            })
    for source in data.get("sources") or []:
        if isinstance(source, dict) and source.get("url"):
            host = domain(str(source.get("url") or ""))
            failed_specificity_recheck = (
                source.get("discovery_method") == "busca_editorial_indexada"
                and not source_is_specific(data, source)
            )
            if excluded_domain(host) or failed_specificity_recheck:
                continue
            seeded.append(source)
    return seeded


def deduplicate_sources(sources: list[dict[str, Any]], max_per_domain: int = 2) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    seen_urls: set[str] = set()
    per_domain: dict[str, int] = {}
    for source in sources:
        url = clean_url(str(source.get("url") or ""))
        host = domain(url)
        if not url or not host or url in seen_urls or per_domain.get(host, 0) >= max_per_domain:
            continue
        seen_urls.add(url)
        per_domain[host] = per_domain.get(host, 0) + 1
        copy = dict(source)
        copy["url"] = url
        result.append(copy)
    return result


def records() -> list[tuple[str, Path, int | None, dict[str, Any]]]:
    result: list[tuple[str, Path, int | None, dict[str, Any]]] = []
    agenda = read_json(AGENDA_PATH)
    for index, entry in enumerate(agenda.get("entries", [])):
        if not entry.get("duplicate_of"):
            result.append(("agenda", AGENDA_PATH, index, entry))
    calendar = read_json(CALENDAR_PATH)
    for index, entry in enumerate(calendar.get("entries", [])):
        result.append(("calendar", CALENDAR_PATH, index, entry))
    for path in sorted(COMPETITIONS_DIR.glob("*.json")):
        if path.name != "index.json":
            result.append(("competition", path, None, read_json(path)))
    for path in sorted((ROOT / "content/events").glob("*.json")):
        if path.name not in {"index.json", "agenda-comunitaria-2026.json"}:
            result.append(("event", path, None, read_json(path)))
    return result


def record_key(kind: str, path: Path, index: int | None, data: dict[str, Any]) -> str:
    return str(data.get("slug") or f"{kind}:{path.stem}:{index if index is not None else ''}:{data.get('title', '')}")


def save_record(path: Path, index: int | None, data: dict[str, Any]) -> None:
    if index is None:
        write_json(path, data)
        return
    payload = read_json(path)
    payload["entries"][index] = data
    payload["last_updated"] = datetime.now(timezone.utc).isoformat()
    write_json(path, payload)


def research_one(data: dict[str, Any], strategy: str = "default") -> dict[str, Any]:
    title = normalize(data.get("title", ""))
    city = normalize(data.get("city", ""))
    state = data.get("state", "")
    start_parts = str(data.get("start_date") or "").split("-")
    dmy = "/".join(reversed(start_parts)) if len(start_parts) == 3 else ""
    queries = [f'"{title}" {city} {state} 2026']
    if strategy == "alternate":
        queries = [
            f'"{title}" "{city}" "{dmy}"',
            f'site:instagram.com "{title}" "{city}" 2026',
            f'site:facebook.com "{title}" "{city}" 2026',
        ]
    elif strategy == "contact":
        contact = str(data.get("contact") or "")
        phones = re.findall(r"\(?\d{2}\)?\s*\d{4,5}[-\s.]?\d{4}", contact)
        phone = phones[0] if phones else ""
        organizer = normalize(data.get("organizer", ""))
        venue = normalize(data.get("venue", ""))
        queries = []
        if phone:
            queries.extend(
                [
                    f'"{title}" "{phone}"',
                    f'"{phone}" "{city}"',
                ]
            )
        if organizer and "nao " not in organizer:
            queries.append(f'"{organizer}" "{city}"')
        if venue and "nao " not in venue and "local detalhado" not in venue:
            queries.append(f'"{title}" "{venue}" "{city}"')
        if not queries:
            queries = [f'{title} {city} {state} moto clube evento 2026']
    discovered: list[dict[str, Any]] = []
    seeded = seed_sources(data)
    seeded_specific_domains = {
        domain(source.get("url", "")) for source in seeded
        if "jb-rider.com.br/eventos.php" not in str(source.get("url") or "")
        and "/modalidades/calendario/busca/" not in str(source.get("url") or "")
    }
    title_tokens = tokens(data.get("title", ""))
    generic_singleton = (
        len(title_tokens) == 1
        and next(iter(title_tokens), "") in GENERIC_SINGLETONS
    )
    candidates: list[dict[str, str]] = []
    if len(seeded_specific_domains) < 2 and not (generic_singleton and strategy == "default"):
        seen_candidates: set[str] = set()
        for query in queries:
            try:
                query_results = search(query)
            except Exception:
                query_results = []
            for candidate in query_results:
                if candidate["url"] not in seen_candidates:
                    seen_candidates.add(candidate["url"])
                    candidates.append(candidate)
    inspected_candidates = 0
    for candidate in candidates[:20]:
        host = domain(candidate["url"])
        if host in {"jb-rider.com.br"}:
            continue
        title_tokens = tokens(data.get("title", ""))
        candidate_haystack = normalize(f"{candidate.get('label', '')} {candidate.get('url', '')}")
        preliminary_words = set(candidate_haystack.split())
        preliminary_matches = sum(token in preliminary_words for token in title_tokens)
        if preliminary_matches < min(2, len(title_tokens)) or not title_tokens:
            continue
        candidate_for_validation = {
            **candidate,
            "type": source_type(candidate["url"]),
            "discovery_method": "busca_editorial_indexada",
        }
        if not source_is_specific(data, candidate_for_validation):
            continue
        inspected_candidates += 1
        indexed_specific = indexed_result_is_specific(data, candidate)
        text = (
            ""
            if domain(candidate["url"]) in {"instagram.com", "facebook.com"}
            else page_text(candidate["url"])
        )
        score = relevance(data, candidate, text)
        minimum = 10 if len(tokens(data.get("title", ""))) >= 2 else 8
        full_haystack = normalize(f"{candidate.get('label', '')} {candidate.get('url', '')} {text[:30000]}")
        full_words = set(full_haystack.split())
        if sum(token in full_words for token in title_tokens) < min(2, len(title_tokens)):
            continue
        if score < minimum and not indexed_specific:
            continue
        if not indexed_specific:
            if not indexed_result_is_specific(
                data,
                {"label": full_haystack, "url": candidate["url"]},
            ):
                continue
        discovered.append({
            "url": candidate["url"],
            "label": candidate["label"][:180] or host,
            "type": source_type(candidate["url"]),
            "supports": supports(text or candidate["label"], candidate["url"]),
            "relevance_score": score,
            "discovery_method": "busca_editorial_indexada",
        })
        if len({domain(item["url"]) for item in discovered}) >= 3 or inspected_candidates >= 6:
            break
    sources = deduplicate_sources(seeded + sorted(discovered, key=lambda item: -item["relevance_score"]))
    specific_domains = {
        domain(source["url"]) for source in sources
        if "jb-rider.com.br/eventos.php" not in source["url"]
        and "/modalidades/calendario/busca/" not in source["url"]
    }
    data["sources"] = sources
    data["source_checked_at"] = datetime.now(timezone.utc).isoformat()
    data["research_status"] = {
        "required_specific_independent_sources": 2,
        "specific_independent_domains_found": len(specific_domains),
        "status": "fontes_cruzadas" if len(specific_domains) >= 2 else "pesquisa_ampliada_ainda_sem_segunda_fonte_indexada",
        "query": queries,
        "reviewed_at": data["source_checked_at"],
    }
    return data


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--limit", type=int, default=25)
    parser.add_argument("--delay", type=float, default=0.35)
    parser.add_argument("--gaps-only", action="store_true")
    parser.add_argument(
        "--audit",
        default="output/source-depth-after-visual-tiles.json",
        help="Relatório de profundidade usado por --gaps-only",
    )
    parser.add_argument("--force", action="store_true")
    parser.add_argument(
        "--resume-only",
        action="store_true",
        help="Seleciona apenas registros ainda ausentes do cache de pesquisa.",
    )
    parser.add_argument(
        "--strategy",
        choices=("default", "alternate", "contact"),
        default="default",
    )
    args = parser.parse_args()
    all_records = records()
    if args.gaps_only:
        audit_path = ROOT / args.audit
        audit = read_json(audit_path)
        pending = {
            item["slug"]
            for item in audit.get("queue", [])
            if item.get("kind") == "agenda"
        }
        all_records = [
            item for item in all_records
            if item[0] == "agenda" and record_key(*item) in pending
        ]
    if args.resume_only and CACHE_PATH.exists():
        resume_cache = read_json(CACHE_PATH)
        completed_keys = set(resume_cache.get("completed", {}))
        all_records = [
            item for item in all_records
            if record_key(*item) not in completed_keys
        ]
    selected = all_records[args.offset: args.offset + args.limit]
    cache = read_json(CACHE_PATH) if CACHE_PATH.exists() else {"completed": {}, "failures": {}}
    completed = 0
    for absolute_index, (kind, path, index, original) in enumerate(selected, args.offset):
        key = record_key(kind, path, index, original)
        if key in cache.get("completed", {}) and not args.force:
            print(f"[{absolute_index + 1}/{len(all_records)}] {key}: já concluído")
            completed += 1
            continue
        try:
            updated = research_one(dict(original), strategy=args.strategy)
            save_record(path, index, updated)
            cache["completed"][key] = {
                "index": absolute_index,
                "sources": len(updated.get("sources") or []),
                "domains": updated.get("research_status", {}).get("specific_independent_domains_found", 0),
                "checked_at": updated.get("source_checked_at"),
            }
            cache["failures"].pop(key, None)
            completed += 1
            print(f"[{absolute_index + 1}/{len(all_records)}] {key}: {len(updated.get('sources') or [])} fontes")
        except Exception as exc:
            cache["failures"][key] = {"index": absolute_index, "error": str(exc)}
            print(f"[{absolute_index + 1}/{len(all_records)}] {key}: ERRO {exc}")
        write_json(CACHE_PATH, cache)
        time.sleep(max(args.delay, 0))
    print(json.dumps({"processed": len(selected), "completed": completed, "total": len(all_records)}, ensure_ascii=False))
    return 0 if completed == len(selected) else 2


if __name__ == "__main__":
    raise SystemExit(main())
