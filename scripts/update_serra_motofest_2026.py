#!/usr/bin/env python3
"""Atualiza o serviço do 7º Serra Motofest com a programação oficial."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENDA = ROOT / "content/events/agenda-comunitaria-2026.json"
CANONICAL_SLUG = "7-serra-moto-fest-serra-es-2026-07-31"


def main() -> int:
    document = json.loads(AGENDA.read_text(encoding="utf-8"))
    entries = document.get("entries", [])
    event = next(entry for entry in entries if entry.get("slug") == CANONICAL_SLUG)

    event.update(
        {
            "title": "7º Serra Motofest",
            "short_name": "7º Serra Motofest",
            "start_date": "2026-07-31",
            "end_date": "2026-08-01",
            "city": "Serra",
            "state": "ES",
            "venue": "Praça Encontro das Águas, Jacaraípe",
            "status": "agendada",
            "event_type": "Encontro de motociclistas e festival de rock",
            "official_url": "https://www.instagram.com/serramotofest/reel/DbYfwbGNVwQ/",
            "source_url": "https://www.instagram.com/serramotofest/reel/DbYfwbGNVwQ/",
            "source_label": "Divulgação oficial do Serra Motofest",
            "verification_status": "fonte_primaria_com_programacao_e_servico_cruzados",
            "cover": "/assets/img/competicoes-eventos-default.svg",
            "image_credit": "Arte: TVDUASRODAS",
            "free": True,
            "summary": (
                "O 7º Serra Motofest acontece em 31 de julho e 1º de agosto de 2026, "
                "na Praça Encontro das Águas, em Jacaraípe, Serra/ES. A entrada é "
                "gratuita e a programação reúne seis shows de rock, exposição de motos, "
                "área de alimentação, encontro de motoclubes e camping."
            ),
            "attractions": [
                "Shows de rock",
                "Dona Fran",
                "Ozzmosis — tributo a Ozzy Osbourne",
                "Texas Hammer Country Rock",
                "Old Man Rock & Roll",
                "Banda Oáz",
                "Last Line",
                "Exposição de motos",
                "Encontro de motoclubes",
                "Área de camping",
                "Área de alimentação",
                "Lazer para toda a família",
            ],
            "body": (
                "## O evento\n\n"
                "O 7º Serra Motofest será realizado na sexta-feira, 31 de julho, e no "
                "sábado, 1º de agosto de 2026, na Praça Encontro das Águas, em Jacaraípe, "
                "Serra/ES. A entrada é gratuita.\n\n"
                "A edição é promovida pelos Bodes do Asfalto — Facção Jacaraípe, com apoio "
                "da Prefeitura da Serra. A estrutura divulgada inclui exposição de motos, "
                "encontro de motoclubes, área de alimentação, camping e atividades de lazer "
                "para toda a família.\n\n"
                "## Programação de sexta-feira — 31 de julho\n\n"
                "- **19h — Dona Fran**\n"
                "- **21h — Ozzmosis**, tributo a Ozzy Osbourne\n"
                "- **23h — Texas Hammer Country Rock**\n\n"
                "## Programação de sábado — 1º de agosto\n\n"
                "- **19h — Old Man Rock & Roll**\n"
                "- **21h — Banda Oáz**\n"
                "- **23h — Last Line**\n\n"
                "## Estrutura e expositores\n\n"
                "Durante os dois dias, o público encontrará exposição de motocicletas, "
                "área de alimentação, encontro de motoclubes e espaço para camping. A Moto "
                "Conecta Multimarcas foi anunciada como expositora oficial, com condições "
                "comerciais especiais durante o evento.\n\n"
                "## Local e entrada\n\n"
                "**Praça Encontro das Águas — Jacaraípe, Serra/ES.** A entrada é gratuita. "
                "A organização ainda não divulgou regras detalhadas do camping nem "
                "informações sobre estacionamento.\n\n"
                "## Canal oficial\n\n"
                "Atualizações de última hora podem ser acompanhadas no Instagram "
                "[@serramotofest](https://www.instagram.com/serramotofest/). Como o evento "
                "é ao ar livre, confirme possíveis mudanças operacionais antes de sair."
            ),
            "last_updated": "2026-07-30",
            "timezone": "America/Sao_Paulo",
            "time_label": (
                "Shows às 19h, 21h e 23h na sexta-feira e no sábado; horário de abertura "
                "do espaço não divulgado"
            ),
            "street_address": "Praça Encontro das Águas, Jacaraípe",
            "full_address": "Praça Encontro das Águas, Jacaraípe, Serra - ES, Brasil",
            "status_basis": (
                "Datas, local, gratuidade, estrutura e programação confirmados no canal "
                "oficial do evento e cruzados com divulgação local específica."
            ),
            "status_checked_at": "2026-07-30",
            "organizer": (
                "Bodes do Asfalto — Facção Jacaraípe, com apoio da Prefeitura da Serra"
            ),
            "contact": "Instagram @serramotofest",
            "source_checked_at": "2026-07-30",
            "visual_verification": {
                "type": "video_oficial_inspecionado_manualmente",
                "source_url": "https://www.instagram.com/serramotofest/reel/DbYfwbGNVwQ/",
                "detail_url": "https://www.instagram.com/p/Danh2n1RXMH/",
                "checked_at": "2026-07-30",
                "review_policy": (
                    "Leitura manual dos quadros do vídeo oficial e cruzamento com a "
                    "publicação local indicada pelo usuário"
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
                ],
            },
            "admission_status": "Entrada gratuita",
            "parking": "Estacionamento não informado pela organização",
            "sources": [
                {
                    "url": "https://www.instagram.com/serramotofest/reel/DbYfwbGNVwQ/",
                    "label": "Serra Motofest — programação oficial de 2026",
                    "type": "fonte primária e vídeo oficial",
                    "supports": (
                        "nome, edição, local, entrada gratuita, bandas e horários dos shows"
                    ),
                    "checked_at": "2026-07-30",
                },
                {
                    "url": "https://www.instagram.com/p/Danh2n1RXMH/",
                    "label": "Boa Dica Serra — serviço do 7º Serra Motofest",
                    "type": "divulgação local específica",
                    "supports": (
                        "datas, local, gratuidade, bandas, estrutura, organizador e apoio "
                        "da Prefeitura da Serra"
                    ),
                    "checked_at": "2026-07-30",
                },
                {
                    "url": (
                        "https://jb-rider.com.br/evento/"
                        "20260731-2-7-serra-moto-fest-serra-es"
                    ),
                    "label": "JB-RIDER — 7º Serra Moto Fest",
                    "type": "agenda independente com página específica",
                    "supports": "datas, cidade, estado e identidade do evento",
                    "checked_at": "2026-07-30",
                },
            ],
            "research_status": {
                "required_specific_independent_sources": 2,
                "specific_independent_domains_found": 2,
                "status": "fonte_primaria_e_fontes_especificas_cruzadas",
                "query": '"7º Serra Motofest" "Jacaraípe" 2026',
                "reviewed_at": "2026-07-30",
                "editorial_rule": (
                    "Programação confirmada no canal oficial e serviço cruzado com "
                    "divulgação local e agenda independente."
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
