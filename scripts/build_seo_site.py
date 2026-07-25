#!/usr/bin/env python3
"""Gera a camada HTML indexável e a rede de entidades da TVDUASRODAS.

O conteúdo editorial continua sendo mantido em ``content``. Este gerador cria
URLs canônicas, HTML completo sem dependência de JavaScript, dados estruturados
e relações internas para matérias, vídeos, competições, eventos, atletas,
temas, marcas e modalidades.
"""

from __future__ import annotations

import html
import json
import re
import unicodedata
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://tvduasrodas.com"
TODAY = date.today().isoformat()
ORG = {
    "@type": "NewsMediaOrganization",
    "@id": f"{BASE_URL}/#organizacao",
    "name": "TVDUASRODAS",
    "url": BASE_URL,
    "logo": {
        "@type": "ImageObject",
        "url": f"{BASE_URL}/assets/img/logotv.png",
    },
    "sameAs": [
        "https://www.youtube.com/@tvduasrodas",
        "https://www.instagram.com/tvduasrodasofc",
    ],
}

TOPICS = {
    "motos": ("Motos", ("moto", "motocicl", "superbike", "motogp", "motocross", "enduro", "rally", "arenacross")),
    "bicicletas": ("Bicicletas", ("bicicleta", "bike", "ciclismo", "mtb", "bmx", "ciclovia", "gravel", "pedal")),
    "scooters": ("Scooters", ("scooter", "kick scooter")),
    "eletricos": ("Elétricos", ("elétric", "eletric", "bateria", "recarga", "e-bike", "ebike")),
    "competicoes": ("Competições", ("campeonato", "competição", "competicao", "corrida", "resultado", "classificação", "classificacao")),
    "eventos": ("Eventos", ("evento", "festival", "feira", "salão", "salao", "fest", "week")),
    "mobilidade": ("Mobilidade urbana", ("mobilidade", "urbano", "cidade", "trânsito", "transito", "micromobilidade")),
    "seguranca": ("Segurança", ("segurança", "seguranca", "frenagem", "chuva", "pontos cegos", "acidente")),
    "tecnologia": ("Tecnologia", ("tecnologia", "dct", "híbr", "hibr", "painel", "dados")),
    "manutencao": ("Manutenção", ("manutenção", "manutencao", "corrente", "lubrifica", "revisão", "revisao")),
    "viagem": ("Viagem", ("viagem", "estrada", "serra", "bagagem", "parada")),
    "lancamentos": ("Lançamentos", ("lançamento", "lancamento", "estreia", "chega", "2026", "2027")),
}

BRANDS = {
    "honda": "Honda",
    "yamaha": "Yamaha",
    "bmw": "BMW Motorrad",
    "ducati": "Ducati",
    "ktm": "KTM",
    "harley-davidson": "Harley-Davidson",
    "royal-enfield": "Royal Enfield",
    "cfmoto": "CFMOTO",
    "kawasaki": "Kawasaki",
    "suzuki": "Suzuki",
    "triumph": "Triumph",
    "caloi": "Caloi",
    "shimano": "Shimano",
}

