#!/usr/bin/env python3
"""Atualiza o 13º Motocólatras Fest com fontes verificadas."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENDA = ROOT / "content/events/agenda-comunitaria-2026.json"
SLUG = "13-motocolatras-fest-araguari-mg-2026-08-21"


def main() -> int:
    document = json.loads(AGENDA.read_text(encoding="utf-8"))
    event = next(
        entry for entry in document.get("entries", []) if entry.get("slug") == SLUG
    )

    event.update(
        {
            "title": "13º Motocólatras Fest",
            "short_name": "13º Motocólatras Fest",
            "start_date": "2026-08-21",
            "end_date": "2026-08-22",
            "city": "Araguari",
            "state": "MG",
            "venue": "Palácio dos Ferroviários",
            "status": "agendada",
            "event_type": "Encontro de motociclistas e festival de rock",
            "official_url": "https://www.instagram.com/motocolatras/",
            "source_url": "https://www.instagram.com/motocolatras/reel/DaS5MKDu0zu/",
            "source_label": "Anúncio oficial do Motocólatras em colaboração com a FAEC",
            "verification_status": "servico_e_programacao_cruzados_com_anuncio_oficial",
            "cover": "/assets/img/competicoes-eventos-default.svg",
            "image_credit": "Arte: TVDUASRODAS",
            "free": False,
            "summary": (
                "O 13º Motocólatras Fest reúne motociclistas em 21 e 22 de agosto "
                "de 2026, no Palácio dos Ferroviários, em Araguari/MG, com nove "
                "bandas de rock, gincana, camping com chuveiro quente, food trucks, "
                "expositores e entrada solidária de 2 kg de alimentos."
            ),
            "attractions": [
                "Nove bandas de rock ao vivo",
                "Banda Hashtag",
                "Gincana motociclista",
                "Prova de marcha lenta",
                "Prova da salsicha",
                "Camping com chuveiro quente",
                "Café da manhã gratuito",
                "Food trucks",
                "Expositores",
                "Ação solidária com arrecadação de alimentos",
            ],
            "body": (
                "## O evento\n\n"
                "O **13º Motocólatras Fest** acontece na sexta-feira, 21 de agosto, "
                "e no sábado, 22 de agosto de 2026, no **Palácio dos Ferroviários**, "
                "em Araguari/MG. Realizado pelo MC Motocólatras, o encontro combina "
                "motociclismo, rock e arrecadação de alimentos em uma programação "
                "voltada também para famílias.\n\n"
                "O anúncio oficial confirma nove bandas de rock, food trucks, "
                "expositores e gincana motociclista com provas de marcha lenta e da "
                "salsicha. A organização também anuncia bebidas a preços acessíveis.\n\n"
                "## Programação de sexta-feira — 21 de agosto\n\n"
                "- **18h:** abertura do evento\n"
                "- **19h:** início dos shows\n"
                "- **Três bandas**, com apresentações previstas até 1h da madrugada\n\n"
                "## Programação de sábado — 22 de agosto\n\n"
                "- **8h:** tradicional café da manhã gratuito na Aramoto\n"
                "- **14h:** início dos shows\n"
                "- **Seis bandas**, com programação prevista até 2h da madrugada\n\n"
                "A programação totaliza nove bandas. A **Banda Hashtag**, com repertório "
                "de rock nacional e internacional, está entre as atrações anunciadas. "
                "A grade completa com nomes e horários individuais ainda está sendo "
                "divulgada no perfil do MC Motocólatras.\n\n"
                "## Camping e estrutura\n\n"
                "O serviço divulgado informa área de camping com chuveiro quente, "
                "café da manhã gratuito, bandas ao vivo, food trucks e expositores. "
                "Não foram publicadas regras detalhadas de acesso, capacidade ou "
                "reserva do camping; consulte a organização antes da viagem.\n\n"
                "## Entrada solidária\n\n"
                "A entrada será feita mediante a doação de **2 kg de alimentos não "
                "perecíveis**. A arrecadação integra o trabalho social desenvolvido "
                "pelo MC Motocólatras em Araguari.\n\n"
                "## Local e contato\n\n"
                "**Palácio dos Ferroviários — Praça Gaioso Neves, 129, bairro Goiás, "
                "Araguari/MG, CEP 38440-001.** Informações: "
                "[(34) 99186-8583](tel:+5534991868583), "
                "[motocolatrasaraguari@gmail.com](mailto:motocolatrasaraguari@gmail.com) "
                "ou [galbatheo@gmail.com](mailto:galbatheo@gmail.com).\n\n"
                "## Antes de viajar\n\n"
                "Acompanhe o perfil **@motocolatras** para conferir a relação final "
                "das bandas, horários individuais, orientações do camping e possíveis "
                "ajustes operacionais."
            ),
            "last_updated": "2026-07-30",
            "timezone": "America/Sao_Paulo",
            "time_label": (
                "Sexta a partir das 18h; sábado: café às 8h e shows a partir das 14h"
            ),
            "street_address": "Praça Gaioso Neves, 129",
            "postal_code": "38440-001",
            "full_address": (
                "Palácio dos Ferroviários, Praça Gaioso Neves, 129, bairro Goiás, "
                "Araguari - MG, CEP 38440-001, Brasil"
            ),
            "status_basis": (
                "Datas, local, atrações, estrutura e entrada confirmados no anúncio "
                "oficial e cruzados com serviço específico e agendas independentes."
            ),
            "status_checked_at": "2026-07-30",
            "organizer": "MC Motocólatras",
            "contact": (
                "(34) 99186-8583; motocolatrasaraguari@gmail.com; "
                "galbatheo@gmail.com"
            ),
            "source_checked_at": "2026-07-30",
            "visual_verification": {
                "type": "anuncio_e_publicacoes_oficiais_inspecionados_manualmente",
                "source_url": (
                    "https://www.instagram.com/motocolatras/reel/DaS5MKDu0zu/"
                ),
                "detail_url": (
                    "https://jacaremoto.com.br/events/"
                    "13o-motocolatras-fest-araguari-mg/"
                ),
                "checked_at": "2026-07-30",
                "review_policy": (
                    "Leitura manual da publicação oficial, do perfil do organizador "
                    "e do serviço detalhado da Jacaré Moto"
                ),
                "confirmed_fields": [
                    "event_name",
                    "edition",
                    "date",
                    "city",
                    "state",
                    "venue",
                    "organizer",
                    "program",
                    "admission",
                    "services_and_attractions",
                    "contact",
                ],
            },
            "admission_status": (
                "Entrada solidária: doação de 2 kg de alimentos não perecíveis"
            ),
            "parking": "Estacionamento não informado pela organização",
            "sources": [
                {
                    "url": (
                        "https://www.instagram.com/motocolatras/reel/"
                        "DaS5MKDu0zu/"
                    ),
                    "label": "MC Motocólatras e FAEC — anúncio oficial",
                    "type": "publicação oficial em colaboração",
                    "supports": (
                        "datas, local, nove bandas, alimentação, gincana, entrada "
                        "solidária, realização e apoios"
                    ),
                    "checked_at": "2026-07-30",
                },
                {
                    "url": "https://www.instagram.com/motocolatras/",
                    "label": "Perfil oficial do MC Motocólatras",
                    "type": "canal do organizador",
                    "supports": (
                        "datas, local, caráter solidário, Banda Hashtag e atualizações"
                    ),
                    "checked_at": "2026-07-30",
                },
                {
                    "url": (
                        "https://jacaremoto.com.br/events/"
                        "13o-motocolatras-fest-araguari-mg/"
                    ),
                    "label": "Jacaré Moto — 13º Motocólatras Fest",
                    "type": "serviço específico do evento",
                    "supports": (
                        "datas, local, horários gerais, distribuição dos shows, "
                        "camping, café da manhã, expositores, entrada e contatos"
                    ),
                    "checked_at": "2026-07-30",
                    "note": (
                        "O texto contém uma referência isolada a 23/08; prevaleceram "
                        "o calendário da própria página e as publicações oficiais, "
                        "que confirmam 21 e 22 de agosto."
                    ),
                },
                {
                    "url": (
                        "https://jb-rider.com.br/evento/"
                        "20260821-2-13-motocolatras-fest-araguari-mg"
                    ),
                    "label": "JB-RIDER — 13 Motocólatras Fest",
                    "type": "agenda independente com página específica",
                    "supports": "período, cidade, estado e identidade do evento",
                    "checked_at": "2026-07-30",
                },
                {
                    "url": (
                        "https://firesoulswebradio.com/evento/"
                        "321600/13-motolatras-fest-araguari-mg"
                    ),
                    "label": "Fire Souls Web Radio — 13º Motocólatras Fest",
                    "type": "agenda independente com registro específico",
                    "supports": "data, cidade e identidade do evento",
                    "checked_at": "2026-07-30",
                },
                {
                    "url": "https://araguari.mg.gov.br/prefeito-vice",
                    "label": "Prefeitura de Araguari — Palácio dos Ferroviários",
                    "type": "fonte oficial do local",
                    "supports": "logradouro, número, bairro e CEP",
                    "checked_at": "2026-07-30",
                },
            ],
            "research_status": {
                "required_specific_independent_sources": 2,
                "specific_independent_domains_found": 5,
                "status": "fontes_especificas_cruzadas_com_anuncio_oficial",
                "query": '"13º Motocólatras Fest" Araguari 2026 programação',
                "reviewed_at": "2026-07-30",
                "editorial_rule": (
                    "Serviço confirmado pelo organizador e cruzado com fonte "
                    "especializada, duas agendas independentes e fonte oficial do local."
                ),
            },
        }
    )

    AGENDA.write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"Evento atualizado: {SLUG}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
