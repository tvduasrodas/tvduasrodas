#!/usr/bin/env python3
"""Normaliza arquivos editoriais em NFC e remove caracteres invisíveis indevidos."""

from __future__ import annotations

import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INVISIBLE = ("\u200b", "\u200c", "\u200d", "\ufeff")


def main() -> int:
    changed = 0
    for extension in ("*.json", "*.md"):
        for path in sorted((ROOT / "content").rglob(extension)):
            original = path.read_text(encoding="utf-8-sig")
            normalized = unicodedata.normalize("NFC", original)
            for character in INVISIBLE:
                normalized = normalized.replace(character, "")
            if normalized != original:
                path.write_text(normalized, encoding="utf-8", newline="\n")
                changed += 1
    print(f"Arquivos editoriais normalizados: {changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
