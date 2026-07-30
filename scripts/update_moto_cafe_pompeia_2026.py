#!/usr/bin/env python3
"""Atualiza o 2º Moto Café de Pompeia com fontes verificadas."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENDA = ROOT / "content/events/agenda-comunitaria-2026.json"
SLUG = "2-moto-cafe-pompeia-sp-2026-08-02"


def main() -> int:
    document = json.loads(AGENDA.read_text(encoding="utf-8"))
    event = next(
        entry for entry in document.get("entries", []) if entry.get("slug") == SLUG
    )

    event.update(
        {
            "title": "2º Moto Café de Pompeia",
            "short_name": "2º Moto Café",
            "start_date": "2026-08-02",
            "end_date": "2026-08-02",
            "city": "Pompeia",
            "state": "SP",
            "venue": "Clube do JK",
            "status": "agendada",
            "event_type": "Moto café e encontro de motociclistas",
            "official_url": "https://www.instagram.com/roledosamigospompeia/",
            "source_url": "https://www.instagram.com/p/Da0cNG3JYIO/",
            "source_label": "Anúncio oficial do Rolê dos Amigos e Moto Café Pompeia",
            "verification_status": "servico_cruzado_com_publicacoes_oficiais",
            "cover": "/assets/img/competicoes-eventos-default.svg",
            "image_credit": "Arte: TVDUASRODAS",
            "free": False,
            "summary": (
                "O 2º Moto Café de Pompeia acontece no domingo, 2 de agosto de "
                "2026, a partir das 9h, no Clube do JK, com café gratuito para "
                "motociclistas, encontro sobre duas rodas e rock ao vivo com "
                "Danielle Dias — Rock & Road."
            ),
            "attractions": [
                "Café gratuito para motociclistas",
                "Danielle Dias — Rock & Road",
                "Rock ao vivo",
                "Confraternização de motociclistas",
                "Evento com orientação de zoeira zero",
            ],
            "body": (
                "## O evento\n\n"
                "O **2º Moto Café de Pompeia** será realizado no domingo, 2 de "
                "agosto de 2026, a partir das **9h**, no **Clube do JK**, em "
                "Pompeia/SP. O encontro é promovido pelo grupo Rolê dos Amigos e "
                "reúne café, motocicletas, amizade e rock ao vivo.\n\n"
                "A organização anuncia **café gratuito para motociclistas** durante "
                "a manhã. O material oficial também destaca a orientação **zoeira "
                "zero**, reforçando o caráter de confraternização do encontro.\n\n"
                "## Música ao vivo\n\n"
                "A atração confirmada é **Danielle Dias**, com a apresentação "
                "**Rock & Road** e repertório voltado ao rock. O horário individual "
                "do show e o encerramento do evento não foram divulgados nas "
                "publicações consultadas.\n\n"
                "## Programação\n\n"
                "- **9h:** início do 2º Moto Café\n"
                "- Café gratuito para motociclistas\n"
                "- Confraternização de motociclistas\n"
                "- Rock ao vivo com **Danielle Dias — Rock & Road**\n\n"
                "## Local\n\n"
                "**Clube do JK — Recanto Luiz Nogueira Ferraro, 38, Pompeia/SP, "
                "CEP 17580-000.** O endereço foi conferido em documento recente da "
                "Prefeitura de Pompeia.\n\n"
                "## Acesso e contato\n\n"
                "A divulgação confirma a gratuidade do café para motociclistas, mas "
                "não informa cobrança ou condição específica para entrada no local. "
                "Também não há orientação publicada sobre estacionamento. Para "
                "atualizações, consulte o perfil oficial **@roledosamigospompeia**.\n\n"
                "## Antes de sair\n\n"
                "Consulte as publicações do organizador próximo ao horário de saída "
                "para verificar eventuais mudanças no show, no acesso ao Clube do JK "
                "ou na programação da manhã."
            ),
            "last_updated": "2026-07-30",
            "timezone": "America/Sao_Paulo",
            "time_label": "Domingo, a partir das 9h; encerramento não divulgado",
            "street_address": "Recanto Luiz Nogueira Ferraro, 38",
            "postal_code": "17580-000",
            "full_address": (
                "Clube do JK, Recanto Luiz Nogueira Ferraro, 38, Pompeia - SP, "
                "CEP 17580-000, Brasil"
            ),
            "status_basis": (
                "Data, horário, local, café e atração musical confirmados nas "
                "publicações oficiais e cruzados com agenda independente."
            ),
            "status_checked_at": "2026-07-30",
            "organizer": "Rolê dos Amigos Pompeia",
            "contact": "Instagram: @roledosamigospompeia",
            "source_checked_at": "2026-07-30",
            "visual_verification": {
                "type": "publicacoes_e_artes_oficiais_inspecionadas_manualmente",
                "source_url": "https://www.instagram.com/p/Da0cNG3JYIO/",
                "detail_url": (
                    "https://www.instagram.com/roledosamigospompeia/"
                ),
                "checked_at": "2026-07-30",
                "review_policy": (
                    "Leitura manual das legendas, artes e publicações recentes "
                    "do perfil oficial do organizador"
                ),
                "confirmed_fields": [
                    "event_name",
                    "edition",
                    "date",
                    "start_time",
                    "city",
                    "state",
                    "venue",
                    "organizer",
                    "musical_attraction",
                    "free_coffee",
                    "conduct_rule",
                ],
            },
            "admission_status": (
                "Condição de entrada não informada; café gratuito para motociclistas"
            ),
            "parking": "Estacionamento não informado pela organização",
            "sources": [
                {
                    "url": "https://www.instagram.com/p/Da0cNG3JYIO/",
                    "label": "Rolê dos Amigos Pompeia — anúncio oficial",
                    "type": "publicação oficial do organizador",
                    "supports": (
                        "edição, data, horário, local, café gratuito e atração musical"
                    ),
                    "checked_at": "2026-07-30",
                },
                {
                    "url": (
                        "https://www.instagram.com/roledosamigospompeia/"
                    ),
                    "label": "Perfil oficial do Moto Café Pompeia",
                    "type": "canal do organizador",
                    "supports": (
                        "identidade do organizador, data, local, zoeira zero e "
                        "atualizações do evento"
                    ),
                    "checked_at": "2026-07-30",
                },
                {
                    "url": (
                        "https://www.instagram.com/roledosamigospompeia/"
                        "p/DaiXymlp6zO/"
                    ),
                    "label": "Moto Café Pompeia — atração confirmada",
                    "type": "publicação oficial de programação",
                    "supports": "Danielle Dias, Rock & Road e início às 9h",
                    "checked_at": "2026-07-30",
                },
                {
                    "url": (
                        "https://jb-rider.com.br/evento/"
                        "20260802-2-moto-cafe-pompeia-sp"
                    ),
                    "label": "JB-RIDER — 2 Moto Café Pompeia/SP",
                    "type": "agenda independente com página específica",
                    "supports": "data, cidade, estado e identidade do evento",
                    "checked_at": "2026-07-30",
                },
                {
                    "url": (
                        "https://www.pompeia.sp.gov.br/public/admin/globalarq/"
                        "licitacao/arquivo/ccd6adfc9e51fbf3c27eabee6d93362e.pdf"
                    ),
                    "label": "Prefeitura de Pompeia — relação de locais municipais",
                    "type": "documento oficial do município",
                    "supports": "endereço atual do Clube do JK",
                    "checked_at": "2026-07-30",
                },
                {
                    "url": (
                        "https://www.pompeia.sp.gov.br/portal/noticias/0/3/"
                        "9800/clube-do-jk"
                    ),
                    "label": "Prefeitura de Pompeia — Clube do JK",
                    "type": "página oficial do local",
                    "supports": "identidade e funcionamento recente do espaço",
                    "checked_at": "2026-07-30",
                },
            ],
            "research_status": {
                "required_specific_independent_sources": 2,
                "specific_independent_domains_found": 3,
                "status": "fontes_oficiais_cruzadas_com_agenda_e_local",
                "query": '"2º Moto Café" Pompeia SP 2026',
                "reviewed_at": "2026-07-30",
                "editorial_rule": (
                    "Serviço confirmado pelo organizador, cruzado com agenda "
                    "independente e documento oficial do local."
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