STOPWORDS = {
    "a", "as", "ao", "aos", "com", "como", "da", "das", "de", "do", "dos",
    "e", "em", "entre", "na", "nas", "no", "nos", "o", "os", "para", "por",
    "que", "se", "sem", "um", "uma", "2026", "tvduasrodas",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def esc(value: Any) -> str:
    return html.escape(str(value or ""), quote=True)


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFD", value)
    ascii_value = "".join(c for c in normalized if unicodedata.category(c) != "Mn")
    return re.sub(r"(^-+|-+$)", "", re.sub(r"[^a-z0-9]+", "-", ascii_value.lower()))


def normalize(value: str) -> str:
    return slugify(value).replace("-", " ")


def iso_day(value: Any) -> str:
    match = re.search(r"\d{4}-\d{2}-\d{2}", str(value or ""))
    return match.group(0) if match else TODAY


def absolute_url(value: str) -> str:
    if not value:
        return ""
    if value.startswith(("http://", "https://")):
        return value
    return f"{BASE_URL}/{value.lstrip('/')}"


def canonicalize_link(value: str) -> str:
    value = value.strip()
    mappings = (
        (r"(?:/)?materia(?:\.html)?\?slug=([^&#)]+)", "materias"),
        (r"(?:/)?competicao(?:\.html)?\?slug=([^&#)]+)", "competicoes"),
        (r"(?:/)?evento(?:\.html)?\?slug=([^&#)]+)", "eventos"),
    )
    for pattern, folder in mappings:
        match = re.fullmatch(pattern, value)
        if match:
            return f"/{folder}/{slugify(unquote(match.group(1)))}/"
    return value


def frontmatter(path: Path) -> tuple[dict[str, Any], str]:
    text = read_text(path)
    if not text.startswith("---"):
        return {}, text
    _, block, body = text.split("---", 2)
    values: dict[str, Any] = {}
    current_list = ""
    for raw in block.splitlines():
        if re.match(r"^\s+-\s+", raw) and current_list:
            values.setdefault(current_list, []).append(raw.split("-", 1)[1].strip().strip("'\""))
            continue
        match = re.match(r"^([A-Za-z_][\w-]*):\s*(.*?)\s*$", raw)
        if not match:
            continue
        key, value = match.groups()
        current_list = key if not value else ""
        values[key] = [] if not value else value.strip().strip("'\"")
    return values, body.strip()


def inline_markdown(text: str) -> str:
    text = esc(text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", text)

    def link(match: re.Match[str]) -> str:
        label, href = match.groups()
        href = canonicalize_link(html.unescape(href))
        external = href.startswith(("http://", "https://"))
        attrs = ' target="_blank" rel="noopener noreferrer"' if external else ""
        return f'<a href="{esc(href)}"{attrs}>{label}</a>'

    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, text)


def markdown(text: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    paragraph: list[str] = []
    in_list = False

    def flush_paragraph() -> None:
        if paragraph:
            out.append(f"<p>{inline_markdown(' '.join(paragraph))}</p>")
            paragraph.clear()

    for raw in lines:
        line = raw.strip()
        if not line:
            flush_paragraph()
            if in_list:
                out.append("</ul>")
                in_list = False
            continue
        image = re.fullmatch(r'!\[([^\]]*)\]\((\S+?)(?:\s+"([^"]*)")?\)', line)
        if image:
            flush_paragraph()
            if in_list:
                out.append("</ul>")
                in_list = False
            alt, src, caption = image.groups()
            out.append(
                f'<figure class="seo-figure"><img src="{esc(src)}" alt="{esc(alt)}" '
                f'loading="lazy" decoding="async"><figcaption>{esc(caption or alt)}</figcaption></figure>'
            )
        elif line.startswith("### "):
            flush_paragraph()
            out.append(f"<h3>{inline_markdown(line[4:])}</h3>")
        elif line.startswith("## "):
            flush_paragraph()
            out.append(f"<h2>{inline_markdown(line[3:])}</h2>")
        elif re.match(r"^[-*]\s+", line):
            flush_paragraph()
            if not in_list:
                out.append("<ul>")
                in_list = True
            item_text = re.sub(r"^[-*]\s+", "", line)
            out.append(f"<li>{inline_markdown(item_text)}</li>")
        elif line.startswith("> "):
            flush_paragraph()
            out.append(f"<blockquote>{inline_markdown(line[2:])}</blockquote>")
        else:
            paragraph.append(line)
    flush_paragraph()
    if in_list:
        out.append("</ul>")
    return "\n".join(out)


def words(value: str) -> set[str]:
    return {
        token for token in normalize(value).split()
        if len(token) > 2 and token not in STOPWORDS
    }


def duration_iso(value: str) -> str:
    parts = [int(x) for x in value.split(":") if x.isdigit()]
    if len(parts) == 2:
        return f"PT{parts[0]}M{parts[1]}S"
    if len(parts) == 3:
        return f"PT{parts[0]}H{parts[1]}M{parts[2]}S"
    return ""


def json_ld(data: Any) -> str:
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return f'<script type="application/ld+json">{payload}</script>'


def breadcrumb_schema(items: list[tuple[str, str]]) -> dict[str, Any]:
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": index,
                "name": label,
                "item": absolute_url(url),
            }
            for index, (label, url) in enumerate(items, 1)
        ],
    }


def page_shell(
    *,
    title: str,
    description: str,
    canonical: str,
    body: str,
    schemas: list[dict[str, Any]],
    image: str = "/assets/img/logotv.png",
    page_type: str = "website",
) -> str:
    canonical_url = absolute_url(canonical)
    image_url = absolute_url(image)
    website = {
        "@type": "WebSite",
        "@id": f"{BASE_URL}/#website",
        "name": "TVDUASRODAS",
        "url": BASE_URL,
        "inLanguage": "pt-BR",
        "publisher": {"@id": f"{BASE_URL}/#organizacao"},
        "potentialAction": {
            "@type": "SearchAction",
            "target": f"{BASE_URL}/busca?q={{search_term_string}}",
            "query-input": "required name=search_term_string",
        },
    }
    graph = {"@context": "https://schema.org", "@graph": [ORG, website, *schemas]}
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{esc(title)} | TVDUASRODAS</title>
  <meta name="description" content="{esc(description[:160])}">
  <meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
  <link rel="canonical" href="{esc(canonical_url)}">
  <link rel="icon" href="/assets/img/logoTVicon_web.ico">
  <link rel="stylesheet" href="/assets/css/style.css?v=20260725seo">
  <meta property="og:locale" content="pt_BR">
  <meta property="og:type" content="{esc(page_type)}">
  <meta property="og:site_name" content="TVDUASRODAS">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(description[:200])}">
  <meta property="og:url" content="{esc(canonical_url)}">
  <meta property="og:image" content="{esc(image_url)}">
  <meta name="twitter:card" content="summary_large_image">
  <base href="/">
  {json_ld(graph)}
</head>
<body class="page-internal seo-page">
  <header class="site-header">
    <div class="container header-inner">
      <div class="logo-wrapper"><a href="/" class="logo-link"><img src="/assets/img/logotv.png" alt="TVDUASRODAS" class="logo-image"></a><div class="brand-sub">Motos · Bikes · Scooters · Elétricos</div></div>
      <nav class="main-nav" aria-label="Navegação principal"><ul>
        <li><a href="/">Início</a></li><li><a href="/revista">Revista</a></li><li><a href="/videos/">Vídeos</a></li>
        <li><a href="/competicoes-eventos">Competições &amp; Eventos</a></li><li><a href="/assuntos/">Assuntos</a></li><li><a href="/arquivo.html">Arquivo</a></li>
      </ul></nav>
    </div>
  </header>
  <main class="section"><div class="container seo-container">{body}</div></main>
  <footer class="site-footer"><div class="container footer-inner"><div class="footer-left">
    <p>© TVDUASRODAS — conteúdo sobre o universo das duas rodas.</p>
    <p class="footer-small"><a href="/sobre">Sobre</a> · <a href="/contato">Contato</a> · <a href="/sitemap.xml">Sitemap</a></p>
  </div></div></footer>
