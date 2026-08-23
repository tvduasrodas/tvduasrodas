#!/usr/bin/env python3
"""Generate sitemap.xml from the public content collections.

Execute ``build_seo_site.py`` antes deste script. O sitemap publica somente as
URLs canônicas com HTML estático; os antigos endereços com parâmetros ficam
fora para não dividir sinais de indexação.
"""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import quote
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://tvduasrodas.com"
SITEMAP = ROOT / "sitemap.xml"
NEWS_SITEMAP = ROOT / "news-sitemap.xml"
EVENT_SITEMAP = ROOT / "event-sitemap.xml"

STATIC_PAGES = [
    ("/", "1.0"),
    ("/revista", "0.9"),
    ("/tv", "0.9"),
    ("/sobre", "0.5"),
    ("/equipe", "0.5"),
    ("/contato", "0.5"),
    ("/imprensa", "0.5"),
    ("/termos", "0.3"),
    ("/politica-de-privacidade", "0.3"),
    ("/politica-editorial", "0.4"),
    ("/politica-de-correcoes", "0.4"),
    ("/guia-scooters-eletricas", "0.7"),
    ("/review-naked-300", "0.7"),
    ("/role-urbano-noturno", "0.7"),
    ("/viagem-serra-mirantes", "0.7"),
    ("/competicoes-eventos", "0.9"),
]

# Update this date when a standalone static page receives a material edit.
# Dynamic collection pages derive their dates from content automatically.
STATIC_LASTMOD_OVERRIDES = {
    "/sobre": "2026-08-22",
    "/equipe": "2026-08-22",
    "/contato": "2026-08-22",
    "/imprensa": "2026-08-22",
    "/politica-de-privacidade": "2026-08-22",
    "/termos": "2026-08-22",
    "/politica-editorial": "2026-08-22",
    "/politica-de-correcoes": "2026-08-22",
    "/guia-scooters-eletricas": "2026-08-22",
    "/review-naked-300": "2026-08-22",
    "/role-urbano-noturno": "2026-08-22",
    "/viagem-serra-mirantes": "2026-08-22",
}


def iso_day(value: object, fallback: str) -> str:
    if not value:
        return fallback
    match = re.search(r"\d{4}-\d{2}-\d{2}", str(value))
    return match.group(0) if match else fallback


def safe_lastmod(value: object, fallback: str, today: str) -> str:
    """Return a trustworthy lastmod that never points into the future."""
    candidate = iso_day(value, fallback)
    return fallback if candidate > today else candidate


def parse_datetime(value: object) -> datetime | None:
    if not value:
        return None
    raw = str(value).strip().strip("'\"")
    try:
        parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        day = iso_day(raw, "")
        if not day:
            return None
        parsed = datetime.fromisoformat(day)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


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


def previous_entries() -> dict[str, tuple[str, str]]:
    if not SITEMAP.exists():
        return {}
    try:
        root = ET.parse(SITEMAP).getroot()
    except ET.ParseError:
        return {}
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    entries: dict[str, tuple[str, str]] = {}
    for item in root.findall("sm:url", ns):
        loc = item.findtext("sm:loc", default="", namespaces=ns)
        lastmod = item.findtext("sm:lastmod", default="", namespaces=ns)
        priority = item.findtext("sm:priority", default="0.6", namespaces=ns)
        if loc and lastmod:
            entries[loc] = (lastmod, priority)
    return entries


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


def json_date(path: Path, fallback: str, today: str) -> str:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    changed_at = (
        data.get("last_updated")
        or data.get("updated_at")
        or data.get("status_checked_at")
        or data.get("source_checked_at")
        or data.get("date")
    )
    return safe_lastmod(changed_at, fallback, today)

def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFD", value)
    ascii_value = "".join(char for char in normalized if unicodedata.category(char) != "Mn")
    return re.sub(r"(^-+|-+$)", "", re.sub(r"[^a-z0-9]+", "-", ascii_value.lower()))


def add_url(urls: list[tuple[str, str, str]], path: str, lastmod: str, priority: str) -> None:
    urls.append((f"{BASE_URL}{path}", lastmod, priority))


