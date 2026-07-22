#!/usr/bin/env python3
"""Generate sitemap.xml from the public content collections.

Run this script after adding or updating an article, video, competition, or
event. Query-string values are percent-encoded so accented Portuguese slugs
remain valid URLs for search engines.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import date, datetime
from pathlib import Path
from urllib.parse import quote
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://tvduasrodas.com"
SITEMAP = ROOT / "sitemap.xml"

STATIC_PAGES = [
    ("/", "1.0"),
    ("/revista.html", "0.9"),
    ("/tv.html", "0.9"),
    ("/materia.html", "0.7"),
    ("/busca.html", "0.6"),
    ("/sobre.html", "0.5"),
    ("/contato.html", "0.5"),
    ("/imprensa.html", "0.5"),
    ("/termos.html", "0.3"),
    ("/politica-de-privacidade.html", "0.3"),
    ("/guia-scooters-eletricas.html", "0.7"),
    ("/review-naked-300.html", "0.7"),
    ("/role-urbano-noturno.html", "0.7"),
    ("/viagem-serra-mirantes.html", "0.7"),
    ("/competicoes-eventos.html", "0.9"),
]

# Update this date when a standalone static page receives a material edit.
# Dynamic collection pages derive their dates from content automatically.
STATIC_LASTMOD_OVERRIDES = {
    "/sobre.html": "2026-07-22",
}


def iso_day(value: object, fallback: str) -> str:
    if not value:
        return fallback
    match = re.search(r"\d{4}-\d{2}-\d{2}", str(value))
    return match.group(0) if match else fallback


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8-sig")
    if not text.startswith("---"):
        return {}
    block = text.split("---", 2)[1]
    values: dict[str, str] = {}
    for line in block.splitlines():
        match = re.match(r"^([A-Za-z_][\w-]*):\s*(.*?)\s*$", line)
        if match:
            values[match.group(1)] = match.group(2).strip("'\"")
    return values


def previous_dates() -> dict[str, str]:
    if not SITEMAP.exists():
        return {}
    try:
        root = ET.parse(SITEMAP).getroot()
    except ET.ParseError:
        return {}
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    dates: dict[str, str] = {}
    for item in root.findall("sm:url", ns):
        loc = item.findtext("sm:loc", default="", namespaces=ns)
        lastmod = item.findtext("sm:lastmod", default="", namespaces=ns)
        if loc and lastmod:
            dates[loc] = lastmod
    return dates


def public_slugs(collection: str) -> list[str]:
    index_path = ROOT / "content" / collection / "index.json"
    suffix = ".json" if collection in {"competitions", "events"} else ".md"
    files = {
        path.stem
        for path in (ROOT / "content" / collection).glob(f"*{suffix}")
        if path.name != "index.json"
    }
    if not index_path.exists():
        return sorted(files)

    indexed = json.loads(index_path.read_text(encoding="utf-8-sig"))
    missing_files = [slug for slug in indexed if slug not in files]
    if missing_files:
        raise FileNotFoundError(
            f"{collection}/index.json references missing files: {', '.join(missing_files)}"
        )

    # Union with files on disk so a newly created public record can never be
    # silently omitted from the sitemap merely because index.json is stale.
    return list(dict.fromkeys([*indexed, *sorted(files - set(indexed))]))


def json_date(path: Path, fallback: str) -> str:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    return iso_day(data.get("last_updated") or data.get("date") or data.get("start_date"), fallback)


def add_url(urls: list[tuple[str, str, str]], path: str, lastmod: str, priority: str) -> None:
    urls.append((f"{BASE_URL}{path}", lastmod, priority))


def main(*, check_only: bool = False) -> None:
    today = date.today().isoformat()
    old_dates = previous_dates()
    urls: list[tuple[str, str, str]] = []

    news: list[tuple[str, str]] = []
    for path in sorted((ROOT / "content" / "news").glob("*.md")):
        values = frontmatter(path)
        news.append((path.stem, iso_day(values.get("updated_at") or values.get("date"), today)))

    videos: list[tuple[str, str]] = []
    for path in sorted((ROOT / "content" / "videos").glob("*.md")):
        values = frontmatter(path)
        youtube_url = values.get("youtube_url", "")
        match = re.search(r"(?:v=|youtu\.be/)([A-Za-z0-9_-]{6,})", youtube_url)
        if not match:
            match = re.fullmatch(r"([A-Za-z0-9_-]{6,})", youtube_url)
        if match:
            videos.append((match.group(1), iso_day(values.get("date"), today)))

    competitions = [
        (slug, json_date(ROOT / "content" / "competitions" / f"{slug}.json", today))
        for slug in public_slugs("competitions")
    ]
    events = [
        (slug, json_date(ROOT / "content" / "events" / f"{slug}.json", today))
        for slug in public_slugs("events")
    ]

    all_dynamic_dates = [lastmod for _, lastmod in news + videos + competitions + events]
    newest = max(all_dynamic_dates, default=today)
    section_dates = {
        "/": newest,
        "/revista.html": max((value for _, value in news), default=today),
        "/materia.html": max((value for _, value in news), default=today),
        "/tv.html": max((value for _, value in videos), default=today),
        "/competicoes-eventos.html": max((value for _, value in competitions + events), default=today),
    }

    for path, priority in STATIC_PAGES:
        full_url = f"{BASE_URL}{path}"
        lastmod = section_dates.get(
            path,
            STATIC_LASTMOD_OVERRIDES.get(path, old_dates.get(full_url, today)),
        )
        add_url(urls, path, lastmod, priority)

    for slug, lastmod in news:
        encoded = quote(slug, safe="-._~")
        add_url(urls, f"/materia.html?slug={encoded}", lastmod, "0.8")

    for video_id, lastmod in videos:
        add_url(urls, f"/tv.html?v={video_id}", lastmod, "0.7")

    for slug, lastmod in competitions:
        add_url(urls, f"/competicao.html?slug={quote(slug, safe='-._~')}", lastmod, "0.8")

    for slug, lastmod in events:
        add_url(urls, f"/evento.html?slug={quote(slug, safe='-._~')}", lastmod, "0.7")

    namespace = "http://www.sitemaps.org/schemas/sitemap/0.9"
    ET.register_namespace("", namespace)
    urlset = ET.Element(f"{{{namespace}}}urlset")
    for loc, lastmod, priority in urls:
        item = ET.SubElement(urlset, f"{{{namespace}}}url")
        ET.SubElement(item, f"{{{namespace}}}loc").text = loc
        ET.SubElement(item, f"{{{namespace}}}lastmod").text = lastmod
        ET.SubElement(item, f"{{{namespace}}}priority").text = priority

    ET.indent(urlset, space="  ")
    xml = ET.tostring(urlset, encoding="unicode", xml_declaration=True)
    expected = xml + "\n"
    breakdown = (
        f"static={len(STATIC_PAGES)}, news={len(news)}, videos={len(videos)}, "
        f"competitions={len(competitions)}, events={len(events)}"
    )

    if check_only:
        current = SITEMAP.read_text(encoding="utf-8") if SITEMAP.exists() else ""
        if current != expected:
            raise SystemExit(
                f"STALE {SITEMAP.name}: expected {len(urls)} URLs ({breakdown}). "
                "Run scripts/update_sitemap.py and publish the result."
            )
        print(f"OK {SITEMAP.name}: {len(urls)} URLs ({breakdown}), newest {newest}")
        return

    SITEMAP.write_text(expected, encoding="utf-8", newline="\n")
    print(f"Updated {SITEMAP.name}: {len(urls)} URLs ({breakdown}), newest {newest}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail without writing when sitemap.xml does not match public content.",
    )
    args = parser.parse_args()
    main(check_only=args.check)