</body>
</html>
"""


def write_page(path: str, content: str) -> None:
    target = ROOT / path.strip("/") / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8", newline="\n")


def card(item: dict[str, Any]) -> str:
    eyebrow = item.get("kind_label", item.get("category", "Conteúdo"))
    image = item.get("image", "")
    media = (
        f'<a class="seo-card__media" href="{esc(item["url"])}"><img src="{esc(image)}" '
        f'alt="{esc(item["title"])}" loading="lazy" decoding="async"></a>'
        if image else ""
    )
    return (
        f'<article class="seo-card">{media}<div><span class="seo-eyebrow">{esc(eyebrow)}</span>'
        f'<h3><a href="{esc(item["url"])}">{esc(item["title"])}</a></h3>'
        f'<p>{esc(item.get("summary", ""))}</p></div></article>'
    )


def related_items(current: dict[str, Any], all_items: list[dict[str, Any]], limit: int = 6) -> list[dict[str, Any]]:
    base = words(current.get("search_text", ""))
    scored: list[tuple[int, dict[str, Any]]] = []
    for item in all_items:
        if item["url"] == current["url"]:
            continue
        score = len(base & words(item.get("search_text", "")))
        if item.get("topics") and current.get("topics"):
            score += 3 * len(set(item["topics"]) & set(current["topics"]))
        if score:
            scored.append((score, item))
    return [item for _, item in sorted(scored, key=lambda pair: (-pair[0], pair[1]["title"]))[:limit]]


def relation_blocks(item: dict[str, Any], all_items: list[dict[str, Any]]) -> str:
    topics = item.get("topics", [])
    brands = item.get("brands", [])
    modalities = item.get("modalities", [])
    chips = [
        *(f'<a href="/assuntos/{slug}/">{esc(TOPICS[slug][0])}</a>' for slug in topics),
        *(f'<a href="/marcas/{slug}/">{esc(BRANDS[slug])}</a>' for slug in brands),
        *(f'<a href="/modalidades/{slug}/">{esc(label)}</a>' for slug, label in modalities),
    ]
    related = related_items(item, all_items)
    chips_html = f'<nav class="seo-relations" aria-label="Assuntos relacionados">{"".join(chips)}</nav>' if chips else ""
    related_html = ""
    if related:
        related_html = (
            '<section class="seo-related"><h2>Conteúdos relacionados</h2><div class="seo-grid">'
            + "".join(card(value) for value in related) + "</div></section>"
        )
    return chips_html + related_html


def classify(item: dict[str, Any]) -> None:
    normalized = normalize(item.get("search_text", ""))
    item["topics"] = [
        slug for slug, (_, patterns) in TOPICS.items()
        if any(normalize(pattern) in normalized for pattern in patterns)
    ]
    item["brands"] = [
        slug for slug, label in BRANDS.items()
        if normalize(slug) in normalized or normalize(label) in normalized
    ]


def load_content() -> tuple[list[dict[str, Any]], dict[str, list[dict[str, Any]]]]:
    items: list[dict[str, Any]] = []
    people: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for path in sorted((ROOT / "content/news").glob("*.md")):
        meta, body = frontmatter(path)
        slug = path.stem
        title = meta.get("title", slug)
        summary = meta.get("summary") or re.sub(r"[*#\[\]()]", "", body)[:220]
        item = {
            "kind": "article", "kind_label": "Matéria", "slug": slug, "title": title,
            "summary": summary, "body": body, "date": meta.get("date", TODAY),
            "lastmod": iso_day(meta.get("updated_at") or meta.get("date")),
            "category": meta.get("category", "Revista"), "author": meta.get("author", "Redação TVDUASRODAS"),
            "image": meta.get("cover", ""), "url": f"/materias/{slugify(slug)}/",
            "search_text": " ".join((title, summary, body, str(meta.get("tags", "")))),
        }
        items.append(item)

    for path in sorted((ROOT / "content/videos").glob("*.md")):
        meta, body = frontmatter(path)
        slug = path.stem
        youtube = meta.get("youtube_url", "")
        match = re.search(r"(?:v=|youtu\.be/)([A-Za-z0-9_-]{6,})", youtube)
        video_id = match.group(1) if match else ""
        title = meta.get("title", slug)
        item = {
            "kind": "video", "kind_label": "Vídeo", "slug": slug, "title": title,
            "summary": re.sub(r"[*#\[\]()]", "", body)[:220], "body": body,
            "date": meta.get("date", TODAY), "lastmod": iso_day(meta.get("date")),
            "category": meta.get("category", "Vídeos"), "channel": meta.get("channel", ""),
            "duration": meta.get("duration", ""), "youtube": youtube, "video_id": video_id,
            "image": meta.get("thumbnail", f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"),
            "url": f"/videos/{slugify(slug)}/",
            "search_text": " ".join((title, body, str(meta.get("tags", "")), str(meta.get("category", "")))),
        }
        items.append(item)

    for path in sorted((ROOT / "content/competitions").glob("*.json")):
        if path.name == "index.json":
            continue
        data = json.loads(read_text(path))
        slug = path.stem
        modalities = [(slugify(data.get("modality", "")), data.get("modality", ""))] if data.get("modality") else []
        item = {
            "kind": "competition", "kind_label": "Competição", "slug": slug,
            "title": data.get("title", slug), "summary": data.get("summary", ""),
            "body": data.get("body", ""), "date": data.get("last_updated", TODAY),
            "lastmod": iso_day(data.get("last_updated")), "category": data.get("modality", "Competição"),
            "image": data.get("cover", ""), "url": f"/competicoes/{slug}/",
            "data": data, "modalities": modalities,
            "search_text": json.dumps(data, ensure_ascii=False),
        }
        items.append(item)
        for result in data.get("standings", []):
            name = str(result.get("competitor", "")).strip()
            if not name:
                continue
            people[normalize(name)].append({
                "name": name,
                "competition": item,
                "category": result.get("category", ""),
                "position": result.get("display_position") or result.get("position", ""),
                "team": result.get("team", ""),
                "result": result.get("points") or result.get("time_gap", ""),
            })

    for path in sorted((ROOT / "content/events").glob("*.json")):
        if path.name == "index.json":
            continue
        data = json.loads(read_text(path))
        slug = path.stem
        item = {
            "kind": "event", "kind_label": "Evento", "slug": slug,
            "title": data.get("title", slug), "summary": data.get("summary", ""),
            "body": data.get("body", ""), "date": data.get("start_date", TODAY),
            "lastmod": iso_day(data.get("last_updated") or data.get("start_date")),
            "category": data.get("event_type", "Evento"), "image": data.get("cover", ""),
            "url": f"/eventos/{slug}/", "data": data,
            "search_text": json.dumps(data, ensure_ascii=False),
        }
        items.append(item)

    calendar = json.loads(read_text(ROOT / "content/calendar/cbm-2026.json"))
    existing = {item["slug"] for item in items if item["kind"] == "event"}
    for data in calendar.get("entries", []):
        if data.get("competition_slug"):
            continue
        slug = slugify(f"{data.get('title', '')}-{data.get('start_date', '')}")
        if not slug or slug in existing:
            continue
        modality = data.get("modality", "")
        item = {
            "kind": "event", "kind_label": "Evento do calendário", "slug": slug,
            "title": data.get("title", slug),
            "summary": " · ".join(filter(None, (data.get("stage"), data.get("city"), data.get("state")))),
            "body": f"## Sobre a prova\n\n{data.get('title')} integra o calendário monitorado pela TVDUASRODAS. Consulte a fonte oficial para confirmar programação, inscrições e alterações.",
            "date": data.get("start_date", TODAY), "lastmod": iso_day(data.get("start_date")),
            "category": modality or "Evento", "image": "/assets/img/competicoes-eventos-default.svg",
            "url": f"/eventos/{slug}/", "data": data,
            "modalities": [(slugify(modality), modality)] if modality else [],
            "search_text": json.dumps(data, ensure_ascii=False),
        }
        items.append(item)

    for path in sorted((ROOT / "content/articles").glob("*.json")):
        data = json.loads(read_text(path))
        slug = path.stem
        body_text = re.sub(r"<[^>]+>", " ", data.get("bodyHtml", ""))
        item = {
            "kind": "guide", "kind_label": "Guia", "slug": slug,
            "title": data.get("title", slug), "summary": data.get("summary", ""),
            "body_html": data.get("bodyHtml", ""), "date": data.get("date", TODAY),
            "lastmod": iso_day(data.get("date")), "category": data.get("category", "Guia"),
            "image": data.get("hero", {}).get("image", ""), "url": f"/guias/{slug}/",
            "search_text": " ".join((data.get("title", ""), data.get("summary", ""), body_text)),
        }
        items.append(item)

    for item in items:
        item.setdefault("modalities", [])
        classify(item)
    return items, people


def render_article(item: dict[str, Any], all_items: list[dict[str, Any]]) -> str:
    canonical = item["url"]
    image = item.get("image") or "/assets/img/logotv.png"
    article_schema = {
        "@type": "NewsArticle",
        "@id": f"{absolute_url(canonical)}#artigo",
        "headline": item["title"],
        "description": item["summary"],
        "datePublished": item["date"],
        "dateModified": item["date"],
        "mainEntityOfPage": absolute_url(canonical),
        "image": [absolute_url(image)],
        "author": {"@type": "Organization", "name": item["author"]},
        "publisher": ORG,
        "articleSection": item["category"],
        "inLanguage": "pt-BR",
    }
    body = f"""
