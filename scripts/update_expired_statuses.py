#!/usr/bin/env python3
"""Mark dated event records as concluded after their local end date."""

from __future__ import annotations

import argparse
import json
from datetime import date, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FILES = (
    ROOT / "content/events/agenda-comunitaria-2026.json",
    ROOT / "content/calendar/cbm-2026.json",
    ROOT / "content/competitions/moto1000gp-2026.json",
)
OPEN_STATUSES = {"agendada", "em_andamento"}


def walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--through", required=True, help="Last concluded date (YYYY-MM-DD)")
    parser.add_argument("--checked-at", required=True, help="ISO-8601 audit timestamp")
    args = parser.parse_args()
    cutoff = date.fromisoformat(args.through)
    datetime.fromisoformat(args.checked_at)
    changed = 0

    for path in FILES:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        file_changed = 0
        for record in walk(data):
            end_text = record.get("end_date") or record.get("local_end")
            status = record.get("status")
            if not end_text or status not in OPEN_STATUSES:
                continue
            try:
                end_date = date.fromisoformat(str(end_text)[:10])
            except ValueError:
                continue
            if end_date <= cutoff:
                record["status"] = "concluida"
                if "status_checked_at" in record or "local_end" in record:
                    record["status_checked_at"] = args.checked_at
                file_changed += 1
        if file_changed:
            path.write_text(
                json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            changed += file_changed
            print(f"{path.relative_to(ROOT)}: {file_changed}")
    print(f"Total atualizado: {changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
