#!/usr/bin/env python3
"""Ponte entre a busca editorial e os registros locais da auditoria."""

from __future__ import annotations

import argparse
import base64
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import research_all_events as research


def needs_more_sources(data: dict) -> bool:
    domains = {
        research.domain(source.get("url", ""))
        for source in (data.get("sources") or [])
        if isinstance(source, dict)
        and source.get("url")
        and "jb-rider.com.br/eventos.php" not in source.get("url", "")
        and "/modalidades/calendario/busca/" not in source.get("url", "")
    }
    return len(domains) < 2


def export_queries(offset: int, limit: int, gaps: bool = False, social: bool = False) -> int:
    payload = []
    selected = []
    for absolute_index, record in enumerate(research.records()):
        if gaps and not needs_more_sources(record[3]):
            continue
        selected.append((absolute_index, record))
    for absolute_index, (kind, path, index, data) in selected[offset: offset + limit]:
        key = research.record_key(kind, path, index, data)
        title = data.get("title", "")
        city = data.get("city", "")
        state = data.get("state", "")
        if social:
            query = f'"{title}" {city} (site:instagram.com OR site:facebook.com OR site:youtube.com) 2026'
        elif gaps:
            query = f'{title} {city} {state} 2026 programação organização Instagram Facebook prefeitura'
        else:
            query = f'"{title}" {city} {state} 2026'
        payload.append({
            "absolute_index": absolute_index,
            "key": key,
            "kind": kind,
            "title": title,
            "city": city,
            "state": state,
            "query": query,
        })
    print(json.dumps(payload, ensure_ascii=False))
    return 0


def merge_payload(encoded: str) -> int:
    batch = json.loads(base64.b64decode(encoded).decode("utf-8"))
    incoming = {item["key"]: item for item in batch}
    merged = 0
    for kind, path, index, original in research.records():
        key = research.record_key(kind, path, index, original)
        item = incoming.get(key)
        if not item:
            continue
        data = dict(original)
        title_tokens = research.tokens(data.get("title", ""))
        discovered = []
        for candidate in item.get("results", []):
            url = research.clean_url(candidate.get("url", ""))
            if not url or research.domain(url) in research.EXCLUDED_DOMAINS:
                continue
            if not research.indexed_result_is_specific(data, {**candidate, "url": url}):
                continue
            combined = research.normalize(
                f"{candidate.get('label', '')} {url} {candidate.get('snippet', '')}"
            )
            combined_words = set(combined.split())
            matched = sum(token in combined_words for token in title_tokens)
            if not title_tokens or matched < min(2, len(title_tokens)):
                continue
            score = research.relevance(data, {"url": url, "label": candidate.get("label", "")}, candidate.get("snippet", ""))
            if score < 13:
                continue
            discovered.append({
                "url": url,
                "label": str(candidate.get("label") or research.domain(url))[:180],
                "type": research.source_type(url),
                "supports": research.supports(candidate.get("snippet", ""), url),
                "relevance_score": score,
                "discovery_method": "busca_editorial_indexada",
            })
        sources = research.deduplicate_sources(
            research.seed_sources(data) + sorted(discovered, key=lambda source: -source["relevance_score"])
        )
        specific_domains = {
            research.domain(source["url"]) for source in sources
            if "jb-rider.com.br/eventos.php" not in source["url"]
            and "/modalidades/calendario/busca/" not in source["url"]
        }
        checked_at = datetime.now(timezone.utc).isoformat()
        data["sources"] = sources
        data["source_checked_at"] = checked_at
        data["research_status"] = {
            "required_specific_independent_sources": 2,
            "specific_independent_domains_found": len(specific_domains),
            "status": "fontes_cruzadas" if len(specific_domains) >= 2 else "pesquisa_ampliada_ainda_sem_segunda_fonte_indexada",
            "query": item.get("query", ""),
            "reviewed_at": checked_at,
        }
        research.save_record(path, index, data)
        merged += 1
    print(json.dumps({"merged": merged, "received": len(batch)}, ensure_ascii=False))
    return 0 if merged == len(batch) else 2


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    export = sub.add_parser("export")
    export.add_argument("--offset", type=int, default=0)
    export.add_argument("--limit", type=int, default=25)
    export.add_argument("--gaps", action="store_true")
    export.add_argument("--social", action="store_true")
    merge = sub.add_parser("merge")
    merge.add_argument("--payload", required=True)
    args = parser.parse_args()
    if args.command == "export":
        return export_queries(args.offset, args.limit, args.gaps, args.social)
    return merge_payload(args.payload)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
