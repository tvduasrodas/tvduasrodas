#!/usr/bin/env python3
"""Gera a camada HTML indexável e a rede de entidades da TVDUASRODAS.

O conteúdo editorial continua sendo mantido em ``content``. Este gerador cria
URLs canônicas, HTML completo sem dependência de JavaScript, dados estruturados
e relações internas para matérias, vídeos, competições, eventos, atletas,
temas, marcas e modalidades.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import unicodedata
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import unquote

from audit_source_depth import evaluate as evaluate_source_depth


ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://tvduasrodas.com"
TODAY = date.today().isoformat()
LEGACY_PERSON_PAGES = {
    "brendon-oliveira": ("Brendon Oliveira", "/atletas/brendon-pereira-de-oliveira/"),
    "charleu-spricigo": ("Charleu Spricigo", "/atletas/charleu-augusto-spricigo/"),
    "daniel-morandini": ("Daniel Morandini", "/competicoes/brasileiro-enduro-regularidade-2026/"),
    "emerson-loth-bomba": ("Emerson Loth Bomba", "/atletas/emerson-loth-pereira/"),
    "fabio-aparecido-santos": ("Fábio Aparecido Santos", "/atletas/fabio-aparecido-dos-santos/"),
    "jan-pancar": ("Jan Pancar", "/competicoes/mxgp-2026/"),
    "jeremy-seewer": ("Jeremy Seewer", "/competicoes/mxgp-2026/"),
    "juan-viera": ("Juan Viera", "/atletas/juan-vieira/"),
    "kayman-freire": ("Kayman Freire", "/competicoes/moto1000gp-2026/"),
    "kevin-horgmo": ("Kevin Horgmo", "/competicoes/mxgp-2026/"),
}
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


def event_has_ended(data: dict[str, Any]) -> bool:
    """Return whether an event date is in the past without hiding its page."""
    raw = str(data.get("end_date") or data.get("start_date") or "")
    match = re.search(r"\d{4}-\d{2}-\d{2}", raw)
    if not match:
        return False
    try:
        return date.fromisoformat(match.group(0)) < date.today()
    except ValueError:
        return False


def event_schema_status(data: dict[str, Any]) -> str:
    status = str(data.get("status") or "").strip().casefold()
    explicit = {
        "concluida": "https://schema.org/EventCompleted",
        "concluido": "https://schema.org/EventCompleted",
        "encerrado": "https://schema.org/EventCompleted",
        "cancelada": "https://schema.org/EventCancelled",
        "cancelado": "https://schema.org/EventCancelled",
        "adiada": "https://schema.org/EventPostponed",
        "adiado": "https://schema.org/EventPostponed",
    }
    if status in explicit:
        return explicit[status]
    if event_has_ended(data):
        return "https://schema.org/EventCompleted"
    return "https://schema.org/EventScheduled"


def offer_valid_from(
    data: dict[str, Any],
    offer: dict[str, Any] | None,
    fallback_lastmod: str,
) -> str:
    """Use the first documented date when the editorial offer was available."""
    candidates = [
        (offer or {}).get("valid_from"),
        (offer or {}).get("availability_starts"),
        data.get("ticket_sales_start"),
        data.get("offer_valid_from"),
        data.get("published_at"),
        data.get("source_checked_at"),
        data.get("last_updated"),
        fallback_lastmod,
    ]
    for value in candidates:
        raw = str(value or "").strip()
        match = re.search(r"\d{4}-\d{2}-\d{2}", raw)
        if not match:
            continue
        if "T" in raw:
            return raw
        return f"{match.group(0)}T00:00:00"
    return ""


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

CATEGORY_LABELS = {
    "bikes": "Bicicletas",
    "cassetadas": "Cassetadas",
    "competicoes": "Competições",
    "cross": "Cross",
    "customizacao": "Customização",
    "dicas": "Dicas",
    "eventos": "Eventos",
    "historia": "História",
    "institucional": "Institucional",
    "lancamentos": "Lançamentos",
    "outros": "Outros",
    "seguranca": "Segurança",
    "tecnologia": "Tecnologia",
    "testes": "Testes",
    "tests": "Testes",
    "urbano": "Urbano",
    "urbanizacao": "Urbanização",
    "viagem": "Viagem",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def esc(value: Any) -> str:
    return html.escape(str("" if value is None else value), quote=True)


def truncate_at_word(value: Any, limit: int) -> str:
    """Limita texto em uma palavra completa, reservando espaço para reticências."""
    if limit <= 0:
        return ""
    text = re.sub(r"\s+", " ", str("" if value is None else value)).strip()
    if len(text) <= limit:
        return text
    if limit == 1:
        return "…"
    budget = limit - 1
    window = text[: budget + 1]
    if window[budget].isspace():
        shortened = window[:budget].rstrip()
    else:
        prefix = window[:budget]
        shortened = prefix.rsplit(" ", 1)[0].rstrip() if " " in prefix else ""
    shortened = shortened.rstrip(" ,;:—-")
    return f"{shortened}…" if shortened else "…"


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFD", value)
    ascii_value = "".join(c for c in normalized if unicodedata.category(c) != "Mn")
    return re.sub(r"(^-+|-+$)", "", re.sub(r"[^a-z0-9]+", "-", ascii_value.lower()))


def normalize(value: str) -> str:
    return slugify(value).replace("-", " ")


def category_label(value: str) -> str:
    return CATEGORY_LABELS.get(slugify(value), value)


def advertising_category(item: dict[str, Any], fallback: str = "geral") -> str:
    explicit = slugify(str(item.get("ad_category", "")))
    if explicit:
        return explicit
    if item.get("kind") == "competition":
        return "competicoes"
    if item.get("kind") == "event":
        return "eventos"
    topics = set(item.get("topics", []))
    for category in (
        "scooters", "eletricos", "bicicletas", "motos",
        "mobilidade", "tecnologia", "competicoes", "eventos",
    ):
        if category in topics:
            return category
    return fallback


def ad_override(item: dict[str, Any], fallback: str = "geral") -> str:
    return f' data-ad-category-override="{esc(advertising_category(item, fallback))}"'


def plain_excerpt(value: str, limit: int = 220) -> str:
    text = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", value)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"[*_`#>|]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return truncate_at_word(text, limit)


def iso_day(value: Any) -> str:
    match = re.search(r"\d{4}-\d{2}-\d{2}", str(value or ""))
    return match.group(0) if match else TODAY


def br_date(value: Any) -> str:
    """Formata datas para exibição pública brasileira sem alterar o dado técnico."""
    raw = str(value or "")
    match = re.search(r"(\d{4})-(\d{2})-(\d{2})", raw)
    if not match:
        return raw
    year, month, day = match.groups()
    return f"{day}/{month}/{year}"


def br_date_range(start: Any, end: Any = "") -> str:
    start_label = br_date(start)
    end_label = br_date(end)
    if not end_label or end_label == start_label:
        return start_label
    return f"{start_label} a {end_label}"


def format_visible_dates(value: Any) -> str:
    """Converte datas ISO em texto, preservando URLs, slugs e timestamps técnicos."""
    return re.sub(
        r"(?<![\w/-])(\d{4})-(\d{2})-(\d{2})(?![\w/-])",
        lambda match: f"{match.group(3)}/{match.group(2)}/{match.group(1)}",
        str(value or ""),
    )


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


def public_editorial_text(text: str) -> str:
    """Remove metadados e linguagem de auditoria do texto exibido ao público."""
    internal_sections = {
        "fontes cruzadas",
        "fonte e atualizacao",
        "fontes e atualizacao",
    }
    public_heading_names = {
        "situacao verificada": "Sobre o evento",
        "leitura visual complementar": "Informações adicionais",
    }
    kept: list[str] = []
    skipping_level: int | None = None
    for raw in str(text or "").splitlines():
        heading = re.match(r"^(#{2,6})\s+(.+?)\s*$", raw)
        if heading:
            level = len(heading.group(1))
            normalized_heading = normalize(heading.group(2))
            if skipping_level is not None:
                if level > skipping_level:
                    continue
                skipping_level = None
            if normalized_heading in internal_sections:
                skipping_level = level
                continue
            replacement = public_heading_names.get(normalized_heading)
            if replacement:
                raw = f"{heading.group(1)} {replacement}"
        elif skipping_level is not None:
            continue
        kept.append(raw)

    value = "\n".join(kept)
    replacements = (
        (
            r"As fontes consultadas ainda não publicaram um serviço completo com rua, número, horário, estacionamento e contato direto\.",
            "O serviço completo com rua, número, horário, estacionamento e contato direto ainda não foi divulgado.",
        ),
        (
            r"Essas ausências são mantidas de forma explícita para evitar informação inventada\.",
            "",
        ),
        (
            r"Quando o endereço não aparece de forma legível, a TVDUASRODAS mantém essa ausência explícita e não inventa rua, número ou CEP\.",
            "Rua, número e CEP ainda não foram divulgados.",
        ),
        (
            r"Os nomes e horários que não atingiram confiança suficiente no processamento visual não foram transformados em informação pública\.",
            "A programação completa ainda não foi divulgada.",
        ),
        (
            r"Não informado de forma legível no flyer consultado\.",
            "Ainda não informado pela organização.",
        ),
        (
            r"Não informado no flyer consultado\.",
            "Ainda não informado pela organização.",
        ),
        (
            r"Organização não identificada de forma legível no flyer consultado",
            "Organização ainda não divulgada",
        ),
        (
            r"Local detalhado não informado de forma legível no flyer",
            "Local ainda não divulgado",
        ),
        (
            r"Endereço detalhado não informado de forma legível no flyer",
            "Endereço ainda não divulgado",
        ),
        (
            r"O flyer foi inspecionado localmente;\s*serviços identificados:",
            "Informações divulgadas:",
        ),
        (
            r"mencionado no flyer",
            "divulgado pela organização",
        ),
        (
            r"Contato não identificado de forma legível no flyer\.",
            "Contato ainda não divulgado.",
        ),
        (
            r"Horário não informado de forma legível no flyer consultado\.",
            "Horário ainda não divulgado.",
        ),
        (r"Horários identificados no flyer:", "Horários divulgados:"),
        (r"Endereço detalhado não informado no flyer; referência:", "Referência de localização:"),
        (
            r"Gratuidade indicada no flyer; confira eventuais condições na arte original\.",
            "Entrada gratuita; confirme eventuais condições com a organização.",
        ),
        (r"Estrutura e atrações legíveis:", "Estrutura e atrações divulgadas:"),
        (r"Marcas de horário legíveis:", "Horários divulgados:"),
        (
            r"A arte foi relida visualmente, mas nenhum dado adicional atingiu confiança suficiente para substituir os campos conservadores\.",
            "",
        ),
        (
            r"A leitura automatizada foi usada como apoio; trechos ambíguos não foram publicados como fato\.",
            "",
        ),
        (r"\bEsta página registra\b", "Este registro preserva"),
        (r"\bleitura automatizada\b", "leitura preliminar do material"),
        (r"\bprocessamento visual\b", "análise do material publicado"),
        (r"\bFontes cruzadas\b", "Fontes públicas consultadas"),
        (r"\bfonte específica independente\b", "outra publicação específica"),
        (r"\bVerificação ainda aberta:\b", "Informações ainda pendentes:"),
        (r"buscas textual, ampliada e visual/social", "pesquisa em fontes públicas"),
        (r"\bLeitura visual complementar\b", "Informações adicionais"),
        (r"\bFonte e atualização\b", "Fontes e contexto"),
        (r"Use os links de fontes cruzadas abaixo", "Consulte as fontes públicas listadas ao fim da página"),
        (
            r"Canais impressos no material:[^.]*\.",
            "",
        ),
        (r"nos canais vinculados abaixo", "nos canais oficiais do evento"),
        (r"nas fontes vinculadas abaixo", "nos canais oficiais do evento"),
        (r"\bflyer consultado\b", "divulgação do evento"),
        (r"\bflyer\b", "divulgação do evento"),
    )
    for pattern, replacement in replacements:
        value = re.sub(pattern, replacement, value, flags=re.IGNORECASE)
    return format_visible_dates(re.sub(r"\n{3,}", "\n\n", value).strip())


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
    scripts: str = "",
    extra_styles: tuple[str, ...] = (),
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
  <script src="/assets/js/google-consent-defaults.js?v=20260823a"></script>
  <meta name="google-adsense-account" content="ca-pub-9006646182680550">
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9006646182680550" crossorigin="anonymous"></script>
  <title>{esc(title)} | TVDUASRODAS</title>
  <meta name="description" content="{esc(truncate_at_word(description, 160))}">
  <meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
  <link rel="canonical" href="{esc(canonical_url)}">
  <link rel="icon" href="/assets/img/logoTVicon_web.ico">
  <link rel="stylesheet" href="/assets/css/style.css?v=20260725responsive1">
{"".join(f'  <link rel="stylesheet" href="{esc(path)}">' for path in extra_styles)}
  <meta property="og:locale" content="pt_BR">
  <meta property="og:type" content="{esc(page_type)}">
  <meta property="og:site_name" content="TVDUASRODAS">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(truncate_at_word(description, 200))}">
  <meta property="og:url" content="{esc(canonical_url)}">
  <meta property="og:image" content="{esc(image_url)}">
  <meta name="twitter:card" content="summary_large_image">
  <base href="/">
  {json_ld(graph)}
</head>
<body class="page-internal seo-page">
  <header class="site-header">
    <div class="container header-inner">
      <div class="logo-wrapper"><a href="/index.html" class="logo-link"><img src="/assets/img/logotv.png" alt="TVDUASRODAS" class="logo-image"></a><div class="brand-sub">Motos · Bikes · Scooters · Elétricos</div></div>
      <nav class="main-nav" aria-label="Navegação principal"><ul>
        <li><a href="/index.html">Início</a></li><li><a href="/revista.html">Revista</a></li><li><a href="/tv.html">TV &amp; Vídeos</a></li>
        <li><a href="/competicoes-eventos.html">Competições &amp; Eventos</a></li><li><a href="/imprensa.html">Imprensa</a></li><li><a href="/contato.html">Contato &amp; Patrocínios</a></li>
      </ul></nav>
    </div>
  </header>
  <main class="section"><div class="container seo-container">{body}</div></main>
  <footer class="site-footer"><div class="container footer-inner"><div class="footer-left">
    <p>© TVDUASRODAS — conteúdo sobre o universo das duas rodas.</p>
    <p class="footer-small"><a href="/sobre">Sobre</a> · <a href="/equipe">Equipe</a> · <a href="/contato">Contato</a> · <a href="/politica-editorial">Política editorial</a> · <a href="/politica-de-correcoes">Correções</a> · <a href="/politica-de-privacidade">Privacidade</a> · <a href="/termos">Termos</a> · <a href="/sitemap.xml">Sitemap</a></p>
  </div></div></footer>
  <script src="/assets/js/ads.js?v=20260823a"></script>
{scripts}
</body>
</html>
"""


