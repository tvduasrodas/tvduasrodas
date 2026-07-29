#!/usr/bin/env python3
"""Normaliza texto importado de flyers antes da geração pública."""

from __future__ import annotations

import json
import re
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
AGENDA = ROOT / "content/events/agenda-comunitaria-2026.json"

CITY_DISPLAY_OVERRIDES = {
    "atilio vivacqua": "Atílio Vivácqua",
    "araxa": "Araxá",
    "caete": "Caeté",
    "caiaponia": "Caiapônia",
    "cha grande": "Chã Grande",
    "divinopolis": "Divinópolis",
    "iacu": "Iaçu",
    "joao camara": "João Câmara",
    "labrea": "Lábrea",
    "luis eduardo magalhaes": "Luís Eduardo Magalhães",
    "maceio": "Maceió",
    "paranavai": "Paranavaí",
    "piunhi": "Piumhi",
    "poco fundo": "Poço Fundo",
    "pocos de caldas": "Poços de Caldas",
    "petrolandia": "Petrolândia",
    "serra de sao bento": "Serra de São Bento",
    "simonesia": "Simonésia",
    "uirauna": "Uiraúna",
    "vicosa": "Viçosa",
}

GENERIC_MOTOFEST_RE = re.compile(
    r"^\s*(?:(?P<edition>\d+\s*[ºª]?|[IVXLCDM]+)\s+)?"
    r"(?P<label>moto\s*festival|moto\s*fest)\s*$",
    re.IGNORECASE,
)


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


def fold(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = "".join(char for char in value if not unicodedata.combining(char))
    return re.sub(r"\s+", " ", value).strip().casefold()


def city_display_name(value: str) -> str:
    return CITY_DISPLAY_OVERRIDES.get(fold(value), value.strip())


def normalize_generic_motofest_names(document: dict[str, Any]) -> list[dict[str, str]]:
    """Acrescenta a cidade somente a títulos genéricos de Moto Fest."""
    changed: list[dict[str, str]] = []
    checked_at = datetime.now(timezone.utc).isoformat()

    for entry in document.get("entries", []):
        if not isinstance(entry, dict):
            continue
        current_title = str(entry.get("title") or "").strip()
        match = GENERIC_MOTOFEST_RE.fullmatch(current_title)
        city = city_display_name(str(entry.get("city") or ""))
        if not match or not city:
            continue

        edition = re.sub(r"\s+", "", match.group("edition") or "")
        if edition.isdigit():
            edition = f"{edition}º"
        label = (
            "Moto Festival"
            if "festival" in fold(match.group("label"))
            else "Moto Fest"
        )
        short_name = f"{city} {label}"
        title = f"{edition} {short_name}".strip()
        if current_title == title and entry.get("short_name") == short_name:
            continue

        entry["title"] = title
        entry["short_name"] = short_name
        entry["last_updated"] = checked_at
        changed.append({
            "slug": str(entry.get("slug") or ""),
            "before": current_title,
            "after": title,
        })

    return changed


def main() -> None:
    document = json.loads(AGENDA.read_text(encoding="utf-8"))
    normalized = clean(document)
    motofest_changes = normalize_generic_motofest_names(normalized)
    AGENDA.write_text(
        json.dumps(normalized, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print("Agenda normalizada em Unicode NFC e sem caracteres invisíveis.")
    print(json.dumps({
        "generic_motofest_names_updated": len(motofest_changes),
        "changes": motofest_changes,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
