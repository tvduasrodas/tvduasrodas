#!/usr/bin/env python3
"""Prioriza eventos que precisam de pesquisa profunda e inspeção visual."""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


ROOT = Path(__file__).resolve().parents[1]
EVENTS_DIR = ROOT / "content" / "events"
PLACEHOLDER = re.compile(r"local informado|a confirmar|confirme com|agenda nacional", re.I)

CHECKS: tuple[tuple[str, int], ...] = (
    ("horario_local", 14),
    ("endereco", 16),
    ("programacao", 14),
    ("acesso", 10),
    ("estacionamento", 8),
    ("organizacao_contato", 10),
    ("fonte_especifica", 12),
    ("inspecao_visual", 8),
    ("status_atualizado", 8),
)


def now_eastern() -> datetime:
    try:
        return datetime.now(ZoneInfo("America/New_York"))
    except ZoneInfoNotFoundError:
        return datetime.now().astimezone()


def text(value: Any) -> str:
    return str(value or "").strip()


def normalized(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = "".join(char for char in value if not unicodedata.combining(char))
    value = re.sub(r"\b\d+\s*[oaºª]?\b", " ", value.lower())
    return re.sub(r"[^a-z0-9]+", " ", value).strip()


def parse_day(value: Any) -> date | None:
    try:
        return date.fromisoformat(text(value)[:10])
    except ValueError:
        return None


def load_events() -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for path in sorted(EVENTS_DIR.glob("*.json")):
        if path.name == "index.json":
            continue
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
        if path.name == "agenda-comunitaria-2026.json":
            for entry in payload.get("entries", []):
                events.append({"source_file": str(path.relative_to(ROOT)), **entry})
        else:
            events.append(
                {
                    "source_file": str(path.relative_to(ROOT)),
                    "slug": path.stem,
                    **payload,
                }
            )
    return events


def evaluate(event: dict[str, Any]) -> dict[str, Any]:
    venue = text(event.get("venue"))
    body = text(event.get("body"))
    source_url = text(event.get("source_url") or event.get("official_url"))
    verification = text(event.get("verification_status"))
    checks = {
        "horario_local": bool(event.get("timezone") and (event.get("local_start") or event.get("time_label"))),
        "endereco": bool(
            venue
            and not PLACEHOLDER.search(venue)
            and (event.get("full_address") or event.get("street_address"))
        ),
        "programacao": bool(event.get("attractions") and body and not PLACEHOLDER.search(body)),
        "acesso": bool(event.get("admission_status") or event.get("ticket_url") or event.get("free") is True),
        "estacionamento": bool(event.get("parking")),
        "organizacao_contato": bool(event.get("organizer") or event.get("contact") or event.get("contact_url")),
        "fonte_especifica": bool(
            source_url
            and "jb-rider.com.br/eventos.php" not in source_url
            and event.get("source_checked_at")
            and verification not in {"", "agenda_comunitaria"}
        ),
        "inspecao_visual": bool(
            event.get("visual_verification")
            or verification in {"flyer_inspecionado_visual", "fonte_oficial_sem_flyer"}
        ),
        "status_atualizado": bool(event.get("status") and event.get("status_checked_at")),
    }
    score = sum(weight for name, weight in CHECKS if checks[name])
    missing = [name for name, _ in CHECKS if not checks[name]]
    start = parse_day(event.get("start_date"))
    today = now_eastern().date()
    if start is None:
        priority = 4
        timing = "data_invalida"
    elif today - timedelta(days=7) <= start <= today + timedelta(days=7):
        priority = 0
        timing = "janela_critica"
    elif today < start <= today + timedelta(days=30):
        priority = 1
        timing = "proximos_30_dias"
    elif start > today:
        priority = 2
        timing = "futuro"
    else:
        priority = 3
        timing = "passado"
    return {
        "slug": event.get("slug"),
        "title": event.get("title"),
        "start_date": event.get("start_date"),
        "city": event.get("city"),
        "state": event.get("state"),
        "source_file": event.get("source_file"),
        "score": score,
        "missing": missing,
        "priority": priority,
        "timing": timing,
        "duplicate_of": event.get("duplicate_of"),
    }


def duplicate_candidates(events: list[dict[str, Any]]) -> list[list[str]]:
    groups: dict[tuple[str, str, str, str], list[str]] = {}
    for event in events:
        if event.get("duplicate_of"):
            continue
        key = (
            normalized(text(event.get("title"))),
            normalized(text(event.get("city"))),
            text(event.get("state")).upper(),
            text(event.get("start_date")),
        )
        if not key[0] or not key[3]:
            continue
        groups.setdefault(key, []).append(text(event.get("slug")))
    return [slugs for slugs in groups.values() if len(slugs) > 1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=30)
    parser.add_argument("--json", action="store_true", help="Exibe o relatório completo em JSON.")
    args = parser.parse_args()

    events = load_events()
    results = [evaluate(event) for event in events]
    queue = sorted(
        (item for item in results if item["missing"] and not item["duplicate_of"]),
        key=lambda item: (item["priority"], item["score"], item["start_date"] or "", item["slug"] or ""),
    )
    duplicates = duplicate_candidates(events)
    complete = sum(not item["missing"] for item in results)
    report = {
        "generated_at": now_eastern().isoformat(),
        "total_events": len(results),
        "complete_events": complete,
        "incomplete_events": len(queue),
        "duplicate_candidate_groups": duplicates,
        "queue": queue,
    }
    if args.json:
        report["queue"] = queue[: max(args.limit, 0)]
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    print(
        f"Eventos: {len(results)} | completos: {complete} | "
        f"pendentes: {len(queue)} | grupos duplicados: {len(duplicates)}"
    )
    for item in queue[: max(args.limit, 0)]:
        print(
            f"[P{item['priority']}] {item['start_date']} | {item['score']:>3}/100 | "
            f"{item['slug']} | faltam: {', '.join(item['missing'])}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
