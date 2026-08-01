#!/usr/bin/env python3
"""Reconcilia a agenda pública ligada ao @jacaremoto com os eventos locais."""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import subprocess
import sys
import unicodedata
import urllib.parse
import urllib.request
from datetime import date
from difflib import SequenceMatcher
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENDA = ROOT / "content/events/agenda-comunitaria-2026.json"
UPLOADS = ROOT / "assets/img/uploads"
TMP = ROOT / "tmp/jacaremoto-sync"
SOURCE_URL = "https://jacaremoto.com.br/"
CHECKED_AT = "2026-08-01T16:30:00-04:00"
MONTHS = {"agosto": 8}


def clean(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value or "")
    value = html.unescape(value).replace("\u200d", "")
    value = re.sub(r"\s+([,.;:!?])", r"\1", value)
    value = re.sub(r"([!?])\1+", r"\1", value)
    return re.sub(r"\s+", " ", value).strip()


def norm(value: str) -> str:
    value = unicodedata.normalize("NFKD", value or "")
    value = "".join(ch for ch in value if not unicodedata.combining(ch)).lower()
    return re.sub(r"[^a-z0-9]+", " ", value).strip()


def slugify(value: str) -> str:
    return norm(value).replace(" ", "-").strip("-")


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 TVDUASRODAS editorial"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def parse_source(document: str) -> list[dict]:
    rows: list[dict] = []
    blocks = re.findall(r'(?s)<li>\s*<div class="eo_s1_box.*?</li>', document)
    for block in blocks:
        title_match = re.search(r'id="slider_1_\d+_eo_title">\s*(.*?)\s*</div>', block, re.S)
        if not title_match:
            continue
        subtitle = re.search(r'id="slider_1_\d+_eo_subtitle"[^>]*>(.*?)</p>', block, re.S)
        image = re.search(r'class="event_img" style="background-image:url\((.*?)\);', block, re.S)
        description = re.search(r'id="slider_1_\d+_eo_desc"[^>]*>(.*?)</p>', block, re.S)
        timing = re.search(r'id="slider_1_\d+_eo_time_long">\s*(.*?)\s*</span>', block, re.S)
        title = clean(title_match.group(1))
        city_label = clean(subtitle.group(1) if subtitle else "")
        time_label = clean(timing.group(1) if timing else "")
        description_text = clean(description.group(1) if description else "")
        image_url = clean(image.group(1) if image else "")
        state_match = re.search(r"(?:-|\s)([A-Z]{2})(?:\s|$)", city_label)
        state = state_match.group(1) if state_match else ""
        city = re.sub(r"\s*-?\s*[A-Z]{2}(?:\s*-.*)?$", "", city_label).strip(" -")
        city = re.sub(r"(?i)^cancelado\s*-?\s*", "", city).strip()
        if re.search(r"(?i)(fest|encontro|anivers)", city) and "-" in city:
            city = city.rsplit("-", 1)[-1].strip()
        dates = re.findall(r"(\d{1,2})\s+Agosto\s+2026", time_label, re.I)
        if not dates or not city or not state:
            continue
        start_date = f"2026-08-{int(dates[0]):02d}"
        end_date = f"2026-08-{int(dates[-1]):02d}"
        rows.append({
            "title": title,
            "city": city,
            "state": state,
            "start_date": start_date,
            "end_date": end_date,
            "time_source": time_label,
            "description": description_text,
            "image_url": image_url,
        })
    return rows


def title_core(value: str, city: str, state: str) -> str:
    result = norm(value)
    for suffix in (norm(city), norm(state)):
        result = re.sub(rf"\b{re.escape(suffix)}\b", " ", result)
    return re.sub(r"\s+", " ", result).strip()


def match_entry(source: dict, entries: list[dict], claimed: set[int]) -> tuple[int | None, float]:
    best_index: int | None = None
    best_score = 0.0
    source_city = norm(source["city"])
    source_title = title_core(source["title"], source["city"], source["state"])
    for index, entry in enumerate(entries):
        if index in claimed or norm(entry.get("state", "")) != norm(source["state"]):
            continue
        event_score = SequenceMatcher(
            None,
            source_title,
            title_core(entry.get("title", ""), entry.get("city", ""), entry.get("state", "")),
        ).ratio()
        city_score = SequenceMatcher(None, source_city, norm(entry.get("city", ""))).ratio()
        try:
            source_start = date.fromisoformat(source["start_date"])
            source_end = date.fromisoformat(source["end_date"])
            entry_start = date.fromisoformat(entry.get("start_date", ""))
            entry_end = date.fromisoformat(entry.get("end_date") or entry.get("start_date", ""))
            overlaps = source_start <= entry_end and entry_start <= source_end
            start_delta = abs((source_start - entry_start).days)
            date_score = 1.0 if start_delta == 0 else 0.85 if overlaps or start_delta <= 1 else 0.0
        except ValueError:
            date_score = 0.0
        if not date_score:
            continue
        city_alias_in_title = (
            norm(entry.get("city", "")) in norm(source["title"])
            or source_city in norm(entry.get("title", ""))
        )
        if not (city_score >= 0.82 and event_score >= 0.38) and not (city_alias_in_title and event_score >= 0.60):
            continue
        score = (event_score * 0.65) + (city_score * 0.20) + (date_score * 0.15)
        if score > best_score:
            best_index, best_score = index, score
    return best_index, best_score


