#!/usr/bin/env python3
"""Remove texto OCR bruto dos artefatos, preservando sinais estruturados e métricas."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "content" / "event-research"


def main() -> int:
    files = sorted(RESEARCH.glob("*ocr-evidence*.json"))
    removed = 0
    for path in files:
        payload = json.loads(path.read_text(encoding="utf-8"))
        for entry in payload.get("ocr_entries", []):
            if "ocr_text" in entry:
                entry.pop("ocr_text")
                removed += 1
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Sanitizado: {path.relative_to(ROOT)}")
    print(f"Campos OCR brutos removidos: {removed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
