#!/usr/bin/env python3
"""Report whether the daily Revista, program and TV targets were met."""

from __future__ import annotations

import argparse
import re
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


ROOT = Path(__file__).resolve().parents[1]
FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---", re.DOTALL)
FIELD = re.compile(r"^([A-Za-z_][\w-]*):\s*(.*?)\s*$", re.MULTILINE)
PROGRAMS = {
    0: "role-de-rua",
    2: "garage-tech",
    3: "role-de-rua",
    5: "estrada-aberta",
    6: "electric-zone",
}


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8-sig")
    match = FRONTMATTER.search(text)
    if not match:
        return {}
    values = {key: value.strip(" '\"") for key, value in FIELD.findall(match.group(1))}
    values["slug"] = path.stem
    return values


def dated_entries(folder: Path, start: str, end: str) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    for path in sorted(folder.glob("*.md")):
        values = frontmatter(path)
        date = values.get("date", "")[:10]
        if start <= date <= end:
            entries.append(values)
    return entries


def duplicates(entries: list[dict[str, str]], field: str) -> list[str]:
    counts = Counter(item.get(field, "").casefold() for item in entries if item.get(field))
    return sorted(value for value, count in counts.items() if count > 1)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--require-complete",
        action="store_true",
        help="exit with status 1 when any mandatory daily target is missing",
    )
    args = parser.parse_args()

    try:
        now = datetime.now(ZoneInfo("America/New_York"))
    except ZoneInfoNotFoundError:
        now = datetime.now().astimezone()

    today = now.date()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    today_text = today.isoformat()
    week_news = dated_entries(ROOT / "content" / "news", week_start.isoformat(), week_end.isoformat())
    week_videos = dated_entries(ROOT / "content" / "videos", week_start.isoformat(), week_end.isoformat())

    for item in week_news:
        if not item.get("contentType"):
            item["contentType"] = "program" if item.get("program") else "article"

    today_news = [item for item in week_news if item.get("date", "")[:10] == today_text]
    articles = [item for item in today_news if item.get("contentType") == "article"]
    news_updates = [item for item in today_news if item.get("contentType") == "news"]
    scheduled_program = PROGRAMS.get(today.weekday())
    programs = [
        item for item in today_news
        if item.get("contentType") == "program" and item.get("program") == scheduled_program
    ]

    weekly_articles = [item for item in week_news if item.get("contentType") == "article"]
    article_category_duplicates = duplicates(weekly_articles, "category")

    today_videos = [item for item in week_videos if item.get("date", "")[:10] == today_text]
    ptbr_videos = [item for item in today_videos if item.get("language") == "pt-BR"]
    weekly_ptbr_videos = [item for item in week_videos if item.get("language") == "pt-BR"]
    video_category_duplicates = duplicates(weekly_ptbr_videos, "category")
    video_channel_duplicates = duplicates(weekly_ptbr_videos, "channel")

    article_ok = bool(articles) and not article_category_duplicates
    video_ok = bool(ptbr_videos) and not video_category_duplicates and not video_channel_duplicates
    program_ok = not scheduled_program or bool(programs)
    complete = article_ok and video_ok and program_ok

    names = lambda items: ", ".join(item["slug"] for item in items) if items else "PENDENTE"
    print(f"Data Eastern: {today_text}")
    print(f"Semana editorial: {week_start.isoformat()} a {week_end.isoformat()}")
    print(f"Matéria diária: {len(articles)} — {names(articles)}")
    print(f"Notícias adicionais: {len(news_updates)} — {names(news_updates) if news_updates else 'nenhuma'}")
    if scheduled_program:
        print(f"Programa obrigatório: {scheduled_program} — {names(programs)}")
    else:
        print("Programa obrigatório: não há programa fixo hoje")
    print(f"TV em pt-BR: {len(ptbr_videos)} — {names(ptbr_videos)}")
    if today_videos and not ptbr_videos:
        print("AVISO: vídeo em outro idioma não cumpre a meta diária da TV")
    if article_category_duplicates:
        print("PENDÊNCIA: categoria de matéria repetida na semana: " + ", ".join(article_category_duplicates))
    if video_category_duplicates:
        print("PENDÊNCIA: categoria de vídeo repetida na semana: " + ", ".join(video_category_duplicates))
    if video_channel_duplicates:
        print("PENDÊNCIA: canal de vídeo repetido na semana: " + ", ".join(video_channel_duplicates))
    print(f"Meta diária: {'CUMPRIDA' if complete else 'PENDENTE'}")

    return 1 if args.require_complete and not complete else 0


if __name__ == "__main__":
    raise SystemExit(main())