def write_page(path: str, content: str) -> None:
    target = ROOT / path.strip("/") / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    content = unicodedata.normalize("NFC", content)
    content = "".join(
        char for char in content
        if unicodedata.category(char) != "Cf"
    )
    if target.exists() and target.read_text(encoding="utf-8") == content:
        return
    target.write_text(content, encoding="utf-8", newline="\n")


def refresh_legacy_person_page(slug: str, name: str, related_url: str) -> None:
    """Keep historical athlete URLs complete, current and self-canonical."""
    target = ROOT / "atletas" / slug / "index.html"
    if not target.exists():
        raise FileNotFoundError(f"Página histórica de atleta ausente: {target}")
    content = target.read_text(encoding="utf-8")
    if "google-consent-defaults.js" not in content:
        scripts = (
            '  <script src="/assets/js/google-consent-defaults.js?v=20260823a"></script>\n'
            '  <meta name="google-adsense-account" content="ca-pub-9006646182680550">\n'
            '  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9006646182680550" crossorigin="anonymous"></script>\n'
        )
        content = re.sub(
            r'(<meta name="viewport"[^>]*>\s*)',
            lambda match: match.group(1) + scripts,
            content,
            count=1,
        )
    marker = 'id="registro-relacionado-legado"'
    if marker not in content:
        note = (
            '<aside class="seo-source" id="registro-relacionado-legado">'
            '<strong>Endereço histórico preservado</strong><p>Este endereço mantém a forma do nome '
            'usada em uma classificação publicada anteriormente. Ele continua público, indexável e '
            'autocanônico; a referência relacionada abaixo permite consultar a grafia atual ou a '
            f'competição de origem sem apagar este registro. <a href="{esc(related_url)}">'
            'Consultar o registro relacionado</a>.</p></aside>\n'
        )
        content = content.replace("</article></div></main>", note + "</article></div></main>", 1)
    trust_links = (
        '<p class="footer-small"><a href="/sobre">Sobre</a> · <a href="/equipe">Equipe</a> · '
        '<a href="/contato">Contato</a> · <a href="/politica-editorial">Política editorial</a> · '
        '<a href="/politica-de-correcoes">Correções</a> · '
        '<a href="/politica-de-privacidade">Privacidade</a> · <a href="/termos">Termos</a> · '
        '<a href="/sitemap.xml">Sitemap</a></p>'
    )
    content = re.sub(
        r'<p class="footer-small">.*?</p>',
        trust_links,
        content,
        count=1,
        flags=re.DOTALL,
    )
    content = re.sub(
        r'/assets/js/ads\.js\?v=[^"]+',
        '/assets/js/ads.js?v=20260823a',
        content,
    )
    target.write_text(unicodedata.normalize("NFC", content), encoding="utf-8", newline="\n")


def card(item: dict[str, Any]) -> str:
    eyebrow = item.get("kind_label", item.get("category", "Conteúdo"))
    image = item.get("image", "")
    needs_artwork_label = item.get("kind") in {"event", "competition"} and "competicoes-eventos-default" in image
    artwork_label = (
        f'<span class="seo-card__artwork-label"><small>TVDUASRODAS</small><strong>{esc(item["title"])}</strong></span>'
        if needs_artwork_label else ""
    )
    media = (
        f'<a class="seo-card__media" href="{esc(item["url"])}"><img src="{esc(image)}" '
        f'alt="{esc(item["title"])}" loading="lazy" decoding="async">{artwork_label}</a>'
        if image else ""
    )
    video_class = " seo-card--video" if item.get("kind") == "video" else ""
    return (
        f'<article class="seo-card{video_class}">{media}<div><span class="seo-eyebrow">{esc(eyebrow)}</span>'
        f'<h3><a href="{esc(item["url"])}">{esc(item["title"])}</a></h3>'
        f'<p>{esc(public_editorial_text(item.get("summary", "")))}</p></div></article>'
    )


def related_items(current: dict[str, Any], all_items: list[dict[str, Any]], limit: int = 6) -> list[dict[str, Any]]:
    base = current.get("_word_set") or words(current.get("search_text", ""))
    current_topics = current.get("_topic_set") or set(current.get("topics", []))
    current_brands = current.get("_brand_set") or set(current.get("brands", []))
    current_modalities = current.get("_modality_set") or {slug for slug, _ in current.get("modalities", [])}
    current_category = current.get("_category_normalized") or normalize(current.get("category", ""))
    scored: list[tuple[int, dict[str, Any]]] = []
    for item in all_items:
        if item["url"] == current["url"]:
            continue
        # Na TV, o formato faz parte do contexto: vídeo recomenda somente vídeo.
        if current.get("kind") == "video" and item.get("kind") != "video":
            continue
        shared_topics = (item.get("_topic_set") or set(item.get("topics", []))) & current_topics
        shared_brands = (item.get("_brand_set") or set(item.get("brands", []))) & current_brands
        shared_modalities = (item.get("_modality_set") or {slug for slug, _ in item.get("modalities", [])}) & current_modalities
        same_category = (
            (item.get("_category_normalized") or normalize(item.get("category", ""))) == current_category
            and bool(current.get("category"))
        )
        lexical = min(len(base & (item.get("_word_set") or words(item.get("search_text", "")))), 5)
        score = (
            lexical
            + 12 * len(shared_topics)
            + 8 * len(shared_brands)
            + 10 * len(shared_modalities)
            + (6 if same_category else 0)
        )
        # Evita relação baseada apenas em uma palavra genérica.
        if score >= 3:
            scored.append((score, item))
    return [
        item for _, item in sorted(
            scored,
            key=lambda pair: (-pair[0], pair[1].get("kind", ""), pair[1]["title"]),
        )[:limit]
    ]


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
        kind_labels = {
            "article": "Matérias relacionadas",
            "video": "Vídeos relacionados",
            "competition": "Competições relacionadas",
            "event": "Eventos relacionados",
            "guide": "Guias relacionados",
        }
        grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for value in related:
            grouped[value.get("kind", "article")].append(value)
        related_html = '<section class="seo-related"><h2>Conteúdos relacionados</h2>'
        for kind in ("video", "article", "competition", "event", "guide"):
            values = grouped.get(kind, [])
            if values:
                related_html += (
                    f'<section class="seo-related-group"><h3>{kind_labels[kind]}</h3>'
                    f'<div class="seo-grid">{"".join(card(value) for value in values)}</div></section>'
                )
        related_html += "</section>"
    return chips_html + related_html


