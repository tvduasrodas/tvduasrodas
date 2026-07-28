#!/usr/bin/env python3
"""Submit sitemaps and refresh the Search Console indexing dashboard.

This integration uses the Search Console Sitemap and URL Inspection APIs.
It deliberately does not use the Google Indexing API.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://tvduasrodas.com"
PROPERTY = "sc-domain:tvduasrodas.com"
SITEMAP_URLS = [
    f"{BASE_URL}/sitemap.xml",
    f"{BASE_URL}/news-sitemap.xml",
    f"{BASE_URL}/event-sitemap.xml",
]
STATUS_FILE = ROOT / "editorial" / "search-console" / "status.json"
SCOPE = "https://www.googleapis.com/auth/webmasters"


def load_google_session():
    try:
        import google.auth
        from google.auth.transport.requests import AuthorizedSession
        from google.oauth2 import service_account
    except ImportError as exc:
        raise SystemExit(
            "Dependências ausentes. Instale requirements-search-console.txt."
        ) from exc

    credentials_file = os.getenv("GOOGLE_SEARCH_CONSOLE_CREDENTIALS_FILE", "").strip()
    credentials_json = os.getenv("GOOGLE_SEARCH_CONSOLE_SERVICE_ACCOUNT_JSON", "").strip()
    if credentials_file:
        credentials = service_account.Credentials.from_service_account_file(
            credentials_file,
            scopes=[SCOPE],
        )
    elif credentials_json:
        if not credentials_json.startswith("{"):
            try:
                credentials_json = base64.b64decode(credentials_json).decode("utf-8")
            except (ValueError, UnicodeDecodeError) as exc:
                raise SystemExit(
                    "GOOGLE_SEARCH_CONSOLE_SERVICE_ACCOUNT_JSON não é JSON nem base64 válido."
                ) from exc
        credentials = service_account.Credentials.from_service_account_info(
            json.loads(credentials_json),
            scopes=[SCOPE],
        )
    else:
        credentials, _ = google.auth.default(
            scopes=[SCOPE],
        )
    return AuthorizedSession(credentials)


def request_json(session, method: str, url: str, **kwargs):
    response = session.request(method, url, timeout=45, **kwargs)
    if response.status_code >= 400:
        detail = response.text[:800]
        raise RuntimeError(f"Search Console retornou HTTP {response.status_code}: {detail}")
    if response.status_code == 204 or not response.content:
        return {}
    return response.json()


def submit_sitemap(session, sitemap_url: str) -> None:
    endpoint = (
        "https://www.googleapis.com/webmasters/v3/sites/"
        f"{quote(PROPERTY, safe='')}/sitemaps/{quote(sitemap_url, safe='')}"
    )
    request_json(session, "PUT", endpoint)


def list_sitemaps(session) -> list[dict]:
    endpoint = (
        "https://www.googleapis.com/webmasters/v3/sites/"
        f"{quote(PROPERTY, safe='')}/sitemaps"
    )
    payload = request_json(session, "GET", endpoint)
    records = []
    for item in payload.get("sitemap", []):
        if item.get("path") not in SITEMAP_URLS:
            continue
        contents = item.get("contents", [])
        records.append({
            "url": item.get("path", ""),
            "last_submitted": item.get("lastSubmitted"),
            "last_downloaded": item.get("lastDownloaded"),
            "pending": bool(item.get("isPending")),
            "warnings": int(item.get("warnings", 0)),
            "errors": int(item.get("errors", 0)),
            "discovered": sum(
                int(content.get("submitted", 0))
                for content in contents
            ),
            "indexed": sum(
                int(content.get("indexed", 0))
                for content in contents
            ),
            "content": contents,
        })
    return sorted(records, key=lambda item: item["url"])


def recent_news_urls() -> list[str]:
    root = ET.parse(ROOT / "news-sitemap.xml").getroot()
    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    return [
        node.text or ""
        for node in root.findall("sm:url/sm:loc", namespace)
        if node.text
    ]


def schema_datetime(value: object) -> datetime | None:
    raw = str(value or "").strip()
    if not raw:
        return None
    try:
        parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def upcoming_event_urls() -> list[str]:
    """Prioritize ongoing and upcoming event pages for inspection monitoring."""
    candidates: list[tuple[datetime, str]] = []
    now = datetime.now(timezone.utc)
    seen: set[str] = set()
    for path in sorted((ROOT / "eventos").glob("*/index.html")):
        text = path.read_text(encoding="utf-8-sig", errors="ignore")
        payloads = re.findall(
            r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            text,
            re.IGNORECASE | re.DOTALL,
        )
        for payload in payloads:
            try:
                document = json.loads(payload)
            except json.JSONDecodeError:
                continue
            nodes = document.get("@graph", [document]) if isinstance(document, dict) else []
            for node in nodes:
                if not isinstance(node, dict):
                    continue
                node_types = node.get("@type", [])
                if isinstance(node_types, str):
                    node_types = [node_types]
                if "Event" not in node_types:
                    continue
                if node.get("eventStatus") == "https://schema.org/EventCancelled":
                    continue
                start = schema_datetime(node.get("startDate"))
                end = schema_datetime(node.get("endDate")) or start
                url = str(node.get("url") or "")
                if (
                    not start
                    or not end
                    or not url
                    or end.date() < now.date()
                    or url in seen
                ):
                    continue
                seen.add(url)
                candidates.append((start, url))
    return [url for _, url in sorted(candidates)]


def inspect_url(session, url: str) -> dict:
    endpoint = "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect"
    payload = request_json(
        session,
        "POST",
        endpoint,
        json={
            "inspectionUrl": url,
            "siteUrl": PROPERTY,
            "languageCode": "pt-BR",
        },
    )
    result = payload.get("inspectionResult", {})
    index = result.get("indexStatusResult", {})
    return {
        "url": url,
        "verdict": index.get("verdict", "VERDICT_UNSPECIFIED"),
        "coverage_state": index.get("coverageState", ""),
        "indexing_state": index.get("indexingState", ""),
        "page_fetch_state": index.get("pageFetchState", ""),
        "robots_txt_state": index.get("robotsTxtState", ""),
        "last_crawl_time": index.get("lastCrawlTime"),
        "google_canonical": index.get("googleCanonical", ""),
        "user_canonical": index.get("userCanonical", ""),
        "sitemaps": index.get("sitemap", []),
        "referring_urls": index.get("referringUrls", []),
        "inspected_at": datetime.now(timezone.utc).isoformat(),
    }


def summarize(entries: list[dict]) -> dict[str, int]:
    indexed = sum(entry.get("verdict") == "PASS" for entry in entries)
    not_indexed = sum(entry.get("verdict") == "FAIL" for entry in entries)
    neutral = len(entries) - indexed - not_indexed
    return {
        "inspected": len(entries),
        "indexed": indexed,
        "not_indexed": not_indexed,
        "processing_or_unknown": neutral,
    }


def write_status(*, sitemaps: list[dict], entries: list[dict]) -> None:
    STATUS_FILE.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "property": PROPERTY,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scope": (
            "Matérias no Google News sitemap das últimas 48 horas e eventos "
            "em andamento ou futuros priorizados por data"
        ),
        "sitemaps": sitemaps,
        "summary": summarize(entries),
        "urls": entries,
    }
    STATUS_FILE.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--submit", action="store_true", help="Submit both sitemaps.")
    parser.add_argument(
        "--inspect-recent",
        action="store_true",
        help="Inspect URLs currently present in news-sitemap.xml.",
    )
    parser.add_argument(
        "--inspect-upcoming-events",
        action="store_true",
        help="Inspect ongoing and upcoming event URLs, ordered by start date.",
    )
    parser.add_argument("--max-urls", type=int, default=50)
    parser.add_argument("--max-event-urls", type=int, default=10)
    args = parser.parse_args()
    if not args.submit and not args.inspect_recent and not args.inspect_upcoming_events:
        parser.error(
            "Use --submit, --inspect-recent, --inspect-upcoming-events, or a combination."
        )

    session = load_google_session()
    if args.submit:
        for sitemap_url in SITEMAP_URLS:
            submit_sitemap(session, sitemap_url)
            print(f"Submitted {sitemap_url}")

    inspection_urls: list[str] = []
    if args.inspect_recent:
        inspection_urls.extend(recent_news_urls()[: max(0, args.max_urls)])
    if args.inspect_upcoming_events:
        inspection_urls.extend(
            upcoming_event_urls()[: max(0, args.max_event_urls)]
        )

    entries = []
    for url in dict.fromkeys(inspection_urls):
        entries.append(inspect_url(session, url))
        print(f"Inspected {url}")

    write_status(sitemaps=list_sitemaps(session), entries=entries)
    print(f"Updated {STATUS_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
