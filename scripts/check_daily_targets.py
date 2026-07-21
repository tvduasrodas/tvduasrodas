#!/usr/bin/env python3
"""Report whether the daily Revista and TV publishing targets were met."""

from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


ROOT = Path(__file__).resolve().parents[1]
DATE_PATTERN = re.compile(r"^date:\s*['\"]?(\d{4}-\d{2}-\d{2})", re.MULTILINE)


def published_today(folder: Path, today: str) -> list[str]:
    matches: list[str] = []
    for path in sorted(folder.glob("*.md")):
        text = path.read_text(encoding="utf-8-sig")
        match = DATE_PATTERN.search(text)
        if match and match.group(1) == today:
            matches.append(path.stem)
    return matches


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--require-complete",
        action="store_true",
        help="exit with status 1 when the Revista or TV target is still missing",
    )
    args = parser.parse_args()

    try:
        now = datetime.now(ZoneInfo("America/New_York"))
    except ZoneInfoNotFoundError:
        # Windows may not ship the IANA timezone database. The automation host
        # itself is configured for Eastern time, so its local zone is correct.
        now = datetime.now().astimezone()
    today = now.date().isoformat()
    articles = published_today(ROOT / "content" / "news", today)
    videos = published_today(ROOT / "content" / "videos", today)
    complete = bool(articles) and bool(videos)

    print(f"Data Eastern: {today}")
    print(f"Revista: {len(articles)} — {', '.join(articles) if articles else 'PENDENTE'}")
    print(f"TV: {len(videos)} — {', '.join(videos) if videos else 'PENDENTE'}")
    print(f"Meta diária: {'CUMPRIDA' if complete else 'PENDENTE'}")

    return 1 if args.require_complete and not complete else 0


if __name__ == "__main__":
    raise SystemExit(main())
