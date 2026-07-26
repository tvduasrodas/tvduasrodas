#!/usr/bin/env python3
"""Cruza páginas específicas do Motociclistas Unidos com a agenda comunitária."""

from __future__ import annotations

import html
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
AGENDA = ROOT / "content" / "events" / "agenda-comunitaria-2026.json"
INDEX_URL = "https://motociclistasunidos.com.br/eventos-geral/"
NOW = datetime.now(timezone.utc).isoformat()

# Correspondências confirmadas por data, município e identidade do evento.
URL_TO_SLUGS = {
    "https://motociclistasunidos.com.br/evento/capital-moto-week-2026/": [
        "capital-moto-week-brasilia-df-2026-07-23",
    ],
    "https://motociclistasunidos.com.br/evento/50a-missa-dos-motociclistas-de-sao-jose-do-rio-preto-sp/": [
        "50-missa-dos-motociclistas-sao-jose-do-rio-preto-sp-2026-07-26",
    ],
    "https://motociclistasunidos.com.br/evento/aniversariantes-do-mes-cavaleiros-do-asfalto-brasil-mc/": [
        "cavaleiros-do-asfalto-sao-paulo-sp-2026-07-26",
    ],
    "https://motociclistasunidos.com.br/evento/moto-show-tres-lagoas/": [
        "motoshow-tres-lagoas-ms-2026-07-31",
        "motoshow-2026-tres-lagoas-ms-2026-07-31",
    ],
    "https://motociclistasunidos.com.br/evento/2-encontro-nacional-de-motociclistas-na-menor-cidade-do-brasil/": [
        "2-encontro-nacional-serra-da-saudade-mg-2026-07-31",
    ],
    "https://motociclistasunidos.com.br/evento/moto-rock/": [
        "motorock-lavras-mg-2026-08-01",
    ],
    "https://motociclistasunidos.com.br/evento/motofest-uberaba/": [
        "motofest-uberaba-mg-2026-08-07",
    ],
    "https://motociclistasunidos.com.br/evento/22o-aniversario-santa-custom-moto-clube/": [
        "santa-custom-mc-franca-sp-2026-08-15",
    ],
    "https://motociclistasunidos.com.br/evento/1o-stl-so-para-loucos-motorock/": [
        "mg-stl-so-para-loucos-sao-thome-das-letras-mg-2026-09-04",
    ],
    "https://motociclistasunidos.com.br/evento/11-anos-kurupira-nao-me-siga-mc-pirassununga/": [
        "kurupira-mc-pirassununga-sp-2026-09-12",
    ],
    "https://motociclistasunidos.com.br/evento/5o-encuentro-internacional-amigos-de-ruta/": [
        "amigos-de-ruta-foz-do-iguacu-pr-2026-09-17",
    ],
    "https://motociclistasunidos.com.br/evento/5o-encontro-de-motociclistas-triciclistas-e-carros-antigos-de-poloni-sp/": [
        "moto-amigos-mg-poloni-sp-2026-09-19",
        "motofest-poloni-sp-2026-09-19",
    ],
    "https://motociclistasunidos.com.br/evento/5o-encontro-de-motociclistas-triciclistas-e-carros-antigos/": [
        "moto-amigos-mg-poloni-sp-2026-09-19",
        "motofest-poloni-sp-2026-09-19",
    ],
    "https://motociclistasunidos.com.br/evento/4o-motofest-resende-encontro-de-motociclistas/": [
        "4-motofest-resende-rj-2026-09-20",
        "motofest-resende-rj-2026-09-20",
    ],
    "https://motociclistasunidos.com.br/evento/encontro-nacional-de-motociclistas-de-lavras/": [
        "7-encontro-de-motociclistas-lavras-mg-2026-09-25",
    ],
    "https://motociclistasunidos.com.br/evento/2o-bora-rock-fest-12-anos-bohemios-moto-clube/": [
        "bohemios-mc-boraceia-sp-2026-09-25",
    ],
    "https://motociclistasunidos.com.br/evento/2o-encontro-de-motociclistas-de-corrego-do-bom-jesus/": [
        "lendario-mc-corrego-do-bom-jesus-mg-2026-11-13",
        "4-encontro-de-motociclistas-corrego-do-bom-jesus-mg-2026-11-13",
    ],
    "https://motociclistasunidos.com.br/evento/21o-guaranhuns-motorcycle-2026/": [
        "21-guaranhuns-garanhuns-pe-2026-11-27",
        "motofest-garanhuns-pe-2026-11-27",
        "mc-guaras-do-asfalto-garanhuns-pe-2026-11-27",
    ],
    "https://motociclistasunidos.com.br/evento/aniversario-de-26-anos-asas-ao-vento-mc/": [
        "asas-ao-vento-mc-braganca-paulista-sp-2026-12-04",
    ],
}