<nav class="seo-breadcrumb"><a href="/">Início</a> › <a href="/revista">Revista</a> › {esc(item["category"])}</nav>
<article class="seo-article">
  <header><span class="seo-eyebrow">{esc(item["category"])}</span><h1>{esc(item["title"])}</h1>
  <p class="seo-lead">{esc(item["summary"])}</p><p class="seo-meta">Por {esc(item["author"])} · {esc(iso_day(item["date"]))}</p></header>
  {f'<figure class="seo-hero"><img src="{esc(image)}" alt="{esc(item["title"])}"><figcaption>{esc(item["title"])}</figcaption></figure>' if image else ""}
  <div class="seo-prose">{markdown(item["body"])}</div>
  {relation_blocks(item, all_items)}
</article>"""
    return page_shell(
        title=item["title"], description=item["summary"], canonical=canonical, body=body,
        schemas=[article_schema, breadcrumb_schema([("Início", "/"), ("Revista", "/revista"), (item["title"], canonical)])],
        image=image, page_type="article",
    )


def render_video(item: dict[str, Any], all_items: list[dict[str, Any]]) -> str:
    canonical = item["url"]
    video_schema = {
        "@type": "VideoObject",
        "@id": f"{absolute_url(canonical)}#video",
        "name": item["title"],
        "description": item["summary"],
        "thumbnailUrl": [absolute_url(item["image"])],
        "uploadDate": item["date"],
        "embedUrl": f"https://www.youtube.com/embed/{item['video_id']}",
        "publisher": ORG,
        "inLanguage": "pt-BR",
    }
    if duration_iso(item.get("duration", "")):
        video_schema["duration"] = duration_iso(item["duration"])
    body = f"""
