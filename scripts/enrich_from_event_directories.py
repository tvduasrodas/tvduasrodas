#!/usr/bin/env python3
"""Cruza eventos com diretórios independentes que publicam registros verificáveis."""

from __future__ import annotations

import argparse
import html
import json
import re
import unicodedata
from datetime import datetime, timezone
from difflib import SequenceMatcher
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import urljoin
from urllib.request import Request, urlopen

import research_all_events as research


ROOT = Path(__file__).resolve().parents[1]
FIRE_LIST = "https://firesoulswebradio.com/eventos/"
MOTOTOUR_PRINT = "https://mototour.com.br/eventos/imprimir"
USER_AGENT = (
    "Mozilla/5.0 (compatible; TVDUASRODAS-EditorialAudit/1.0; "
    "+https://tvduasrodas.com/)"
)
MONTHS = {
    "janeiro": 1, "fevereiro": 2, "marco": 3, "abril": 4, "maio": 5,
    "junho": 6, "julho": 7, "agosto": 8, "setembro": 9, "outubro": 10,
    "novembro": 11, "dezembro": 12,
}
GENERIC = {
    "moto", "motos", "motofest", "motociclista", "motociclistas", "encontro",
    "nacional", "evento", "festival", "rock", "anos", "ano", "mc", "mg",
    "asfalto", "do", "da", "dos", "das", "de", "e", "em", "no", "na", "os",
    "as", "um", "uma",
}


def fetch(url: str) -> str:
    request = Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept-Language": "pt-BR,pt;q=0.9"},
    )
    with urlopen(request, timeout=45) as response:
        return response.read(4_000_000).decode(
            response.headers.get_content_charset() or "utf-8", errors="replace"
        )


def norm(value: Any) -> str:
    text = unicodedata.normalize("NFKD", str(value or ""))
    text = "".join(char for char in text if not unicodedata.combining(char))
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def meaningful_words(value: Any) -> set[str]:
    return {
        word for word in norm(value).split()
        if len(word) >= 2 and word not in GENERIC
    }


def edition_number(value: Any) -> int | None:
    text = str(value or "").strip()
    match = re.match(r"^(\d{1,2})(?:\s|[º°ª])", text)
    if match:
        return int(match.group(1))
    match = re.search(r"(\d{1,2})\s*[º°ª]", text)
    if match:
        return int(match.group(1))
    roman = re.match(r"^(X{0,3})(IX|IV|V?I{0,3})(?:\s|[º°ª])", text, re.I)
    if not roman:
        return None
    token = (roman.group(1) + roman.group(2)).upper()
    values = {"I": 1, "V": 5, "X": 10}
    total = 0
    previous = 0
    for char in reversed(token):
        current = values[char]
        total += -current if current < previous else current
        previous = max(previous, current)
    return total or None


def date_parts(value: str) -> tuple[int, int, int] | None:
    match = re.match(r"(\d{4})-(\d{2})-(\d{2})", str(value or ""))
    if not match:
        return None
    return int(match.group(1)), int(match.group(2)), int(match.group(3))


def identity_score(record: dict[str, Any], candidate: str) -> tuple[int, list[str]]:
    record_title = norm(record.get("title"))
    candidate_text = norm(candidate)
    title_words = set(record_title.split())
    candidate_words = set(candidate_text.split())
    meaningful = meaningful_words(record_title)
    shared_meaningful = meaningful & candidate_words
    record_edition = edition_number(record.get("title"))
    candidate_edition = edition_number(candidate)
    reasons: list[str] = []
    if record_edition and candidate_edition and record_edition != candidate_edition:
        return 0, []
    if record_title and record_title in candidate_text:
        return 30, ["título integral identificado"]
    if len(shared_meaningful) >= 2:
        return min(28, 10 * len(shared_meaningful)), ["identidade nominal específica"]
    if len(shared_meaningful) == 1:
        return 13, ["um identificador nominal específico"]
    fuzzy = max(
        (
            SequenceMatcher(None, left, right).ratio()
            for left in meaningful
            for right in candidate_words
            if len(left) >= 5 and len(right) >= 5
        ),
        default=0.0,
    )
    if fuzzy >= 0.78:
        return 11, ["identificador nominal com variação ortográfica"]
    if record_edition and record_edition == candidate_edition:
        return 8, ["edição específica confirmada"]
    return 0, []


class FireParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.href = ""
        self.parts: list[str] = []
        self.events: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "a":
            href = dict(attrs).get("href") or ""
            if "/evento/" in href:
                self.href = href
                self.parts = []

    def handle_data(self, data: str) -> None:
        if self.href:
            self.parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self.href:
            label = " ".join(" ".join(self.parts).split())
            if label:
                self.events.append(
                    {"url": urljoin(FIRE_LIST, self.href), "label": label}
                )
            self.href = ""
            self.parts = []


class MototourParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_row = False
        self.in_cell = False
        self.cell_parts: list[str] = []
        self.cells: list[str] = []
        self.rows: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "tr":
            self.in_row = True
            self.cells = []
        elif tag == "td" and self.in_row:
            self.in_cell = True
            self.cell_parts = []

    def handle_data(self, data: str) -> None:
        if self.in_cell:
            self.cell_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "td" and self.in_cell:
            self.cells.append(" ".join(" ".join(self.cell_parts).split()))
            self.in_cell = False
        elif tag == "tr" and self.in_row:
            if len(self.cells) >= 3 and re.search(r"\b(?:Dia|De)\b", self.cells[0], re.I):
                self.rows.append(
                    {"date_label": self.cells[0], "location": self.cells[1], "title": self.cells[2]}
                )
            self.in_row = False


def fire_matches(record: dict[str, Any], candidates: list[dict[str, str]]) -> dict[str, Any] | None:
    parts = date_parts(str(record.get("start_date") or ""))
    city = norm(record.get("city"))
    if not parts or not city:
        return None
    _, month, day = parts
    ranked: list[tuple[int, dict[str, str], list[str]]] = []
    for candidate in candidates:
        label = candidate["label"]
        date_match = re.search(r"\b(\d{1,2})/(\d{1,2})\b", label)
        if not date_match or (int(date_match.group(1)), int(date_match.group(2))) != (day, month):
            continue
        normalized = norm(label)
        if city not in normalized:
            continue
        identity, reasons = identity_score(record, label)
        if not identity:
            continue
        ranked.append((70 + identity, candidate, ["data e cidade confirmadas", *reasons]))
    ranked.sort(key=lambda item: item[0], reverse=True)
    if not ranked:
        return None
    if len(ranked) > 1 and ranked[0][0] == ranked[1][0] and ranked[0][1]["url"] != ranked[1][1]["url"]:
        return None
    value, candidate, reasons = ranked[0]
    return {"score": value, "candidate": candidate, "reasons": reasons}


def mototour_start_date(label: str, year: int = 2026) -> tuple[int, int, int] | None:
    text = norm(label)
    month = next((number for name, number in MONTHS.items() if name in text), None)
    if not month:
        return None
    day_match = re.search(r"\b(?:dia|de)\s+(\d{1,2})\b", text)
    if not day_match:
        return None
    year_match = re.search(r"\b(20\d{2})\b", text)
    return int(year_match.group(1)) if year_match else year, month, int(day_match.group(1))


def mototour_matches(record: dict[str, Any], rows: list[dict[str, str]]) -> dict[str, Any] | None:
    parts = date_parts(str(record.get("start_date") or ""))
    city = norm(record.get("city"))
    state = norm(record.get("state"))
    if not parts or not city:
        return None
    ranked: list[tuple[int, dict[str, str], list[str]]] = []
    for row in rows:
        if mototour_start_date(row["date_label"], parts[0]) != parts:
            continue
        location = norm(row["location"])
        if city not in location or state and not re.search(rf"\b{re.escape(state)}\b", location):
            continue
        identity, reasons = identity_score(record, row["title"])
        if not identity:
            continue
        ranked.append((70 + identity, row, ["data, cidade e UF confirmadas", *reasons]))
    ranked.sort(key=lambda item: item[0], reverse=True)
    if not ranked:
        return None
    if len(ranked) > 1 and ranked[0][0] == ranked[1][0] and norm(ranked[0][1]["title"]) != norm(ranked[1][1]["title"]):
        return None
    value, row, reasons = ranked[0]
    return {"score": value, "candidate": row, "reasons": reasons}


