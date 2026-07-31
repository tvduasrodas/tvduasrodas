#!/usr/bin/env python3
"""Atualiza o 2º Encontro de Motociclistas de Lavras Novas."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENDA = ROOT / "content/events/agenda-comunitaria-2026.json"
SLUG = "2-encontro-de-motociclistas-lavras-novas-mg-2026-08-01"
SYMPla = "https://www.sympla.com.br/evento/2-encontro-de-motociclistas-de-lavras-novas/3461338"
JACARE = "https://jacaremoto.com.br/events/2-encontro-de-motociclistas-de-lavras-novas/"


def main() -> int:
    document = json.loads(AGENDA.read_text(encoding="utf-8"))
    event = next(entry for entry in document["entries"] if entry.get("slug") == SLUG)

    event.update(
        {
            "title": "2º Encontro de Motociclistas de Lavras Novas",
            "short_name": "2º Encontro de Motociclistas de Lavras Novas",
            "venue": "Campo de Futebol do Vila Nova",
            "event_type": "Encontro de motociclistas e festival de rock",
            "official_url": SYMPla,
            "source_url": JACARE,
            "source_label": "Sympla e agenda Jacaré Moto",
            "verification_status": "inscricao_oficial_e_agenda_especializada_conferidas",
            "featured": False,
            "free": True,
            "summary": (
                "O 2º Encontro de Motociclistas de Lavras Novas acontece em 1º e 2 de agosto de 2026, "
                "no Campo de Futebol do Vila Nova, distrito de Lavras Novas, em Ouro Preto/MG. A entrada "
                "é gratuita, com inscrição pela Sympla, e a programação inclui Banda NAH, rock, "
                "gastronomia e Rifa Show de Prêmios."
            ),
            "attractions": [
                "Banda NAH",
                "Rifa Show de Prêmios",
                "Rock",
                "Gastronomia",
                "Chope",
                "Troféus para participantes",
            ],
            "body": (
                "## Serviço confirmado\n\n"
                "O **2º Encontro de Motociclistas de Lavras Novas** será realizado de **1º a 2 de "
                "agosto de 2026**, no **Campo de Futebol do Vila Nova**, no distrito de Lavras Novas, "
                "em Ouro Preto/MG. A programação começa no sábado às **9h** e termina no domingo às "
                "**18h**.\n\n"
                "## Programação e atrações\n\n"
                "A agenda do Jacaré Moto anuncia show da **Banda NAH no sábado, às 12h**. O encontro "
                "também terá rock, gastronomia, chope, troféus para participantes e sorteio da "
                "**Rifa Show de Prêmios**. Outras atrações e horários não foram detalhados nas fontes "
                "consultadas.\n\n"
                "## Entrada e inscrição\n\n"
                "A **entrada é gratuita**, mas a organização orienta a retirada antecipada do ingresso "
                "pela Sympla. A página de inscrição identifica o evento como presencial e confirma os "
                "horários de 9h de sábado a 18h de domingo.\n\n"
                "## Local e endereço\n\n"
                "**Campo de Futebol do Vila Nova**  \n"
                "Rua Nossa Senhora dos Prazeres, 394  \n"
                "Lavras Novas, Ouro Preto - MG\n\n"
                "## Organização e contato\n\n"
                "A agenda especializada informa realização do **Vinicius Riders Lavras Novas**. "
                "Contatos publicados: **(31) 992 310 497**, **(31) 895 697 994** e "
                "**ridelavrasnovas@gmail.com**. O perfil indicado é "
                "[@ride_lavrasnovas](https://www.instagram.com/ride_lavrasnovas/).\n\n"
                "## Fontes e atualização\n\n"
                "Datas, horários, gratuidade, endereço e descrição foram confirmados na página oficial "
                "de inscrições da Sympla e cruzados com a agenda específica do Jacaré Moto. Confirme "
                "eventuais mudanças com a organização antes de viajar."
            ),
            "last_updated": "2026-07-31",
            "timezone": "America/Sao_Paulo",
            "local_start": "2026-08-01T09:00:00-03:00",
            "local_end": "2026-08-02T18:00:00-03:00",
            "time_label": "Sábado, das 9h; encerramento no domingo, às 18h",
            "street_address": "Rua Nossa Senhora dos Prazeres, 394",
            "full_address": "Campo de Futebol do Vila Nova, Rua Nossa Senhora dos Prazeres, 394, Lavras Novas, Ouro Preto - MG",
            "status_basis": "Datas, horários, endereço e gratuidade confirmados na página oficial de inscrições da Sympla.",
            "status_checked_at": "2026-07-31",
            "organizer": "Vinicius Riders Lavras Novas",
            "support": ["Banana da Terra — produtor cadastrado na Sympla"],
            "contact": "(31) 992 310 497 · (31) 895 697 994 · ridelavrasnovas@gmail.com · Instagram: @ride_lavrasnovas",
            "source_checked_at": "2026-07-31",
            "visual_verification": {
                "type": "paginas_especificas_inspecionadas_manualmente",
                "source_url": JACARE,
                "detail_url": SYMPla,
                "checked_at": "2026-07-31",
                "review_policy": "Transcrição conservadora do serviço publicado na Sympla e na agenda Jacaré Moto",
                "confirmed_fields": [
                    "edition",
                    "start_date",
                    "end_date",
                    "start_time",
                    "end_time",
                    "venue",
                    "street_address",
                    "city",
                    "state",
                    "free_admission",
                    "organizer",
                    "contacts",
                    "attractions",
                ],
            },
            "admission_status": "Entrada gratuita; retirada antecipada de ingresso pela Sympla",
            "parking": "Não informado nas fontes consultadas",
            "sources": [
                {
                    "url": SYMPla,
                    "label": "Sympla — página oficial de inscrição do evento",
                    "type": "canal oficial de inscrição",
                    "supports": "nome, datas, horários, local, endereço, gratuidade e descrição",
                    "checked_at": "2026-07-31",
                },
                {
                    "url": JACARE,
                    "label": "Jacaré Moto — agenda específica do evento",
                    "type": "agenda independente especializada",
                    "supports": "datas, horários, Banda NAH, estrutura, realizador e contatos",
                    "checked_at": "2026-07-31",
                },
                {
                    "url": "https://www.instagram.com/ride_lavrasnovas/",
                    "label": "Ride Lavras Novas — perfil indicado pela organização",
                    "type": "canal social do realizador",
                    "supports": "identidade e contato do realizador",
                    "checked_at": "2026-07-31",
                },
            ],
            "research_status": {
                "required_specific_independent_sources": 2,
                "specific_independent_domains_found": 3,
                "status": "canal_oficial_e_fontes_cruzadas",
                "query": '"2º Encontro de Motociclistas de Lavras Novas" 2026',
                "reviewed_at": "2026-07-31",
                "editorial_rule": "Serviço confirmado na inscrição oficial; programação complementar atribuída à agenda especializada.",
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