<nav class="seo-breadcrumb"><a href="/">Início</a> › <a href="/videos/">Vídeos</a> › {esc(item["category"])}</nav>
<article class="seo-article">
  <header><span class="seo-eyebrow">Vídeo · {esc(item["category"])}</span><h1>{esc(item["title"])}</h1>
  <p class="seo-lead">{esc(item["summary"])}</p><p class="seo-meta">{esc(item.get("channel"))} · {esc(iso_day(item["date"]))}</p></header>
  <div class="seo-video"><iframe src="https://www.youtube.com/embed/{esc(item["video_id"])}" title="{esc(item["title"])}" allowfullscreen loading="eager"></iframe></div>
  <div class="seo-prose">{markdown(item["body"])}</div>
  {relation_blocks(item, all_items)}
</article>"""
    return page_shell(
        title=item["title"], description=item["summary"], canonical=canonical, body=body,
        schemas=[video_schema, breadcrumb_schema([("Início", "/"), ("Vídeos", "/videos/"), (item["title"], canonical)])],
        image=item["image"], page_type="video.other",
    )


def linked_markdown(text: str, people: dict[str, list[dict[str, Any]]]) -> str:
    rendered = markdown(text)
    # A tabela de resultados contém os links principais. No texto corrido,
    # fazemos ligações apenas para nomes completos para evitar falsos positivos.
    for key, records in sorted(people.items(), key=lambda pair: -len(pair[1][0]["name"])):
        name = records[0]["name"]
        if name in rendered and f'>{esc(name)}</a>' not in rendered:
            rendered = rendered.replace(
                name, f'<a href="/atletas/{slugify(name)}/">{esc(name)}</a>', 1
            )
    return rendered


def render_competition(
    item: dict[str, Any], all_items: list[dict[str, Any]], people: dict[str, list[dict[str, Any]]]
) -> str:
    data = item["data"]
    canonical = item["url"]
    standings = data.get("standings", [])
    rows = []
    for result in standings:
        name = result.get("competitor", "")
        rows.append(
            f"<tr><td>{esc(result.get('display_position') or result.get('position'))}</td>"
            f'<td><a href="/atletas/{slugify(name)}/"><strong>{esc(name)}</strong></a></td>'
            f"<td>{esc(result.get('category'))}</td><td>{esc(result.get('team'))}</td>"
            f"<td>{esc(result.get('points') or result.get('time_gap'))}</td></tr>"
        )
    rounds = "".join(
        f"<tr><td>{esc(stage.get('name'))}</td><td>{esc(stage.get('start_date'))}</td>"
        f"<td>{esc(stage.get('location'))}</td><td>{esc(stage.get('winner') or stage.get('status'))}</td></tr>"
        for stage in data.get("rounds", [])
    )
    start = data.get("next_stage", {}).get("start_date") or (data.get("rounds") or [{}])[0].get("start_date")
    end = data.get("next_stage", {}).get("end_date") or start
    schema = {
        "@type": "SportsEvent",
        "@id": f"{absolute_url(canonical)}#competicao",
        "name": item["title"],
        "description": item["summary"],
        "startDate": start,
        "endDate": end,
        "image": [absolute_url(item["image"])],
        "url": absolute_url(canonical),
        "organizer": {"@type": "Organization", "name": data.get("organizer", ""), "url": data.get("official_url", "")},
        "location": {
            "@type": "Place",
            "name": data.get("next_stage", {}).get("venue") or data.get("next_stage", {}).get("city") or "Brasil",
            "address": {
                "@type": "PostalAddress",
                "addressLocality": data.get("next_stage", {}).get("city", ""),
                "addressRegion": data.get("next_stage", {}).get("state", ""),
                "addressCountry": data.get("country", "Brasil"),
            },
        },
        "eventStatus": "https://schema.org/EventScheduled",
    }
    body = f"""
<nav class="seo-breadcrumb"><a href="/">Início</a> › <a href="/competicoes-eventos">Competições</a> › {esc(item["title"])}</nav>
<article class="seo-article">
  <header><span class="seo-eyebrow">{esc(data.get("modality"))} · Temporada {esc(data.get("season"))}</span>
  <h1>{esc(item["title"])}</h1><p class="seo-lead">{esc(item["summary"])}</p>
  <p class="seo-meta">Organização: {esc(data.get("organizer"))} · Atualizado em {esc(item["lastmod"])}</p></header>
  <figure class="seo-hero"><img src="{esc(item["image"])}" alt="{esc(item["title"])}"><figcaption>{esc(data.get("image_credit"))}</figcaption></figure>
  <div class="seo-prose">{linked_markdown(item["body"], people)}</div>
  <section><h2>{esc(data.get("standings_title") or "Classificação e resultados")}</h2>
  {('<div class="seo-table"><table><thead><tr><th>Pos.</th><th>Atleta/piloto</th><th>Categoria</th><th>Equipe</th><th>Resultado</th></tr></thead><tbody>' + ''.join(rows) + '</tbody></table></div>') if rows else '<p>Classificação aguardando publicação oficial.</p>'}
  </section>
  <section><h2>Etapas e calendário</h2>{('<div class="seo-table"><table><thead><tr><th>Etapa</th><th>Data</th><th>Local</th><th>Resultado/situação</th></tr></thead><tbody>' + rounds + '</tbody></table></div>') if rounds else '<p>Calendário em confirmação.</p>'}</section>
  <aside class="seo-source"><strong>Fonte e atualização</strong><p>Dados conferidos com a entidade ou organização oficial. <a href="{esc(data.get("official_url"))}" target="_blank" rel="noopener noreferrer">Consultar fonte oficial</a>.</p></aside>
  {relation_blocks(item, all_items)}
