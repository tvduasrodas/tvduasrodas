#!/usr/bin/env python3
"""Audita datas ISO que ainda estejam visíveis nas páginas HTML do portal."""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ISO_VISIBLE = re.compile(r"(?<![\w/-])20\d{2}-\d{2}-\d{2}(?![\w/-])")
IGNORED_DIRS = {".git", "node_modules", "output", "tmp"}


class VisibleTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.hidden_depth = 0
        self.text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style", "template"}:
            self.hidden_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "template"} and self.hidden_depth:
            self.hidden_depth -= 1

    def handle_data(self, data: str) -> None:
        if not self.hidden_depth:
            self.text.append(data)


def main() -> int:
    failures: list[str] = []
    scanned = 0
    for path in ROOT.rglob("*.html"):
        if any(part in IGNORED_DIRS for part in path.parts):
            continue
        scanned += 1
        parser = VisibleTextParser()
        parser.feed(path.read_text(encoding="utf-8-sig", errors="replace"))
        visible = " ".join(parser.text)
        matches = sorted(set(ISO_VISIBLE.findall(visible)))
        if matches:
            failures.append(
                f"{path.relative_to(ROOT)}: {', '.join(matches[:8])}"
            )

    print(f"Auditoria de datas visíveis: {scanned} HTML, {len(failures)} pendência(s).")
    for failure in failures:
        print(f"ERRO: {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