def city_title(title: str, city: str, state: str) -> str:
    if norm(city) in norm(title) and norm(state) in norm(title):
        return title
    if norm(city) in norm(title):
        return f"{title.rstrip(' -–—/')} — {state}"
    return f"{title.rstrip(' -–—/')} — {city}/{state}"


def extract_time(description: str, fallback: str) -> str:
    marks = re.findall(r"(?i)\b(?:in[ií]cio|fim|a partir das?|[àa]s)\s*[:.]?\s*(\d{1,2}(?:h\d{0,2})?)", description)
    if marks:
        return "Horários divulgados: " + ", ".join(dict.fromkeys(marks))
    cleaned = re.sub(r"\s+(?:DATA\s+)?0:00\b", "", fallback).strip()
    return cleaned or "Horário não informado pela fonte consultada"


def extract_venue(description: str) -> str:
    match = re.search(r"(?i)\bLocal\s*:\s*([^.;]{4,160})", description)
    if match:
        return match.group(1).strip(" -")
    return ""


def attractions(description: str) -> list[str]:
    mapping = {
        "Área de camping": r"(?i)\bcamping\b",
        "Café da manhã": r"(?i)caf[eé] da manh[ãa]",
        "Praça de alimentação": r"(?i)(pra[çc]a de alimenta[çc][ãa]o|gastronom)",
        "Shows de rock": r"(?i)(shows? de rock|bandas? de rock|rock and roll)",
        "Expositores": r"(?i)\bexpositores?\b",
        "Área kids": r"(?i)([áa]rea kids|espa[çc]o kids)",
        "Troféus": r"(?i)\btrof[eé]us?\b",
        "Chuveiro quente": r"(?i)chuveiros? quente",
        "Entrada franca": r"(?i)entrada (?:franca|gratuita)",
        "Ação solidária": r"(?i)(doa[çc][ãa]o|solid[áa]ri)",
    }
    return [label for label, pattern in mapping.items() if re.search(pattern, description)]


def admission(description: str) -> tuple[bool, str]:
    if re.search(r"(?i)entrada (?:franca|gratuita)", description):
        return True, "Entrada franca conforme a agenda Jacaré Moto"
    value = re.search(r"(?i)entrada\s*(?:R\$)?\s*(\d+[,.]?\d*)", description)
    if value:
        return False, f"Entrada informada: R$ {value.group(1)}; confirme com a organização"
    if re.search(r"(?i)(doa[çc][ãa]o|solid[áa]ri)", description):
        return False, "A fonte menciona entrada ou ação solidária; confirme a condição com a organização"
    return False, "Não informado na agenda Jacaré Moto consultada"


def append_update(body: str, source: dict) -> str:
    marker = "## Atualização Jacaré Moto — 1º de agosto de 2026"
    if marker in body:
        body = body.split(marker, 1)[0].rstrip()
    venue = extract_venue(source["description"])
    facts = [
        f"A agenda vinculada ao @jacaremoto confirma **{source['title']}** em {source['city']}/{source['state']}, de {source['start_date']} a {source['end_date']}.",
        f"Horários: {extract_time(source['description'], source['time_source'])}.",
        f"Local: {venue}." if venue else "Local detalhado não informado na agenda consultada; confirme com a organização.",
    ]
    if source["description"]:
        facts.append(f"Informações adicionais da divulgação: {source['description']}")
    return body.rstrip() + "\n\n" + marker + "\n\n" + "\n\n".join(facts)


def ensure_source(entry: dict, source: dict) -> None:
    sources = entry.setdefault("sources", [])
    if not any("jacaremoto.com.br" in item.get("url", "") for item in sources if isinstance(item, dict)):
        sources.append({
            "url": SOURCE_URL,
            "label": "Agenda e flyer publicados pelo Jacaré Moto",
            "type": "agenda comunitária e evidência visual",
            "supports": "título, cidade, período, flyer e informações adicionais legíveis",
            "checked_at": CHECKED_AT,
        })