def fetch_index() -> str:
    request = Request(INDEX_URL, headers={"User-Agent": "TVDUASRODAS editorial audit/1.0"})
    with urlopen(request, timeout=45) as response:
        return response.read().decode("utf-8", errors="replace")


def visible_text(value: str) -> str:
    value = re.sub(r"<!--.*?-->", " ", value or "", flags=re.S)
    value = re.sub(r"<br\s*/?>", "\n", value, flags=re.I)
    value = re.sub(r"</(?:p|li|ul|ol)>", "\n", value, flags=re.I)
    value = re.sub(r"<[^>]+>", " ", value)
    value = html.unescape(value)
    return re.sub(r"[ \t]+", " ", re.sub(r"\n+", "\n", value)).strip()


def parse_events(raw: str) -> dict[str, dict]:
    result: dict[str, dict] = {}
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', raw, re.S):
        try:
            event = json.loads(html.unescape(block))
        except (json.JSONDecodeError, TypeError):
            continue
        if event.get("@type") == "Event" and event.get("url"):
            result[str(event["url"])] = event
    return result


def merge_sources(existing: list, incoming: dict) -> list:
    by_url = {
        str(source.get("url", "")).rstrip("/"): source
        for source in existing
        if isinstance(source, dict) and source.get("url")
    }
    by_url[str(incoming["url"]).rstrip("/")] = incoming
    return list(by_url.values())


def main() -> int:
    events = parse_events(fetch_index())
    agenda = json.loads(AGENDA.read_text(encoding="utf-8-sig"))
    by_slug = {entry["slug"]: entry for entry in agenda["entries"]}
    changed = 0
    missing_urls: list[str] = []

    for url, slugs in URL_TO_SLUGS.items():
        event = events.get(url)
        if not event:
            missing_urls.append(url)
            continue
        locations = event.get("location") or []
        location = locations[0] if isinstance(locations, list) and locations else locations
        location = location if isinstance(location, dict) else {}
        address = location.get("address") or {}
        address = address if isinstance(address, dict) else {}
        description = visible_text(str(event.get("description") or ""))
        start = str(event.get("startDate") or "")
        end = str(event.get("endDate") or "")
        time_match = re.search(r"T(\d{2}):(\d{2})", start)

        for slug in slugs:
            entry = by_slug.get(slug)
            if not entry:
                continue
            if location.get("name"):
                entry["venue"] = location["name"]
            if address.get("streetAddress"):
                entry["street_address"] = address["streetAddress"]
                entry["full_address"] = address["streetAddress"]
            if time_match:
                entry["time_label"] = (
                    f"Início às {int(time_match.group(1))}h"
                    + (time_match.group(2) if time_match.group(2) != "00" else "")
                    + "; confira a programação detalhada com a organização"
                )
            if re.match(r"\d{4}-\d{1,2}-\d{1,2}", end):
                y, m, d = map(int, re.match(r"(\d{4})-(\d{1,2})-(\d{1,2})", end).groups())
                entry["end_date"] = f"{y:04d}-{m:02d}-{d:02d}"
            if description:
                body = str(entry.get("body") or "").rstrip()
                body = re.sub(
                    r"\n*## Dados adicionais do Motociclistas Unidos\n.*?(?=\n## |\Z)",
                    "",
                    body,
                    flags=re.S,
                ).rstrip()
                entry["body"] = (
                    body
                    + "\n\n## Dados adicionais do Motociclistas Unidos\n\n"
                    + description
                )
            source = {
                "url": url,
                "label": f"Motociclistas Unidos — {event.get('name', 'página específica do evento')}",
                "type": "agenda independente com página específica e dados estruturados",
                "supports": "datas, horário, local, endereço e informações de serviço descritas na página",
                "checked_at": NOW,
                "discovery_method": "cruzamento_multifonte_por_data_cidade_e_identidade",
            }
            entry["sources"] = merge_sources(list(entry.get("sources") or []), source)
            entry["source_checked_at"] = NOW
            entry["last_updated"] = NOW
            changed += 1

    agenda["last_updated"] = NOW
    AGENDA.write_text(json.dumps(agenda, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"records_changed": changed, "missing_urls": missing_urls}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