def add_source(
    record: dict[str, Any],
    *,
    url: str,
    label: str,
    supports: str,
    method: str,
    score: int,
    reasons: list[str],
    checked_at: str,
) -> bool:
    if any(
        isinstance(source, dict) and source.get("url") == url
        for source in record.get("sources") or []
    ):
        return False
    record["sources"] = research.deduplicate_sources(
        list(record.get("sources") or []) + [{
            "url": url,
            "label": label,
            "type": "fonte específica independente",
            "supports": supports,
            "checked_at": checked_at,
            "discovery_method": method,
            "relevance_score": score,
        }]
    )
    record["source_checked_at"] = checked_at
    matches = record.setdefault("directory_matches", [])
    matches.append({
        "url": url,
        "score": score,
        "reasons": reasons,
        "checked_at": checked_at,
    })
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    fire_parser = FireParser()
    fire_parser.feed(fetch(FIRE_LIST))
    fire_candidates = {
        item["url"]: item for item in fire_parser.events
    }.values()
    mototour_parser = MototourParser()
    mototour_parser.feed(fetch(MOTOTOUR_PRINT))
    checked_at = datetime.now(timezone.utc).isoformat()
    matches: list[dict[str, Any]] = []
    changed = 0

    for kind, path, index, original in research.records():
        if original.get("duplicate_of") or not original.get("start_date"):
            continue
        updated = dict(original)
        fire = fire_matches(original, list(fire_candidates))
        moto = mototour_matches(original, mototour_parser.rows)
        if fire:
            candidate = fire["candidate"]
            matches.append({
                "directory": "Fire Souls",
                "slug": original.get("slug") or path.stem,
                "title": original.get("title"),
                "city": original.get("city"),
                "date": original.get("start_date"),
                "score": fire["score"],
                "source_label": candidate["label"],
                "source_url": candidate["url"],
            })
            if args.apply:
                changed += int(add_source(
                    updated,
                    url=candidate["url"],
                    label=f"{candidate['label']} — registro específico na Fire Souls Web Radio",
                    supports="data, horário inicial, cidade, identidade do evento e material visual",
                    method="cruzamento_estruturado_fire_souls",
                    score=fire["score"],
                    reasons=fire["reasons"],
                    checked_at=checked_at,
                ))
        if moto:
            row = moto["candidate"]
            matches.append({
                "directory": "Mototour",
                "slug": original.get("slug") or path.stem,
                "title": original.get("title"),
                "city": original.get("city"),
                "date": original.get("start_date"),
                "score": moto["score"],
                "source_label": row["title"],
                "source_url": MOTOTOUR_PRINT,
            })
            if args.apply:
                changed += int(add_source(
                    updated,
                    url=MOTOTOUR_PRINT,
                    label=f"{row['title']} — {row['date_label']}, {row['location']}",
                    supports="data, período, cidade, UF e identidade do evento",
                    method="cruzamento_estruturado_mototour",
                    score=moto["score"],
                    reasons=moto["reasons"],
                    checked_at=checked_at,
                ))
        if args.apply and updated != original:
            research.save_record(path, index, updated)

    report = {
        "fire_candidates": len(list(fire_candidates)),
        "mototour_rows": len(mototour_parser.rows),
        "matched_sources": len(matches),
        "changed_sources": changed,
        "matches": matches,
    }
    serialized = json.dumps(report, ensure_ascii=False, indent=2)
    if args.report:
        output = args.report if args.report.is_absolute() else ROOT / args.report
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(serialized + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in report.items() if key != "matches"}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