</article>"""
    return page_shell(
        title=item["title"], description=item["summary"], canonical=canonical, body=body,
        schemas=[schema, breadcrumb_schema([("Início", "/"), ("Competições", "/competicoes-eventos"), (item["title"], canonical)])],
        image=item["image"],
    )


def render_event(item: dict[str, Any], all_items: list[dict[str, Any]]) -> str:
    data = item["data"]
    canonical = item["url"]
    location_name = data.get("venue") or data.get("location") or data.get("city") or "Local a confirmar"
    schema = {
        "@type": "Event",
        "@id": f"{absolute_url(canonical)}#evento",
        "name": item["title"],
        "description": item["summary"],
        "startDate": data.get("start_date"),
        "endDate": data.get("end_date") or data.get("start_date"),
        "eventStatus": "https://schema.org/EventScheduled",
        "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
        "url": absolute_url(canonical),
        "image": [absolute_url(item["image"])],
        "location": {
            "@type": "Place", "name": location_name,
            "address": {"@type": "PostalAddress", "addressLocality": data.get("city", ""), "addressRegion": data.get("state", ""), "addressCountry": "BR"},
        },
    }
    if data.get("official_url"):
        schema["organizer"] = {"@type": "Organization", "name": data.get("organizer") or item["title"], "url": data["official_url"]}
    body = f"""
<nav class="seo-breadcrumb"><a href="/">Início</a> › <a href="/competicoes-eventos">Eventos</a> › {esc(item["title"])}</nav>
<article class="seo-article">
  <header><span class="seo-eyebrow">{esc(item["category"])}</span><h1>{esc(item["title"])}</h1>
  <p class="seo-lead">{esc(item["summary"])}</p></header>
  <figure class="seo-hero"><img src="{esc(item["image"])}" alt="{esc(item["title"])}"><figcaption>{esc(data.get("image_credit"))}</figcaption></figure>
  <section class="seo-service"><div><span>Data</span><strong>{esc(data.get("start_date"))} a {esc(data.get("end_date") or data.get("start_date"))}</strong></div>
  <div><span>Local</span><strong>{esc(location_name)}</strong><small>{esc(data.get("city"))}/{esc(data.get("state"))}</small></div></section>
  <div class="seo-prose">{markdown(item["body"])}</div>
  {relation_blocks(item, all_items)}
  <aside class="seo-source"><strong>Confirme antes de ir</strong><p>Programação e regras podem mudar. <a href="{esc(data.get("official_url", "#"))}" target="_blank" rel="noopener noreferrer">Consulte o canal oficial</a>.</p></aside>
</article>"""
    return page_shell(
        title=item["title"], description=item["summary"], canonical=canonical, body=body,
        schemas=[schema, breadcrumb_schema([("Início", "/"), ("Eventos", "/competicoes-eventos"), (item["title"], canonical)])],
        image=item["image"],
    )


def render_guide(item: dict[str, Any], all_items: list[dict[str, Any]]) -> str:
    canonical = item["url"]
    schema = {
        "@type": "Article", "@id": f"{absolute_url(canonical)}#guia",
        "headline": item["title"], "description": item["summary"], "mainEntityOfPage": absolute_url(canonical),
        "image": [absolute_url(item["image"])], "author": ORG, "publisher": ORG, "inLanguage": "pt-BR",
    }
    body = f"""
<nav class="seo-breadcrumb"><a href="/">Início</a> › <a href="/arquivo.html">Guias</a> › {esc(item["title"])}</nav>
<article class="seo-article"><header><span class="seo-eyebrow">{esc(item["category"])}</span><h1>{esc(item["title"])}</h1>
<p class="seo-lead">{esc(item["summary"])}</p></header>
<figure class="seo-hero"><img src="{esc(item["image"])}" alt="{esc(item["title"])}"></figure>
<div class="seo-prose">{item.get("body_html", "")}</div>{relation_blocks(item, all_items)}</article>"""
    return page_shell(
        title=item["title"], description=item["summary"], canonical=canonical, body=body,
        schemas=[schema, breadcrumb_schema([("Início", "/"), ("Arquivo", "/arquivo.html"), (item["title"], canonical)])],
        image=item["image"], page_type="article",
    )


def render_person(name: str, records: list[dict[str, Any]], all_items: list[dict[str, Any]]) -> tuple[str, str]:
    slug = slugify(name)
    canonical = f"/atletas/{slug}/"
    mentioned = [
        item for item in all_items
        if normalize(name) in normalize(item.get("search_text", ""))
    ]
    first = records[0]
    description = (
        f"Resultados de {name} em competições acompanhadas pela TVDUASRODAS, "
        f"com categoria, posição, equipe, fonte e links para as classificações."
    )
    rows = "".join(
        f'<tr><td><a href="{esc(record["competition"]["url"])}">{esc(record["competition"]["title"])}</a></td>'
        f'<td>{esc(record["category"])}</td><td><strong>{esc(record["position"])}</strong></td>'
        f'<td>{esc(record["team"])}</td><td>{esc(record["result"])}</td></tr>'
        for record in records
    )
    cards = "".join(card(item) for item in mentioned[:8])
    schema = {
        "@type": "WebPage",
        "@id": f"{absolute_url(canonical)}#pagina",
        "name": f"{name}: resultados e classificações",
        "description": description,
        "mainEntity": {
            "@type": "Person", "@id": f"{absolute_url(canonical)}#pessoa",
            "name": name,
            "affiliation": {"@type": "Organization", "name": first["team"]} if first["team"] else None,
        },
        "isPartOf": {"@id": f"{BASE_URL}/#website"},
        "inLanguage": "pt-BR",
    }
    if schema["mainEntity"]["affiliation"] is None:
        del schema["mainEntity"]["affiliation"]
    body = f"""