def download_flyer(source: dict, slug: str, dry_run: bool) -> tuple[str, str]:
    if not source["image_url"]:
        return "", "sem URL de imagem"
    destination = UPLOADS / f"{slug}-flyer-jacaremoto.webp"
    public_path = f"/assets/img/uploads/{destination.name}"
    if dry_run:
        return public_path, "simulado"
    if destination.exists():
        return public_path, f"publicado ({destination.stat().st_size} bytes)"
    TMP.mkdir(parents=True, exist_ok=True)
    extension = Path(urllib.parse.urlparse(source["image_url"]).path).suffix or ".jpg"
    original = TMP / f"{slug}{extension}"
    try:
        original.write_bytes(fetch(source["image_url"]))
        subprocess.run(
            [sys.executable, str(ROOT / "scripts/optimize_image.py"), str(original), str(destination), "1400", "80"],
            check=True,
            capture_output=True,
            text=True,
        )
        if destination.stat().st_size > 350_000:
            retry = TMP / f"{slug}-retry.webp"
            subprocess.run(
                [sys.executable, str(ROOT / "scripts/optimize_image.py"), str(original), str(retry), "1200", "72"],
                check=True,
                capture_output=True,
                text=True,
            )
            if retry.stat().st_size < destination.stat().st_size:
                retry.replace(destination)
            else:
                retry.unlink(missing_ok=True)
        return public_path, f"publicado ({destination.stat().st_size} bytes)"
    except Exception as exc:  # noqa: BLE001
        destination.unlink(missing_ok=True)
        return "", f"falha: {exc}"


def new_entry(source: dict) -> dict:
    slug = slugify(f"{source['title']} {source['city']} {source['state']} {source['start_date']}")
    free, admission_status = admission(source["description"])
    found_attractions = attractions(source["description"])
    return {
        "slug": slug,
        "title": city_title(source["title"], source["city"], source["state"]),
        "short_name": source["title"],
        "start_date": source["start_date"],
        "end_date": source["end_date"],
        "city": source["city"],
        "state": source["state"],
        "country": "Brasil",
        "scope": "Nacional",
        "region": "Sudeste" if source["state"] in {"MG", "SP", "RJ", "ES"} else "Brasil",
        "venue": extract_venue(source["description"]) or "Local detalhado não informado na agenda consultada",
        "status": "agendada",
        "event_type": "Encontro de motociclistas",
        "segment": "Motos",
        "official_url": SOURCE_URL,
        "source_url": SOURCE_URL,
        "source_label": "Agenda e flyer publicados pelo Jacaré Moto",
        "verification_status": "flyer_jacaremoto_inspecionado",
        "cover": "/assets/img/competicoes-eventos-default.svg",
        "image_credit": "Flyer: Jacaré Moto / organização do evento",
        "featured": False,
        "free": free,
        "summary": f"{source['title']} em {source['city']}/{source['state']}, de {source['start_date']} a {source['end_date']}. Serviço confrontado com a agenda Jacaré Moto.",
        "attractions": found_attractions or ["Programação detalhada não informada na agenda consultada"],
        "body": append_update("", source).lstrip(),
        "last_updated": CHECKED_AT,
        "timezone": "America/Sao_Paulo",
        "time_label": extract_time(source["description"], source["time_source"]),
        "street_address": extract_venue(source["description"]) or "Não informado na agenda consultada",
        "full_address": extract_venue(source["description"]) or f"Local detalhado não informado; referência: {source['city']}/{source['state']}",
        "status_basis": "Período e cidade divulgados na agenda Jacaré Moto; confirme alterações antes de viajar.",
        "status_checked_at": CHECKED_AT,
        "organizer": "Organização não identificada na agenda consultada",
        "contact": "Não informado na agenda consultada",
        "source_checked_at": CHECKED_AT,
        "admission_status": admission_status,
        "parking": "Não informado na agenda consultada",
        "sources": [],
    }