def render_research_sources(data: dict[str, Any], *, fallback_url: str = "") -> str:
    """Render the public evidence trail without exposing internal workflow notes."""
    candidates = data.get("sources") if isinstance(data.get("sources"), list) else []
    candidates = [source for source in candidates if isinstance(source, dict)]
    for url, label in (
        (data.get("source_url"), data.get("source_label") or "Fonte do registro"),
        (fallback_url, "Página oficial"),
    ):
        if url:
            candidates.append({"url": url, "label": label, "supports": "identificação e informações públicas"})

    sources: list[dict[str, str]] = []
    seen: set[str] = set()
    for source in candidates:
        url = str(source.get("url") or "").strip()
        if not url.startswith(("https://", "http://")) or url in seen:
            continue
        seen.add(url)
        sources.append({
            "url": url,
            "label": public_editorial_text(str(source.get("label") or "Fonte pública consultada")),
            "supports": public_editorial_text(str(source.get("supports") or "")),
        })
        if len(sources) == 8:
            break

    checked = data.get("source_checked_at") or data.get("last_updated")
    checked_note = (
        f" <span>Consulta editorial: {esc(br_date(checked))}.</span>"
        if checked else ""
    )
    if not sources:
        return (
            '<section class="seo-sources"><h2>Fontes públicas consultadas</h2>'
            f'<p>A página registra somente os dados disponíveis no acervo editorial.{checked_note}</p></section>'
        )
    links = "".join(
        '<li><a href="{url}" target="_blank" rel="noopener noreferrer">{label}</a>{supports}</li>'.format(
            url=esc(source["url"]),
            label=esc(source["label"]),
            supports=(f' — confirma {esc(source["supports"])}' if source["supports"] else ""),
        )
        for source in sources
    )
    return (
        '<section class="seo-sources"><h2>Fontes públicas consultadas</h2>'
        f'<p>Links usados para conferir os fatos publicados nesta página.{checked_note}</p>'
        f'<ul>{links}</ul></section>'
    )


def render_verified_facts(data: dict[str, Any]) -> str:
    """Summarize only populated service fields already present in the record."""
    location = data.get("full_address") or data.get("street_address") or data.get("venue") or data.get("location")
    facts = [
        ("Data", br_date_range(data.get("start_date"), data.get("end_date"))),
        ("Horário divulgado", data.get("time_label") or data.get("local_start")),
        ("Local", location),
        ("Organização", data.get("organizer")),
        ("Acesso", data.get("admission_status")),
        ("Estacionamento", data.get("parking")),
        ("Contato público", data.get("contact")),
    ]
    placeholder = re.compile(r"a confirmar|ainda não|não informad|não divulgad|confirme com", re.I)
    rows = "".join(
        f'<div><dt>{esc(label)}</dt><dd>{esc(public_editorial_text(str(value)))}</dd></div>'
        for label, value in facts
        if value and not placeholder.search(str(value))
    )
    attractions = [
        public_editorial_text(str(value))
        for value in data.get("attractions", [])
        if str(value).strip()
    ][:8]
    attractions_html = (
        '<h3>Atrações ou atividades divulgadas</h3><ul>'
        + "".join(f"<li>{esc(value)}</li>" for value in attractions)
        + "</ul>"
        if attractions else ""
    )
    if not rows and not attractions_html:
        return ""
    return (
        '<section class="seo-verified"><h2>O que foi verificado</h2>'
        '<p>Resumo dos dados confirmados nas fontes públicas registradas no acervo editorial.</p>'
        f'<dl class="seo-facts">{rows}</dl>{attractions_html}</section>'
    )


def classify(item: dict[str, Any]) -> None:
    normalized = normalize(item.get("search_text", ""))
    # Reused when building hundreds of athlete pages. Caching it here avoids
    # normalizing the complete editorial corpus once per person.
    item["_normalized_search_text"] = normalized
    explicit_topics = item.pop("_explicit_topics", [])
    explicit_brands = item.pop("_explicit_brands", [])
    topics_defined = item.pop("_explicit_topics_defined", False)
    brands_defined = item.pop("_explicit_brands_defined", False)
    item["topics"] = explicit_topics if topics_defined else [
        slug for slug, (_, patterns) in TOPICS.items()
        if any(normalize(pattern) in normalized for pattern in patterns)
    ]
    item["brands"] = explicit_brands if brands_defined else [
        slug for slug, label in BRANDS.items()
        if normalize(slug) in normalized or normalize(label) in normalized
    ]
    item["_word_set"] = words(item.get("search_text", ""))
    item["_topic_set"] = set(item.get("topics", []))
    item["_brand_set"] = set(item.get("brands", []))
    item["_modality_set"] = {slug for slug, _ in item.get("modalities", [])}
    item["_category_normalized"] = normalize(item.get("category", ""))


