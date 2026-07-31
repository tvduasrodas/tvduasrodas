#!/usr/bin/env python3
"""Atualiza o 3º Encontro de Amigos Motociclistas de Taquaritinga."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENDA = ROOT / "content/events/agenda-comunitaria-2026.json"
SLUG = "3-encontro-de-motociclistas-taquaritinga-sp-2026-08-01"


def main() -> int:
    document = json.loads(AGENDA.read_text(encoding="utf-8"))
    event = next(entry for entry in document["entries"] if entry.get("slug") == SLUG)

    event.update(
        {
            "title": "3º Encontro de Amigos Motociclistas",
            "short_name": "3º Encontro de Amigos Motociclistas",
            "venue": "Clube Náutico Taquaritinga",
            "event_type": "Encontro de motociclistas e festival de rock",
            "source_label": "Cartaz oficial do evento",
            "verification_status": "cartaz_oficial_inspecionado_manualmente",
            "cover": "/assets/img/uploads/3-encontro-amigos-motociclistas-taquaritinga-2026.webp",
            "image_credit": "Divulgação: organização do evento",
            "summary": (
                "O 3º Encontro de Amigos Motociclistas será realizado em 1º e 2 de agosto de 2026, "
                "no Clube Náutico Taquaritinga, em Taquaritinga/SP. A programação reúne cinco shows, "
                "exposição de motos, gastronomia e a comemoração dos 56 anos do clube."
            ),
            "attractions": [
                "MobyDick",
                "Namadruga",
                "Wagner Seixas — cover de Raul Seixas",
                "Conexão Amazônica — tributo à Legião Urbana",
                "Elvis & Eu — tributo a Elvis Presley",
                "Exposição de motos de alto padrão",
                "Gastronomia",
            ],
            "body": (
                "## Serviço confirmado\n\n"
                "O **3º Encontro de Amigos Motociclistas** acontece no **Clube Náutico Taquaritinga**, "
                "em Taquaritinga/SP, nos dias **1º e 2 de agosto de 2026**. O encontro integra as "
                "comemorações do aniversário de **56 anos do clube**.\n\n"
                "## Programação de sábado — 1º de agosto\n\n"
                "- **13h:** MobyDick\n"
                "- **16h:** Namadruga\n"
                "- **20h:** Wagner Seixas — cover de Raul Seixas\n\n"
                "## Programação de domingo — 2 de agosto\n\n"
                "- **12h:** Conexão Amazônica — tributo à Legião Urbana\n"
                "- **16h:** Elvis & Eu — tributo a Elvis Presley\n\n"
                "## Estrutura e atrações\n\n"
                "O cartaz anuncia **exposição de motos de alto padrão**, música, gastronomia, lazer e "
                "diversão, além da participação de motoclubes convidados.\n\n"
                "## Entrada, estacionamento e contato\n\n"
                "O material consultado não informa valor de entrada, regras de estacionamento ou "
                "contato direto. Confirme essas condições com a organização antes de viajar.\n\n"
                "## Fonte e atualização\n\n"
                "Datas, local, atrações e horários foram transcritos do cartaz oficial enviado à "
                "TVDUASRODAS e confrontados com a página específica já vinculada ao evento."
            ),
            "last_updated": "2026-07-31",
            "timezone": "America/Sao_Paulo",
            "local_start": "2026-08-01T13:00:00-03:00",
            "time_label": "Sábado às 13h, 16h e 20h; domingo às 12h e 16h",
            "street_address": "Clube Náutico Taquaritinga",
            "full_address": "Clube Náutico Taquaritinga, Taquaritinga - SP",
            "status_basis": "Datas, local, programação e horários confirmados no cartaz oficial do evento.",
            "status_checked_at": "2026-07-31",
            "organizer": "Diretoria 2026/2027 do Clube Náutico Taquaritinga",
            "contact": "Não informado no cartaz oficial consultado",
            "source_checked_at": "2026-07-31",
            "visual_verification": {
                "type": "cartaz_oficial_inspecionado_manualmente",
                "source_url": event["source_url"],
                "detail_url": event["official_url"],
                "checked_at": "2026-07-31",
                "review_policy": "Leitura manual do cartaz, com transcrição conservadora dos nomes e horários",
                "confirmed_fields": [
                    "event_name",
                    "start_date",
                    "end_date",
                    "city",
                    "state",
                    "venue",
                    "organizer",
                    "lineup",
                    "show_times",
                    "services_and_attractions",
                ],
            },
            "admission_status": "Não informado no cartaz oficial consultado",
            "parking": "Não informado no cartaz oficial consultado",
            "research_status": {
                "required_specific_independent_sources": 2,
                "specific_independent_domains_found": 2,
                "status": "cartaz_oficial_e_fontes_cruzadas",
                "query": '"3º Encontro de Amigos Motociclistas" Taquaritinga 2026',
                "reviewed_at": "2026-07-31",
                "editorial_rule": "Serviço e programação transcritos do cartaz oficial; itens ausentes não foram presumidos.",
            },
        }
    )

    for source in event.get("sources", []):
        source["checked_at"] = "2026-07-31"

    AGENDA.write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"Evento atualizado: {SLUG}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
