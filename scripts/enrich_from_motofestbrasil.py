#!/usr/bin/env python3
"""Cruza a agenda local com páginas específicas do Motofest Brasil.

O portal entrega os próximos eventos em um payload Nuxt público. Este utilitário
decodifica esse payload, exige coincidência de data e cidade e usa identidade
textual/visual para evitar associações por simples semelhança de nomes.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import unicodedata
from datetime import datetime, timezone
from difflib import SequenceMatcher
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Iterable
from urllib.request import Request, urlopen

import research_all_events as research


ROOT = Path(__file__).resolve().parents[1]
HOME_URL = "https://motofestbrasil.com.br/"
DETAIL_BASE = "https://motofestbrasil.com.br/motofest/"
USER_AGENT = (
    "Mozilla/5.0 (compatible; TVDUASRODAS-EditorialAudit/1.0; "
    "+https://tvduasrodas.com/)"
)
GENERIC = {
    "moto", "motofest", "motos", "motociclista", "motociclistas", "encontro",
    "nacional", "evento", "festival", "rock", "anos", "ano", "mc", "mg",
    "asfalto", "do", "da", "dos", "das", "de", "e", "em", "no", "na", "os",
    "as", "um", "uma",
}


class PlainText(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        value = " ".join(data.split())
        if value:
            self.parts.append(value)


def fetch(url: str) -> str:
    request = Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept-Language": "pt-BR,pt;q=0.9"},
    )
    with urlopen(request, timeout=40) as response:
        return response.read(8_000_000).decode(
            response.headers.get_content_charset() or "utf-8", errors="replace"
        )


def norm(value: Any) -> str:
    text = unicodedata.normalize("NFKD", str(value or ""))
    text = "".join(char for char in text if not unicodedata.combining(char))
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def words(value: Any, *, meaningful: bool = False) -> set[str]:
    result = {word for word in norm(value).split() if len(word) >= 2}
    return result - GENERIC if meaningful else result


def strip_html(value: str) -> str:
    parser = PlainText()
    parser.feed(html.unescape(value or ""))
    return " ".join(parser.parts)


def nuxt_payload(document: str) -> list[Any]:
    match = re.search(
        r'<script[^>]+id=["\']__NUXT_DATA__["\'][^>]*>(.*?)</script>',
        document,
        flags=re.S | re.I,
    )
    if not match:
        raise RuntimeError("payload __NUXT_DATA__ não localizado")
    payload = json.loads(html.unescape(match.group(1)))
    if not isinstance(payload, list):
        raise RuntimeError("payload Nuxt inesperado")
    return payload


def resolve_devalue(payload: list[Any]) -> Any:
    memo: dict[int, Any] = {}

    def resolve_ref(index: int) -> Any:
        if index < 0:
            return None
        if index in memo:
            return memo[index]
        value = payload[index]
        if isinstance(value, dict):
            result: dict[str, Any] = {}
            memo[index] = result
            for key, child in value.items():
                result[key] = resolve(child)
            return result
        if isinstance(value, list):
            result_list: list[Any] = []
            memo[index] = result_list
            result_list.extend(resolve(child) for child in value)
            return result_list
        memo[index] = value
        return value

    def resolve(value: Any) -> Any:
        if isinstance(value, bool) or value is None:
            return value
        if isinstance(value, int):
            return resolve_ref(value) if 0 <= value < len(payload) else value
        if isinstance(value, list):
            return [resolve(child) for child in value]
        if isinstance(value, dict):
            return {key: resolve(child) for key, child in value.items()}
        return value

    return resolve_ref(0)


def walk(value: Any, seen: set[int] | None = None) -> Iterable[dict[str, Any]]:
    seen = seen or set()
    marker = id(value)
    if marker in seen:
        return
    seen.add(marker)
    if isinstance(value, dict):
        if value.get("slug") and value.get("title") and value.get("dateStart"):
            yield value
        for child in value.values():
            yield from walk(child, seen)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child, seen)


def event_city(event: dict[str, Any]) -> str:
    location = event.get("location")
    if isinstance(location, dict):
        return str(location.get("city") or location.get("name") or "")
    return str(location or "")


def identity_haystack(event: dict[str, Any]) -> str:
    return " ".join(
        str(event.get(key) or "")
        for key in ("title", "slug", "description", "keywords", "image", "instagram")
    )


def score(record: dict[str, Any], event: dict[str, Any]) -> tuple[int, list[str]]:
    reasons: list[str] = []
    record_date = str(record.get("start_date") or "")
    event_start = str(event.get("dateStart") or "")[:10]
    event_end = str(event.get("dateEnd") or event_start)[:10]
    if not record_date or not (event_start <= record_date <= event_end):
        return 0, ["data incompatível"]
    total = 42
    reasons.append("data dentro do período")

    city = norm(record.get("city"))
    city_source = norm(event_city(event))
    if not city or city not in city_source.split() and city not in city_source:
        return 0, ["cidade incompatível"]
    total += 28
    reasons.append("cidade confirmada")

    title = norm(record.get("title"))
    haystack = norm(identity_haystack(event))
    title_words = words(title)
    meaningful = words(title, meaningful=True)
    overlap = title_words & set(haystack.split())
    meaningful_overlap = meaningful & set(haystack.split())
    ratio = SequenceMatcher(None, title, norm(event.get("title"))).ratio()

    if title and title in haystack:
        total += 30
        reasons.append("título identificado no registro ou material visual")
    elif meaningful and meaningful_overlap:
        total += min(24, 8 * len(meaningful_overlap))
        reasons.append("identidade nominal específica")
    elif len(overlap) >= 2:
        total += 14
        reasons.append("dois termos do título")
    elif ratio >= 0.58:
        total += 12
        reasons.append("alta similaridade de título")
    elif len(title_words) <= 2 and overlap:
        total += 6
        reasons.append("título genérico compatível")
    else:
        return 0, ["identidade insuficiente"]
    return total, reasons


def best_match(record: dict[str, Any], events: list[dict[str, Any]]) -> dict[str, Any] | None:
    ranked: list[tuple[int, dict[str, Any], list[str]]] = []
    for event in events:
        value, reasons = score(record, event)
        if value:
            ranked.append((value, event, reasons))
    ranked.sort(key=lambda item: item[0], reverse=True)
    if not ranked or ranked[0][0] < 76:
        return None
    if len(ranked) > 1 and ranked[0][0] == ranked[1][0]:
        first = norm(ranked[0][1].get("title"))
        second = norm(ranked[1][1].get("title"))
        if first != second:
            return None
    value, event, reasons = ranked[0]
    return {"score": value, "reasons": reasons, "event": event}


def add_source(record: dict[str, Any], matched: dict[str, Any], checked_at: str) -> bool:
    event = matched["event"]
    slug = str(event.get("slug") or "").strip("/")
    detail_url = DETAIL_BASE + slug
    if any(
        isinstance(source, dict) and source.get("url") == detail_url
        for source in record.get("sources") or []
    ):
        return False
    description = strip_html(str(event.get("description") or ""))
    location = event.get("location") if isinstance(event.get("location"), dict) else {}
    source = {
        "url": detail_url,
        "label": f"{event.get('title')} — página específica no Motofest Brasil",
        "type": "fonte específica independente",
        "supports": ", ".join(
            item
            for item, present in (
                ("data e edição", event.get("dateStart")),
                ("cidade e local", event_city(event)),
                ("programação e atrações", description),
                ("organização e canais", event.get("instagram") or event.get("website")),
                ("evidência visual", event.get("image")),
            )
            if present
        ),
        "checked_at": checked_at,
        "discovery_method": "cruzamento_estruturado_motofestbrasil",
        "relevance_score": matched["score"],
    }
    record["sources"] = research.deduplicate_sources(
        list(record.get("sources") or []) + [source]
    )
    if location.get("name") and (
        not record.get("full_address")
        or re.search(r"não informado|a confirmar|local informado", str(record["full_address"]), re.I)
    ):
        record["full_address"] = str(location["name"])
    if not record.get("organizer") and event.get("instagram"):
        record["organizer"] = f"Organização divulgada em @{str(event['instagram']).lstrip('@')}"
    image = str(event.get("image") or "")
    visual = record.get("visual_verification")
    if image and (not isinstance(visual, dict) or not visual.get("detail_url")):
        record["visual_verification"] = {
            "status": "material visual localizado e associado por data, cidade e identidade",
            "detail_url": detail_url,
            "image_url": image,
            "checked_at": checked_at,
            "method": "imagem e descrição pública do registro específico",
        }
    record["source_checked_at"] = checked_at
    record["motofestbrasil_match"] = {
        "url": detail_url,
        "score": matched["score"],
        "reasons": matched["reasons"],
        "checked_at": checked_at,
    }
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    decoded = resolve_devalue(nuxt_payload(fetch(HOME_URL)))
    events_by_slug: dict[str, dict[str, Any]] = {}
    for event in walk(decoded):
        slug = str(event.get("slug") or "")
        if slug:
            events_by_slug[slug] = event
    events = list(events_by_slug.values())
    checked_at = datetime.now(timezone.utc).isoformat()
    matches: list[dict[str, Any]] = []
    changed = 0

    for kind, path, index, original in research.records():
        if original.get("duplicate_of"):
            continue
        matched = best_match(original, events)
        if not matched:
            continue
        item = {
            "kind": kind,
            "slug": original.get("slug") or path.stem,
            "title": original.get("title"),
            "city": original.get("city"),
            "date": original.get("start_date"),
            "score": matched["score"],
            "reasons": matched["reasons"],
            "source_title": matched["event"].get("title"),
            "source_slug": matched["event"].get("slug"),
            "source_url": DETAIL_BASE + str(matched["event"].get("slug")),
        }
        matches.append(item)
        if args.apply:
            updated = dict(original)
            if add_source(updated, matched, checked_at):
                research.save_record(path, index, updated)
                changed += 1

    report = {
        "portal_events": len(events),
        "matched_records": len(matches),
        "changed_records": changed,
        "matches": matches,
    }
    serialized = json.dumps(report, ensure_ascii=False, indent=2)
    if args.report:
        output = args.report if args.report.is_absolute() else ROOT / args.report
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(serialized + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in report if key != "matches"}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