def load_content() -> tuple[list[dict[str, Any]], dict[str, list[dict[str, Any]]]]:
    items: list[dict[str, Any]] = []
    people: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for path in sorted((ROOT / "content/news").glob("*.md")):
        meta, body = frontmatter(path)
        slug = path.stem
        title = meta.get("title", slug)
        summary = meta.get("summary") or plain_excerpt(body)
        item = {
            "kind": "article", "kind_label": "Matéria", "slug": slug, "title": title,
            "summary": summary, "body": body, "date": meta.get("date", TODAY),
            "updated_at": meta.get("updated_at") or meta.get("date", TODAY),
            "lastmod": iso_day(meta.get("updated_at") or meta.get("date")),
            "category": category_label(meta.get("category", "Revista")), "author": meta.get("author", "Redação TVDUASRODAS"),
            "ad_category": meta.get("ad_category", ""),
            "image": meta.get("cover", ""), "url": f"/materias/{slugify(slug)}/",
            "cover_credit": meta.get("coverCredit", ""),
            "cover_source": meta.get("coverSource", ""),
            "cover_license": meta.get("coverLicense", ""),
            "cover_type": meta.get("coverType", ""),
            "_explicit_topics": [
                value.strip() for value in str(meta.get("topics", "")).split(",")
                if value.strip() in TOPICS
            ],
            "_explicit_topics_defined": "topics" in meta,
            "_explicit_brands": [
                value.strip() for value in str(meta.get("brands", "")).split(",")
                if value.strip() in BRANDS
            ],
            "_explicit_brands_defined": "brands" in meta,
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
            "summary": plain_excerpt(body), "body": body,
            "date": meta.get("date", TODAY), "lastmod": iso_day(meta.get("date")),
            "category": category_label(meta.get("category", "Vídeos")), "channel": meta.get("channel", ""),
            "ad_category": meta.get("ad_category", ""),
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
            "title": data.get("title", slug), "summary": format_visible_dates(data.get("summary", "")),
            "body": format_visible_dates(data.get("body", "")), "date": data.get("last_updated", TODAY),
            "lastmod": iso_day(data.get("last_updated")), "category": data.get("modality", "Competição"),
            "ad_category": data.get("ad_category", ""),
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
                "number": result.get("number", ""),
                "nationality": result.get("nationality", ""),
                "profile_url": result.get("profile_url", ""),
                "date": result.get("date") or data.get("last_updated", ""),
                "source_url": result.get("source_url") or data.get("results_url") or data.get("official_url", ""),
            })
        latest_result = data.get("latest_result") or {}
        for result in latest_result.get("classification", []):
            name = str(result.get("competitor", "")).strip()
            if not name:
                continue
            category = result.get("category") or latest_result.get("session", "")
            existing = people[normalize(name)]
            if any(record["competition"]["url"] == item["url"] and record["category"] == category for record in existing):
                continue
            existing.append({
                "name": name,
                "competition": item,
                "category": category,
                "position": result.get("display_position") or result.get("position", ""),
                "team": result.get("team", ""),
                "result": result.get("points") or result.get("time_gap", ""),
                "number": result.get("number", ""),
                "nationality": result.get("nationality", ""),
                "profile_url": result.get("profile_url", ""),
                "date": result.get("date") or latest_result.get("date") or data.get("last_updated", ""),
                "source_url": result.get("source_url") or data.get("results_url") or data.get("official_url", ""),
            })

    for path in sorted((ROOT / "content/events").glob("*.json")):
        if path.name in {"index.json", "agenda-comunitaria-2026.json"}:
            continue
        data = json.loads(read_text(path))
        slug = path.stem
        item = {
            "kind": "event", "kind_label": "Evento", "slug": slug,
            "title": data.get("title", slug), "summary": format_visible_dates(data.get("summary", "")),
            "body": format_visible_dates(data.get("body", "")), "date": data.get("start_date", TODAY),
            "lastmod": iso_day(data.get("last_updated") or data.get("start_date")),
            "category": data.get("event_type", "Evento"), "image": data.get("cover", ""),
            "ad_category": data.get("ad_category", ""),
            "url": f"/eventos/{slug}/", "data": data,
            "source_kind": "evento",
            "search_text": json.dumps(data, ensure_ascii=False),
        }
        items.append(item)

    community_path = ROOT / "content/events/agenda-comunitaria-2026.json"
    if community_path.exists():
        community = json.loads(read_text(community_path))
        existing_event_slugs = {item["slug"] for item in items if item["kind"] == "event"}
        for data in community.get("entries", []):
            slug = data.get("slug") or slugify(
                f"{data.get('title', '')}-{data.get('city', '')}-{data.get('state', '')}-{data.get('start_date', '')}"
            )
            if not slug or slug in existing_event_slugs:
                continue
            existing_event_slugs.add(slug)
            item = {
                "kind": "event", "kind_label": "Evento", "slug": slug,
                "title": data.get("title", slug), "summary": format_visible_dates(data.get("summary", "")),
                "body": format_visible_dates(data.get("body", "")), "date": data.get("start_date", TODAY),
                "lastmod": iso_day(data.get("last_updated") or data.get("start_date")),
                "category": data.get("event_type", "Evento"), "image": data.get("cover", ""),
                "ad_category": data.get("ad_category", ""),
                "url": f"/eventos/{slug}/", "data": data,
                "source_kind": "agenda",
                "search_text": json.dumps(data, ensure_ascii=False),
            }
            items.append(item)

    calendar = json.loads(read_text(ROOT / "content/calendar/cbm-2026.json"))
    existing = {item["slug"] for item in items if item["kind"] == "event"}
    for data in calendar.get("entries", []):
        if data.get("competition_slug"):
            continue
        derived_slug = slugify(f"{data.get('title', '')}-{data.get('start_date', '')}")
        primary_slug = str(data.get("slug") or derived_slug).strip()
        related_slugs = [
            str(value).strip() for value in data.get("related_slugs", [])
            if str(value).strip()
        ]
        for slug in dict.fromkeys([primary_slug, *related_slugs]):
            if not slug or slug in existing:
                continue
            existing.add(slug)
            modality = data.get("modality", "")
            event_data = dict(data)
            if slug != primary_slug:
                event_data["duplicate_of"] = primary_slug
            item = {
                "kind": "event", "kind_label": "Evento do calendário", "slug": slug,
                "title": event_data.get("title", slug),
                "summary": format_visible_dates(event_data.get("summary") or " · ".join(filter(None, (event_data.get("stage"), event_data.get("city"), event_data.get("state"))))),
                "body": format_visible_dates(event_data.get("body") or f"## Sobre a prova\n\n{event_data.get('title')} integra o calendário monitorado pela TVDUASRODAS. Consulte a fonte oficial para confirmar programação, inscrições e alterações."),
                "date": event_data.get("start_date", TODAY),
                "lastmod": iso_day(event_data.get("last_updated") or event_data.get("source_checked_at") or event_data.get("start_date")),
                "category": modality or "Evento",
                "image": event_data.get("cover") or "/assets/img/competicoes-eventos-default.svg",
                "url": f"/eventos/{slug}/", "data": event_data,
                "source_kind": "calendario",
                "modalities": [(slugify(modality), modality)] if modality else [],
                "search_text": json.dumps(event_data, ensure_ascii=False),
            }
            items.append(item)

    for path in sorted((ROOT / "content/articles").glob("*.json")):
        data = json.loads(read_text(path))
        slug = path.stem
        body_text = re.sub(r"<[^>]+>", " ", data.get("bodyHtml", ""))
        item = {
            "kind": "guide", "kind_label": "Guia", "slug": slug,
            "title": data.get("title", slug), "summary": format_visible_dates(data.get("summary", "")),
            "body_html": format_visible_dates(data.get("bodyHtml", "")), "date": data.get("date", TODAY),
            "lastmod": iso_day(data.get("date")), "category": data.get("category", "Guia"),
            "ad_category": data.get("ad_category", ""),
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
    image = item.get("image", "")
    article_schema = {
        "@type": "NewsArticle",
        "@id": f"{absolute_url(canonical)}#artigo",
        "headline": item["title"],
        "description": item["summary"],
        "datePublished": item["date"],
        "dateModified": item["updated_at"],
        "mainEntityOfPage": absolute_url(canonical),
        "author": {
            "@type": "Organization",
            "name": item["author"],
            "url": absolute_url("/equipe"),
        },
        "publisher": ORG,
        "articleSection": item["category"],
        "inLanguage": "pt-BR",
    }
    if image:
        article_schema["image"] = [absolute_url(image)]
    cover_caption_parts = []
    if item.get("cover_credit"):
        cover_caption_parts.append(esc(item["cover_credit"]))
    if item.get("cover_source"):
        cover_caption_parts.append(
            f'<a href="{esc(item["cover_source"])}" target="_blank" '
            'rel="noopener noreferrer">Fonte da imagem ↗</a>'
        )
    if item.get("cover_license"):
        cover_caption_parts.append(f'Licença: {esc(item["cover_license"])}')
    cover_caption = (
        f'<figcaption>{" · ".join(cover_caption_parts)}</figcaption>'
        if cover_caption_parts else ""
    )
    body = f"""
<nav class="seo-breadcrumb"><a href="/">Início</a> › <a href="/materias/">Matérias</a> › {esc(item["category"])}</nav>
<article class="seo-article">
  <header><span class="seo-eyebrow">{esc(item["category"])}</span><h1>{esc(item["title"])}</h1>
  <p class="seo-lead">{esc(item["summary"])}</p><p class="seo-meta">Por <a href="/equipe">{esc(item["author"])}</a> · {esc(br_date(item["date"]))}</p></header>
  {f'<figure class="seo-hero"><img src="{esc(image)}" alt="{esc(item["title"])}">{cover_caption}</figure>' if image else ""}
  <aside class="tdr-ad-slot" data-ad-slot="article-sidebar"{ad_override(item)} aria-label="Publicidade relacionada à matéria"></aside>
  <div class="seo-prose">{markdown(format_visible_dates(item["body"]))}</div>
  <aside class="tdr-ad-slot" data-ad-slot="article-inline"{ad_override(item)} aria-label="Banner relacionado à matéria"></aside>
  {relation_blocks(item, all_items)}
</article>"""
    return page_shell(
        title=item["title"], description=item["summary"], canonical=canonical, body=body,
        schemas=[article_schema, breadcrumb_schema([("Início", "/"), ("Matérias", "/materias/"), (item["title"], canonical)])],
        image=image or "/assets/img/logotv.png", page_type="article",
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
        "contentUrl": item["youtube"],
        "publisher": ORG,
        "inLanguage": "pt-BR",
    }
    if duration_iso(item.get("duration", "")):
        video_schema["duration"] = duration_iso(item["duration"])
    body = f"""
<nav class="seo-breadcrumb"><a href="/">Início</a> › <a href="/videos/">Vídeos</a> › {esc(item["category"])}</nav>
<article class="seo-article">
  <header><span class="seo-eyebrow">Vídeo · {esc(item["category"])}</span><h1>{esc(item["title"])}</h1>
  <p class="seo-lead">{esc(item["summary"])}</p><p class="seo-meta">{esc(item.get("channel"))} · {esc(br_date(item["date"]))}</p></header>
  <div class="seo-video"><iframe src="https://www.youtube.com/embed/{esc(item["video_id"])}" title="{esc(item["title"])}" allowfullscreen loading="eager"></iframe></div>
  <aside class="tdr-ad-slot" data-ad-slot="video-sidebar"{ad_override(item)} aria-label="Publicidade relacionada ao vídeo"></aside>
  <div class="seo-prose">{markdown(format_visible_dates(item["body"]))}</div>
  <aside class="tdr-ad-slot" data-ad-slot="video-inline"{ad_override(item)} aria-label="Banner relacionado ao vídeo"></aside>
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


def render_round_outcome(stage: dict[str, Any]) -> str:
    winner = str(stage.get("winner") or "").strip()
    if winner:
        return (
            '<span class="seo-result-status seo-result-status--resultado">'
            f'<span>Resultado</span><strong>{esc(winner)}</strong></span>'
        )
    status = str(stage.get("status") or "a confirmar").strip()
    status_key = slugify(status)
    labels = {
        "agendada": "Agendada",
        "proximo": "Próxima",
        "em-andamento": "Em andamento",
        "concluida": "Concluída",
        "encerrado": "Encerrada",
        "adiada": "Adiada",
        "cancelada": "Cancelada",
        "a-confirmar": "A confirmar",
    }
    return (
        f'<span class="seo-result-status seo-result-status--{esc(status_key)}">'
        f'{esc(labels.get(status_key, status.replace("_", " ").capitalize()))}</span>'
    )


def render_competition(
    item: dict[str, Any], all_items: list[dict[str, Any]], people: dict[str, list[dict[str, Any]]]
) -> str:
    data = item["data"]
    canonical = item["url"]
    standings = data.get("standings", [])
    standings_groups = []
    for category in dict.fromkeys(str(result.get("category") or "Geral") for result in standings):
        category_rows = []
        for result in [entry for entry in standings if str(entry.get("category") or "Geral") == category]:
            name = result.get("competitor", "")
            category_rows.append(
                f"<tr><td>{esc(result.get('display_position') or result.get('position'))}</td>"
                f'<td><a href="/atletas/{slugify(name)}/"><strong>{esc(name)}</strong></a></td>'
                f"<td>{esc(result.get('team'))}</td>"
                f"<td>{esc(result.get('points') if result.get('points') is not None else result.get('time_gap'))}</td></tr>"
            )
        standings_groups.append(
            f'<section class="seo-competition-block seo-standing-block">'
            f'<header><span class="seo-block-label">Classificação por categoria</span><h3>{esc(category)}</h3></header>'
            f'<div class="seo-table"><table><thead><tr><th>Pos.</th><th>Atleta/piloto</th>'
            f'<th>Equipe</th><th>Resultado</th></tr></thead><tbody>{"".join(category_rows)}</tbody></table></div>'
            f'</section>'
        )
    latest_result = data.get("latest_result") or {}
    latest_classification = latest_result.get("classification") or []
    latest_groups = []
    for category in dict.fromkeys(
        str(result.get("category") or latest_result.get("session") or "Geral")
        for result in latest_classification
    ):
        latest_rows = []
        for result in [
            entry for entry in latest_classification
            if str(entry.get("category") or latest_result.get("session") or "Geral") == category
        ]:
            name = result.get("competitor", "")
            latest_rows.append(
                f"<tr><td>{esc(result.get('display_position') or result.get('position'))}</td>"
                f'<td><a href="/atletas/{slugify(name)}/"><strong>{esc(name)}</strong></a></td>'
                f"<td>{esc(result.get('team'))}</td><td>{esc(result.get('time_gap'))}</td>"
                f"<td>{esc(result.get('points'))}</td></tr>"
            )
        latest_groups.append(
            f'<section class="seo-competition-block seo-result-block">'
            f'<header><span class="seo-block-label">Resultado da categoria</span><h3>{esc(category)}</h3></header>'
            f'<div class="seo-table"><table><thead><tr><th>Pos.</th><th>Atleta/piloto</th>'
            f'<th>Equipe</th><th>Tempo / diferença</th><th>Pontos</th></tr></thead>'
            f'<tbody>{"".join(latest_rows)}</tbody></table></div></section>'
        )
    rounds = "".join(
        f"<tr><td>{esc(stage.get('name'))}</td><td>{esc(br_date_range(stage.get('start_date'), stage.get('end_date')))}</td>"
        f"<td>{esc(stage.get('location'))}</td><td>{render_round_outcome(stage)}</td></tr>"
        for stage in data.get("rounds", [])
    )
    start = data.get("next_stage", {}).get("start_date") or (data.get("rounds") or [{}])[0].get("start_date")
    end = data.get("next_stage", {}).get("end_date") or start
    competition_dates = {**data, "start_date": start, "end_date": end or start}
    event_status = event_schema_status(competition_dates)
    if start:
        schema = {
            "@type": "SportsEvent",
            "@id": f"{absolute_url(canonical)}#competicao",
            "name": item["title"],
            "description": item["summary"],
            "startDate": start,
            "endDate": end or start,
            "image": [absolute_url(item["image"])],
            "url": absolute_url(canonical),
            "organizer": {
                "@type": "Organization",
                "name": data.get("organizer", ""),
                "url": data.get("official_url") or absolute_url(canonical),
            },
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
            "eventStatus": event_status,
        }
    else:
        # Uma temporada sem calendário confirmado não é um evento elegível para
        # resultado avançado. Não publicamos data nula nem inventamos uma data.
        schema = {
            "@type": "WebPage",
            "@id": f"{absolute_url(canonical)}#pagina",
            "name": item["title"],
            "description": item["summary"],
            "url": absolute_url(canonical),
            "image": [absolute_url(item["image"])],
            "about": {
                "@type": "Thing",
                "name": item["title"],
                "description": item["summary"],
            },
        }
    body = f"""
<nav class="seo-breadcrumb"><a href="/">Início</a> › <a href="/competicoes-eventos">Competições</a> › {esc(item["title"])}</nav>
<article class="seo-article">
  <header><span class="seo-eyebrow">{esc(data.get("modality"))} · Temporada {esc(data.get("season"))}</span>
  <h1>{esc(item["title"])}</h1><p class="seo-lead">{esc(item["summary"])}</p>
  <p class="seo-meta">Organização: {esc(data.get("organizer"))} · Atualizado em {esc(br_date(item["lastmod"]))}</p>
  </header>
  <aside class="tdr-ad-slot" data-ad-slot="detail-billboard" data-ad-category-override="competicoes" aria-label="Patrocínio da cobertura da competição"></aside>
  <figure class="seo-hero seo-artwork-hero"><img src="{esc(item["image"])}" alt="{esc(item["title"])}">{('<span class="seo-artwork-hero__label"><small>TVDUASRODAS · Competição</small><strong>' + esc(item["title"]) + '</strong></span>') if 'competicoes-eventos-default' in item["image"] else ''}<figcaption>{esc(data.get("image_credit"))}</figcaption></figure>
  <div class="seo-prose">{linked_markdown(public_editorial_text(item["body"]), people)}</div>
{('<section class="seo-competition-section" id="resultado-recente"><header><span class="seo-block-label">Resultado oficial mais recente</span><h2>' + esc(latest_result.get("event") or "Último resultado") + '</h2><p>' + esc(" · ".join(filter(None, [latest_result.get("session"), br_date(latest_result.get("date"))]))) + '</p></header><div class="seo-competition-stack">' + "".join(latest_groups) + '</div></section>') if latest_groups else ''}
  <section class="seo-competition-section" id="classificacao"><header><span class="seo-block-label">{esc(data.get("standings_eyebrow") or "Classificação oficial")}</span><h2>{esc(data.get("standings_title") or "Classificação do campeonato")}</h2></header>
  {('<div class="seo-competition-stack">' + ''.join(standings_groups) + '</div>') if standings_groups else '<div class="seo-competition-empty"><strong>Classificação aguardando publicação oficial.</strong><p>Os blocos de cada categoria serão incluídos após a divulgação da entidade organizadora.</p></div>'}
  </section>
  <section class="seo-competition-section" id="calendario"><header><span class="seo-block-label">Programação da temporada</span><h2>Etapas e calendário</h2></header>{('<div class="seo-competition-block"><div class="seo-table"><table><thead><tr><th>Etapa</th><th>Data</th><th>Local</th><th>Resultado/situação</th></tr></thead><tbody>' + rounds + '</tbody></table></div></div>') if rounds else '<div class="seo-competition-empty"><strong>Calendário em confirmação.</strong></div>'}</section>
  {render_research_sources(data, fallback_url=data.get("official_url", ""))}
  <div class="ce-actions"><a class="btn btn-primary" href="{esc(data.get("official_url"))}" target="_blank" rel="noopener">Visitar site oficial ↗</a>{('<a class="btn btn-outline" href="' + esc(data.get("results_url")) + '" target="_blank" rel="noopener">Resultados oficiais ↗</a>') if data.get("results_url") and data.get("results_url") != data.get("official_url") else ''}</div>
  {relation_blocks(item, all_items)}
</article>"""
    return page_shell(
        title=item["title"], description=item["summary"], canonical=canonical, body=body,
        schemas=[schema, breadcrumb_schema([("Início", "/"), ("Competições", "/competicoes-eventos"), (item["title"], canonical)])],
        image=item["image"],
        extra_styles=("/assets/css/competition-status.css?v=20260725a",),
    )


def render_event(item: dict[str, Any], all_items: list[dict[str, Any]]) -> str:
    data = item["data"]
    canonical = item["url"]
    public_summary = public_editorial_text(item["summary"])
    is_correction_record = data.get("schema_type") == "WebPage"
    location_name = public_editorial_text(
        data.get("venue") or data.get("location") or data.get("city") or "Local a confirmar"
    )
    street_address = public_editorial_text(data.get("street_address", ""))
    organizer = public_editorial_text(data.get("organizer", ""))
    organizer_is_known = bool(
        organizer
        and "ainda não" not in organizer.casefold()
        and "não divulgad" not in organizer.casefold()
    )
    event_status = event_schema_status(data)
    event_completed = event_status == "https://schema.org/EventCompleted"
    schema = {
        "@type": "Event",
        "@id": f"{absolute_url(canonical)}#evento",
        "name": item["title"],
        "description": public_summary,
        "startDate": data.get("local_start") or data.get("start_date"),
        "endDate": data.get("local_end") or data.get("end_date") or data.get("local_start") or data.get("start_date"),
        "eventStatus": event_status,
        "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
        "url": absolute_url(canonical),
        "image": [absolute_url(item["image"])],
        "location": {
            "@type": "Place", "name": location_name,
            "address": {
                "@type": "PostalAddress",
                "streetAddress": street_address,
                "addressLocality": data.get("city", ""),
                "addressRegion": data.get("state", ""),
                "postalCode": data.get("postal_code", ""),
                "addressCountry": data.get("country", "Brasil"),
            },
        },
    }
    if organizer_is_known:
        schema["organizer"] = {
            "@type": "Organization",
            "name": organizer,
            "url": data.get("organizer_url") or data.get("official_url") or absolute_url(canonical),
        }
    structured_offers = []
    for offer in data.get("offers", []):
        if event_completed or not isinstance(offer, dict) or offer.get("price") is None:
            continue
        structured_offer = {
            "@type": "Offer",
            "price": offer["price"],
            "priceCurrency": offer.get("price_currency") or "BRL",
            "availability": "https://schema.org/InStock",
            "url": offer.get("url") or data.get("ticket_url") or absolute_url(canonical),
        }
        if offer.get("name"):
            structured_offer["name"] = offer["name"]
        valid_from = offer_valid_from(data, offer, item["lastmod"])
        if valid_from:
            structured_offer["validFrom"] = valid_from
        structured_offers.append(structured_offer)
    if structured_offers:
        schema["offers"] = structured_offers
    elif data.get("free") is True and not event_completed:
        schema["offers"] = {
            "@type": "Offer",
            "price": 0,
            "priceCurrency": data.get("price_currency") or "BRL",
            "availability": "https://schema.org/InStock",
            "url": data.get("ticket_url") or data.get("official_url") or absolute_url(canonical),
            "validFrom": offer_valid_from(data, None, item["lastmod"]),
        }
    if is_correction_record:
        # This URL documents an unconfirmed legacy claim. Publishing Event
        # structured data here would falsely tell search engines it is scheduled.
        schema = {
            "@type": "WebPage",
            "@id": f"{absolute_url(canonical)}#pagina",
            "name": item["title"],
            "description": public_summary,
            "url": absolute_url(canonical),
            "inLanguage": "pt-BR",
            "isPartOf": {"@id": f"{BASE_URL}/#website"},
        }
    source_label = {
        "agenda_comunitaria": "Ver divulgação do evento ↗",
        "flyer_inspecionado_visual": "Ver divulgação do evento ↗",
    }.get(data.get("verification_status"), "Visitar site oficial do evento ↗")
    if is_correction_record:
        source_label = "Consultar portal turístico municipal ↗"
    relations = relation_blocks(item, all_items)
    time_label = public_editorial_text(data.get("time_label") or "Horário ainda não divulgado")
    full_address = public_editorial_text(
        data.get("full_address")
        or " · ".join(filter(None, (location_name, data.get("city"), data.get("state"))))
    )
    admission = public_editorial_text(
        data.get("admission_status")
        or ("Entrada gratuita" if data.get("free") else "Confirme com a organização")
    )
    parking = public_editorial_text(data.get("parking") or "Ainda não informado pela organização")
    if is_correction_record:
        service_html = (
            '<section class="seo-service">'
            '<div><span>Situação do registro</span><strong>Evento de 2026 não confirmado</strong>'
            '<small>URL histórica preservada e indexável</small></div>'
            f'<div><span>Local citado no cadastro antigo</span><strong>{esc(location_name)}</strong>'
            f'<small>{esc(" · ".join(filter(None, (data.get("city"), data.get("state")))))}</small></div>'
            '<div><span>Data no endereço antigo</span><strong>Não usar como confirmação</strong>'
            '<small>A data do slug faz parte do registro legado, não de uma divulgação verificada.</small></div>'
            '<div><span>Orientação</span><strong>Consulte as fontes e a nota de correção</strong></div>'
            '</section>'
        )
    else:
        service_html = (
            '<section class="seo-service">'
            f'<div><span>Data e horário</span><strong>{esc(br_date_range(data.get("start_date"), data.get("end_date")))}</strong><small>{esc(time_label)}</small></div>'
            f'<div><span>Endereço</span><strong>{esc(location_name)}</strong><small>{esc(full_address)}</small></div>'
            f'<div><span>Acesso</span><strong>{esc(admission)}</strong></div>'
            f'<div><span>Estacionamento</span><strong>{esc(parking)}</strong></div>'
            + (f'<div><span>Organização</span><strong>{esc(organizer)}</strong></div>' if organizer_is_known else '')
            + '</section>'
        )
    related_records: list[str] = []
    duplicate_slug = str(data.get("duplicate_of") or "").strip()
    if duplicate_slug:
        duplicate_url = f"/eventos/{duplicate_slug}/"
        related_records.append(
            '<p>Esta página preserva a grafia e as informações do registro recebido '
            'na agenda. O cadastro editorial também o relaciona a outro registro do '
            'mesmo anúncio; esse vínculo permite comparar os dados e não significa '
            'que tenham ocorrido dois eventos distintos. '
            f'<a href="{esc(duplicate_url)}">Consultar o registro de evento relacionado</a>.</p>'
        )
    competition_slug = (
        str(data.get("competition_slug") or "").strip()
        if data.get("reclassified_as") == "competition"
        else ""
    )
    if competition_slug:
        competition_url = f"/competicoes/{competition_slug}/"
        related_records.append(
            '<p>Este registro preserva a grafia e as informações recebidas na agenda '
            'comunitária. Ele também está ligado ao calendário esportivo indicado '
            'abaixo; o vínculo apresenta o contexto da competição e não representa '
            'um segundo evento. '
            f'<a href="{esc(competition_url)}">Consultar o calendário relacionado</a>.</p>'
        )
    related_record_section = (
        '<section class="seo-source" id="registro-relacionado">'
        '<h2>Registro relacionado</h2>'
        + "".join(related_records)
        + "</section>"
        if related_records
        else ""
    )
    official_url = str(data.get("official_url") or "").strip()
    if is_correction_record:
        lifecycle_note = (
            '<aside class="seo-source"><strong>Registro histórico de correção — página preservada</strong>'
            '<p>Esta URL permanece pública, indexável, autocanônica e presente nos sitemaps. '
            'A redação não localizou divulgação específica que confirme o evento indicado no '
            'cadastro antigo; por isso, a página documenta o conflito sem inventar programação, '
            'local, organização ou realização.</p></aside>'
        )
    elif event_completed:
        lifecycle_note = (
        '<aside class="seo-source"><strong>Evento encerrado — página preservada</strong>'
        '<p>Esta URL continua pública, indexável e disponível no sitemap como registro '
        'histórico. A página pode receber resultados, fotos, vídeos e atualizações '
        'publicadas após o evento.</p></aside>'
        )
    else:
        verification_link = (
            f'<a href="{esc(official_url)}" target="_blank" rel="noopener noreferrer">Consulte a organização do evento</a>.'
            if official_url
            else 'Consulte as fontes públicas listadas nesta página antes do deslocamento.'
        )
        lifecycle_note = (
            '<aside class="seo-source"><strong>Confirme antes de ir</strong><p>Programação, '
            f'endereço e regras podem mudar. {verification_link}</p></aside>'
        )
    source_cta = (
        f'<div class="ce-actions"><a class="btn btn-primary" href="{esc(official_url)}" target="_blank" rel="noopener">{esc(source_label)}</a></div>'
        if official_url
        else ""
    )
    body = f"""
<nav class="seo-breadcrumb"><a href="/">Início</a> › <a href="/competicoes-eventos">Eventos</a> › {esc(item["title"])}</nav>
<article class="seo-article">
  <header><span class="seo-eyebrow">{esc(item["category"])}</span><h1>{esc(item["title"])}</h1>
  <p class="seo-lead">{esc(public_summary)}</p>
  {('<div class="ce-actions"><a class="btn btn-outline" href="' + esc(data.get("ticket_url")) + '" target="_blank" rel="noopener">Ingressos / acesso ↗</a></div>') if data.get("ticket_url") and data.get("ticket_url") != data.get("official_url") else ''}</header>
  <aside class="tdr-ad-slot" data-ad-slot="detail-billboard" data-ad-category-override="eventos" aria-label="Patrocínio da cobertura do evento"></aside>
  <figure class="seo-hero seo-artwork-hero"><img src="{esc(item["image"])}" alt="{esc(item["title"])}">{('<span class="seo-artwork-hero__label"><small>TVDUASRODAS · Evento</small><strong>' + esc(item["title"]) + '</strong></span>') if 'competicoes-eventos-default' in item["image"] else ''}<figcaption>{esc(data.get("image_credit"))}</figcaption></figure>
  {service_html}
  {render_verified_facts(data)}
  <div class="seo-prose">{markdown(public_editorial_text(item["body"]))}</div>
  {related_record_section}
  {lifecycle_note}
  {render_research_sources(data, fallback_url=("" if is_correction_record else data.get("official_url", "")))}
  {source_cta}
  {relations}
</article>"""
    body = "\n".join(line.rstrip() for line in body.splitlines())
    return page_shell(
        title=item["title"], description=public_summary, canonical=canonical, body=body,
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
<div class="seo-ad-pair">
  <aside class="tdr-ad-slot" data-ad-slot="article-sidebar"{ad_override(item)} aria-label="Publicidade lateral relacionada ao guia"></aside>
  <aside class="tdr-ad-slot" data-ad-slot="article-inline"{ad_override(item)} aria-label="Banner relacionado ao guia"></aside>
</div>
<div class="seo-prose">{item.get("body_html", "")}</div>{relation_blocks(item, all_items)}</article>"""
    return page_shell(
        title=item["title"], description=item["summary"], canonical=canonical, body=body,
        schemas=[schema, breadcrumb_schema([("Início", "/"), ("Arquivo", "/arquivo.html"), (item["title"], canonical)])],
        image=item["image"], page_type="article",
    )


def render_person(name: str, records: list[dict[str, Any]], all_items: list[dict[str, Any]]) -> tuple[str, str]:
    slug = slugify(name)
    canonical = f"/atletas/{slug}/"
    normalized_name = normalize(name)
    mentioned = [
        item for item in all_items
        if normalized_name in item.get("_normalized_search_text", "")
    ]
    first = max(
        records,
        key=lambda record: sum(
            bool(record.get(field))
            for field in ("number", "nationality", "profile_url", "team", "position", "result")
        ),
    )
    competition_name = first["competition"]["title"]
    category = first.get("category", "")
    position = first.get("position", "")
    team = first.get("team", "")
    description = (
        f"{name}: classificação, equipe e resultados no {competition_name}. "
        f"Veja a posição na {category}, a pontuação publicada e as fontes oficiais."
    )
    competition_count = len({record["competition"]["url"] for record in records})
    categories = sorted({str(record.get("category") or "").strip() for record in records if record.get("category")})
    teams = sorted({str(record.get("team") or "").strip() for record in records if record.get("team")})
    record_summary = (
        f"O acervo reúne {len(records)} registro(s) em {competition_count} competição(ões), "
        f"com {len(categories)} categoria(s) e {len(teams)} equipe(s) identificada(s)."
    )
    rows = "".join(
        f'<tr><td><a href="{esc(record["competition"]["url"])}">{esc(record["competition"]["title"])}</a></td>'
        f'<td>{esc(record["category"])}</td><td><strong>{esc(record["position"])}</strong></td>'
        f'<td>{esc(record["team"])}</td><td>{esc(record["result"])}</td>'
        f'<td>{esc(br_date(record.get("date")))}</td>'
        f'<td>{("<a href=\"" + esc(record["source_url"]) + "\" target=\"_blank\" rel=\"noopener noreferrer\">Fonte oficial ↗</a>") if record.get("source_url") else "—"}</td></tr>'
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
            "nationality": first.get("nationality") or None,
            "sameAs": [first["profile_url"]] if first.get("profile_url") else None,
            "identifier": str(first["number"]) if first.get("number") else None,
        },
        "isPartOf": {"@id": f"{BASE_URL}/#website"},
        "inLanguage": "pt-BR",
    }
    for optional_key in ("affiliation", "nationality", "sameAs", "identifier"):
        if schema["mainEntity"].get(optional_key) is None:
            del schema["mainEntity"][optional_key]
    facts = "".join(
        (
            f"<div><span>{esc(label)}</span><strong>{esc(value)}</strong></div>"
            for label, value in (
                ("Número", first.get("number")),
                ("Nacionalidade", first.get("nationality")),
                ("Categoria", category),
                ("Equipe", team),
                ("Classificação", position),
            )
            if value not in (None, "")
        )
    )
    official_profile = (
        f'<div class="ce-actions"><a class="btn btn-outline" href="{esc(first["profile_url"])}" '
        'target="_blank" rel="noopener noreferrer">Ver perfil no MX1 GP Brasil ↗</a></div>'
        if first.get("profile_url") else ""
    )
    body = f"""
<nav class="seo-breadcrumb"><a href="/">Início</a> › <a href="/atletas/">Atletas e pilotos</a> › {esc(name)}</nav>
<article class="seo-article"><header><span class="seo-eyebrow">Atleta ou piloto em resultados publicados</span>
<h1>{esc(name)}</h1><p class="seo-lead">{esc(description)}</p><p>{esc(record_summary)}</p>{official_profile}</header>
{f'<section class="seo-service seo-athlete-facts">{facts}</section>' if facts else ""}
<section><h2>Resultados de {esc(name)}</h2><div class="seo-table"><table>
<thead><tr><th>Competição</th><th>Categoria</th><th>Posição</th><th>Equipe</th><th>Resultado</th><th>Data de referência</th><th>Fonte</th></tr></thead><tbody>{rows}</tbody></table></div></section>
{f'<section><h2>Matérias e páginas relacionadas</h2><div class="seo-grid">{cards}</div></section>' if cards else ""}
<aside class="seo-source"><strong>Sobre esta página</strong><p>Esta é uma página de referência editorial baseada nas classificações publicadas pelas entidades e organizadores. Não é um perfil oficial da pessoa.</p></aside>
</article>"""
    return canonical, page_shell(
        title=f"{name}: resultados e classificações", description=description, canonical=canonical, body=body,
        schemas=[schema, breadcrumb_schema([("Início", "/"), ("Atletas", "/atletas/"), (name, canonical)])],
    )


