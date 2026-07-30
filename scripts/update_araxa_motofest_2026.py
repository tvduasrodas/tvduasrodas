#!/usr/bin/env python3
"""Completa o serviço do 23º 100 Destino Motofest de Araxá."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENDA = ROOT / "content/events/agenda-comunitaria-2026.json"
CANONICAL_SLUG = "motofest-araxa-mg-2026-08-28"


def main() -> int:
    document = json.loads(AGENDA.read_text(encoding="utf-8"))
    event = next(
        entry for entry in document.get("entries", [])
        if entry.get("slug") == CANONICAL_SLUG
    )

    event.update(
        {
            "title": "23º 100 Destino Motofest",
            "short_name": "100 Destino Motofest",
            "start_date": "2026-08-28",
            "end_date": "2026-08-30",
            "city": "Araxá",
            "state": "MG",
            "country": "Brasil",
            "scope": "Nacional",
            "region": "Sudeste",
            "venue": "Praça Lago Norte do Barreiro",
            "status": "agendada",
            "event_type": "Encontro de motociclistas e festival de rock",
            "segment": "Motos",
            "official_url": "https://www.instagram.com/p/DbJlW4zIPyo/",
            "source_url": "https://www.instagram.com/p/DbJlW4zIPyo/",
            "source_label": "Publicação oficial do 100 Destino Motofest",
            "verification_status": "programacao_oficial_inspecionada_e_fontes_cruzadas",
            "cover": "/assets/img/uploads/araxa-motofest-2026-artwork.svg",
            "image_credit": "Arte: TVDUASRODAS",
            "featured": False,
            "free": True,
            "summary": (
                "O 23º 100 Destino Motofest acontece de 28 a 30 de agosto de "
                "2026, na Praça Lago Norte do Barreiro, em Araxá/MG. A "
                "programação oficial reúne 12 apresentações de rock; uma agenda "
                "especializada informa entrada gratuita, sujeita a reconfirmação "
                "com a organização."
            ),
            "attractions": [
                "Krusty",
                "Battery Metallica Sinfônico, de Uberlândia",
                "Nirvana Tributo, de Belo Horizonte",
                "Niobium",
                "Aeropeppers",
                "Latitude 19",
                "Big Jackers",
                "Beatles 4Ever, de São Paulo",
                "Power of Peppers — tributo a Red Hot Chili Peppers, de São Paulo",
                "Vinith",
                "Maivma Jamma",
                "Peixe Piloto",
                "Encontro de motociclistas e motoclubes",
            ],
            "body": (
                "## Serviço confirmado\n\n"
                "O **23º 100 Destino Motofest** será realizado de **sexta-feira, "
                "28 de agosto, a domingo, 30 de agosto de 2026**, na **Praça Lago "
                "Norte do Barreiro**, em Araxá/MG. O evento é realizado pelo "
                "**Moto Clube 100 Destino**, com patrocínio máster da Prefeitura "
                "de Araxá.\n\n"
                "As datas também constam no calendário oficial de eventos 2026 "
                "do município. A programação cultural publicada pelo organizador "
                "prevê 12 apresentações ao longo dos três dias.\n\n"
                "## Programação de sexta-feira — 28 de agosto\n\n"
                "- **19h:** abertura\n"
                "- **20h:** Krusty\n"
                "- **22h:** Battery Metallica Sinfônico, de Uberlândia\n"
                "- **23h30:** Nirvana Tributo, de Belo Horizonte\n\n"
                "## Programação de sábado — 29 de agosto\n\n"
                "- **12h:** Niobium\n"
                "- **14h:** Aeropeppers\n"
                "- **16h:** Latitude 19\n"
                "- **19h:** Big Jackers\n"
                "- **21h:** Beatles 4Ever, de São Paulo\n"
                "- **23h30:** Power of Peppers — tributo a Red Hot Chili Peppers, "
                "de São Paulo\n\n"
                "## Programação de domingo — 30 de agosto\n\n"
                "- **12h:** Vinith\n"
                "- **14h:** Maivma Jamma\n"
                "- **16h:** Peixe Piloto\n\n"
                "## Entrada, estacionamento e camping\n\n"
                "A agenda mineira Rodas de Prata identifica o encontro como **sem "
                "cobrança de entrada**. Como a publicação oficial consultada não "
                "detalha essa condição, recomendamos confirmar a gratuidade com a "
                "organização perto da data.\n\n"
                "Não foram divulgadas regras específicas de estacionamento, "
                "camping, credenciamento de motoclubes ou acesso de veículos à "
                "praça. Esses serviços permanecem explicitamente como não "
                "informados.\n\n"
                "## Canal oficial\n\n"
                "Acompanhe o perfil "
                "[@100destinomotofest](https://www.instagram.com/100destinomotofest/) "
                "para avisos, mudanças de horários e orientações de acesso. Antes "
                "de viajar, reconfirme a programação e as condições de entrada."
            ),
            "last_updated": "2026-07-30",
            "timezone": "America/Sao_Paulo",
            "local_start": "2026-08-28T19:00:00-03:00",
            "local_end": "2026-08-30T17:00:00-03:00",
            "time_label": (
                "Sexta a partir das 19h; sábado e domingo a partir das 12h"
            ),
            "street_address": "Praça Lago Norte do Barreiro",
            "neighborhood": "Barreiro",
            "full_address": "Praça Lago Norte do Barreiro, Barreiro, Araxá - MG",
            "status_basis": (
                "Datas, edição, local e programação confirmados na publicação "
                "oficial do organizador; período também confirmado no calendário "
                "oficial da Prefeitura de Araxá."
            ),
            "status_checked_at": "2026-07-30",
            "organizer": "Moto Clube 100 Destino",
            "support": ["Prefeitura de Araxá — patrocínio máster"],
            "contact": "Instagram: @100destinomotofest",
            "source_checked_at": "2026-07-30",
            "visual_verification": {
                "type": "carrossel_oficial_inspecionado_manualmente",
                "source_url": "https://www.instagram.com/p/DbJlW4zIPyo/",
                "checked_at": "2026-07-30",
                "review_policy": (
                    "Leitura manual da legenda e das lâminas de programação, com "
                    "transcrição conservadora dos nomes e horários publicados"
                ),
                "confirmed_fields": [
                    "edition",
                    "start_date",
                    "end_date",
                    "city",
                    "state",
                    "venue",
                    "organizer",
                    "lineup",
                    "show_times",
                ],
            },
            "admission_status": (
                "Entrada gratuita segundo a agenda Rodas de Prata; confirme com "
                "a organização perto da data"
            ),
            "parking": "Não informado na publicação oficial consultada",
            "sources": [
                {
                    "url": "https://www.instagram.com/p/DbJlW4zIPyo/",
                    "label": (
                        "100 Destino Motofest — programação oficial da 23ª edição"
                    ),
                    "type": "fonte primária do organizador",
                    "supports": (
                        "edição, datas, local, realização, atrações e horários"
                    ),
                    "checked_at": "2026-07-30",
                },
                {
                    "url": (
                        "https://araxa.mg.gov.br/noticia/8658/"
                        "calend-rio-de-eventos-2026-promete-impulsionar-o-turismo-em-arax-"
                    ),
                    "label": "Prefeitura de Araxá — calendário oficial de 2026",
                    "type": "fonte institucional pública",
                    "supports": "realização do Moto Fest de 28 a 30 de agosto",
                    "checked_at": "2026-07-30",
                },
                {
                    "url": "https://www.rodasdeprata.com.br/agenda/",
                    "label": "Rodas de Prata — agenda de encontros de Minas Gerais",
                    "type": "agenda independente especializada",
                    "supports": (
                        "23ª edição, datas, cidade, organizador e indicação de "
                        "entrada gratuita"
                    ),
                    "checked_at": "2026-07-30",
                },
                {
                    "url": (
                        "https://jb-rider.com.br/evento/"
                        "20260828-3-motofest-araxa-mg"
                    ),
                    "label": "JB-RIDER — Motofest Araxá/MG",
                    "type": "agenda independente com página específica",
                    "supports": "datas, cidade, estado e identidade do evento",
                    "checked_at": "2026-07-30",
                },
            ],
            "research_status": {
                "required_specific_independent_sources": 2,
                "specific_independent_domains_found": 4,
                "status": "fonte_primaria_e_fontes_oficiais_cruzadas",
                "query": '"23º 100 Destino Motofest" Araxá 2026',
                "reviewed_at": "2026-07-30",
                "editorial_rule": (
                    "Programação transcrita do canal oficial; gratuidade atribuída "
                    "à agenda especializada e marcada para reconfirmação; camping "
                    "e estacionamento não presumidos."
                ),
            },
        }
    )

    AGENDA.write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"Evento atualizado: {CANONICAL_SLUG}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