<nav class="seo-breadcrumb"><a href="/">Início</a> › <a href="/atletas/">Atletas e pilotos</a> › {esc(name)}</nav>
<article class="seo-article"><header><span class="seo-eyebrow">Atleta ou piloto em resultados publicados</span>
<h1>{esc(name)}</h1><p class="seo-lead">{esc(description)}</p></header>
<section><h2>Resultados de {esc(name)}</h2><div class="seo-table"><table>
<thead><tr><th>Competição</th><th>Categoria</th><th>Posição</th><th>Equipe</th><th>Resultado</th></tr></thead><tbody>{rows}</tbody></table></div></section>
{f'<section><h2>Matérias e páginas relacionadas</h2><div class="seo-grid">{cards}</div></section>' if cards else ""}
<aside class="seo-source"><strong>Sobre esta página</strong><p>Esta é uma página de referência editorial baseada nas classificações publicadas pelas entidades e organizadores. Não é um perfil oficial da pessoa.</p></aside>
</article>"""
    return canonical, page_shell(
        title=f"{name}: resultados e classificações", description=description, canonical=canonical, body=body,
        schemas=[schema, breadcrumb_schema([("Início", "/"), ("Atletas", "/atletas/"), (name, canonical)])],
    )


def render_collection(
    *, label: str, description: str, canonical: str, collection: list[dict[str, Any]],
    breadcrumb_parent: tuple[str, str] | None = None,
) -> str:
    cards = "".join(card(item) for item in sorted(collection, key=lambda x: (x.get("lastmod", ""), x["title"]), reverse=True))
    schema = {
        "@type": "CollectionPage", "@id": f"{absolute_url(canonical)}#colecao",
        "name": label, "description": description, "url": absolute_url(canonical),
        "hasPart": [{"@type": "CreativeWork", "name": item["title"], "url": absolute_url(item["url"])} for item in collection],
        "inLanguage": "pt-BR",
    }
    crumbs = [("Início", "/")]
    if breadcrumb_parent:
        crumbs.append(breadcrumb_parent)
    crumbs.append((label, canonical))
    body = f"""