def render_people_index(collection: list[dict[str, Any]]) -> str:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in sorted(collection, key=lambda value: normalize(value["title"])):
        initial = normalize(item["title"])[:1].upper() or "#"
        groups[initial].append(item)
    alphabet = "".join(
        f'<a href="/atletas/#{esc(initial)}">{esc(initial)}</a>'
        for initial in groups
    )
    sections = "".join(
        f'<section id="{esc(initial)}"><h2>{esc(initial)}</h2><p>{len(items)} nome(s) com resultados publicados.</p>'
        f'<div class="seo-grid">{"".join(card(item) for item in items)}</div></section>'
        for initial, items in groups.items()
    )
    description = (
        "Índice alfabético de atletas e pilotos citados em classificações oficiais "
        "publicadas pela TVDUASRODAS."
    )
    body = f"""
<nav class="seo-breadcrumb"><a href="/">Início</a> › Atletas e pilotos</nav>
<header class="seo-collection-header"><span class="seo-eyebrow">Resultados documentados</span><h1>Atletas e pilotos</h1>
<p class="seo-lead">{esc(description)}</p>
<p>Este índice reúne {len(collection)} nomes. Cada perfil agrega todas as posições, categorias, equipes, datas de referência, competições e links de fonte disponíveis no acervo.</p>
<p>Os nomes são organizados alfabeticamente para facilitar a consulta. As páginas são referências editoriais baseadas em resultados publicados por entidades e organizadores; não são perfis oficiais dos competidores.</p></header>
<nav class="seo-relations" aria-label="Navegação alfabética">{alphabet}</nav>{sections}"""
    schema = {
        "@type": "CollectionPage",
        "@id": f"{BASE_URL}/atletas/#colecao",
        "name": "Atletas e pilotos",
        "description": description,
        "url": f"{BASE_URL}/atletas/",
        "hasPart": [
            {"@type": "Person", "name": item["title"], "url": absolute_url(item["url"])}
            for item in collection
        ],
        "inLanguage": "pt-BR",
    }
    return page_shell(
        title="Atletas e pilotos",
        description=description,
        canonical="/atletas/",
        body=body,
        schemas=[schema, breadcrumb_schema([("Início", "/"), ("Atletas e pilotos", "/atletas/")])],
    )


