#!/usr/bin/env python3
"""Atualiza o serviço do 4º Simonésia Motofest com fontes verificadas."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENDA = ROOT / "content/events/agenda-comunitaria-2026.json"
CANONICAL_SLUG = "motofest-simonesia-mg-2026-08-07"


def main() -> int:
    document = json.loads(AGENDA.read_text(encoding="utf-8"))
    entries = document.get("entries", [])
    event = next(entry for entry in entries if entry.get("slug") == CANONICAL_SLUG)

    event.update(
        {
            "title": "4º Simonésia Motofest",
            "short_name": "4º Simonésia Motofest",
            "start_date": "2026-08-07",
            "end_date": "2026-08-08",
            "city": "Simonésia",
            "state": "MG",
            "venue": "Parque de Exposições de Simonésia",
            "status": "agendada",
            "event_type": "Encontro de motociclistas e festival de rock",
            "official_url": "https://eventostop.com.br/eventos/4o-simonesia-motofest/",
            "source_url": "https://eventostop.com.br/eventos/4o-simonesia-motofest/",
            "source_label": "Serviço completo do 4º Simonésia Motofest no Eventos Top",
            "verification_status": "programacao_e_servico_cruzados_com_cartaz",
            "cover": "/assets/img/competicoes-eventos-default.svg",
            "image_credit": "Arte: TVDUASRODAS",
            "free": False,
            "summary": (
                "O 4º Simonésia Motofest acontece em 7 e 8 de agosto de 2026, no "
                "Parque de Exposições de Simonésia/MG, com quatro shows de rock, "
                "camping gratuito, café da manhã, carros antigos, motorhomes, "
                "expositores e entrada solidária."
            ),
            "attractions": [
                "Sabbra Cadabra — tributo a Black Sabbath",
                "Pammela Princi",
                "Velho Bill",
                "Rock Society",
                "Exposição de carros antigos",
                "Exposição de motorhomes",
                "Recepção de motociclistas",
                "Troféus para motoclubes",
                "Camping gratuito",
                "Café da manhã gratuito",
                "Expositores",
                "Locução de Breno Motta",
            ],
            "body": (
                "## O evento\n\n"
                "O 4º Simonésia Motofest será realizado na sexta-feira, 7 de agosto, "
                "e no sábado, 8 de agosto de 2026, no Parque de Exposições de "
                "Simonésia/MG. O encontro é organizado pela Associação de Motociclistas "
                "de Manhuaçu e Região (AMMAR).\n\n"
                "A estrutura anunciada inclui recepção de motociclistas, troféus para "
                "motoclubes, camping gratuito, café da manhã, expositores e participação "
                "de carros antigos e motorhomes. A locução oficial será de Breno Motta.\n\n"
                "## Programação de sexta-feira — 7 de agosto\n\n"
                "As atividades começam **a partir das 16h**, com shows de:\n\n"
                "- **Pammela Princi**\n"
                "- **Sabbra Cadabra**, tributo a Black Sabbath\n\n"
                "## Programação de sábado — 8 de agosto\n\n"
                "A programação começa **a partir das 10h**, com shows de:\n\n"
                "- **Velho Bill**\n"
                "- **Rock Society**\n\n"
                "A divulgação consultada não informa o horário individual de cada banda.\n\n"
                "## Entrada solidária e camping\n\n"
                "O público é convidado a colaborar com **1 kg de alimento não perecível**, "
                "destinado a entidades locais. O cartaz anuncia camping gratuito e café "
                "da manhã. Regras de acesso, vagas e horários do camping não foram "
                "detalhados; confirme diretamente com a organização.\n\n"
                "## Local\n\n"
                "**Parque de Exposições de Simonésia — Simonésia/MG.** Informações com "
                "Paulo Paraguai pelo telefone "
                "[(33) 98801-1010](tel:+5533988011010).\n\n"
                "## Antes de viajar\n\n"
                "Confirme possíveis mudanças de programação, regras do camping e "
                "condições da entrada solidária com a organização, especialmente por "
                "se tratar de evento ao ar livre."
            ),
            "last_updated": "2026-07-30",
            "timezone": "America/Sao_Paulo",
            "time_label": (
                "Sexta-feira a partir das 16h; sábado a partir das 10h"
            ),
            "street_address": "Parque de Exposições de Simonésia",
            "full_address": "Parque de Exposições de Simonésia, Simonésia - MG, Brasil",
            "status_basis": (
                "Datas, local, horários gerais, atrações e estrutura confirmados no "
                "cartaz do evento e cruzados com três agendas específicas."
            ),
            "status_checked_at": "2026-07-30",
            "organizer": (
                "Associação de Motociclistas de Manhuaçu e Região (AMMAR)"
            ),
            "contact": "Paulo Paraguai: (33) 98801-1010",
            "source_checked_at": "2026-07-30",
            "visual_verification": {
                "type": "cartaz_do_evento_inspecionado_manualmente",
                "source_url": (
                    "https://eventostop.com.br/wp-content/uploads/2026/07/"
                    "simonesia-motofest-2026-cartaz.webp"
                ),
                "detail_url": (
                    "https://eventostop.com.br/eventos/4o-simonesia-motofest/"
                ),
                "checked_at": "2026-07-30",
                "review_policy": (
                    "Leitura manual do cartaz e cruzamento com o serviço textual "
                    "da página específica"
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
                    "services_and_attractions",
                    "admission",
                    "contact",
                ],
            },
            "admission_status": (
                "Entrada solidária: doação sugerida de 1 kg de alimento não perecível"
            ),
            "parking": "Estacionamento não informado pela organização",
            "sources": [
                {
                    "url": "https://eventostop.com.br/eventos/4o-simonesia-motofest/",
                    "label": "Eventos Top — Simonésia Motofest 2026",
                    "type": "serviço editorial específico com cartaz",
                    "supports": (
                        "datas, local, organização, programação, horários gerais, "
                        "entrada solidária, camping, café da manhã, exposições e locução"
                    ),
                    "checked_at": "2026-07-30",
                },
                {
                    "url": "https://maxacalis.com.br/agenda.html",
                    "label": "Maxacalis MC — agenda de agosto de 2026",
                    "type": "agenda independente de motociclismo",
                    "supports": "edição, datas, cidade e estado",
                    "checked_at": "2026-07-30",
                },
                {
                    "url": "https://mototour.com.br/eventos/imprimir",
                    "label": "Mototour — 4º Motofest de Simonésia",
                    "type": "agenda independente",
                    "supports": "edição, período, cidade e estado",
                    "checked_at": "2026-07-30",
                },
                {
                    "url": (
                        "https://jb-rider.com.br/evento/"
                        "20260807-2-motofest-simonesia-mg"
                    ),
                    "label": "JB-RIDER — Motofest Simonésia/MG",
                    "type": "agenda independente com página específica",
                    "supports": "datas, cidade, estado e identidade do evento",
                    "checked_at": "2026-07-30",
                },
            ],
            "research_status": {
                "required_specific_independent_sources": 2,
                "specific_independent_domains_found": 4,
                "status": "fontes_especificas_cruzadas_com_cartaz",
                "query": '"4º Simonésia Motofest" 2026 programação',
                "reviewed_at": "2026-07-30",
                "editorial_rule": (
                    "Serviço detalhado conferido no cartaz e cruzado com três agendas "
                    "independentes de motociclismo."
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