def render_news_sitemap(news: list[dict[str, str]], now: datetime) -> str:
    sitemap_namespace = "http://www.sitemaps.org/schemas/sitemap/0.9"
    news_namespace = "http://www.google.com/schemas/sitemap-news/0.9"
    ET.register_namespace("", sitemap_namespace)
    ET.register_namespace("news", news_namespace)
    urlset = ET.Element(f"{{{sitemap_namespace}}}urlset")
    cutoff = now.astimezone(timezone.utc) - timedelta(days=2)

    ordered = sorted(news, key=lambda item: item["published_at"], reverse=True)
    recent_urls = {
        item["url"]
        for item in ordered
        if item["published_at"] and cutoff <= datetime.fromisoformat(item["published_at"]) <= now
    }
    if len(recent_urls) > 1000:
        raise ValueError(
            "news-sitemap.xml excederia o limite de 1.000 blocos news:news"
        )

    # Every published article URL remains in this file permanently. Google
    # explicitly permits retaining older URLs as long as their news:news
    # metadata is removed after two days.
    for article in ordered:
        item = ET.SubElement(urlset, f"{{{sitemap_namespace}}}url")
        ET.SubElement(item, f"{{{sitemap_namespace}}}loc").text = article["url"]
        if article["url"] not in recent_urls:
            continue
        news_item = ET.SubElement(item, f"{{{news_namespace}}}news")
        publication = ET.SubElement(news_item, f"{{{news_namespace}}}publication")
        ET.SubElement(publication, f"{{{news_namespace}}}name").text = "TVDUASRODAS"
        ET.SubElement(publication, f"{{{news_namespace}}}language").text = "pt"
        ET.SubElement(news_item, f"{{{news_namespace}}}publication_date").text = article["publication_date"]
        ET.SubElement(news_item, f"{{{news_namespace}}}title").text = article["title"]

    ET.indent(urlset, space="  ")
    return ET.tostring(urlset, encoding="unicode", xml_declaration=True) + "\n"


def render_event_sitemap(manifest: list[dict[str, object]], today: str) -> str:
    """Publish every canonical event URL, including completed events."""
    sitemap_namespace = "http://www.sitemaps.org/schemas/sitemap/0.9"
    image_namespace = "http://www.google.com/schemas/sitemap-image/1.1"
    ET.register_namespace("", sitemap_namespace)
    ET.register_namespace("image", image_namespace)
    urlset = ET.Element(f"{{{sitemap_namespace}}}urlset")

    events = sorted(
        (item for item in manifest if item.get("kind") == "event"),
        key=lambda item: str(item.get("url", "")),
    )
    for event in events:
        item = ET.SubElement(urlset, f"{{{sitemap_namespace}}}url")
        ET.SubElement(item, f"{{{sitemap_namespace}}}loc").text = (
            f"{BASE_URL}{event['url']}"
        )
        ET.SubElement(item, f"{{{sitemap_namespace}}}lastmod").text = safe_lastmod(
            event.get("lastmod"),
            today,
            today,
        )
        if event.get("image"):
            image = ET.SubElement(item, f"{{{image_namespace}}}image")
            ET.SubElement(image, f"{{{image_namespace}}}loc").text = str(event["image"])

    ET.indent(urlset, space="  ")
    return ET.tostring(urlset, encoding="unicode", xml_declaration=True) + "\n"