def render_collection(
    *, label: str, description: str, canonical: str, collection: list[dict[str, Any]],
    breadcrumb_parent: tuple[str, str] | None = None,
) -> str:
    ordered = sorted(collection, key=lambda x: (x.get("lastmod", ""), x["title"]), reverse=True)
    cards = "".join(card(item) for item in ordered)
    lead_ad = (
        '<aside class="tdr-ad-slot" data-ad-slot="article-inline" aria-label="Publicidade entre as matérias"></aside>'
        if canonical == "/materias/" else ""
    )
    closing_ad = (
        '<aside class="tdr-ad-slot" data-ad-slot="article-sidebar" aria-label="Publicidade após as matérias"></aside>'
        if canonical == "/materias/" else ""
    )
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
    kinds: dict[str, int] = defaultdict(int)
    for item in collection:
        kinds[str(item.get("kind_label") or item.get("kind") or "Conteúdo")] += 1
    breakdown = ", ".join(
        f"{count} {kind.lower()}" for kind, count in sorted(kinds.items())
    )
    dates = sorted({str(item.get("lastmod") or "") for item in collection if item.get("lastmod")})
    date_note = (
        f" O período documentado vai de {br_date(dates[0])} a {br_date(dates[-1])}."
        if dates else ""
    )
    context = (
        '<section class="seo-collection-context"><h2>Sobre esta coleção</h2>'
        f'<p>Esta página reúne {len(collection)} item(ns) do acervo público'
        f'{(" — " + esc(breakdown)) if breakdown else ""}.{esc(date_note)}</p>'
        '<p>Os cards apontam para páginas canônicas com contexto, data e relações editoriais. '
        'A coleção é atualizada quando novas matérias, vídeos, eventos, competições ou guias são publicados.</p></section>'
    )
    body = f"""
<nav class="seo-breadcrumb">{" › ".join(f'<a href="{url}">{esc(name)}</a>' for name, url in crumbs[:-1])} › {esc(label)}</nav>
<header class="seo-collection-header"><span class="seo-eyebrow">TVDUASRODAS</span><h1>{esc(label)}</h1><p class="seo-lead">{esc(description)}</p></header>
{context}{lead_ad}<div class="seo-grid">{cards or '<p>Nenhum conteúdo publicado nesta coleção.</p>'}</div>{closing_ad}"""
    return page_shell(
        title=label, description=description, canonical=canonical, body=body,
        schemas=[schema, breadcrumb_schema(crumbs)],
    )


