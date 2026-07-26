#!/usr/bin/env python3
"""Remove resultados de busca genéricos associados ao evento errado.

Fontes estruturadas e fontes revisadas manualmente não são alteradas. Para uma
fonte descoberta pela busca editorial, a cidade e a identidade específica do
evento precisam aparecer juntas; perfis oficiais também podem ser validados
por dois termos distintivos do organizador.
"""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
AGENDA = ROOT / "content/events/agenda-comunitaria-2026.json"
GENERIC = {
    "1o", "2o", "3o", "4o", "5o", "6o", "7o", "8o", "9o",
    "ano", "anos", "aniversario", "brasil", "cafe", "clube", "dia",
    "encontro", "evento", "fest", "festa", "festival", "moto", "motociclista",
    "motociclistas", "motoclube", "motoclubes", "motofest", "motorock",
    "nacional", "passeio", "rock", "show", "solidario", "triciclistas",
    "da", "das", "de", "do", "dos", "e", "em", "na", "no",
    "ac", "al", "am", "ap", "ba", "ce", "df", "es", "go", "ma", "mg",
    "ms", "mt", "pa", "pb", "pe", "pi", "pr", "rj", "rn", "ro", "rr",
    "rs", "sc", "se", "sp", "to",
}

# Resultados inspecionados e confirmados como homônimos de outros setores,
# outras cidades ou outros eventos.
FALSE_POSITIVE_URLS = {
    "https://www.facebook.com/novoamanhaonline",
    "https://www.facebook.com/radiocidadelimeirafm/videos/novo-amanha/710689803784545",
    "https://www.wikiloc.com/trails/motorcycling/brazil/minas-gerais/pouso-alegre",
    "https://www.wikiloc.com/trails/cycling/brazil/minas-gerais/pouso-alegre",
    "https://uaisummit.com.br/",
    "https://www.mg.gov.br/instituicao_unidade/uai-uberaba-unidade-de-atendimento-integrado",
    "https://motofestbrasil.com.br/motofest/forca-acao-manobras-radicais-serra-es",
    "https://motofestbrasil.com.br/motofest/corvos-mc-7-anos-ss-campina-grande-pb",
    "https://motofestbrasil.com.br/motofest/sextou-do-motociclista-garanhuns-pe",
    "https://motofestbrasil.com.br/motofest/sexta-aberta-cruz-de-ferro-mc-subsede-macae-rj",
    "https://eventostop.com.br/eventos/1o-encontro-anual-de-carros-antigos-de-sao-fidelis-2026",
    "https://www.guicheweb.com.br/festa-julina-beneficente-de-sorocaba--henrique-e-juliano_52341",
    "https://www.globgov.com/BR/Maric%C3%A1/129103857184759/Ponta-Negra-RJ",
    "https://www.facebook.com/ComunidadePontaNegraMaricaRj",
    "https://www.pontanegranoticias.com.br/",
    "https://www.facebook.com/PontaNegraDoAlto/videos/ponta-negra-maric%C3%A1-rj-2026-/2394865927617298",
    "https://www.instagram.com/pontanegra.marica",
    "https://www.facebook.com/pontanegra.mariica",
}


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFKD", value or "")
    value = value.encode("ascii", "ignore").decode("ascii").lower()
    return re.sub(r"[^a-z0-9]+", " ", unquote(value)).strip()


def tokens(value: str) -> set[str]:
    return {
        token for token in normalize(value).split()
        if len(token) >= 3 and token not in GENERIC
    }


def source_is_specific(entry: dict, source: dict) -> bool:
    haystack = normalize(f"{source.get('label', '')} {source.get('url', '')}")
    raw_url = unquote(source.get("url", "")).lower()
    url = normalize(raw_url)
    haystack_tokens = set(haystack.split())
    city_tokens = tokens(entry.get("city", ""))
    title_tokens = tokens(entry.get("title", "")) - city_tokens
    organizer_tokens = tokens(entry.get("organizer", "")) - city_tokens

    city_match = bool(city_tokens) and city_tokens.issubset(haystack_tokens)
    identity = title_tokens | organizer_tokens
    identity_hits = identity & haystack_tokens

    # Título/organizador distintivo e cidade: padrão para páginas do evento.
    strong_identity_hits = {
        token for token in identity_hits
        if len(token) >= 5
    }
    if city_match and (
        len(identity_hits) >= 2 or bool(strong_identity_hits)
    ):
        return True

    # Diretórios editoriais usam páginas individuais cujo slug traz a cidade,
    # mesmo quando o nome do evento é totalmente genérico.
    event_directories = (
        "mototour.com.br", "motofestbrasil.com.br", "firesoulswebradio.com",
        "motociclistasunidos.com.br", "jacaremoto.com.br", "motoclub.run",
        "sympla.com.br", "ingressolink.com.br",
    )
    if city_match and any(domain in raw_url for domain in event_directories):
        if any(marker in url for marker in (" evento ", " eventos ", " motofest ")):
            return True

    # Se a cidade já faz parte do nome do evento, todos os seus termos ainda
    # precisam estar presentes e a página deve indicar o ano/edição atual.
    if city_match and not identity and (
        "2026" in haystack_tokens or entry.get("start_date", "") in haystack
    ):
        return True

    # Um perfil oficial pode não repetir a cidade, mas precisa identificar o
    # organizador com pelo menos dois termos não genéricos.
    source_type = normalize(source.get("type", ""))
    official_channel = (
        "fonte primaria" in source_type
        or "canal oficial" in source_type
        or "instagram.com" in haystack
        or "facebook.com" in haystack
    )
    required = min(2, len(identity))
    if official_channel and required >= 2 and len(identity_hits) >= required:
        return True

    return False


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument(
        "--report", default="output/weak-indexed-sources.json"
    )
    args = parser.parse_args()

    document = json.loads(AGENDA.read_text(encoding="utf-8"))
    removed: list[dict] = []
    for entry in document.get("entries", []):
        kept = []
        for source in entry.get("sources", []):
            if source.get("url") in FALSE_POSITIVE_URLS:
                removed.append({
                    "slug": entry.get("slug"),
                    "title": entry.get("title"),
                    "city": entry.get("city"),
                    "source": source,
                })
                continue
            if (
                source.get("discovery_method") == "busca_editorial_indexada"
                and not source_is_specific(entry, source)
            ):
                removed.append({
                    "slug": entry.get("slug"),
                    "title": entry.get("title"),
                    "city": entry.get("city"),
                    "source": source,
                })
            else:
                kept.append(source)
        if args.apply:
            entry["sources"] = kept

    report = ROOT / args.report
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(
        json.dumps(removed, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    if args.apply:
        AGENDA.write_text(
            json.dumps(document, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    print(f"Fontes fracas identificadas: {len(removed)}; aplicar={args.apply}")


if __name__ == "__main__":
    main()
