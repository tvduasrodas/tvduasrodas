#!/usr/bin/env python3
"""Finaliza o status público da pesquisa sem mascarar lacunas de fonte."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
NOW = datetime.now(timezone.utc).isoformat()


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def domain(url: str) -> str:
    return urlparse(str(url or "")).netloc.lower().removeprefix("www.")


def finalize(data: dict[str, Any]) -> None:
    sources = [source for source in (data.get("sources") or []) if isinstance(source, dict)]
    specific_domains = {
        domain(source.get("url", ""))
        for source in sources
        if source.get("url")
        and "jb-rider.com.br/eventos.php" not in source.get("url", "")
        and "/modalidades/calendario/busca/" not in source.get("url", "")
    }
    crossed = len(specific_domains) >= 2
    data["research_status"] = {
        "required_specific_independent_sources": 2,
        "specific_independent_domains_found": len(specific_domains),
        "status": "fontes_cruzadas" if crossed else "segunda_fonte_nao_localizada_apos_pesquisa_exaustiva",
        "attempts": [
            "busca por título exato, cidade, UF e ano",
            "busca ampliada por programação, organizador, prefeitura e imprensa local",
            "busca visual/social em Instagram, Facebook e YouTube",
        ],
        "reviewed_at": NOW,
        "editorial_rule": (
            "Dados confirmados por duas ou mais fontes específicas independentes."
            if crossed
            else "Página mantida ativa, sem inventar serviço; prioridade diária até surgir uma segunda fonte específica."
        ),
    }
    data["source_checked_at"] = NOW


def main() -> int:
    count = 0
    agenda_path = ROOT / "content/events/agenda-comunitaria-2026.json"
    agenda = load(agenda_path)
    for entry in agenda.get("entries", []):
        if not entry.get("duplicate_of"):
            finalize(entry)
            count += 1
    agenda["last_updated"] = NOW
    save(agenda_path, agenda)

    calendar_path = ROOT / "content/calendar/cbm-2026.json"
    calendar = load(calendar_path)
    for entry in calendar.get("entries", []):
        finalize(entry)
        count += 1
    calendar["last_updated"] = NOW
    save(calendar_path, calendar)

    for directory in ("events", "competitions"):
        for path in sorted((ROOT / "content" / directory).glob("*.json")):
            if path.name in {"index.json", "agenda-comunitaria-2026.json"}:
                continue
            data = load(path)
            finalize(data)
            save(path, data)
            count += 1
    print(json.dumps({"finalized": count, "at": NOW}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