def render_video_collection(collection: list[dict[str, Any]]) -> str:
    videos = sorted(
        (item for item in collection if item.get("video_id")),
        key=lambda item: (item.get("lastmod", ""), item["title"]),
        reverse=True,
    )
    description = (
        "Player central e catálogo de vídeos da TVDUASRODAS sobre motos, bicicletas, "
        "competições, tecnologia e mobilidade."
    )
    if not videos:
        return render_collection(
            label="TV & Vídeos", description=description, canonical="/videos/", collection=[]
        )

    current = videos[0]
    category_pairs = sorted({
        (slugify(video.get("category", "outros")) or "outros", video.get("category", "Outros"))
        for video in videos
    })
    filters = ['<button class="video-hub-filter is-active" type="button" data-filter="all">Todos</button>']
    filters.extend(
        f'<button class="video-hub-filter" type="button" data-filter="{esc(slug)}">{esc(label)}</button>'
        for slug, label in category_pairs
    )
    cards = []
    for video in videos:
        category_slug = slugify(video.get("category", "outros")) or "outros"
        cards.append(
            f'<article class="seo-card seo-card--video video-hub-card" '
            f'data-category="{esc(category_slug)}" data-video-id="{esc(video["video_id"])}" '
            f'data-video-title="{esc(video["title"])}">'
            f'<a class="seo-card__media" href="{esc(video["url"])}" '
            f'aria-label="Reproduzir {esc(video["title"])} no player principal">'
            f'<img src="{esc(video["image"])}" alt="{esc(video["title"])}" loading="lazy" decoding="async"></a>'
            f'<div><span class="seo-eyebrow">Vídeo · {esc(video.get("category", "Vídeos"))}</span>'
            f'<h3><a href="{esc(video["url"])}">{esc(video["title"])}</a></h3>'
            f'<p>{esc(video.get("summary", ""))}</p></div></article>'
        )

    body = f"""
<nav class="seo-breadcrumb"><a href="/">Início</a> › TV &amp; Vídeos</nav>
<header class="seo-collection-header video-hub-heading"><span class="seo-eyebrow">TVDUASRODAS</span>
<h1>TV &amp; Vídeos</h1><p class="seo-lead">{esc(description)}</p></header>
<div class="video-hub-feature">
  <section class="video-hub-player" aria-labelledby="videoHubTitle">
    <div class="video-hub-player__label"><span>Agora no player</span><strong id="videoHubTitle">{esc(current["title"])}</strong></div>
    <div class="seo-video"><iframe id="videoHubPlayer" src="https://www.youtube.com/embed/{esc(current["video_id"])}"
    title="{esc(current["title"])}" allowfullscreen loading="eager"></iframe></div>
  </section>
  <section class="video-hub-programming" aria-labelledby="videoProgrammingTitle">
    <header class="video-hub-programming__header"><span class="seo-eyebrow">Programação TVDUASRODAS</span>
      <h2 id="videoProgrammingTitle">Grade de programação</h2>
      <p>Programas recorrentes do canal e suas reportagens relacionadas.</p>
    </header>
    <div class="video-hub-programming__grid">
      <a class="video-hub-program-card" href="/revista?programa=role-de-rua"><span>Segundas e quintas</span><strong>Rolê de Rua</strong><p>Rotas urbanas, encontros e cultura sobre duas rodas.</p></a>
      <a class="video-hub-program-card" href="/revista?programa=garage-tech"><span>Quartas</span><strong>Garage Tech</strong><p>Manutenção, oficina, equipamentos e tecnologia.</p></a>
      <a class="video-hub-program-card" href="/revista?programa=estrada-aberta"><span>Sábados</span><strong>Estrada Aberta</strong><p>Viagens, planejamento, segurança e experiências na estrada.</p></a>
      <a class="video-hub-program-card" href="/revista?programa=electric-zone"><span>Domingos</span><strong>Electric Zone</strong><p>Mobilidade elétrica, bicicletas, scooters e inovação.</p></a>
    </div>
  </section>
</div>
<div class="video-hub-ad"><span class="video-hub-ad__label">Publicidade</span>
  <aside class="tdr-ad-slot" data-ad-slot="video-inline" data-ad-category-override="geral"
  aria-label="Publicidade contextual da TV"></aside>
</div>
<section class="video-hub-library" aria-labelledby="videoLibraryTitle">
  <header><span class="seo-eyebrow">Somente vídeos</span><h2 id="videoLibraryTitle">Escolha por categoria</h2>
  <p>Selecione uma categoria e clique em um vídeo para reproduzi-lo no player principal.</p></header>
  <div class="video-hub-filters" aria-label="Categorias de vídeos">{"".join(filters)}</div>
  <div class="seo-grid video-hub-grid">{"".join(cards)}</div>
  <p class="video-hub-empty" hidden>Nenhum vídeo encontrado nesta categoria.</p>
</section>"""
    schema = {
        "@type": "CollectionPage",
        "@id": f"{BASE_URL}/videos/#colecao",
        "name": "TV & Vídeos",
        "description": description,
        "url": f"{BASE_URL}/videos/",
        "mainEntity": {
            "@type": "ItemList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": position,
                    "name": video["title"],
                    "url": absolute_url(video["url"]),
                }
                for position, video in enumerate(videos, 1)
            ],
        },
        "inLanguage": "pt-BR",
    }
    scripts = """<script>
(() => {
  const player = document.getElementById("videoHubPlayer");
  const title = document.getElementById("videoHubTitle");
  const cards = [...document.querySelectorAll(".video-hub-card")];
  const filters = [...document.querySelectorAll(".video-hub-filter")];
  const empty = document.querySelector(".video-hub-empty");
  const play = (card, autoplay = true) => {
    if (!card || !player) return;
    const id = card.dataset.videoId;
    const label = card.dataset.videoTitle || "Vídeo TVDUASRODAS";
    player.src = `https://www.youtube.com/embed/${id}${autoplay ? "?autoplay=1" : ""}`;
    player.title = label;
    if (title) title.textContent = label;
    cards.forEach((item) => item.classList.toggle("is-playing", item === card));
    window.TVAds?.setContext({ type: "video", title: label, category: card.dataset.category });
    document.querySelector(".video-hub-player")?.scrollIntoView({ behavior: "smooth", block: "start" });
  };
  filters.forEach((button) => button.addEventListener("click", () => {
    const category = button.dataset.filter;
    let visible = 0;
    filters.forEach((item) => item.classList.toggle("is-active", item === button));
    cards.forEach((card) => {
      const show = category === "all" || card.dataset.category === category;
      card.hidden = !show;
      if (show) visible += 1;
    });
    if (empty) empty.hidden = visible !== 0;
  }));
  cards.forEach((card) => card.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", (event) => {
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      play(card);
    });
  }));
  const requested = new URLSearchParams(location.search).get("v");
  const initial = cards.find((card) => card.dataset.videoId === requested) || cards[0];
  if (initial) {
    initial.classList.add("is-playing");
    window.TVAds?.setContext({
      type: "video",
      title: initial.dataset.videoTitle,
      category: initial.dataset.category
    });
  }
})();
</script>"""
    return page_shell(
        title="TV & Vídeos",
        description=description,
        canonical="/videos/",
        body=body,
        schemas=[schema, breadcrumb_schema([("Início", "/"), ("TV & Vídeos", "/videos/")])],
        image=current["image"],
        page_type="website",
        scripts=scripts,
    )


