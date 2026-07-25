#!/usr/bin/env python3
"""Audita codificação, caracteres ilegíveis e erros recorrentes em textos públicos."""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEXT_EXTENSIONS = {".css", ".html", ".js", ".json", ".md", ".py", ".txt", ".xml", ".yml", ".yaml"}
EXCLUDED_PARTS = {
    ".audit-deps",
    ".git",
    ".python-deps",
    ".reel-deps",
    ".social-build-deps",
    ".social-deps",
    "node_modules",
}
MOJIBAKE = re.compile(
    "(?:"
    "\\u00c3[\\u0080-\\u00bf]|"
    "\\u00c2[\\u0080-\\u00bf]|"
    "\\u00e2(?:\\u20ac|\\u0080|\\u0099)|"
    "\\u00f0\\u0178|"
    "\\u00ef\\u00bf\\u00bd|"
    "\\ufffd"
    ")"
)
ILLEGAL_CONTROLS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]")
ZERO_WIDTH = re.compile("[\u200b\u200c\u200d\ufeff]")
SPACE_BEFORE_PUNCTUATION = re.compile(r"[ \t]+[,;:!?]")
REPEATED_PUNCTUATION = re.compile(r"([!?;:,])\1+")
URL = re.compile(r"https?://\S+")
MARKDOWN_DESTINATION = re.compile(r"(\])\([^)]+\)")
FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*(.*)\Z", re.DOTALL)
TITLE_FIELD = re.compile(r"^title:\s*(.*?)\s*$", re.MULTILINE)

# Erros inequívocos já encontrados em conteúdo editorial. A lista é conservadora
# para não alterar nomes próprios, marcas, modalidades ou termos técnicos.
COMMON_ERRORS = {
    "conciêntização": "conscientização",
    "conscientizacao": "conscientização",
    "materia": "matéria",
    "referencias": "referências",
    "transito": "trânsito",
    "equilibrio": "equilíbrio",
    "posicao": "posição",
    "confortavel": "confortável",
    "seguranca": "segurança",
    "guidao": "guidão",
    "protecao": "proteção",
    "rotacao": "rotação",
    "semaforos": "semáforos",
    "emergencia": "emergência",
    "conclusao": "conclusão",
    "opcao": "opção",
    "unica": "única",
    "diario": "diário",
    "economica": "econômica",
    "eletronico": "eletrônico",
    "voce": "você",
    "acao": "ação",
    "cenarios": "cenários",
}
ERROR_WORDS = re.compile(
    r"\b(" + "|".join(re.escape(word) for word in COMMON_ERRORS) + r")\b",
    re.IGNORECASE,
)
PUBLIC_JSON_KEYS = {
    "alt",
    "attractions",
    "body",
    "bodyHtml",
    "caption",
    "competitor",
    "country",
    "event_type",
    "image_credit",
    "kicker",
    "location",
    "modality",
    "name",
    "note",
    "organizer",
    "scope",
    "sponsor",
    "stage",
    "standings_eyebrow",
    "standings_title",
    "summary",
    "tagline",
    "title",
    "venue",
    "winner",
}


class VisibleTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hidden_depth = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style", "template"}:
            self.hidden_depth += 1
        if not self.hidden_depth:
            for name, value in attrs:
                if name in {"alt", "aria-label", "title"} and value:
                    self.parts.append(value)

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "template"} and self.hidden_depth:
            self.hidden_depth -= 1

    def handle_data(self, data: str) -> None:
        if not self.hidden_depth:
            self.parts.append(data)


def public_json_text(value: object, key: str = "") -> list[str]:
    if isinstance(value, str):
        return [value] if key in PUBLIC_JSON_KEYS else []
    if isinstance(value, list):
        return [
            text
            for item in value
            for text in public_json_text(item, key)
        ]
    if isinstance(value, dict):
        return [
            text
            for child_key, child in value.items()
            for text in public_json_text(child, child_key)
        ]
    return []


def editorial_text(path: Path, text: str) -> str:
    if path.suffix.lower() == ".md":
        if "content" not in path.parts:
            return ""
        match = FRONTMATTER.match(text)
        if not match:
            return clean_visible_text(text)
        title = TITLE_FIELD.search(match.group(1))
        return clean_visible_text(f"{title.group(1) if title else ''}\n{match.group(2)}")
    if path.suffix.lower() == ".json" and "content" in path.parts:
        try:
            return clean_visible_text("\n".join(public_json_text(json.loads(text))))
        except json.JSONDecodeError:
            return ""
    if path.suffix.lower() == ".html" and path.parent == ROOT:
        parser = VisibleTextParser()
        parser.feed(text)
        return "\n".join(parser.parts)
    return ""


def clean_visible_text(text: str) -> str:
    text = MARKDOWN_DESTINATION.sub(r"\1", text)
    return URL.sub("", text)


def line_number(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def main() -> int:
    errors: list[str] = []
    scanned = 0
    for path in sorted(ROOT.rglob("*")):
        if (
            not path.is_file()
            or path.suffix.lower() not in TEXT_EXTENSIONS
            or any(part in EXCLUDED_PARTS for part in path.parts)
        ):
            continue
        scanned += 1
        relative = path.relative_to(ROOT)
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            errors.append(f"{relative}: não está em UTF-8 ({exc})")
            continue
        if unicodedata.normalize("NFC", text) != text:
            errors.append(f"{relative}: contém caracteres fora da normalização Unicode NFC")
        for pattern, label in (
            (MOJIBAKE, "texto com codificação corrompida"),
            (ILLEGAL_CONTROLS, "caractere de controle ilegível"),
            (ZERO_WIDTH, "caractere invisível"),
        ):
            match = pattern.search(text)
            if match:
                errors.append(
                    f"{relative}:{line_number(text, match.start())}: {label}: {match.group(0)!r}"
                )
        visible = editorial_text(path, text)
        for pattern, label in (
            (SPACE_BEFORE_PUNCTUATION, "espaço indevido antes da pontuação"),
            (REPEATED_PUNCTUATION, "pontuação repetida"),
        ):
            match = pattern.search(visible)
            if match:
                errors.append(f"{relative}: {label}: {match.group(0)!r}")
        for match in ERROR_WORDS.finditer(visible):
            found = match.group(0)
            errors.append(
                f"{relative}: grafia suspeita {found!r}; usar "
                f"{COMMON_ERRORS[found.lower()]!r}"
            )

    print(f"Auditoria PT-BR: {scanned} arquivo(s), {len(errors)} erro(s)")
    for error in errors:
        print(f"ERRO: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
