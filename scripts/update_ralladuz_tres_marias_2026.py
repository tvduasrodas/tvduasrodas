#!/usr/bin/env python3
"""Atualiza o serviço do VI Encontro de Três Marias com fontes verificadas."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENDA = ROOT / "content/events/agenda-comunitaria-2026.json"
EVENT_FILE = ROOT / "content/events/ralladuz-mc-tres-marias-mg-2026-08-27.json"
CANONICAL_SLUG = "ralladuz-mc-tres-marias-mg-2026-08-27"


def main() -> int:
    document = json.loads(AGENDA.read_text(encoding="utf-8"))
    entries = document.get("entries", [])
    by_slug = {entry.get("slug"): entry for entry in entries}
    event = by_slug[CANONICAL_SLUG]

    event.update(
        {
            "title": "6º Encontro Nacional de Motociclistas e Triciclistas de Três Marias 2026",
            "short_name": "6º Encontro de Três Marias",
            "aliases": ["vi-encontro-tres-marias-mg-2026-08-27"],
            "city": "Três Marias",
            "venue": "Praia Mar de Minas",
            "event_type": "Encontro nacional de motociclistas e triciclistas",
            "official_url": "https://www.instagram.com/p/DXFVWjWChDc/",
            "source_url": "https://www.instagram.com/p/DXFVWjWChDc/",
            "source_label": "Divulgação oficial do Ralladuz MC",
            "verification_status": "fonte_primaria_cruzada_com_servico_independente",
            "cover": "/assets/img/uploads/vi-encontro-motociclistas-tres-marias-2026.webp",
            "image_credit": "Arte: Ralladuz MC / Prefeitura de Três Marias",
            "free": True,
            "summary": (
                "O 6º Encontro Nacional de Motociclistas e Triciclistas será realizado "
                "de 27 a 30 de agosto de 2026, na Praia Mar de Minas, em Três Marias/MG, "
                "com entrada franca, shows de rock, camping, café da manhã gratuito, "
                "expositores e praça de alimentação."
            ),
            "attractions": [
                "Shows de rock e música ao vivo",
                "Encontro de motociclistas, triciclistas e motoclubes",
                "Expositores",
                "Troféus",
                "Área de camping estruturada",
                "Café da manhã gratuito no sábado e no domingo",
                "Praça de alimentação com preços anunciados como justos",
            ],
            "body": (
                "## O evento\n\n"
                "Três Marias recebe o 6º Encontro Nacional de Motociclistas e Triciclistas "
                "entre 27 e 30 de agosto de 2026. A programação será montada na Praia Mar de "
                "Minas, cenário à beira da represa do Rio São Francisco, e tem organização "
                "do Ralladuz MC, com realização da Prefeitura de Três Marias.\n\n"
                "## Programação e atrações\n\n"
                "A divulgação oficial confirma shows de rock e música ao vivo, troféus, "
                "expositores e confraternização entre motociclistas, triciclistas e motoclubes. "
                "A relação de bandas e os horários de cada apresentação ainda não foram "
                "publicados pelos organizadores. A TVDUASRODAS atualizará este serviço quando "
                "a grade detalhada estiver disponível.\n\n"
                "## Estrutura\n\n"
                "O encontro terá área de camping estruturada, café da manhã gratuito no sábado "
                "e no domingo e praça de alimentação. A organização anuncia comida e bebida a "
                "preço justo. A arte oficial também orienta os visitantes a não empinar motos "
                "dentro do evento.\n\n"
                "## Entrada e inscrições\n\n"
                "A entrada é franca. O Ralladuz MC informa que as inscrições estão abertas e "
                "direciona os participantes ao link disponível no perfil oficial "
                "[@ralladuz](https://www.instagram.com/ralladuz/). Como regras, benefícios e "
                "eventuais prazos podem ser atualizados, faça a conferência diretamente com a "
                "organização antes de concluir a inscrição.\n\n"
                "## Local\n\n"
                "**Praia Mar de Minas — Três Marias/MG.** O encontro acontece de quinta-feira, "
                "27 de agosto, a domingo, 30 de agosto. Os horários diários de abertura e "
                "encerramento ainda não foram divulgados.\n\n"
                "## Contato da organização\n\n"
                "- Telefones: [(38) 98822-6444](tel:+5538988226444) e "
                "[(38) 98416-1417](tel:+5538984161417)\n"
                "- E-mails: [ralladuz.mc@gmail.com](mailto:ralladuz.mc@gmail.com) e "
                "[jannyfranca3m@hotmail.com](mailto:jannyfranca3m@hotmail.com)\n"
                "- Instagram: [@ralladuz](https://www.instagram.com/ralladuz/)\n\n"
                "## Antes de viajar\n\n"
                "Confirme horários, programação musical, regras do camping e condições de "
                "acesso nos canais do Ralladuz MC. Eventos ao ar livre podem ter ajustes "
                "operacionais próximos à data."
            ),
            "last_updated": "2026-07-28",
            "time_label": "Horários diários ainda não divulgados pela organização",
            "street_address": "Praia Mar de Minas",
            "full_address": "Praia Mar de Minas, Três Marias - MG, Brasil",
            "status_basis": (
                "Datas, local e estrutura confirmados na divulgação oficial do Ralladuz MC; "
                "entrada e contatos cruzados com a página específica do Jacaremoto."
            ),
            "status_checked_at": "2026-07-28",
            "organizer": "Ralladuz MC, com realização da Prefeitura de Três Marias",
            "contact": (
                "(38) 98822-6444; (38) 98416-1417; ralladuz.mc@gmail.com; "
                "jannyfranca3m@hotmail.com; Instagram @ralladuz"
            ),
            "source_checked_at": "2026-07-28",
            "visual_verification": {
                "type": "arte_oficial_inspecionada_no_canal_do_organizador",
                "source_url": "https://www.instagram.com/p/DXFVWjWChDc/",
                "detail_url": (
                    "https://jacaremoto.com.br/events/"
                    "6o-encontro-de-motociclistas-e-triciclistas-em-tres-marias-mg/"
                ),
                "checked_at": "2026-07-28",
                "review_policy": (
                    "Leitura visual manual da arte oficial e cruzamento textual com página "
                    "específica do evento"
                ),
                "confirmed_fields": [
                    "event_name",
                    "edition",
                    "date",
                    "city",
                    "state",
                    "venue",
                    "organizer",
                    "services_and_attractions",
                    "admission",
                    "contact",
                ],
            },
            "admission_status": "Entrada franca",
            "parking": "Estacionamento não informado pela organização",
            "sources": [
                {
                    "url": "https://www.instagram.com/p/DXFVWjWChDc/",
                    "label": "Post oficial do Ralladuz MC — VI Encontro 2026",
                    "type": "fonte primária e arte oficial",
                    "supports": (
                        "nome, edição, datas, local, organização, camping, café da manhã, "
                        "alimentação, música ao vivo, troféus e inscrições"
                    ),
                    "checked_at": "2026-07-28",
                },
                {
                    "url": (
                        "https://jacaremoto.com.br/events/"
                        "6o-encontro-de-motociclistas-e-triciclistas-em-tres-marias-mg/"
                    ),
                    "label": "6º Encontro de Motociclistas e Triciclistas — Jacaremoto",
                    "type": "serviço editorial específico",
                    "supports": (
                        "datas, entrada franca, local, expositores, organização e contatos"
                    ),
                    "checked_at": "2026-07-28",
                },
                {
                    "url": "https://mototour.com.br/eventos/imprimir",
                    "label": "Agenda de eventos Mototour",
                    "type": "agenda independente",
                    "supports": "edição, período, cidade e estado",
                    "checked_at": "2026-07-28",
                },
                {
                    "url": "https://www.ralladuz.com.br/",
                    "label": "Site do Motoclube Ralladuz",
                    "type": "canal institucional",
                    "supports": "identidade do motoclube e vínculo com Três Marias",
                    "checked_at": "2026-07-28",
                },
            ],
            "research_status": {
                "required_specific_independent_sources": 2,
                "specific_independent_domains_found": 3,
                "status": "fonte_primaria_e_fontes_especificas_cruzadas",
                "query": (
                    "\"6º Encontro Nacional de Motociclistas e Triciclistas\" "
                    "\"Três Marias\" 2026"
                ),
                "reviewed_at": "2026-07-28",
                "editorial_rule": (
                    "Dados centrais confirmados no canal do organizador e cruzados com "
                    "serviços específicos do evento."
                ),
            },
        }
    )

    EVENT_FILE.write_text(
        json.dumps(event, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"Evento atualizado: {CANONICAL_SLUG}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
