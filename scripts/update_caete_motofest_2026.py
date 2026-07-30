#!/usr/bin/env python3
"""Atualiza o 1º Moto Fest Caeté Moto Grupo com fontes verificadas."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENDA = ROOT / "content/events/agenda-comunitaria-2026.json"
CANONICAL_SLUG = "motofest-caete-mg-2026-08-07"
DUPLICATE_SLUG = "motofest-caete-mg-2026-08-08"


def main() -> int:
    document = json.loads(AGENDA.read_text(encoding="utf-8"))
    entries = document.get("entries", [])
    event = next(entry for entry in entries if entry.get("slug") == CANONICAL_SLUG)
    duplicate = next(entry for entry in entries if entry.get("slug") == DUPLICATE_SLUG)

    event.update(
        {
            "title": "1º Moto Fest Caeté Moto Grupo",
            "short_name": "1º Moto Fest Caeté",
            "start_date": "2026-08-07",
            "end_date": "2026-08-09",
            "city": "Caeté",
            "state": "MG",
            "venue": "Poliesportivo de Caeté",
            "status": "agendada",
            "event_type": "Encontro de motociclistas e festival de rock",
            "official_url": "https://www.instagram.com/caetemotogrupo/",
            "source_url": "https://www.instagram.com/p/DavM_exRdvN/",
            "source_label": "Anúncio do Caeté Moto Grupo em colaboração com o Jornal Gazeta",
            "verification_status": "servico_e_programacao_cruzados_com_divulgacao_oficial",
            "cover": "/assets/img/competicoes-eventos-default.svg",
            "image_credit": "Arte: TVDUASRODAS",
            "free": True,
            "summary": (
                "O 1º Moto Fest Caeté Moto Grupo acontece de 7 a 9 de agosto de 2026 "
                "no Poliesportivo de Caeté/MG, com entrada franca, sete shows de rock, "
                "camping, praça de alimentação, exposição de carros antigos, motos e "
                "triciclos, expositores e atividades sobre duas rodas."
            ),
            "attractions": [
                "Sete shows de rock: dois na sexta, quatro no sábado e um no domingo",
                "T-Rex Rock",
                "Tio Chico Classic Rock",
                "Los Balas",
                "Banda Dvolvers",
                "Triad Rock",
                "Locução de Xororó",
                "Área de camping",
                "Praça de alimentação",
                "Encontro de motorhomes",
                "Exposição de carros antigos",
                "Exposição de motocicletas e triciclos",
                "Expositores",
                "Pedal da World Bikes no domingo",
                "Passeio de scooters e bicicletas elétricas",
            ],
            "body": (
                "## O evento\n\n"
                "O **1º Moto Fest Caeté Moto Grupo** será realizado de sexta-feira, "
                "7 de agosto, a domingo, 9 de agosto de 2026, no **Poliesportivo de "
                "Caeté**, em Caeté/MG. A entrada é franca durante os três dias.\n\n"
                "A organização espera receber mais de 120 motogrupos de Minas Gerais e "
                "de outros estados. A estrutura anunciada reúne área de camping, praça "
                "de alimentação, encontro de motorhomes, expositores e exposições de "
                "carros antigos, motocicletas e triciclos.\n\n"
                "## Shows de rock\n\n"
                "A programação terá **sete bandas**: duas apresentações na sexta-feira, "
                "quatro no sábado e uma no domingo. Entre as atrações já divulgadas pela "
                "organização e pelos próprios artistas estão:\n\n"
                "- **T-Rex Rock**\n"
                "- **Tio Chico Classic Rock**\n"
                "- **Los Balas**\n"
                "- **Banda Dvolvers**\n"
                "- **Triad Rock**\n\n"
                "A locução terá participação de **Xororó**. A ordem dos shows, os "
                "horários individuais e os dois nomes restantes não estavam publicados "
                "nas fontes consultadas; acompanhe o Caeté Moto Grupo para atualizações.\n\n"
                "## Domingo sobre duas rodas\n\n"
                "No domingo, 9 de agosto, a World Bikes promove uma atividade dentro do "
                "Moto Fest. A saída será **às 7h**, no estande da loja, com pedal de MTB "
                "de aproximadamente 30 km e passeio de 12 km para scooters e bicicletas "
                "elétricas. A divulgação anuncia café da manhã, sorteio de brindes e "
                "medalha para os 150 primeiros inscritos. A inscrição é separada e deve "
                "ser conferida diretamente com a World Bikes.\n\n"
                "## Local e acesso\n\n"
                "**Poliesportivo de Caeté — Avenida Carlos Cruz, s/nº, Caeté/MG, "
                "CEP 34800-000.** O cartaz anuncia entrada franca em todos os dias. "
                "Regras, capacidade e horários de acesso ao camping não foram "
                "detalhados; consulte a organização antes de viajar.\n\n"
                "## Antes de viajar\n\n"
                "A programação pode receber novas atrações e ajustes de horário. "
                "Consulte as publicações do **Caeté Moto Grupo** próximo à data, "
                "especialmente para conferir shows, camping e condições de acesso."
            ),
            "last_updated": "2026-07-30",
            "timezone": "America/Sao_Paulo",
            "time_label": (
                "Horários dos shows a confirmar; pedal no domingo com saída às 7h"
            ),
            "street_address": "Avenida Carlos Cruz, s/nº",
            "postal_code": "34800-000",
            "full_address": (
                "Poliesportivo de Caeté, Avenida Carlos Cruz, s/nº, Caeté - MG, "
                "CEP 34800-000, Brasil"
            ),
            "status_basis": (
                "Datas, local, entrada franca, estrutura e distribuição dos shows "
                "confirmados em publicação colaborativa e cartaz do organizador."
            ),
            "status_checked_at": "2026-07-30",
            "organizer": "Caeté Moto Grupo",
            "contact": "Instagram: @caetemotogrupo",
            "source_checked_at": "2026-07-30",
            "visual_verification": {
                "type": "cartaz_e_publicacoes_oficiais_inspecionados_manualmente",
                "source_url": "https://www.instagram.com/caetemotogrupo/reel/DbLRAyPKKi2/",
                "detail_url": "https://www.instagram.com/p/DavM_exRdvN/",
                "checked_at": "2026-07-30",
                "review_policy": (
                    "Leitura manual do cartaz e das legendas publicadas pelo organizador "
                    "e por parceiros do evento"
                ),
                "confirmed_fields": [
                    "event_name",
                    "edition",
                    "date",
                    "city",
                    "state",
                    "venue",
                    "organizer",
                    "admission",
                    "program_structure",
                    "bands_announced",
                    "services_and_attractions",
                ],
            },
            "admission_status": "Entrada franca em todos os dias",
            "parking": "Estacionamento não informado pela organização",
            "sources": [
                {
                    "url": "https://www.instagram.com/p/DavM_exRdvN/",
                    "label": "Caeté Moto Grupo e Jornal Gazeta — anúncio do evento",
                    "type": "publicação colaborativa com o organizador",
                    "supports": (
                        "edição, datas, sete bandas, distribuição dos shows, estrutura, "
                        "organização e expectativa de público"
                    ),
                    "checked_at": "2026-07-30",
                },
                {
                    "url": "https://www.instagram.com/caetemotogrupo/reel/DbLRAyPKKi2/",
                    "label": "Caeté Moto Grupo — cartaz atualizado",
                    "type": "publicação oficial do organizador",
                    "supports": (
                        "datas, Poliesportivo de Caeté, entrada franca, camping, "
                        "alimentação, exposições e locução"
                    ),
                    "checked_at": "2026-07-30",
                },
                {
                    "url": "https://www.instagram.com/caetemotogrupo/",
                    "label": "Perfil oficial do Caeté Moto Grupo",
                    "type": "canal do organizador",
                    "supports": (
                        "bandas anunciadas e atualizações recentes da programação"
                    ),
                    "checked_at": "2026-07-30",
                },
                {
                    "url": "https://www.instagram.com/worldbikes.bja/p/DbMHoPjpCax/",
                    "label": "World Bikes — pedal dentro do Moto Fest",
                    "type": "publicação de parceiro da programação",
                    "supports": (
                        "data, horário, percursos, café da manhã, medalhas e sorteios"
                    ),
                    "checked_at": "2026-07-30",
                },
                {
                    "url": "https://jb-rider.com.br/evento/20260807-3-motofest-caete-mg",
                    "label": "JB-RIDER — Motofest Caeté/MG",
                    "type": "agenda independente com página específica",
                    "supports": "período, cidade, estado e identidade do evento",
                    "checked_at": "2026-07-30",
                },
                {
                    "url": "https://maxacalis.com.br/agenda.html",
                    "label": "Maxacalis MC — agenda de agosto de 2026",
                    "type": "agenda independente de motociclismo",
                    "supports": (
                        "edição, cidade e realização no fim de semana; a agenda omite "
                        "a abertura de sexta-feira, confirmada pelo organizador"
                    ),
                    "checked_at": "2026-07-30",
                },
                {
                    "url": "https://lbjj.com.br/xiii_copa_caete/",
                    "label": "Liga Brasileira de Jiu-Jitsu — Ginásio Poliesportivo de Caeté",
                    "type": "referência independente do local",
                    "supports": "logradouro e CEP do Poliesportivo de Caeté",
                    "checked_at": "2026-07-30",
                },
            ],
            "research_status": {
                "required_specific_independent_sources": 2,
                "specific_independent_domains_found": 4,
                "status": "fontes_especificas_cruzadas_com_cartaz_oficial",
                "query": '"1º Moto Fest Caeté Moto Grupo" 2026',
                "reviewed_at": "2026-07-30",
                "editorial_rule": (
                    "Informações centrais confirmadas pelo organizador e cruzadas com "
                    "agendas independentes; endereço conferido em referência do local."
                ),
            },
        }
    )

    duplicate.update(
        {
            "title": "1º Moto Fest Caeté Moto Grupo",
            "short_name": "1º Moto Fest Caeté",
            "city": "Caeté",
            "venue": "Poliesportivo de Caeté",
            "last_updated": "2026-07-30",
            "duplicate_of": CANONICAL_SLUG,
            "canonical_url": f"/eventos/{CANONICAL_SLUG}/",
        }
    )

    AGENDA.write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"Evento atualizado: {CANONICAL_SLUG}")
    print(f"Rota duplicada consolidada: {DUPLICATE_SLUG}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
