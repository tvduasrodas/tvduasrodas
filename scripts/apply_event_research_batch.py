#!/usr/bin/env python3
"""Aplica lotes auditáveis de pesquisa a eventos sem reformatar toda a agenda."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def merge(target: dict[str, Any], patch: dict[str, Any]) -> dict[str, Any]:
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(target.get(key), dict):
            target[key] = merge(target[key], value)
        else:
            target[key] = value
    return target


def object_bounds(text: str, slug: str) -> tuple[int, int]:
    match = re.search(rf'"slug"\s*:\s*"{re.escape(slug)}"', text)
    if not match:
        raise ValueError(f"slug não encontrado: {slug}")

    start = text.rfind("{", 0, match.start())
    if start < 0:
        raise ValueError(f"início do objeto não encontrado: {slug}")

    depth = 0
    in_string = False
    escaped = False
    for index in range(start, len(text)):
        char = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return start, index + 1
    raise ValueError(f"fim do objeto não encontrado: {slug}")


def render_indented_object(payload: dict[str, Any], outer_indent: int) -> str:
    lines = json.dumps(payload, ensure_ascii=False, indent=4).splitlines()
    return lines[0] + "\n" + "\n".join((" " * outer_indent) + line for line in lines[1:])


def update_community(path: Path, patches: list[dict[str, Any]]) -> None:
    text = path.read_text(encoding="utf-8-sig")
    seen: set[str] = set()
    for item in patches:
        slug = item["slug"]
        if slug in seen:
            raise ValueError(f"slug repetido no lote: {slug}")
        seen.add(slug)
        start, end = object_bounds(text, slug)
        current = json.loads(text[start:end])
        updated = merge(current, item["patch"])
        line_start = text.rfind("\n", 0, start) + 1
        outer_indent = start - line_start
        text = text[:start] + render_indented_object(updated, outer_indent) + text[end:]
    path.write_text(text, encoding="utf-8")


def update_standalone(path: Path, patch: dict[str, Any]) -> None:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    merge(payload, patch)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("batch", type=Path)
    args = parser.parse_args()

    batch_path = args.batch if args.batch.is_absolute() else ROOT / args.batch
    batch = json.loads(batch_path.read_text(encoding="utf-8"))
    grouped: dict[Path, list[dict[str, Any]]] = {}
    for item in batch["updates"]:
        target = ROOT / item["target_file"]
        grouped.setdefault(target, []).append(item)

    for target, items in grouped.items():
        if target.name == "agenda-comunitaria-2026.json":
            update_community(target, items)
        else:
            if len(items) != 1 or items[0].get("slug"):
                raise ValueError(f"arquivo individual exige uma única atualização sem slug: {target}")
            update_standalone(target, items[0]["patch"])
        print(f"Atualizado: {target.relative_to(ROOT)} ({len(items)} registro(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
