#!/usr/bin/env python3
"""Normaliza texto importado de flyers antes da geração pública."""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
AGENDA = ROOT / "content/events/agenda-comunitaria-2026.json"


def clean(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: clean(item) for key, item in value.items()}
    if isinstance(value, list):
        return [clean(item) for item in value]
    if not isinstance(value, str):
        return value
    value = unicodedata.normalize("NFC", value)
    value = "".join(
        char for char in value
        if unicodedata.category(char) != "Cf"
    )
    value = re.sub(r"\s+([,.;:!?])", r"\1", value)
    value = re.sub(r"([!?])\1+", r"\1", value)
    value = re.sub(r"\bCONFORTAVEL\b", "CONFORTÁVEL", value)
    value = re.sub(r"\bConfortavel\b", "Confortável", value)
    return value


def main() -> None:
    document = json.loads(AGENDA.read_text(encoding="utf-8"))
    normalized = clean(document)
    AGENDA.write_text(
        json.dumps(normalized, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print("Agenda normalizada em Unicode NFC e sem caracteres invisíveis.")


if __name__ == "__main__":
    main()
