#!/usr/bin/env python3
"""Completa o serviço do 25º Moto Fest Paranavaí."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENDA = ROOT / "content/events/agenda-comunitaria-2026.json"
CANONICAL_SLUG = "25-motofest-paranavai-pr-2026-09-04"


def main() -> int:
    document = json.loads(AGENDA.read_text(encoding="utf-8"))
    event = next(
        entry for entry in document.get("entries", [])
        if entry.get("slug") == CANONICAL_SLUG
    )

    event.update(
        {
            "title": "25º Moto Fest Paranavaí",
            "short_name": "Moto Fest Paranavaí",
            "start_date": "2026-09-04",
            "end_date": "2026-09-06",
            "city": "Paranavaí",
            "state": "PR",
            "country": "Brasil",
            "scope": "Nacional",
            "region": "Sul",
            "venue": "Parque de Exposições Presidente Arthur da Costa e Silva",
            "status": "agendada",
            "event_type": "Encontro de motociclistas e triciclistas",
            "segment": "Motos",
            "official_url": "https://www.instagram.com/p/DbR80tjuWdx/",
            "source_url": "https://www.instagram.com/p/DbR80tjuWdx/",
            "source_label": "Publicação oficial do Moto Fest Paranavaí",
            "verification_status": "anuncios_oficiais_inspecionados_e_fontes_cruzadas",
            "cover": "/assets/img/uploads/paranavai-motofest-2026-artwork.svg",
            "image_credit": "Arte: TVDUASRODAS",
            "featured": False,
            "free": False,
            "summary": (
                "O 25º Moto Fest Paranavaí será realizado de 4 a 6 de setembro "
                "de 2026, no Parque de Exposições de Paranavaí/PR. O perfil "
                "oficial já confirmou atrações como Ratos de Bar, Arde Rock, "
                "West Valmets, Hillbilly Rawhide e The Beast Experience; a grade "
                "por dia e os horários ainda serão divulgados."
            ),
            "attractions": [
                "Ratos de Bar",
                "Arde Rock",
                "West Valmets",
                "Hillbilly Rawhide",
                "The Beast Experience — tributo ao Iron Maiden",
                "Tennessee",
                "DeepStrong",
                "Estação X",
                "Motores Ácidos",
                "Systemáticos",
                "Immortal Grunge",
                "Flash Black — tributos a Queen e ABBA",
                "Alta Voltagem — tributo ao AC/DC",
                "Tributo ao Guns N’ Roses",
                "Mamonas Assassinas Cover",
                "4º Concurso de Cosplay",
                "Show de wheeling",
                "Show com robô de LED",
                "Costelão ao fogo de chão",
            ],
            "body": (
                "## O que está confirmado\n\n"
                "O **25º Moto Fest Paranavaí** acontece na sexta-feira, 4 de "
                "setembro, no sábado, 5, e no domingo, 6 de setembro de 2026. "
                "O local confirmado é o **Parque de Exposições Presidente Arthur "
                "da Costa e Silva**, em Paranavaí/PR.\n\n"
                "A edição celebra **25 anos** do encontro, apresentado pelo "
                "organizador como um evento nacional de motociclistas e "
                "triciclistas. O perfil oficial informa que a programação por "
                "dia e os horários completos ainda serão divulgados.\n\n"
                "## Atrações anunciadas pelo perfil oficial\n\n"
                "As publicações do organizador já confirmaram **Ratos de Bar**, "
                "**Arde Rock**, **West Valmets**, **Hillbilly Rawhide** e "
                "**The Beast Experience**, tributo ao Iron Maiden. Os anúncios "
                "foram publicados separadamente e ainda não distribuem as bandas "
                "entre sexta, sábado e domingo.\n\n"
                "Uma agenda especializada atualizada para a edição de 2026 "
                "também lista **Tennessee, DeepStrong, Estação X, Motores Ácidos, "
                "Systemáticos, Immortal Grunge, Flash Black**, com tributos a "
                "Queen e ABBA, **Alta Voltagem**, com tributo ao AC/DC, um tributo "
                "ao Guns N’ Roses e **Mamonas Assassinas Cover**. Esses nomes "
                "devem ser reconfirmados na grade final do organizador.\n\n"
                "## Estrutura e atividades\n\n"
                "A mesma agenda especializada informa **4º Concurso de Cosplay**, "
                "**show de wheeling**, apresentação com **robô de LED**, praça de "
                "alimentação, segurança 24 horas, banheiros masculinos e femininos "
                "com chuveiro, estacionamento para motos e o tradicional costelão "
                "ao fogo de chão. Horários e regras de participação dessas "
                "atividades ainda não aparecem nos anúncios oficiais consultados.\n\n"
                "## Ingressos e camping\n\n"
                "A agenda Moto Eventos MS informa ingresso de **R$ 50**. A "
                "publicação oficial usada como fonte principal não especifica se "
                "o valor é um passaporte para os três dias, nem informa lotes ou "
                "pontos de venda; confirme diretamente com o evento antes de "
                "pagar ou viajar.\n\n"
                "Não foi localizada confirmação atual sobre área de camping para "
                "2026. Embora edições anteriores tenham oferecido camping e café "
                "da manhã, esses serviços não foram presumidos para esta edição.\n\n"
                "## Local e contatos\n\n"
                "O Parque de Exposições fica às margens da **BR-376**, na região "
                "da Zona 11, em Paranavaí. O endereço do recinto foi cruzado com "
                "o calendário da Secretaria do Turismo do Paraná.\n\n"
                "Contatos divulgados no cartaz oficial: **Borracha, "
                "(44) 99917-2121**, e **Roberta, (44) 99901-1311**. Acompanhe "
                "também o perfil "
                "[@motofestpvai](https://www.instagram.com/motofestpvai/) para a "
                "grade definitiva, horários e orientações de acesso."
            ),
            "last_updated": "2026-07-30",
            "timezone": "America/Sao_Paulo",
            "time_label": "Programação por dia e horários ainda não divulgados",
            "street_address": "BR-376, Zona 11",
            "neighborhood": "Zona 11",
            "full_address": (
                "Parque de Exposições Presidente Arthur da Costa e Silva, "
                "BR-376, Zona 11, Paranavaí - PR"
            ),
            "status_basis": (
                "Edição, datas, cidade, local e atrações confirmados em anúncios "
                "recentes do perfil oficial; dados operacionais complementares "
                "atribuídos à agenda especializada."
            ),
            "status_checked_at": "2026-07-30",
            "organizer": "Equipe Moto Fest Paranavaí",
            "contact": (
                "Borracha: (44) 99917-2121 • Roberta: (44) 99901-1311 • "
                "Instagram: @motofestpvai"
            ),
            "source_checked_at": "2026-07-30",
            "visual_verification": {
                "type": "publicacoes_oficiais_inspecionadas_manualmente",
                "source_url": "https://www.instagram.com/p/DbR80tjuWdx/",
                "detail_url": "https://www.instagram.com/motofestpvai/",
                "checked_at": "2026-07-30",
                "review_policy": (
                    "Leitura manual da legenda, do cartaz e do perfil oficial; "
                    "dados de terceiros mantidos com atribuição e ressalva"
                ),
                "confirmed_fields": [
                    "edition",
                    "start_date",
                    "end_date",
                    "city",
                    "state",
                    "venue",
                    "official_profile",
                    "contacts",
                    "officially_announced_attractions",
                ],
            },
            "admission_status": (
                "R$ 50 segundo a agenda Moto Eventos MS; formato do ingresso, "
                "lotes e venda devem ser confirmados com a organização"
            ),
            "parking": (
                "Estacionamento para motos informado pela agenda especializada; "
                "regras e capacidade não divulgadas"
            ),
            "sources": [
                {
                    "url": "https://www.instagram.com/p/DbR80tjuWdx/",
                    "label": (
                        "Moto Fest Paranavaí — anúncio oficial de Ratos de Bar"
                    ),
                    "type": "fonte primária do organizador",
                    "supports": (
                        "25ª edição, datas, local, Ratos de Bar e contatos"
                    ),
                    "checked_at": "2026-07-30",
                },
                {
                    "url": "https://www.instagram.com/motofestpvai/",
                    "label": "Moto Fest Paranavaí — perfil oficial",
                    "type": "canal do organizador",
                    "supports": (
                        "datas, identidade, West Valmets, Hillbilly Rawhide, "
                        "The Beast Experience, Arde Rock e comunicados recentes"
                    ),
                    "checked_at": "2026-07-30",
                },
                {
                    "url": "https://sites.google.com/view/motoeventosms/agenda-ms",
                    "label": "Moto Eventos MS — agenda 2026",
                    "type": "agenda independente especializada",
                    "supports": (
                        "datas, endereço, valor informado, estrutura, atividades "
                        "e relação complementar de atrações"
                    ),
                    "checked_at": "2026-07-30",
                },
                {
                    "url": (
                        "https://www.turismo.pr.gov.br/Evento/Effeta-2026"
                    ),
                    "label": (
                        "Secretaria do Turismo do Paraná — referência do recinto"
                    ),
                    "type": "fonte institucional pública",
                    "supports": (
                        "nome oficial do Parque de Exposições e localização na "
                        "BR-376, em Paranavaí"
                    ),
                    "checked_at": "2026-07-30",
                },
                {
                    "url": (
                        "https://jb-rider.com.br/evento/"
                        "20260904-3-25-motofest-paranavai-pr"
                    ),
                    "label": "JB-RIDER — 25º Motofest Paranavaí",
                    "type": "agenda independente com página específica",
                    "supports": "edição, datas, cidade e estado",
                    "checked_at": "2026-07-30",
                },
            ],
            "research_status": {
                "required_specific_independent_sources": 2,
                "specific_independent_domains_found": 5,
                "status": "fonte_primaria_e_fontes_independentes_cruzadas",
                "query": '"25º Moto Fest Paranavaí" 2026',
                "reviewed_at": "2026-07-30",
                "editorial_rule": (
                    "Fatos do canal oficial tratados como confirmados; valor, "
                    "estrutura e atrações adicionais atribuídos à agenda "
                    "especializada; grade por dia mantida como pendente."
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