def reconcile(dry_run: bool) -> dict:
    document = fetch(SOURCE_URL).decode("utf-8", errors="replace")
    sources = parse_source(document)
    data = json.loads(AGENDA.read_text(encoding="utf-8"))
    duplicate_slug = "13o-motocolatras-fest-araguari-mg-13o-motocolatras-fest-araguari-mg-2026-08-21"
    entries = [entry for entry in data["entries"] if entry.get("slug") != duplicate_slug]
    agenda_count = len(entries)
    standalone_paths: dict[int, Path] = {}
    for path in sorted((ROOT / "content/events").glob("*.json")):
        if path == AGENDA or path.name == "index.json":
            continue
        standalone = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(standalone, dict) and standalone.get("slug"):
            standalone_paths[len(entries)] = path
            entries.append(standalone)
    touched_standalone: set[int] = set()
    claimed: set[int] = set()
    report: list[dict] = []
    for source in sources:
        index, score = match_entry(source, entries, claimed)
        created = index is None
        if created:
            entry = new_entry(source)
            entries.append(entry)
            index = len(entries) - 1
        else:
            entry = entries[index]
            if index in standalone_paths:
                touched_standalone.add(index)
        claimed.add(index)
        if norm(entry.get("city", "")).startswith("cancelado"):
            entry["city"] = source["city"]
            entry["summary"] = re.sub(r"em\s+(?:CANCELADO\s*|-\s*)+", "em ", entry.get("summary", ""), flags=re.I)
            if entry.get("full_address", "").startswith("Local detalhado não informado; referência:"):
                entry["full_address"] = f"Local detalhado não informado; referência: {source['city']}/{source['state']}"
        existing_title = entry.get("title", "")
        existing_title = re.sub(r"\s+—\s+(?:CANCELADO\s*|-\s*)+[^/]+/[A-Z]{2}$", "", existing_title, flags=re.I)
        preferred = existing_title if len(title_core(existing_title, entry.get("city", ""), entry.get("state", ""))) >= len(title_core(source["title"], source["city"], source["state"])) else source["title"]
        entry["title"] = city_title(preferred, entry.get("city") or source["city"], entry.get("state") or source["state"])
        entry.setdefault("short_name", source["title"])
        entry["end_date"] = max(entry.get("end_date", source["end_date"]), source["end_date"])
        venue = extract_venue(source["description"])
        if venue and (not entry.get("venue") or "não informado" in norm(entry.get("venue", ""))):
            entry["venue"] = venue
            entry["street_address"] = venue
            entry["full_address"] = f"{venue}, {source['city']}/{source['state']}"
        if not entry.get("time_label") or "não informado" in norm(entry.get("time_label", "")):
            entry["time_label"] = extract_time(source["description"], source["time_source"])
        current_attractions = entry.setdefault("attractions", [])
        for attraction in attractions(source["description"]):
            if attraction not in current_attractions:
                current_attractions.append(attraction)
        free, admission_status = admission(source["description"])
        if free:
            entry["free"] = True
        if not entry.get("admission_status") or "não informado" in norm(entry.get("admission_status", "")):
            entry["admission_status"] = admission_status
        entry["body"] = append_update(entry.get("body", ""), source)
        entry["last_updated"] = CHECKED_AT
        entry["source_checked_at"] = CHECKED_AT
        entry["jacaremoto_flyer_url"] = source["image_url"]
        entry["jacaremoto_agenda_url"] = SOURCE_URL
        if "cancelado" in norm(source["title"] + " " + source["description"]):
            entry["status"] = "cancelado"
        ensure_source(entry, source)
        flyer_path, image_status = download_flyer(source, entry["slug"], dry_run)
        if flyer_path:
            entry["flyer"] = flyer_path
            if not entry.get("cover") or "competicoes-eventos-default" in entry.get("cover", ""):
                entry["cover"] = flyer_path
                entry["image_credit"] = "Flyer: Jacaré Moto / organização do evento"
        report.append({
            "source_title": source["title"],
            "slug": entry["slug"],
            "action": "created" if created else "updated",
            "match_score": round(score, 3),
            "image": image_status,
            "cover": entry.get("cover", ""),
        })
    data["last_updated"] = CHECKED_AT
    if not dry_run:
        data["entries"] = entries[:agenda_count] + [
            entry for index, entry in enumerate(entries[agenda_count:], start=agenda_count)
            if index not in standalone_paths
        ]
        AGENDA.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        for index in touched_standalone:
            standalone_paths[index].write_text(json.dumps(entries[index], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        source_log = ROOT / "content/events/fontes-jacaremoto-2026-08-01.md"
        lines = [
            "# Varredura Jacaré Moto — agosto de 2026",
            "",
            f"Fonte: {SOURCE_URL}",
            f"Perfil: https://www.instagram.com/jacaremoto/",
            f"Consulta: {CHECKED_AT}",
            "",
            f"Foram reconciliados {len(report)} flyers/eventos. Dados existentes mais completos foram preservados; lacunas receberam informações adicionais da agenda. Flyers foram baixados, convertidos para WebP e armazenados localmente.",
            "",
            "## Inventário",
            "",
        ]
        for item, source in zip(report, sources):
            lines.append(f"- **{source['title']} — {source['city']}/{source['state']}** ({source['start_date']} a {source['end_date']}): `{item['action']}`, imagem {item['image']}; origem {source['image_url']}")
        source_log.write_text("\n".join(lines) + "\n", encoding="utf-8")
        if TMP.exists():
            shutil.rmtree(TMP)
    return {
        "source_count": len(sources),
        "updated": sum(item["action"] == "updated" for item in report),
        "created": sum(item["action"] == "created" for item in report),
        "images_ok": sum(item["image"].startswith(("publicado", "simulado")) for item in report),
        "image_failures": [item for item in report if not item["image"].startswith(("publicado", "simulado"))],
        "items": report,
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    result = reconcile(args.dry_run)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not result["image_failures"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