def main(*, check_only: bool = False) -> None:
    today = date.today().isoformat()
    now = datetime.now(timezone.utc)
    old_entries = previous_entries()
    old_dates = {
        loc: values[0]
        for loc, values in old_entries.items()
    }
    urls: list[tuple[str, str, str]] = []

    news: list[tuple[str, str]] = []
    news_items: list[dict[str, str]] = []
    for path in sorted((ROOT / "content" / "news").glob("*.md")):
        values = frontmatter(path)
        published_at = parse_datetime(values.get("date"))
        changed_at = values.get("updated_at") or values.get("date")
        news.append((path.stem, safe_lastmod(changed_at, today, today)))
        if published_at:
            news_items.append({
                "url": f"{BASE_URL}/materias/{slugify(path.stem)}/",
                "title": values.get("title", path.stem),
                "publication_date": str(values.get("date") or published_at.date().isoformat()),
                "published_at": published_at.isoformat(),
            })

    videos: list[tuple[str, str]] = []
    for path in sorted((ROOT / "content" / "videos").glob("*.md")):
        values = frontmatter(path)
        youtube_url = values.get("youtube_url", "")
        match = re.search(r"(?:v=|youtu\.be/)([A-Za-z0-9_-]{6,})", youtube_url)
        if not match:
            match = re.fullmatch(r"([A-Za-z0-9_-]{6,})", youtube_url)
        if match:
            videos.append((match.group(1), safe_lastmod(values.get("date"), today, today)))

    competitions = [
        (
            slug,
            json_date(
                ROOT / "content" / "competitions" / f"{slug}.json",
                old_dates.get(f"{BASE_URL}/competicoes/{slugify(slug)}/", today),
                today,
            ),
        )
        for slug in public_slugs("competitions")
    ]
    events = [
        (
            slug,
            json_date(
                ROOT / "content" / "events" / f"{slug}.json",
                old_dates.get(f"{BASE_URL}/eventos/{slugify(slug)}/", today),
                today,
            ),
        )
        for slug in public_slugs("events")
    ]
    calendar_data = json.loads(
        (ROOT / "content" / "calendar" / "cbm-2026.json").read_text(encoding="utf-8-sig")
    )
    calendar_events = [
        (
            slugify(f"{item.get('title', '')}-{item.get('start_date', '')}"),
            safe_lastmod(
                item.get("last_updated")
                or item.get("source_checked_at")
                or calendar_data.get("last_updated"),
                today,
                today,
            ),
        )
        for item in calendar_data.get("entries", [])
        if not item.get("competition_slug")
    ]
    existing_event_slugs = {slug for slug, _ in events}
    calendar_events = [
        item for item in calendar_events
        if item[0] and item[0] not in existing_event_slugs
    ]

    all_dynamic_dates = [lastmod for _, lastmod in news + videos + competitions + events + calendar_events]
    newest = max(all_dynamic_dates, default=today)
    section_dates = {
        "/": newest,
        "/revista": max((value for _, value in news), default=today),
        "/tv": max((value for _, value in videos), default=today),
        "/competicoes-eventos": max((value for _, value in competitions + events + calendar_events), default=today),
    }

    for path, priority in STATIC_PAGES:
        full_url = f"{BASE_URL}{path}"
        lastmod = section_dates.get(
            path,
            STATIC_LASTMOD_OVERRIDES.get(path, old_dates.get(full_url, today)),
        )
        add_url(urls, path, lastmod, priority)

    manifest_path = ROOT / "content" / "seo-manifest.json"
    if not manifest_path.exists():
        raise FileNotFoundError(
            "content/seo-manifest.json ausente; execute scripts/build_seo_site.py"
        )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    expected_events = render_event_sitemap(manifest, today)
    for item in manifest:
        add_url(
            urls,
            str(item["url"]),
            safe_lastmod(item.get("lastmod"), today, today),
            str(item.get("priority", "0.6")),
        )

    # A canonical article URL that has already been published must never
    # disappear merely because a source index or manifest was regenerated.
    # Removal requires an explicit, reviewed migration instead of an
    # automatic sitemap rewrite.
    current_locs = {loc for loc, _, _ in urls}
    protected_prefix = f"{BASE_URL}/materias/"
    for loc, (lastmod, priority) in old_entries.items():
        if loc == protected_prefix or not loc.startswith(protected_prefix):
            continue
        if loc not in current_locs:
            urls.append((loc, safe_lastmod(lastmod, today, today), priority))
            current_locs.add(loc)

    namespace = "http://www.sitemaps.org/schemas/sitemap/0.9"
    image_namespace = "http://www.google.com/schemas/sitemap-image/1.1"
    video_namespace = "http://www.google.com/schemas/sitemap-video/1.1"
    ET.register_namespace("", namespace)
    ET.register_namespace("image", image_namespace)
    ET.register_namespace("video", video_namespace)
    media_by_url = {
        f"{BASE_URL}{item['url']}": item
        for item in manifest
    }
    urlset = ET.Element(f"{{{namespace}}}urlset")
    for loc, lastmod, priority in urls:
        item = ET.SubElement(urlset, f"{{{namespace}}}url")
        ET.SubElement(item, f"{{{namespace}}}loc").text = loc
        ET.SubElement(item, f"{{{namespace}}}lastmod").text = lastmod
        ET.SubElement(item, f"{{{namespace}}}priority").text = priority
        media = media_by_url.get(loc, {})
        if media.get("image"):
            image = ET.SubElement(item, f"{{{image_namespace}}}image")
            ET.SubElement(image, f"{{{image_namespace}}}loc").text = media["image"]
        if media.get("video"):
            video_data = media["video"]
            video = ET.SubElement(item, f"{{{video_namespace}}}video")
            ET.SubElement(video, f"{{{video_namespace}}}thumbnail_loc").text = video_data["thumbnail"]
            ET.SubElement(video, f"{{{video_namespace}}}title").text = video_data["title"]
            ET.SubElement(video, f"{{{video_namespace}}}description").text = video_data["description"]
            ET.SubElement(video, f"{{{video_namespace}}}player_loc").text = video_data["player"]
            ET.SubElement(video, f"{{{video_namespace}}}publication_date").text = video_data["upload_date"]

    ET.indent(urlset, space="  ")
    xml = ET.tostring(urlset, encoding="unicode", xml_declaration=True)
    expected = xml + "\n"
    expected_news = render_news_sitemap(news_items, now)
    breakdown = (
        f"static={len(STATIC_PAGES)}, canonical_generated={len(manifest)}"
    )

    if check_only:
        current = SITEMAP.read_text(encoding="utf-8") if SITEMAP.exists() else ""
        current_news = NEWS_SITEMAP.read_text(encoding="utf-8") if NEWS_SITEMAP.exists() else ""
        current_events = EVENT_SITEMAP.read_text(encoding="utf-8") if EVENT_SITEMAP.exists() else ""
        stale = []
        if current != expected:
            stale.append(SITEMAP.name)
        if current_news != expected_news:
            stale.append(NEWS_SITEMAP.name)
        if current_events != expected_events:
            stale.append(EVENT_SITEMAP.name)
        if stale:
            raise SystemExit(
                f"STALE {', '.join(stale)}: expected {len(urls)} URLs ({breakdown}). "
                "Run scripts/update_sitemap.py and publish the result."
            )
        news_url_count = expected_news.count("<url>")
        recent_news_count = expected_news.count("<news:news>")
        event_count = expected_events.count("<url>")
        print(
            f"OK {SITEMAP.name}: {len(urls)} URLs ({breakdown}), newest {newest}; "
            f"{NEWS_SITEMAP.name}: {news_url_count} permanent article URLs, "
            f"{recent_news_count} with recent news metadata; "
            f"{EVENT_SITEMAP.name}: {event_count} permanent event URLs"
        )
        return

    SITEMAP.write_text(expected, encoding="utf-8", newline="\n")
    NEWS_SITEMAP.write_text(expected_news, encoding="utf-8", newline="\n")
    EVENT_SITEMAP.write_text(expected_events, encoding="utf-8", newline="\n")
    news_url_count = expected_news.count("<url>")
    recent_news_count = expected_news.count("<news:news>")
    event_count = expected_events.count("<url>")
    print(
        f"Updated {SITEMAP.name}: {len(urls)} URLs ({breakdown}), newest {newest}; "
        f"{NEWS_SITEMAP.name}: {news_url_count} permanent article URLs, "
        f"{recent_news_count} with recent news metadata; "
        f"{EVENT_SITEMAP.name}: {event_count} permanent event URLs"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail without writing when sitemap.xml does not match public content.",
    )
    args = parser.parse_args()
    main(check_only=args.check)