<nav class="seo-breadcrumb">{" › ".join(f'<a href="{url}">{esc(name)}</a>' for name, url in crumbs[:-1])} › {esc(label)}</nav>
<header class="seo-collection-header"><span class="seo-eyebrow">TVDUASRODAS</span><h1>{esc(label)}</h1><p class="seo-lead">{esc(description)}</p></header>
<div class="seo-grid">{cards or '<p>Nenhum conteúdo publicado nesta coleção.</p>'}</div>"""
    return page_shell(
        title=label, description=description, canonical=canonical, body=body,
        schemas=[schema, breadcrumb_schema(crumbs)],
    )


def build() -> None:
    items, people = load_content()
    manifest: list[dict[str, Any]] = []

    for item in items:
        if item["kind"] == "article":
            output = render_article(item, items)
        elif item["kind"] == "video":
            output = render_video(item, items)
        elif item["kind"] == "competition":
            output = render_competition(item, items, people)
        elif item["kind"] == "event":
            output = render_event(item, items)
        else:
            output = render_guide(item, items)
        write_page(item["url"], output)
        manifest_item = {
            "url": item["url"], "lastmod": item["lastmod"],
            "priority": "0.8" if item["kind"] in {"article", "competition"} else "0.7",
            "image": absolute_url(item["image"]) if item.get("image") else "",
            "kind": item["kind"],
        }
        if item["kind"] == "video":
            manifest_item["video"] = {
                "thumbnail": absolute_url(item["image"]), "title": item["title"],
                "description": item["summary"], "upload_date": item["date"],
                "player": f"https://www.youtube.com/embed/{item['video_id']}",
            }
        manifest.append(manifest_item)

    person_index: list[dict[str, Any]] = []
    for _, records in sorted(people.items(), key=lambda pair: pair[1][0]["name"]):
        name = records[0]["name"]
        canonical, output = render_person(name, records, items)
        write_page(canonical, output)
        person_item = {
            "title": name, "url": canonical, "summary": f"{len(records)} resultado(s) publicado(s)",
            "kind_label": "Atleta ou piloto", "search_text": name,
        }
        person_index.append(person_item)
        manifest.append({"url": canonical, "lastmod": max(r["competition"]["lastmod"] for r in records), "priority": "0.6", "kind": "person"})

    indexes = [
        ("Vídeos", "Vídeos sobre motos, bicicletas, competições, tecnologia e mobilidade.", "/videos/", [i for i in items if i["kind"] == "video"]),
        ("Atletas e pilotos", "Índice de atletas e pilotos citados em classificações oficiais publicadas pela TVDUASRODAS.", "/atletas/", person_index),
        ("Assuntos", "Temas centrais da cobertura editorial da TVDUASRODAS.", "/assuntos/", [
            {"title": label, "url": f"/assuntos/{slug}/", "summary": f"Matérias, vídeos, eventos e competições sobre {label.lower()}.", "kind_label": "Tema"}
            for slug, (label, _) in TOPICS.items()
        ]),
        ("Marcas", "Marcas de motos, bicicletas, componentes e mobilidade citadas no acervo editorial.", "/marcas/", [
            {"title": label, "url": f"/marcas/{slug}/", "summary": f"Conteúdos relacionados à {label}.", "kind_label": "Marca"}
            for slug, label in BRANDS.items() if any(slug in item.get("brands", []) for item in items)
        ]),
    ]
    for label, description, canonical, collection in indexes:
        write_page(canonical, render_collection(label=label, description=description, canonical=canonical, collection=collection))
        manifest.append({"url": canonical, "lastmod": TODAY, "priority": "0.8", "kind": "index"})

    for slug, (label, _) in TOPICS.items():
        collection = [item for item in items if slug in item.get("topics", [])]
        if not collection:
            continue
        canonical = f"/assuntos/{slug}/"
        description = f"Notícias, guias, vídeos, competições e eventos sobre {label.lower()} na TVDUASRODAS."
        write_page(canonical, render_collection(label=label, description=description, canonical=canonical, collection=collection, breadcrumb_parent=("Assuntos", "/assuntos/")))
        manifest.append({"url": canonical, "lastmod": max(i["lastmod"] for i in collection), "priority": "0.7", "kind": "topic"})

    for slug, label in BRANDS.items():
        collection = [item for item in items if slug in item.get("brands", [])]
        if not collection:
            continue
        canonical = f"/marcas/{slug}/"
        description = f"Notícias, lançamentos, vídeos e referências à {label} publicados pela TVDUASRODAS."
        write_page(canonical, render_collection(label=label, description=description, canonical=canonical, collection=collection, breadcrumb_parent=("Marcas", "/marcas/")))
        manifest.append({"url": canonical, "lastmod": max(i["lastmod"] for i in collection), "priority": "0.6", "kind": "brand"})

    modalities: dict[str, dict[str, Any]] = {}
    for item in items:
        for slug, label in item.get("modalities", []):
            if slug:
                modalities.setdefault(slug, {"label": label, "items": []})["items"].append(item)
    modality_index = [
        {"title": data["label"], "url": f"/modalidades/{slug}/", "summary": f"Calendário, resultados e conteúdos de {data['label']}.", "kind_label": "Modalidade"}
        for slug, data in modalities.items()
    ]
    write_page("/modalidades/", render_collection(
        label="Modalidades", description="Modalidades esportivas acompanhadas pela TVDUASRODAS.",
        canonical="/modalidades/", collection=modality_index,
    ))
    manifest.append({"url": "/modalidades/", "lastmod": TODAY, "priority": "0.8", "kind": "index"})
    for slug, data in modalities.items():
        canonical = f"/modalidades/{slug}/"
        description = f"Calendário, competições, resultados, atletas e conteúdos sobre {data['label']}."
        write_page(canonical, render_collection(label=data["label"], description=description, canonical=canonical, collection=data["items"], breadcrumb_parent=("Modalidades", "/modalidades/")))
        manifest.append({"url": canonical, "lastmod": max(i["lastmod"] for i in data["items"]), "priority": "0.7", "kind": "modality"})

    archive_body = """
<header class="seo-collection-header"><span class="seo-eyebrow">Índice editorial</span><h1>Arquivo completo da TVDUASRODAS</h1>
<p class="seo-lead">Acesso rastreável a matérias, vídeos, guias, competições, eventos, atletas, marcas, assuntos e modalidades.</p></header>
""" + "".join(
        f'<section><h2>{esc(label)}</h2><div class="seo-grid">{"".join(card(i) for i in collection)}</div></section>'
        for label, collection in (
            ("Matérias", [i for i in items if i["kind"] == "article"]),
            ("Vídeos", [i for i in items if i["kind"] == "video"]),
            ("Competições", [i for i in items if i["kind"] == "competition"]),
            ("Eventos", [i for i in items if i["kind"] == "event"]),
            ("Guias", [i for i in items if i["kind"] == "guide"]),
        )
    )
    archive_schema = {
        "@type": "CollectionPage", "name": "Arquivo completo da TVDUASRODAS",
        "url": f"{BASE_URL}/arquivo.html", "inLanguage": "pt-BR",
    }
    archive_html = page_shell(
        title="Arquivo completo", description="Índice de todo o conteúdo publicado pela TVDUASRODAS.",
        canonical="/arquivo.html", body=archive_body, schemas=[archive_schema],
    )
    (ROOT / "arquivo.html").write_text(archive_html, encoding="utf-8", newline="\n")
    manifest.append({"url": "/arquivo.html", "lastmod": TODAY, "priority": "0.9", "kind": "index"})

    manifest_path = ROOT / "content/seo-manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(
        f"SEO gerado: {len(items)} conteúdos, {len(person_index)} pessoas, "
        f"{len(manifest)} URLs canônicas."
    )


if __name__ == "__main__":
    build()
