#!/usr/bin/env python3
"""Atualiza o Madalena BikeFest 2026 com a divulgação oficial verificada."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENDA = ROOT / "content/events/agenda-comunitaria-2026.json"
SLUG = "bikefest-santa-maria-madalena-rj-2026-07-31"


def main() -> int:
    document = json.loads(AGENDA.read_text(encoding="utf-8"))
    event = next(entry for entry in document["entries"] if entry.get("slug") == SLUG)

    event.update(
        {
            "title": "Madalena BikeFest 2026",
            "short_name": "Madalena BikeFest",
            "start_date": "2026-07-31",
            "end_date": "2026-08-01",
            "venue": "Santa Maria Madalena — endereço exato ainda não divulgado",
            "official_url": "https://www.instagram.com/p/DafucwvFgvb/",
            "source_url": "https://www.instagram.com/p/DafucwvFgvb/",
            "source_label": "Publicação colaborativa do Madalena BikeFest",
            "verification_status": "fonte_primaria_social_com_programacao_completa",
            "cover": "/assets/img/uploads/madalena-bikefest-2026-capa.webp",
            "image_credit": "Arte: Madalena BikeFest / Hotel Girassol da Serra",
            "free": False,
            "summary": (
                "O Madalena BikeFest 2026 acontece em 31 de julho e 1º de agosto, "
                "em Santa Maria Madalena/RJ, com 12 shows de rock, Globo da Morte, "
                "locução de Cascatinha e entrada solidária em benefício do Lar dos Velhinhos."
            ),
            "attractions": [
                "Globo da Morte",
                "Locução de Cascatinha",
                "Madrevinil",
                "TDM — Guns N’ Roses Experience",
                "Thunder Rock",
                "Rodrigo Santos",
                "Maiden Macaé",
                "Kilômetro 50",
                "Rock da Kombi",
                "VMAX",
                "Rock in Concert — Banda Euterpe Madalenense",
                "Back in Blues",
                "Radial 80",
                "Rise Mob",
            ],
            "body": (
                "## Madalena BikeFest 2026\n\n"
                "Santa Maria Madalena recebe dois dias de encontro motociclístico, rock e "
                "atrações para o público em 31 de julho e 1º de agosto de 2026. A divulgação "
                "do perfil do evento confirma 12 apresentações musicais, Globo da Morte e "
                "locução de Cascatinha.\n\n"
                "## Programação de sexta-feira — 31 de julho\n\n"
                "- **16h — Madrevinil**\n"
                "- **18h — TDM — Guns N’ Roses Experience**\n"
                "- **20h — Thunder Rock**\n"
                "- **22h — Rodrigo Santos**\n"
                "- **0h — Maiden Macaé**\n\n"
                "![Programação de sexta-feira do Madalena BikeFest 2026]"
                "(/assets/img/uploads/madalena-bikefest-2026-sexta.webp)\n"
                "*Programação de 31 de julho. Arte: Madalena BikeFest / Hotel Girassol da Serra.*\n\n"
                "## Programação de sábado — 1º de agosto\n\n"
                "- **12h — Kilômetro 50**\n"
                "- **14h — Rock da Kombi**\n"
                "- **16h — VMAX**\n"
                "- **18h — Rock in Concert — Banda Euterpe Madalenense**\n"
                "- **20h — Back in Blues**\n"
                "- **22h — Radial 80**\n"
                "- **0h — Rise Mob**\n\n"
                "![Programação de sábado do Madalena BikeFest 2026]"
                "(/assets/img/uploads/madalena-bikefest-2026-sabado.webp)\n"
                "*Programação de 1º de agosto. Arte: Madalena BikeFest / Hotel Girassol da Serra.*\n\n"
                "## Entrada solidária\n\n"
                "A entrada anunciada é **1 pacote de fraldas geriátricas por pessoa**. A "
                "arrecadação será destinada ao Lar dos Velhinhos. Como a doação faz parte "
                "do acesso divulgado, leve o item antes de chegar ao evento.\n\n"
                "## Local e estrutura\n\n"
                "A publicação confirma o município de **Santa Maria Madalena/RJ**, mas não "
                "informa o endereço exato da área do evento. Em edições recentes, o encontro "
                "foi realizado na Rua Barão de Madalena, no Centro; essa referência histórica "
                "não substitui a confirmação do local em 2026.\n\n"
                "A divulgação atual também não confirma camping, estacionamento, chuveiros "
                "ou horários do Globo da Morte. Consulte o perfil "
                "[@madalena_bikefest](https://www.instagram.com/madalena_bikefest/) antes de viajar.\n\n"
                "## Antes de ir\n\n"
                "Confira eventuais alterações de endereço, horários e regras de acesso nos "
                "canais oficiais. A programação musical foi publicada em colaboração com o "
                "perfil do Madalena BikeFest em 7 de julho de 2026."
            ),
            "last_updated": "2026-07-28",
            "time_label": "Sexta a partir das 16h; sábado a partir das 12h",
            "street_address": "Endereço exato ainda não divulgado para 2026",
            "full_address": "Santa Maria Madalena - RJ, Brasil; endereço exato a confirmar",
            "status_basis": (
                "Datas, programação, entrada solidária e atrações confirmadas em publicação "
                "colaborativa com o perfil do Madalena BikeFest."
            ),
            "status_checked_at": "2026-07-28",
            "organizer": "Madalena BikeFest",
            "contact": "Instagram: @madalena_bikefest",
            "source_checked_at": "2026-07-28",
            "visual_verification": {
                "type": "carrossel_oficial_inspecionado_manualmente",
                "source_url": "https://www.instagram.com/p/DafucwvFgvb/",
                "detail_url": "https://www.instagram.com/madalena_bikefest/",
                "checked_at": "2026-07-28",
                "review_policy": (
                    "Leitura manual da legenda e das três artes do carrossel, com separação "
                    "entre dados confirmados para 2026 e referências históricas."
                ),
                "confirmed_fields": [
                    "event_name",
                    "start_date",
                    "end_date",
                    "city",
                    "state",
                    "daily_schedule",
                    "admission",
                    "special_attraction",
                    "announcer",
                ],
            },
            "admission_status": (
                "Entrada solidária: 1 pacote de fraldas geriátricas por pessoa, "
                "em benefício do Lar dos Velhinhos"
            ),
            "parking": "Estacionamento não informado na divulgação de 2026",
            "sources": [
                {
                    "url": "https://www.instagram.com/p/DafucwvFgvb/",
                    "label": "Madalena BikeFest 2026 — publicação colaborativa oficial",
                    "type": "fonte primária e artes oficiais",
                    "supports": (
                        "datas, cidade, grade de shows, Globo da Morte, locução, "
                        "entrada solidária e destino da arrecadação"
                    ),
                    "checked_at": "2026-07-28",
                },
                {
                    "url": "https://jb-rider.com.br/evento/20260731-bikefest-santa-maria-madalena-rj",
                    "label": "Agenda JB-RIDER — Bikefest Santa Maria Madalena",
                    "type": "agenda comunitária específica",
                    "supports": "data inicial, cidade e estado",
                    "checked_at": "2026-07-28",
                },
                {
                    "url": (
                        "https://www.pmsmm.rj.gov.br/noticias?data=24-07-2025&id=2009"
                        "&secretaria=turismo&titulo=vem_ai_o_xxi_encontro_de_motociclistas"
                        "_de_santa_maria_madalena"
                    ),
                    "label": "Prefeitura de Santa Maria Madalena — edição de 2025",
                    "type": "fonte institucional histórica",
                    "supports": (
                        "tradição do evento, participação da Secretaria de Turismo e "
                        "referência histórica de local; não usada como programação de 2026"
                    ),
                    "checked_at": "2026-07-28",
                },
            ],
            "research_status": {
                "required_specific_independent_sources": 2,
                "specific_independent_domains_found": 3,
                "status": "fonte_primaria_e_contexto_institucional_cruzados",
                "query": "\"Madalena BikeFest\" \"Santa Maria Madalena\" 2026",
                "reviewed_at": "2026-07-28",
                "editorial_rule": (
                    "Programação de 2026 publicada somente com base no canal do evento; "
                    "dados de anos anteriores identificados como contexto histórico."
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
