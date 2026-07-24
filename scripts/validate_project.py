#!/usr/bin/env python3
"""Valida a integridade local do portal TVDUASRODAS sem alterar arquivos."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree as ET
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


ROOT = Path(__file__).resolve().parents[1]
EDITORIAL_RULES_V2 = "2026-07-23"
FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---", re.DOTALL)
FIELD = re.compile(r"^([A-Za-z_][\w-]*):\s*(.*?)\s*$", re.MULTILINE)
ASSET = re.compile(r"(?:href|src)=[\"']([^\"']+)[\"']", re.IGNORECASE)


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8-sig")
    match = FRONTMATTER.search(text)
    if not match:
        return {}
    return {key: value.strip(" '\"") for key, value in FIELD.findall(match.group(1))}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-daily", action="store_true")
    args = parser.parse_args()
    errors: list[str] = []
    warnings: list[str] = []
    ad_categories = {
        "motos", "bicicletas", "scooters", "eletricos", "mobilidade",
        "tecnologia", "competicoes", "eventos", "geral",
    }

    json_files = sorted((ROOT / "content").rglob("*.json"))
    json_files += sorted((ROOT / "editorial").rglob("*.json"))
    for path in json_files:
        try:
            json.loads(path.read_text(encoding="utf-8-sig"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"JSON inválido: {path.relative_to(ROOT)}: {exc}")

    required = {
        "news": {"title", "date", "category"},
        "videos": {"title", "date", "youtube_url", "category"},
    }
    allowed_categories = {
        "news": {
            "Moto", "Lancamentos", "tests", "bikes", "Eventos", "Urbanizacao",
            "Urbano", "Dicas", "Dicas e Manutenção", "Seguranca", "Tecnologia", "Outro",
        },
        "videos": {
            "cassetadas", "cross", "competicoes", "eventos", "urbano", "lancamentos",
            "testes", "dicas", "tecnologia", "viagem", "historia", "customizacao",
            "institucional", "outros",
        },
    }
    daily_news: list[dict[str, str]] = []
    try:
        today = datetime.now(ZoneInfo("America/New_York"))
    except ZoneInfoNotFoundError:
        today = datetime.now().astimezone()
    for collection, fields in required.items():
        for path in sorted((ROOT / "content" / collection).glob("*.md")):
            values = frontmatter(path)
            missing = sorted(field for field in fields if not values.get(field))
            if missing:
                errors.append(
                    f"Frontmatter incompleto: {path.relative_to(ROOT)}: {', '.join(missing)}"
                )
            category = values.get("category")
            if category and category not in allowed_categories[collection]:
                errors.append(
                    f"Categoria fora do CMS: {path.relative_to(ROOT)}: {category}"
                )
            ad_category = values.get("ad_category")
            if ad_category and ad_category not in ad_categories:
                errors.append(
                    f"Categoria publicitária inválida: {path.relative_to(ROOT)}: {ad_category}"
                )
            if collection == "news" and values.get("date", "").startswith(today.date().isoformat()):
                daily_news.append(values)
            published_date = values.get("date", "")[:10]
            if collection == "news":
                content_type = values.get("contentType")
                if content_type and content_type not in {"article", "news", "program"}:
                    errors.append(
                        f"Tipo editorial inválido: {path.relative_to(ROOT)}: {content_type}"
                    )
                if published_date >= EDITORIAL_RULES_V2 and not content_type:
                    errors.append(f"contentType ausente: {path.relative_to(ROOT)}")
                if content_type == "program":
                    for field in ("program", "programLabel", "episodeDuration", "readingTime"):
                        if not values.get(field):
                            errors.append(
                                f"Programa sem {field}: {path.relative_to(ROOT)}"
                            )
                elif values.get("program"):
                    errors.append(
                        f"Publicação comum marcada como programa: {path.relative_to(ROOT)}"
                    )
            if collection == "videos" and published_date >= EDITORIAL_RULES_V2:
                if values.get("language") != "pt-BR":
                    errors.append(
                        f"Vídeo novo sem áudio pt-BR: {path.relative_to(ROOT)}"
                    )
                if not values.get("channel"):
                    errors.append(f"Canal do vídeo ausente: {path.relative_to(ROOT)}")
            cover = values.get("cover") or values.get("thumbnail")
            if cover and cover.startswith("/"):
                target = ROOT / unquote(cover.lstrip("/"))
                if not target.exists():
                    errors.append(f"Imagem ausente: {path.relative_to(ROOT)} -> {cover}")

    scheduled_program = {
        0: "role-de-rua",
        2: "garage-tech",
        3: "role-de-rua",
        5: "estrada-aberta",
        6: "electric-zone",
    }.get(today.weekday())
    if args.require_daily and scheduled_program and daily_news:
        if not any(item.get("program") == scheduled_program for item in daily_news):
            warnings.append(
                f"Grade do dia sem programa {scheduled_program}; confirmar exceção editorial no relatório"
            )

    noindex_paths: set[str] = set()
    dynamic_pages = {"materia.html", "competicao.html", "evento.html"}
    for path in sorted(ROOT.glob("*.html")):
        text = path.read_text(encoding="utf-8-sig")
        if not re.search(r"<html[^>]+lang=[\"']pt-BR[\"']", text, re.IGNORECASE):
            errors.append(f"Idioma pt-BR ausente: {path.name}")
        if not re.search(r"<title>\s*.+?\s*</title>", text, re.IGNORECASE | re.DOTALL):
            errors.append(f"Título ausente: {path.name}")
        if re.search(r'name=["\']robots["\'][^>]+noindex', text, re.IGNORECASE):
            noindex_paths.add(path.name)
        elif path.name not in dynamic_pages:
            if not re.search(r'name=["\']description["\']', text, re.IGNORECASE):
                errors.append(f"Meta description ausente: {path.name}")
            if not re.search(r'rel=["\']canonical["\']', text, re.IGNORECASE):
                errors.append(f"Canonical ausente: {path.name}")
        for ref in ASSET.findall(text):
            if "${" in ref:
                continue
            parsed = urlsplit(ref)
            if parsed.scheme or parsed.netloc or ref.startswith(("#", "mailto:", "tel:", "data:")):
                continue
            local = unquote(parsed.path).lstrip("/")
            if not local:
                continue
            target = ROOT / local
            if not target.exists():
                errors.append(f"Referência local ausente: {path.name} -> {ref}")

    config = (ROOT / "admin" / "config.yml").read_text(encoding="utf-8-sig")
    if re.search(r'widget:\s*["\']date["\']', config):
        errors.append("Sveltia CMS: ainda existem campos com widget date obsoleto")

    ads_path = ROOT / "content" / "ads" / "config.json"
    try:
        ads = json.loads(ads_path.read_text(encoding="utf-8-sig"))
        formats = ads.get("formats", {})
        required_formats = {
            "retangulo-lateral-300": (300, 250),
            "faixa-editorial-728": (728, 90),
            "billboard-cobertura-970": (970, 250),
        }
        for name, (width, height) in required_formats.items():
            item = formats.get(name, {})
            if (item.get("width"), item.get("height")) != (width, height):
                errors.append(f"Formato publicitário inválido: {name}")
        campaigns = ads.get("campaigns", [])
        campaign_ids = [item.get("id") for item in campaigns]
        if len(campaign_ids) != len(set(campaign_ids)):
            errors.append("Campanhas publicitárias com IDs duplicados")
        for campaign in campaigns:
            invalid_categories = set(campaign.get("categories", [])) - ad_categories
            invalid_formats = set(campaign.get("formats", [])) - set(formats)
            if invalid_categories:
                errors.append(
                    f"Campanha {campaign.get('id')} com categoria inválida: "
                    f"{', '.join(sorted(invalid_categories))}"
                )
            if invalid_formats:
                errors.append(
                    f"Campanha {campaign.get('id')} com formato inválido: "
                    f"{', '.join(sorted(invalid_formats))}"
                )
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"Configuração publicitária inválida: {exc}")

    try:
        sitemap = ET.parse(ROOT / "sitemap.xml").getroot()
        namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        urls = [node.text or "" for node in sitemap.findall("sm:url/sm:loc", namespace)]
        if len(urls) != len(set(urls)):
            errors.append("sitemap.xml contém URLs duplicadas")
        if any("#U" in url or "%23U" in url for url in urls):
            errors.append("sitemap.xml contém fragmento inválido #U")
        for name in noindex_paths:
            if any(urlsplit(url).path.rstrip("/").endswith(f"/{name}") for url in urls):
                errors.append(f"Página noindex presente no sitemap: {name}")
    except (OSError, ET.ParseError) as exc:
        errors.append(f"sitemap.xml inválido: {exc}")

    for image in sorted((ROOT / "assets" / "img" / "uploads").glob("*")):
        if image.is_file() and image.stat().st_size > 350 * 1024:
            warnings.append(
                f"Imagem acima de 350 KB: {image.relative_to(ROOT)} "
                f"({image.stat().st_size / 1024:.0f} KB)"
            )

    checks = [[sys.executable, "scripts/update_sitemap.py", "--check"]]
    if args.require_daily:
        checks.append([sys.executable, "scripts/check_daily_targets.py", "--require-complete"])
    for command in checks:
        result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
        if result.returncode:
            errors.append((result.stdout + result.stderr).strip())

    print(
        f"Validação: {len(json_files)} JSON, "
        f"{len(list(ROOT.glob('*.html')))} HTML, "
        f"{len(errors)} erro(s), {len(warnings)} aviso(s)"
    )
    for item in errors:
        print(f"ERRO: {item}")
    for item in warnings:
        print(f"AVISO: {item}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