def segmented_archive_section(
    label: str,
    collection: list[dict[str, Any]],
    *,
    batch_size: int = 60,
) -> str:
    ordered = sorted(collection, key=lambda item: (item.get("lastmod", ""), item["title"]), reverse=True)
    chunks = [ordered[index:index + batch_size] for index in range(0, len(ordered), batch_size)] or [[]]
    groups = "".join(
        f'<section class="seo-archive-group"><h3>Bloco {number} de {len(chunks)}</h3>'
        f'<div class="seo-grid">{"".join(card(item) for item in chunk)}</div></section>'
        for number, chunk in enumerate(chunks, 1)
    )
    return (
        f'<section class="seo-archive-section"><h2>{esc(label)} <small>({len(collection)})</small></h2>'
        f'<p>Conteúdo segmentado em {len(chunks)} bloco(s) para facilitar navegação e leitura sem retirar nenhuma URL do acervo.</p>'
        f'{groups}</section>'
    )


def write_event_research_queue(items: list[dict[str, Any]]) -> None:
    audits = []
    for item in items:
        if item.get("kind") != "event":
            continue
        audit = evaluate_source_depth(item.get("source_kind", "evento"), item["slug"], item["data"])
        audits.append({
            "url": item["url"],
            "slug": item["slug"],
            "title": item["title"],
            "source_kind": item.get("source_kind", "evento"),
            "lastmod": item["lastmod"],
            "complete": audit["complete"],
            "missing": audit["missing"],
            "source_count": audit["source_count"],
            "specific_independent_domains": audit["specific_independent_domains"],
        })
    queue = [item for item in audits if not item["complete"]]
    report = {
        "generated_at": TODAY,
        "purpose": "Fila editorial para aprofundar eventos já publicados sem retirar URLs do ar.",
        "total_public_event_pages": len(audits),
        "complete_records": len(audits) - len(queue),
        "incomplete_records": len(queue),
        "queue": sorted(queue, key=lambda item: (len(item["missing"]), item["title"])),
    }
    target = ROOT / "editorial" / "review" / "eventos-incompletos.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def build(only_slugs: set[str] | None = None) -> None:
    items, people = load_content()
    write_event_research_queue(items)
    manifest: list[dict[str, Any]] = []
    full_build = not only_slugs

    for item in items:
        if full_build or item["slug"] in only_slugs:
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
    current_person_urls: set[str] = set()
    for _, records in sorted(people.items(), key=lambda pair: pair[1][0]["name"]):
        name = records[0]["name"]
        canonical = f"/atletas/{slugify(name)}/"
        selected_person = full_build or any(
            record["competition"]["slug"] in (only_slugs or set()) for record in records
        )
        if selected_person:
            canonical, output = render_person(name, records, items)
            write_page(canonical, output)
        current_person_urls.add(canonical)
        person_item = {
            "title": name, "url": canonical, "summary": f"{len(records)} resultado(s) publicado(s)",
            "kind_label": "Atleta ou piloto", "search_text": name,
        }
        person_index.append(person_item)
        manifest.append({"url": canonical, "lastmod": max(r["competition"]["lastmod"] for r in records), "priority": "0.6", "kind": "person"})

    for slug, (name, related_url) in LEGACY_PERSON_PAGES.items():
        canonical = f"/atletas/{slug}/"
        if canonical in current_person_urls:
            continue
        if full_build:
            refresh_legacy_person_page(slug, name, related_url)
        person_index.append({
            "title": name,
            "url": canonical,
            "summary": "Registro histórico de classificação preservado, com vínculo para a grafia atual ou para a competição de origem.",
            "kind_label": "Atleta ou piloto — registro histórico",
            "search_text": name,
        })
        manifest.append({"url": canonical, "lastmod": TODAY, "priority": "0.6", "kind": "person"})

    video_items = [i for i in items if i["kind"] == "video"]
    if full_build:
        write_page("/videos/", render_video_collection(video_items))
    manifest.append({"url": "/videos/", "lastmod": TODAY, "priority": "0.9", "kind": "index"})

    article_items = [i for i in items if i["kind"] == "article"]
    write_page("/materias/", render_collection(
        label="Matérias",
        description="Notícias, testes, lançamentos, viagens, mobilidade e cultura sobre duas rodas.",
        canonical="/materias/",
        collection=article_items,
    ))
    manifest.append({"url": "/materias/", "lastmod": TODAY, "priority": "0.9", "kind": "index"})

    indexes = [
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
        output = (
            render_people_index(collection)
            if canonical == "/atletas/"
            else render_collection(label=label, description=description, canonical=canonical, collection=collection)
        )
        write_page(canonical, output)
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
        if full_build:
            write_page(canonical, render_collection(label=data["label"], description=description, canonical=canonical, collection=data["items"], breadcrumb_parent=("Modalidades", "/modalidades/")))
        manifest.append({"url": canonical, "lastmod": max(i["lastmod"] for i in data["items"]), "priority": "0.7", "kind": "modality"})

    archive_collections = (
        ("Matérias", [i for i in items if i["kind"] == "article"]),
        ("Vídeos", [i for i in items if i["kind"] == "video"]),
        ("Competições", [i for i in items if i["kind"] == "competition"]),
        ("Eventos", [i for i in items if i["kind"] == "event"]),
        ("Guias", [i for i in items if i["kind"] == "guide"]),
    )
    archive_body = f"""
<header class="seo-collection-header"><span class="seo-eyebrow">Índice editorial</span><h1>Arquivo completo da TVDUASRODAS</h1>
<p class="seo-lead">Acesso rastreável a {len(items)} matérias, vídeos, guias, competições e eventos, além dos índices de atletas, marcas, assuntos e modalidades.</p>
<p>Todo o acervo público continua representado no manifesto e nos sitemaps. Nesta página, os links são agrupados por tipo e segmentados em blocos menores para tornar a consulta mais clara.</p>
<nav class="seo-relations" aria-label="Índices especializados"><a href="/materias/">Matérias</a><a href="/videos/">Vídeos</a><a href="/atletas/">Atletas</a><a href="/assuntos/">Assuntos</a><a href="/marcas/">Marcas</a><a href="/modalidades/">Modalidades</a></nav></header>
""" + "".join(
        segmented_archive_section(label, collection)
        for label, collection in archive_collections
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
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--only",
        action="append",
        default=[],
        metavar="SLUG",
        help="Renderiza apenas o conteúdo informado e atualiza índices e manifesto.",
    )
    args = parser.parse_args()
    build(set(args.only))
