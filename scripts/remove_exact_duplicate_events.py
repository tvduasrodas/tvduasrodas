#!/usr/bin/env python3
"""Remove repetições exatas de slug da agenda, preservando a primeira ocorrência."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENDA = ROOT / "content" / "events" / "agenda-comunitaria-2026.json"


def main() -> int:
    payload = json.loads(AGENDA.read_text(encoding="utf-8-sig"))
    entries = payload.get("entries", [])
    counts = Counter(str(item.get("slug") or "") for item in entries)
    duplicate_slugs = {slug for slug, count in counts.items() if slug and count > 1}

    seen: set[str] = set()
    cleaned: list[dict] = []
    removed: list[str] = []
    for item in entries:
        slug = str(item.get("slug") or "")
        if slug in seen:
            removed.append(slug)
            continue
        seen.add(slug)
        cleaned.append(item)

    payload["entries"] = cleaned
    AGENDA.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Slugs duplicados detectados: {len(duplicate_slugs)}")
    print(f"Registros repetidos removidos: {len(removed)}")
    for slug in removed:
        print(f"REMOVIDO {slug}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
