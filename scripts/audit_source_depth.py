#!/usr/bin/env python3
"""Audita profundidade, independência e rastreabilidade das fontes da central."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
PLACEHOLDER = re.compile(
    r"não informado|a confirmar|confirme com|local informado|agenda nacional|"
    r"não detalhado|não divulgado",
    re.I,
)
GENERIC_PATHS = (
    "/modalidades/calendario/busca/",
    "/eventos.php",
)
PRIMARY_TYPES = ("primária", "oficial", "organizador", "regulamento", "entidade esportiva")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def domain(url: str) -> str:
    return urlparse(str(url or "")).netloc.lower().removeprefix("www.")


def canonical_sources(data: dict[str, Any]) -> list[dict[str, Any]]:
    sources = data.get("sources") if isinstance(data.get("sources"), list) else []
    seen: set[str] = set()
    clean: list[dict[str, Any]] = []
    for source in sources:
        if not isinstance(source, dict):
            continue
        url = str(source.get("url") or "").strip()
        host = domain(url)
        if not url or not host or url in seen:
            continue
        seen.add(url)
        clean.append(source)
    return clean


def inventory() -> list[tuple[str, str, dict[str, Any]]]:
    rows: list[tuple[str, str, dict[str, Any]]] = []
    events_dir = ROOT / "content/events"
    for path in sorted(events_dir.glob("*.json")):
        if path.name == "index.json":
            continue
        payload = load_json(path)
        if path.name == "agenda-comunitaria-2026.json":
            for entry in payload.get("entries", []):
                rows.append(("agenda", str(entry.get("slug") or ""), entry))
        else:
            rows.append(("evento", path.stem, payload))
    calendar = load_json(ROOT / "content/calendar/cbm-2026.json")
    for entry in calendar.get("entries", []):
        slug = re.sub(r"[^a-z0-9]+", "-", f"{entry.get('title', '')}-{entry.get('start_date', '')}".lower()).strip("-")
        rows.append(("calendario", slug, entry))
    for path in sorted((ROOT / "content/competitions").glob("*.json")):
        if path.name != "index.json":
            rows.append(("competicao", path.stem, load_json(path)))
    return rows


def evaluate(kind: str, slug: str, data: dict[str, Any]) -> dict[str, Any]:
    sources = canonical_sources(data)
    domains = {domain(source.get("url", "")) for source in sources}
    specific = [
        source for source in sources
        if not any(path in str(source.get("url") or "") for path in GENERIC_PATHS)
    ]
    specific_domains = {domain(source.get("url", "")) for source in specific}
    primary = any(
        any(marker in f"{source.get('type', '')} {source.get('label', '')}".lower() for marker in PRIMARY_TYPES)
        for source in specific
    )
    body = str(data.get("body") or "")
    summary = str(data.get("summary") or "")
    source_support = all(str(source.get("supports") or "").strip() for source in specific)

    missing: list[str] = []
    if len(specific_domains) < 2:
        missing.append("duas_fontes_especificas_independentes")
    if not primary:
        missing.append("fonte_primaria")
    if specific and not source_support:
        missing.append("rastreabilidade_por_fato")
    if not data.get("source_checked_at"):
        missing.append("data_da_checagem")
    if kind != "competicao":
        if not (data.get("time_label") or data.get("local_start")):
            missing.append("horario_local")
        if not (data.get("full_address") or data.get("street_address") or data.get("venue") or data.get("location") or data.get("city")):
            missing.append("local")
        if not body or len(body) < 350:
            missing.append("conteudo_aprofundado")
        if not data.get("organizer"):
            missing.append("organizacao")
        if not data.get("visual_verification"):
            missing.append("evidencia_visual_ou_justificativa")
    else:
        if not body or len(body) < 350:
            missing.append("contexto_da_competicao")
        if not (data.get("rounds") or data.get("calendar_status")):
            missing.append("calendario_de_etapas")
        if not (data.get("standings") or data.get("latest_result") or data.get("classification_status")):
            missing.append("classificacao_ou_resultado")
    placeholders = sum(
        bool(PLACEHOLDER.search(str(data.get(field) or "")))
        for field in ("time_label", "full_address", "parking", "admission_status", "contact")
    )
    return {
        "kind": kind,
        "slug": slug,
        "title": data.get("title"),
        "date": data.get("start_date") or data.get("season"),
        "city": data.get("city"),
        "state": data.get("state"),
        "source_count": len(sources),
        "independent_domains": len(domains),
        "specific_independent_domains": len(specific_domains),
        "placeholder_fields": placeholders,
        "missing": missing,
        "complete": not missing,
        "duplicate_of": data.get("duplicate_of"),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()
    results = [evaluate(*row) for row in inventory()]
    canonical = [item for item in results if not item.get("duplicate_of")]
    incomplete = [item for item in canonical if not item["complete"]]
    by_kind: dict[str, dict[str, int]] = {}
    for item in canonical:
        bucket = by_kind.setdefault(item["kind"], {"total": 0, "complete": 0})
        bucket["total"] += 1
        bucket["complete"] += int(item["complete"])
    report = {
        "total_records": len(results),
        "canonical_records": len(canonical),
        "complete_records": len(canonical) - len(incomplete),
        "incomplete_records": len(incomplete),
        "by_kind": by_kind,
        "queue": incomplete,
    }
    serialized = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        output = args.output if args.output.is_absolute() else ROOT / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(serialized + "\n", encoding="utf-8")
    if not args.quiet:
        print(serialized)
    return 1 if incomplete else 0


if __name__ == "__main__":
    raise SystemExit(main())
