#!/usr/bin/env python3
"""Valida a integridade local do portal TVDUASRODAS sem alterar arquivos."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import date, datetime, timedelta, timezone
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
            "Urbano", "Dicas", "Dicas e Manutenção", "Seguranca", "Segurança", "Tecnologia", "Outro",
        },
        "videos": {
            "cassetadas", "cross", "competicoes", "eventos", "urbano", "lancamentos",
            "testes", "dicas", "tecnologia", "bicicletas-bmx", "viagem", "historia", "customizacao",
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
        if "assets/js/ads.js" not in text:
            errors.append(f"Sistema publicitário ausente: {path.name}")
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
        if path.name in dynamic_pages:
            if path.name not in noindex_paths:
                errors.append(f"Página dinâmica legada precisa de noindex: {path.name}")
            legacy_canonical = re.search(
                r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)',
                text,
                re.IGNORECASE,
            )
            if not legacy_canonical or not legacy_canonical.group(1).strip():
                errors.append(f"Canonical de fallback ausente: {path.name}")
        if path.name == "tv.html":
            if len(re.findall(r'class=["\'][^"\']*tv-program-card', text)) < 4:
                errors.append("Grade de programação da TV incompleta")
            if 'data-ad-slot="video-sidebar"' in text:
                errors.append("Publicidade lateral da TV voltou a competir com o player")
            if "autoplay=1&mute=1&playsinline=1" not in text:
                errors.append("Autoplay silencioso do vídeo mais recente ausente")
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
            html_fallback = ROOT / f"{local}.html"
            if not target.exists() and html_fallback.exists():
                target = html_fallback
            elif (ref.endswith("/") or not target.suffix) and not target.is_file():
                target = target / "index.html"
            if not target.exists():
                errors.append(f"Referência local ausente: {path.name} -> {ref}")

    generated_roots = (
        "materias", "videos", "competicoes", "eventos", "guias",
        "atletas", "assuntos", "marcas", "modalidades",
    )
    generated_html = sorted(
        page
        for folder in generated_roots
        for page in (ROOT / folder).rglob("index.html")
        if (ROOT / folder).exists()
    )
    generated_canonicals: set[str] = set()
    for path in generated_html:
        text = path.read_text(encoding="utf-8-sig")
        relative = path.relative_to(ROOT)
        is_redirect = bool(
            re.search(r'<meta[^>]+http-equiv=["\']refresh["\']', text, re.IGNORECASE)
            and re.search(r'<meta[^>]+name=["\']robots["\'][^>]+noindex', text, re.IGNORECASE)
        )
        if not is_redirect and "assets/js/ads.js" not in text:
            errors.append(f"Sistema publicitário ausente: {relative}")
        slots = set(re.findall(r'data-ad-slot=["\']([^"\']+)', text))
        folder = relative.parts[0]
        if not is_redirect and folder in {"materias", "guias"}:
            for required_slot in {"article-sidebar", "article-inline"}:
                if required_slot not in slots:
                    errors.append(f"Espaço {required_slot} ausente: {relative}")
        elif not is_redirect and folder == "videos" and relative.parts[-2] != "videos":
            for required_slot in {"video-sidebar", "video-inline"}:
                if required_slot not in slots:
                    errors.append(f"Espaço {required_slot} ausente: {relative}")
        elif not is_redirect and folder in {"competicoes", "eventos"}:
            if "detail-billboard" not in slots:
                errors.append(f"Espaço detail-billboard ausente: {relative}")
        for pattern, label in (
            (r'<html[^>]+lang=["\']pt-BR["\']', "idioma pt-BR"),
            (r"<title>\s*.+?</title>", "title"),
            (r'<meta[^>]+name=["\']description["\']', "meta description"),
            (
                r'<meta[^>]+name=["\']robots["\'][^>]+(?:index|noindex)',
                "diretiva robots",
            ),
            (r"<h1[^>]*>.+?</h1>", "h1"),
        ):
            if not re.search(pattern, text, re.IGNORECASE | re.DOTALL):
                errors.append(f"{label} ausente: {relative}")
        canonical_match = re.search(
            r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)',
            text, re.IGNORECASE,
        )
        if not canonical_match:
            errors.append(f"Canonical ausente: {relative}")
        elif canonical_match.group(1) in generated_canonicals and not is_redirect:
            errors.append(f"Canonical duplicado: {canonical_match.group(1)}")
        elif not is_redirect:
            generated_canonicals.add(canonical_match.group(1))
        if not is_redirect and folder in {"competicoes", "eventos"}:
            internal_markers = (
                "Fontes cruzadas e atualização",
                "Esta página registra ",
                "fonte específica independente",
                "Verificação ainda aberta:",
                "buscas textual, ampliada e visual/social",
                "Fonte e atualização",
                "Fontes cruzadas",
                "Leitura visual complementar",
                "leitura automatizada",
                "processamento visual",
                "flyer consultado",
            )
            for marker in internal_markers:
                if marker.casefold() in text.casefold():
                    errors.append(
                        f"Metadado interno exposto na página pública: {relative} -> {marker}"
                    )
        for payload in re.findall(
            r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            text, re.IGNORECASE | re.DOTALL,
        ):
            try:
                document = json.loads(payload)
                nodes = document.get("@graph", [document]) if isinstance(document, dict) else []
                for node in nodes:
                    if not isinstance(node, dict):
                        continue
                    node_types = node.get("@type", [])
                    if isinstance(node_types, str):
                        node_types = [node_types]
                    if {"Event", "SportsEvent"} & set(node_types):
                        if not node.get("startDate"):
                            errors.append(f"Evento estruturado sem startDate: {relative}")
                        if not node.get("endDate"):
                            errors.append(f"Evento estruturado sem endDate: {relative}")
                    if "VideoObject" in node_types:
                        if not node.get("embedUrl"):
                            errors.append(f"Vídeo estruturado sem embedUrl: {relative}")
                        if not node.get("contentUrl"):
                            errors.append(f"Vídeo estruturado sem contentUrl: {relative}")
            except json.JSONDecodeError as exc:
                errors.append(f"JSON-LD inválido: {relative}: {exc}")
        for ref in ASSET.findall(text):
            parsed = urlsplit(ref)
            if parsed.scheme or parsed.netloc or ref.startswith(("#", "mailto:", "tel:", "data:")):
                continue
            local = unquote(parsed.path).lstrip("/")
            if not local:
                continue
            target = ROOT / local
            html_fallback = ROOT / f"{local}.html"
            if not target.exists() and html_fallback.exists():
                target = html_fallback
            elif ref.endswith("/") or not target.suffix:
                target = target / "index.html" if not target.is_file() else target
            if not target.exists():
                errors.append(f"Link/recurso gerado ausente: {relative} -> {ref}")

    manifest_path = ROOT / "content" / "seo-manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
        manifest_urls = [item.get("url", "") for item in manifest]
        if len(manifest_urls) != len(set(manifest_urls)):
            errors.append("Manifesto SEO contém URLs duplicadas")
        for url in manifest_urls:
            target = ROOT / url.strip("/")
            target = target / "index.html" if url.endswith("/") else target
            if not target.exists():
                errors.append(f"Manifesto SEO aponta para arquivo ausente: {url}")
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"Manifesto SEO inválido: {exc}")

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
            "faixa-home-970": (970, 120),
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
        lastmods = [
            node.text or ""
            for node in sitemap.findall("sm:url/sm:lastmod", namespace)
        ]
        if len(urls) != len(set(urls)):
            errors.append("sitemap.xml contém URLs duplicadas")
        if any(value > date.today().isoformat() for value in lastmods):
            errors.append("sitemap.xml contém lastmod no futuro")
        if any("#U" in url or "%23U" in url for url in urls):
            errors.append("sitemap.xml contém fragmento inválido #U")
        if any("?slug=" in url or "?v=" in url for url in urls):
            errors.append("sitemap.xml ainda contém URL dinâmica não canônica")
        for name in noindex_paths:
            if any(urlsplit(url).path.rstrip("/").endswith(f"/{name}") for url in urls):
                errors.append(f"Página noindex presente no sitemap: {name}")
    except (OSError, ET.ParseError) as exc:
        errors.append(f"sitemap.xml inválido: {exc}")

    try:
        news_sitemap = ET.parse(ROOT / "news-sitemap.xml").getroot()
        namespaces = {
            "sm": "http://www.sitemaps.org/schemas/sitemap/0.9",
            "news": "http://www.google.com/schemas/sitemap-news/0.9",
        }
        news_urls = [
            node.text or ""
            for node in news_sitemap.findall("sm:url/sm:loc", namespaces)
        ]
        news_dates = [
            node.text or ""
            for node in news_sitemap.findall(
                "sm:url/news:news/news:publication_date", namespaces
            )
        ]
        news_titles = [
            node.text or ""
            for node in news_sitemap.findall(
                "sm:url/news:news/news:title", namespaces
            )
        ]
        if len(news_urls) > 1000:
            errors.append("news-sitemap.xml excede 1.000 matérias")
        if len(news_urls) != len(set(news_urls)):
            errors.append("news-sitemap.xml contém URLs duplicadas")
        if not (len(news_urls) == len(news_dates) == len(news_titles)):
            errors.append("news-sitemap.xml possui metadados incompletos")
        if any(url not in urls for url in news_urls):
            errors.append("news-sitemap.xml possui URL ausente do sitemap principal")
        now = datetime.now(timezone.utc)
        cutoff = now - timedelta(days=2)
        for value in news_dates:
            try:
                published = datetime.fromisoformat(value.replace("Z", "+00:00"))
                if published.tzinfo is None:
                    published = published.replace(tzinfo=timezone.utc)
                published = published.astimezone(timezone.utc)
            except ValueError:
                errors.append(f"Data inválida no news-sitemap.xml: {value}")
                continue
            if published < cutoff or published > now:
                errors.append(
                    f"Matéria fora da janela de 48 horas no news-sitemap.xml: {value}"
                )
    except (OSError, ET.ParseError) as exc:
        errors.append(f"news-sitemap.xml inválido: {exc}")

    published_sources = [
        *sorted((ROOT / "content").rglob("*.md")),
        *sorted((ROOT / "content").rglob("*.json")),
        *sorted(ROOT.glob("*.html")),
    ]
    published_text = "\n".join(
        path.read_text(encoding="utf-8-sig", errors="ignore")
        for path in published_sources
    )
    for image in sorted((ROOT / "assets" / "img" / "uploads").glob("*")):
        if (
            image.is_file()
            and image.name in published_text
            and image.stat().st_size > 350 * 1024
        ):
            warnings.append(
                f"Imagem acima de 350 KB: {image.relative_to(ROOT)} "
                f"({image.stat().st_size / 1024:.0f} KB)"
            )

    checks = [
        [sys.executable, "scripts/update_sitemap.py", "--check"],
        [sys.executable, "scripts/audit_ptbr.py"],
    ]
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
