#!/usr/bin/env python3
"""Diferencia títulos genéricos por cidade e separa competições da agenda."""

from __future__ import annotations

import json
import re
import unicodedata
from collections import Counter
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENDA = ROOT / "content/events/agenda-comunitaria-2026.json"
COMPETITIONS = ROOT / "content/competitions"
COMPETITION_INDEX = COMPETITIONS / "index.json"

SPORT_SLUGS = {
    "campeonato-amapaense-de-ciclismo-2026-macapa-ap-2026-08-01",
    "campeonato-de-motocross-de-rondonia-2026-cerejeiras-e-corumbiara-ro-2026-08-01",
}


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFD", value or "")
    value = "".join(char for char in value if unicodedata.category(char) != "Mn")
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def city_label(entry: dict) -> str:
    city = str(entry.get("city") or "").strip()
    return city.split(" - ")[0].strip()


def is_generic_title(title: str) -> bool:
    value = normalize(title)
    specific_exceptions = (
        "capital moto week",
        "encontro nacional v strom",
    )
    if any(exception in value for exception in specific_exceptions):
        return False
    patterns = (
        r"\bencontro (?:nacional |estadual )?(?:de )?motociclistas\b",
        r"\bencontro (?:nacional |estadual )?(?:de )?motociclistas e triciclistas\b",
        r"\bencontro nacional\b",
        r"\bbiker fest\b",
        r"\bbike fest\b",
        r"\bmoto cafe\b",
        r"\bmotofest\b",
        r"\bmoto fest\b",
        r"\bmotorock\b",
    )
    return any(re.search(pattern, value) for pattern in patterns)


def date_suffix(value: str) -> str:
    parsed = date.fromisoformat(value)
    months = (
        "janeiro", "fevereiro", "março", "abril", "maio", "junho",
        "julho", "agosto", "setembro", "outubro", "novembro", "dezembro",
    )
    return f"{parsed.day} de {months[parsed.month - 1]}"


def competition_record(entry: dict) -> dict:
    title = entry["title"]
    modality = (
        "Motocross"
        if "motocross" in normalize(title)
        else "Ciclismo de estrada, contrarrelógio e mountain bike"
    )
    start = entry.get("start_date", "")
    end = entry.get("end_date") or start
    return {
        "title": title,
        "short_name": entry.get("short_name") or title,
        "season": start[:4] or "2026",
        "country": entry.get("country") or "Brasil",
        "scope": entry.get("scope") or "Estadual",
        "modality": modality,
        "status": entry.get("status") or "agendada",
        "organizer": entry.get("organizer") or "Organização indicada nas fontes oficiais",
        "official_url": entry.get("official_url") or entry.get("source_url", ""),
        "results_url": entry.get("results_url", ""),
        "cover": entry.get("cover") or "/assets/img/competicoes-eventos-default.svg",
        "image_credit": entry.get("image_credit") or "Arte institucional: TVDUASRODAS",
        "featured": entry.get("featured", False),
        "summary": entry.get("summary", ""),
        "last_updated": entry.get("last_updated") or "2026-07-30",
        "next_stage": {
            "name": title,
            "start_date": start,
            "end_date": end,
            "venue": entry.get("venue", ""),
            "city": entry.get("city", ""),
            "state": entry.get("state", ""),
            "note": entry.get("time_label") or entry.get("status_note") or "Programação sujeita a atualização da organização.",
        },
        "categories": entry.get("categories") or [modality],
        "rounds": [{
            "order": 1,
            "start_date": start,
            "end_date": end,
            "name": entry.get("stage") or title,
            "location": entry.get("full_address") or ", ".join(filter(None, (entry.get("venue"), entry.get("city"), entry.get("state")))),
            "status": "agendada",
            "winner": "",
            "results_url": entry.get("results_url", ""),
        }],
        "related_videos": entry.get("videos", []),
        "body": entry.get("body", ""),
        "sources": entry.get("sources", []),
        "source_checked_at": entry.get("source_checked_at") or entry.get("last_updated") or "2026-07-30",
        "research_status": entry.get("research_status", {}),
        "classification_status": {
            "status": "aguardando_resultados",
            "checked_at": entry.get("source_checked_at") or "2026-07-30",
            "note": "Classificação e resultados serão atualizados após a publicação oficial da organização.",
        },
        "calendar_status": {
            "status": "publicado",
            "checked_at": entry.get("source_checked_at") or "2026-07-30",
            "note": "Competição confirmada nas fontes indicadas nesta página.",
        },
    }


def main() -> None:
    document = json.loads(AGENDA.read_text(encoding="utf-8"))
    entries = document.get("entries", [])
    active = [entry for entry in entries if not entry.get("duplicate_of")]

    repeated = Counter(normalize(entry.get("title", "")) for entry in active)
    changed_titles = 0
    for entry in active:
        title = str(entry.get("title") or "").strip()
        city = city_label(entry)
        if not city:
            continue
        needs_city = repeated[normalize(title)] > 1 or is_generic_title(title)
        if not needs_city or normalize(city) in normalize(title):
            continue
        entry["title"] = f"{title} de {city}"
        if not entry.get("short_name") or normalize(entry.get("short_name")) == normalize(title):
            entry["short_name"] = entry["title"]
        changed_titles += 1

    collisions = Counter(normalize(entry.get("title", "")) for entry in active)
    dated_titles = 0
    for entry in active:
        if collisions[normalize(entry.get("title", ""))] < 2:
            continue
        start = entry.get("start_date")
        if not start:
            continue
        entry["title"] = f"{entry['title']} — {date_suffix(start)}"
        if entry.get("short_name"):
            entry["short_name"] = entry["title"]
        dated_titles += 1

    competition_index = json.loads(COMPETITION_INDEX.read_text(encoding="utf-8"))
    reclassified = 0
    for entry in active:
        slug = entry.get("slug")
        if slug not in SPORT_SLUGS:
            continue
        entry["competition_slug"] = slug
        entry["reclassified_as"] = "competition"
        entry["canonical_url"] = f"/competicoes/{slug}/"
        target = COMPETITIONS / f"{slug}.json"
        target.write_text(
            json.dumps(competition_record(entry), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        if slug not in competition_index:
            competition_index.append(slug)
        reclassified += 1

    document["last_updated"] = "2026-07-30"
    AGENDA.write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    COMPETITION_INDEX.write_text(
        json.dumps(competition_index, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"Títulos com cidade adicionada: {changed_titles}")
    print(f"Títulos diferenciados também por data: {dated_titles}")
    print(f"Competições reclassificadas: {reclassified}")


if __name__ == "__main__":
    main()
