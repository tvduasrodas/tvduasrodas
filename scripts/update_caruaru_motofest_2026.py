#!/usr/bin/env python3
"""Completa o serviço do Caruaru MotoFest 2026 com fontes verificadas."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENDA = ROOT / "content/events/agenda-comunitaria-2026.json"
CANONICAL_SLUG = "motofest-caruaru-pe-2026-09-17"


def main() -> int:
    document = json.loads(AGENDA.read_text(encoding="utf-8"))
    entries = document.get("entries", [])
    event = next(entry for entry in entries if entry.get("slug") == CANONICAL_SLUG)

    event.update(
        {
            "title": "Caruaru MotoFest 2026",
            "short_name": "Caruaru MotoFest",
            "start_date": "2026-09-17",
            "end_date": "2026-09-20",
            "city": "Caruaru",
            "state": "PE",
            "country": "Brasil",
            "scope": "Nacional",
            "region": "Nordeste",
            "venue": "Pátio de Eventos Luiz Gonzaga",
            "status": "agendada",
            "event_type": "Encontro de motociclistas e festival musical",
            "segment": "Motos",
            "official_url": "https://www.instagram.com/p/DUNmbuPEUtp/",
            "source_url": "https://www.instagram.com/p/DUNmbuPEUtp/",
            "source_label": "Anúncio oficial do Movimento Motociclístico de Caruaru",
            "verification_status": "datas_confirmadas_e_contexto_oficial_cruzado",
            "cover": "/assets/img/uploads/caruaru-motofest-2026-artwork.svg",
            "image_credit": "Arte: TVDUASRODAS",
            "featured": False,
            "free": False,
            "summary": (
                "O Caruaru MotoFest 2026 está confirmado de 17 a 20 de setembro, "
                "no Pátio de Eventos Luiz Gonzaga, em Caruaru/PE. O encontro é "
                "realizado pela Prefeitura de Caruaru em parceria com o Movimento "
                "Motociclístico de Caruaru; programação, horários e regras de acesso "
                "da edição de 2026 ainda serão divulgados."
            ),
            "attractions": [
                "Encontro de motociclistas e motoclubes de várias regiões",
                "Formato tradicional com passeios motociclísticos por atrativos de Caruaru",
                "Gastronomia regional",
                "Shows de forró e rock no formato histórico do evento",
                "Grade de atrações e horários de 2026 ainda não divulgada",
            ],
            "body": (
                "## O que já está confirmado\n\n"
                "O **Caruaru MotoFest 2026** será realizado de **quinta-feira, 17 de "
                "setembro, a domingo, 20 de setembro**, em Caruaru/PE. As datas foram "
                "confirmadas pelo Movimento Motociclístico de Caruaru (MMC) no anúncio "
                "oficial da edição e no site da entidade.\n\n"
                "O portal turístico da Prefeitura de Caruaru informa que o evento é "
                "promovido pelo município em parceria com o MMC e acontece no **Pátio "
                "de Eventos Luiz Gonzaga**, tradicional palco de grandes celebrações "
                "da cidade.\n\n"
                "## Como é o Caruaru MotoFest\n\n"
                "Na descrição institucional do município, o encontro reúne motociclistas "
                "de diferentes regiões do país e está entre os maiores eventos do gênero "
                "no Nordeste. O formato tradicional inclui **passeios motociclísticos "
                "por atrativos turísticos**, experiências de **gastronomia regional** e "
                "shows que combinam **forró e rock**.\n\n"
                "Essas atividades descrevem o perfil permanente do Caruaru MotoFest. "
                "A programação específica de 2026 — atrações, ordem dos shows, horários "
                "e passeios — ainda não havia sido publicada nos canais oficiais na "
                "data desta atualização.\n\n"
                "## Local e como chegar\n\n"
                "O **Pátio de Eventos Luiz Gonzaga** fica na Rua Agnelo Dias Vidal, no "
                "bairro Nossa Senhora das Dores, região central de Caruaru. A referência "
                "cadastral consultada indica o CEP **55002-310**.\n\n"
                "Por se tratar de uma área de grandes eventos, podem ocorrer bloqueios "
                "e mudanças temporárias no trânsito do entorno. O plano de mobilidade "
                "específico do MotoFest 2026 ainda não foi divulgado; confira os canais "
                "da Prefeitura e da Autarquia de Mobilidade de Caruaru perto da data.\n\n"
                "## Entrada, estacionamento e camping\n\n"
                "A organização ainda não informou se a entrada será gratuita, se haverá "
                "área oficial de estacionamento, camping, café da manhã para motociclistas "
                "ou credenciamento de motoclubes. Esses serviços não devem ser presumidos "
                "com base em edições anteriores.\n\n"
                "## Canais oficiais\n\n"
                "Acompanhe o perfil [@mmc.caruaru](https://www.instagram.com/mmc.caruaru/) "
                "e o site [mmc-caruaru.com.br](https://mmc-caruaru.com.br/) para a grade "
                "de atrações e atualizações. Antes de viajar, confirme horários, acesso "
                "ao Pátio e eventuais alterações de programação."
            ),
            "last_updated": "2026-07-30",
            "timezone": "America/Sao_Paulo",
            "time_label": "Horários de abertura, shows e passeios ainda não divulgados",
            "street_address": "Rua Agnelo Dias Vidal",
            "postal_code": "55002-310",
            "full_address": (
                "Pátio de Eventos Luiz Gonzaga, Rua Agnelo Dias Vidal, Nossa Senhora "
                "das Dores, Caruaru - PE, CEP 55002-310, Brasil"
            ),
            "status_basis": (
                "Período confirmado no anúncio e no site do MMC; local e organização "
                "confirmados no portal turístico oficial da Prefeitura de Caruaru."
            ),
            "status_checked_at": "2026-07-30",
            "organizer": (
                "Prefeitura de Caruaru e Movimento Motociclístico de Caruaru (MMC)"
            ),
            "contact": "Instagram: @mmc.caruaru • Site: mmc-caruaru.com.br",
            "source_checked_at": "2026-07-30",
            "visual_verification": {
                "type": "publicacao_oficial_inspecionada_manualmente",
                "source_url": "https://www.instagram.com/p/DUNmbuPEUtp/",
                "detail_url": "https://mmc-caruaru.com.br/",
                "checked_at": "2026-07-30",
                "review_policy": (
                    "Leitura manual da legenda do anúncio oficial e cruzamento com o "
                    "site do MMC, o portal turístico municipal e agenda específica"
                ),
                "confirmed_fields": [
                    "event_name",
                    "start_date",
                    "end_date",
                    "city",
                    "state",
                    "venue",
                    "organizer",
                    "traditional_event_format",
                ],
            },
            "admission_status": "Condição de entrada ainda não divulgada",
            "parking": "Estacionamento e operação de trânsito ainda não divulgados",
            "sources": [
                {
                    "url": "https://www.instagram.com/p/DUNmbuPEUtp/",
                    "label": "MMC Caruaru — anúncio oficial do Caruaru MotoFest 2026",
                    "type": "fonte primária do organizador",
                    "supports": "nome do evento e período de 17 a 20 de setembro de 2026",
                    "checked_at": "2026-07-30",
                },
                {
                    "url": "https://mmc-caruaru.com.br/",
                    "label": "Movimento Motociclístico de Caruaru — site oficial",
                    "type": "canal do organizador",
                    "supports": (
                        "período do evento e identificação do MMC como agremiação "
                        "responsável por promover o motoclubismo de Caruaru"
                    ),
                    "checked_at": "2026-07-30",
                },
                {
                    "url": "https://conheca.caruaru.pe.gov.br/eventos",
                    "label": "Conheça Caruaru — página oficial de eventos",
                    "type": "fonte oficial da Prefeitura de Caruaru",
                    "supports": (
                        "organização conjunta, Pátio de Eventos Luiz Gonzaga, mês de "
                        "realização e formato tradicional do Caruaru MotoFest"
                    ),
                    "checked_at": "2026-07-30",
                },
                {
                    "url": "https://jb-rider.com.br/evento/20260917-4-motofest-caruaru-pe",
                    "label": "JB-RIDER — MotoFest Caruaru/PE",
                    "type": "agenda independente com página específica",
                    "supports": "período, cidade, estado e identidade do evento",
                    "checked_at": "2026-07-30",
                },
                {
                    "url": (
                        "https://www.google.com/maps/search/"
                        "P%C3%A1tio+de+Eventos+Luiz+Gonzaga+Caruaru"
                    ),
                    "label": "Google Maps — Pátio de Eventos Luiz Gonzaga",
                    "type": "referência cartográfica",
                    "supports": "logradouro, bairro e CEP do local",
                    "checked_at": "2026-07-30",
                },
            ],
            "research_status": {
                "required_specific_independent_sources": 2,
                "specific_independent_domains_found": 4,
                "status": "fonte_primaria_e_fontes_oficiais_cruzadas",
                "query": '"Caruaru MotoFest" "17 a 20 de setembro" 2026',
                "reviewed_at": "2026-07-30",
                "editorial_rule": (
                    "Datas tratadas como confirmadas; programação, gratuidade, "
                    "estacionamento e camping permanecem explicitamente pendentes."
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
