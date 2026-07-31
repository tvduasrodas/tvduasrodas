#!/usr/bin/env python3
"""Gera o catálogo leve usado pela busca geral do painel editorial."""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
OUTPUT = ROOT / "admin" / "content-index.json"


def clean_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1]
    return value.replace("\\'", "'").replace('\\"', '"')


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8-sig")
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    data: dict[str, str] = {}
    for line in parts[1].splitlines():
        match = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if match:
            data[match.group(1)] = clean_scalar(match.group(2))
    return data


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii").lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value


def cms_url(collection: str, entry: str) -> str:
    return f"/admin/#/collections/{quote(collection)}/entries/{quote(entry)}"


def public_url(kind: str, slug: str) -> str:
    prefixes = {
        "Matéria": "materias",
        "Matéria do acervo": "materias",
        "Vídeo": "videos",
        "Competição": "competicoes",
        "Evento": "eventos",
        "Evento da agenda": "eventos",
        "Etapa esportiva": "eventos",
    }
    prefix = prefixes.get(kind)
    return f"/{prefix}/{slug}/" if prefix and slug else ""


def add(
    rows: list[dict],
    *,
    title: str,
    kind: str,
    slug: str,
    source: str,
    edit: str,
    date: str = "",
    category: str = "",
    city: str = "",
    state: str = "",
    status: str = "",
    summary: str = "",
    url: str = "",
) -> None:
    title = str(title or slug or source).strip()
    if not title:
        return
    rows.append(
        {
            "title": title,
            "type": kind,
            "slug": str(slug or ""),
            "date": str(date or ""),
            "category": str(category or ""),
            "city": str(city or ""),
            "state": str(state or ""),
            "status": str(status or ""),
            "summary": re.sub(r"\s+", " ", str(summary or "")).strip()[:360],
            "url": url or public_url(kind, str(slug or "")),
            "edit_url": edit,
            "source": source.replace("\\", "/"),
        }
    )


def index_markdown(rows: list[dict]) -> None:
    specs = [
        ("news", "news", "Matéria"),
        ("videos", "videos", "Vídeo"),
    ]
    for folder, collection, kind in specs:
        for path in sorted((CONTENT / folder).glob("*.md")):
            data = frontmatter(path)
            slug = slugify(path.stem)
            add(
                rows,
                title=data.get("title", path.stem),
                kind=kind,
                slug=slug,
                date=data.get("date", ""),
                category=data.get("category", ""),
                summary=data.get("summary", ""),
                source=path.relative_to(ROOT).as_posix(),
                edit=cms_url(collection, path.stem),
            )

    page_urls = {"sobre": "/sobre.html", "contato": "/contato.html"}
    for path in sorted((CONTENT / "pages").glob("*.md")):
        data = frontmatter(path)
        add(
            rows,
            title=data.get("title", path.stem),
            kind="Página fixa",
            slug=path.stem,
            source=path.relative_to(ROOT).as_posix(),
            edit=cms_url("pages", path.stem),
            url=page_urls.get(path.stem, f"/{slugify(path.stem)}.html"),
        )

    for path in sorted((CONTENT / "home").glob("*.md")):
        data = frontmatter(path)
        entry = path.stem.replace("-", "_")
        add(
            rows,
            title=data.get("title", path.stem),
            kind="Configuração da home",
            slug=path.stem,
            source=path.relative_to(ROOT).as_posix(),
            edit=cms_url("home", entry),
            url="/",
        )


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def index_json_entries(rows: list[dict]) -> None:
    specs = [
        ("articles", "legacy_articles", "Matéria do acervo"),
        ("competitions", "competitions", "Competição"),
        ("events", "events", "Evento"),
    ]
    for folder, collection, kind in specs:
        for path in sorted((CONTENT / folder).glob("*.json")):
            if path.name in {"index.json", "agenda-comunitaria-2026.json"}:
                continue
            try:
                data = load_json(path)
            except (OSError, json.JSONDecodeError):
                continue
            if not isinstance(data, dict) or not data.get("title"):
                continue
            slug = str(data.get("slug") or path.stem)
            add(
                rows,
                title=data.get("title", slug),
                kind=kind,
                slug=slug,
                date=data.get("date") or data.get("start_date") or data.get("season", ""),
                category=data.get("category") or data.get("modality") or data.get("event_type", ""),
                city=data.get("city", ""),
                state=data.get("state", ""),
                status=data.get("status", ""),
                summary=data.get("summary", ""),
                source=path.relative_to(ROOT).as_posix(),
                edit=cms_url(collection, path.stem),
            )


def index_consolidated(rows: list[dict]) -> None:
    specs = [
        (
            CONTENT / "events" / "agenda-comunitaria-2026.json",
            "Evento da agenda",
            "agenda_comunitaria_2026",
        ),
        (
            CONTENT / "calendar" / "cbm-2026.json",
            "Etapa esportiva",
            "calendario_categorias_2026",
        ),
    ]
    for path, kind, entry_name in specs:
        try:
            data = load_json(path)
        except (OSError, json.JSONDecodeError):
            continue
        edit = cms_url("consolidated_agendas", entry_name)
        for item in data.get("entries", []):
            if not isinstance(item, dict):
                continue
            if path.name == "agenda-comunitaria-2026.json" and (
                item.get("duplicate_of") or item.get("reclassified_as") == "competition"
            ):
                continue
            base = " ".join(
                str(part or "")
                for part in (
                    item.get("title"),
                    item.get("stage"),
                    item.get("city"),
                    item.get("state"),
                    item.get("start_date"),
                )
            )
            slug = str(item.get("slug") or slugify(base))
            add(
                rows,
                title=item.get("title", slug),
                kind=kind,
                slug=slug,
                date=item.get("start_date", ""),
                category=item.get("event_type") or item.get("modality") or item.get("segment", ""),
                city=item.get("city", ""),
                state=item.get("state", ""),
                status=item.get("status", ""),
                summary=item.get("summary", ""),
                source=f"{path.relative_to(ROOT).as_posix()}#{slug}",
                edit=edit,
            )


def build() -> dict:
    rows: list[dict] = []
    index_markdown(rows)
    index_json_entries(rows)
    index_consolidated(rows)
    rows.sort(key=lambda row: (row["title"].casefold(), row["type"], row["slug"]))
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["type"]] = counts.get(row["type"], 0) + 1
    return {
        "schema_version": 1,
        "total": len(rows),
        "counts": dict(sorted(counts.items())),
        "entries": rows,
    }


def main() -> None:
    payload = build()
    OUTPUT.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Índice do CMS: {payload['total']} itens em {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
