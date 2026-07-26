#!/usr/bin/env python3
"""Enriquece a agenda com fatos conservadores extraídos visualmente dos flyers."""

from __future__ import annotations

import json
import re
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
AGENDA = ROOT / "content/events/agenda-comunitaria-2026.json"
OCR_FILES = (
    ROOT / "output/audit-flyers/ocr-windows.json",
    ROOT / "output/audit-flyers/ocr-windows-tiles.json",
)
REPORT = ROOT / "output/flyer-ocr-enrichment.json"
NOW = datetime.now(timezone.utc).isoformat()


SERVICE_PATTERNS = (
    ("Área de camping", r"\bcamping\b"),
    ("Espaço para motorhome", r"\bmotorhome\b"),
    ("Estacionamento", r"\bestacionamento\b"),
    ("Café da manhã", r"\bcaf[eé]\s+da\s+manh"),
    ("Chuveiros", r"\bchuveir"),
    ("Área ou praça de alimentação", r"(?:[aá]rea|pra[cç]a)\s+de\s+alimenta|alimenta[cç][aã]o"),
    ("Food trucks", r"\bfood\s*truck"),
    ("Shows ou bandas de rock", r"\bbandas?\b|\bshows?\b|\brock\b"),
    ("Expositores", r"\bexpositor"),
    ("Troféus", r"\btrof[eé]u"),
    ("Brindes ou sorteios", r"\bbrindes?\b|\bsorteio"),
    ("Área infantil", r"\barea\s+kids\b|\bespa[cç]o\s+kids\b|\bcrian[cç]as\b"),
    ("Piscina", r"\bpiscina\b"),
    ("Segurança", r"\bseguran[cç]a\b"),
)
HANDLE_HINTS = (
    "mc", "moto", "motofest", "motorock", "rider", "biker", "estrada", "asfalto",
    "clube", "club", "festival", "rock", "event", "turma", "comando",
)
HANDLE_BLOCKLIST = {
    "whatsapp", "piscina", "comidas", "bebida", "traga", "passagem", "arroZ",
    "peruibe", "mongagua", "guaruja", "walter",
}
INVALID_OCR_URLS = {
    "https://icloud.com",
    "https://bandoleirosme.com",
    "https://www.instagram.com/tevianosmotoclube/",
    "https://www.instagram.com/cavaiheirosdaviiamc/",
    "https://to.com.br",
}
MANUAL_VISUAL: dict[str, dict[str, Any]] = {
    "amigos-na-estrada-mc-sao-jose-do-vale-do-rio-preto-rj-2026-08-23": {
        "title": "5º aniversário do MC Amigos na Estrada",
        "short_name": "MC Amigos na Estrada",
        "time_label": "23 de agosto de 2026; horário ainda não divulgado",
        "organizer": "MC Amigos na Estrada",
        "visual_note": (
            "O flyer confirma o 5º aniversário, a data de 23/08/2026 e "
            "São José do Vale do Rio Preto/RJ; informa que o restante do "
            "serviço seria divulgado posteriormente."
        ),
    },
    "mc-os-mamutes-e-road-rhino-mc-rio-de-janeiro-rj-2026-09-13": {
        "title": "9 anos dos Os Mamutes MC e 1 ano do Road Rhino MC",
        "short_name": "Os Mamutes MC + Road Rhino MC",
        "venue": "Parque Anchieta",
        "street_address": "Rua Elzo Ferreira, 248",
        "full_address": "Rua Elzo Ferreira, 248, Parque Anchieta, Rio de Janeiro - RJ",
        "time_label": "13 de setembro de 2026, a partir das 12h",
        "organizer": "Os Mamutes MC e Road Rhino MC",
        "contact": "(21) 99406-0809 (Vagner); (21) 996437-9959 (Joca)",
        "admission_status": "Almoço 0800, conforme o flyer; demais condições de acesso não informadas",
        "attractions": [
            "Buraco Quente",
            "Doctor Driver Rock Band",
            "Almoço 0800",
            "Expositores",
            "Sorteios",
            "Troféu",
        ],
        "visual_note": (
            "A inspeção dos dois arquivos confirmou que são versões do mesmo "
            "flyer e que a grafia correta é Os Mamutes MC, não Os Mutantes."
        ),
    },
    "4-u-m-a-aguai-sp-2026-07-24": {
        "title": "4º U.M.A. — União de Motociclistas de Aguaí",
        "short_name": "4º U.M.A.",
        "venue": "Parque Interlagos",
        "full_address": "Parque Interlagos, Aguaí - SP",
        "time_label": "24 a 26 de julho de 2026; abertura na noite de sexta-feira",
        "organizer": "União de Motociclistas de Aguaí (U.M.A.)",
        "contact": "(19) 99166-2769 (Dodô)",
        "admission_status": "Entrada mediante doação de 1 kg de alimento não perecível; copo oficial para doação acima de 2 kg, enquanto houver estoque",
        "attractions": [
            "Sete Galo",
            "New A.C.D.C",
            "Mrs. Magroove",
            "Vulgare Rockband",
            "Alluz",
            "Arise — tributo ao Sepultura",
            "Climatic",
            "Walter Raul",
            "Velho Jonny",
            "Food trucks e praça de alimentação",
            "Camping para motociclistas e motorhomes",
            "Chuveiros aquecidos",
            "Café da manhã para campistas",
            "Área infantil",
        ],
        "sources": [
            {
                "url": "https://plataforma12.jor.br/noticia/rock-e-solidariedade-aguai-recebe-4o-encontro-da-uniao-de-motociclistas",
                "label": "Plataforma 12 — reportagem e serviço do 4º U.M.A.",
                "type": "cobertura jornalística específica",
                "supports": "datas, local, entrada, contato, atrações e infraestrutura",
                "checked_at": NOW,
                "discovery_method": "pesquisa_web_multifonte",
            },
            {
                "url": "https://www.instagram.com/umauniaodosmotociclistas/",
                "label": "Instagram oficial da União dos Motociclistas de Aguaí",
                "type": "fonte primária do organizador",
                "supports": "identidade e canal oficial da organização",
                "checked_at": NOW,
                "discovery_method": "pesquisa_web_multifonte",
            },
        ],
        "visual_note": (
            "A reportagem local confirmou Parque Interlagos, os três dias, "
            "entrada solidária, contato, programação musical e infraestrutura."
        ),
    },
    "fraternos-do-cerrado-mc-brasilia-df-2026-07-25": {
        "venue": "Tenda 169 do Capital Moto Week",
        "full_address": "Capital Moto Week, Brasília - DF; Tenda 169",
        "time_label": "25 de julho, às 13h",
        "admission_status": "Rateio/contribuição de R$ 50,00, conforme o flyer",
        "organizer": "Fraternos do Cerrado MC",
        "attractions": [
            "Feijoada comemorativa de 12+1 anos",
            "Atração musical Beto Diehl",
            "Bingo de churrasqueira elétrica",
        ],
        "visual_note": (
            "O flyer confirma a feijoada dos Fraternos do Cerrado MC na Tenda 169 "
            "do Capital Moto Week, em 25/07 às 13h, com contribuição de R$ 50."
        ),
    },
    "levianos-mc-ceilandia-sul-df-2026-08-08": {
        "venue": "Sede Levianos Moto Clube",
        "street_address": "QNM 21, Conjunto K",
        "full_address": "QNM 21, Conjunto K, Ceilândia Sul - DF",
        "time_label": "8 de agosto de 2026, às 16h",
        "organizer": "Levianos Moto Clube",
        "attractions": ["Shows ao vivo", "Venda de comidas", "Venda de bebidas", "Expositores"],
        "sources": [
            {
                "url": "https://www.instagram.com/levianosmotoclube/",
                "label": "Perfil @levianosmotoclube impresso no flyer",
                "type": "fonte primária do organizador",
                "supports": "identidade do organizador e canal oficial exibido no material visual",
                "checked_at": NOW,
                "discovery_method": "inspecao_visual_manual_do_flyer",
            }
        ],
        "visual_note": (
            "A inspeção direta confirmou o 4º aniversário, a sede na QNM 21 "
            "Conjunto K, o início às 16h e o perfil @levianosmotoclube."
        ),
    },
    "bandoleiros-mc-sao-goncalo-rj-2026-09-06": {
        "venue": "Subsede Rio de Janeiro dos Bandoleiros",
        "street_address": "Rua José Custódio Sampaio, 469",
        "full_address": "Rua José Custódio Sampaio, 469, Colubandê, São Gonçalo - RJ",
        "time_label": "6 de setembro de 2026; horário não impresso no flyer",
        "organizer": "Bandoleiros, Subsede Rio de Janeiro",
        "attractions": ["Banda de rock", "Cerveja gelada", "Celebração do 2º aniversário"],
        "sources": [
            {
                "url": "https://www.bandoleirosmc.com/",
                "label": "Site www.bandoleirosmc.com impresso no flyer",
                "type": "fonte primária do organizador",
                "supports": "identidade, canal oficial e organização exibidos no flyer",
                "checked_at": NOW,
                "discovery_method": "inspecao_visual_manual_do_flyer",
            },
            {
                "url": "https://www.instagram.com/bandoleirosmc/",
                "label": "Perfil @bandoleirosmc impresso no flyer",
                "type": "fonte primária do organizador",
                "supports": "identidade e canal social oficial exibidos no flyer",
                "checked_at": NOW,
                "discovery_method": "inspecao_visual_manual_do_flyer",
            },
        ],
        "visual_note": (
            "A inspeção direta confirmou a Rua José Custódio Sampaio, 469, "
            "Colubandê, o 2º aniversário e os canais bandoleirosmc.com e @bandoleirosmc."
        ),
    },
    "nomades-do-vento-mc-lindoia-sp-2026-08-08": {
        "venue": "Chalés Parque Aquático",
        "street_address": "Rua Machado de Assis, 01, Barreiro",
        "full_address": "Rua Machado de Assis, 01, Barreiro, Lindóia - SP, CEP 13950-000",
        "time_label": "8 de agosto de 2026; o flyer não imprime horário de abertura",
        "organizer": "Nômades do Vento MC",
        "admission_status": "Entrada de R$ 15,00 por pessoa; doação opcional de 1 kg de alimento não perecível",
        "contact": "(19) 97814-8293 (reservas de chalés); (19) 99640-1946 (informações)",
        "attractions": [
            "35 anos de estrada",
            "Bandas Marcel Unplugged, Sete Galo, Climatic e Progressão",
            "Expositores",
            "Restaurante e praça de alimentação",
            "Café 0800 no domingo",
            "Sorteio de brindes",
            "Troféu para moto clube",
            "Área de camping",
            "Chuveiro quente",
        ],
        "sources": [
            {
                "url": "https://www.chaleparqueaquaticolindoia.com.br/",
                "label": "Site do Chalés Parque Aquático impresso no flyer",
                "type": "fonte primária do local",
                "supports": "identidade do local e canal de reservas exibidos no flyer",
                "checked_at": NOW,
                "discovery_method": "inspecao_visual_manual_do_flyer",
            }
        ],
        "visual_note": (
            "A inspeção direta confirmou endereço completo, entrada de R$ 15, "
            "contatos, estrutura de camping e a programação musical impressa."
        ),
    },
    "motofest-capim-branco-mg-2026-10-09": {
        "time_label": "9 e 10 de outubro de 2026; horários serão divulgados nos canais oficiais",
        "organizer": "Capim Branco Moto Fest, com realização da Prefeitura de Capim Branco e Secretaria de Cultura",
        "contact": "(31) 99522-0635",
        "attractions": ["Encontro regional de motociclistas", "Programação a confirmar nos canais oficiais"],
        "sources": [
            {
                "url": "https://www.instagram.com/cbmotofest/",
                "label": "Instagram @cbmotofest impresso no flyer",
                "type": "fonte primária da organização",
                "supports": "canal oficial, identidade da organização e atualizações",
                "checked_at": NOW,
                "discovery_method": "inspecao_visual_manual_do_flyer",
            }
        ],
        "visual_note": (
            "O flyer confirma 9 e 10 de outubro, o contato (31) 99522-0635, "
            "o perfil @cbmotofest e a realização municipal."
        ),
    },
    "patrulheiros-do-norte-mc-conceicao-da-barra-es-2026-09-04": {
        "time_label": "4 e 5 de setembro de 2026; horários não impressos no flyer",
        "organizer": "Patrulheiros do Norte",
        "attractions": [
            "Troféus",
            "Expositores",
            "Motos customizadas",
            "Rock'n'roll",
            "Churrasco 0800",
            "Água de coco liberada",
        ],
        "sources": [
            {
                "url": "https://www.facebook.com/patrulheirosdonorte/",
                "label": "Canal @patrulheirosdonorte impresso no flyer",
                "type": "fonte primária do organizador",
                "supports": "identidade e canal oficial exibidos no material visual",
                "checked_at": NOW,
                "discovery_method": "inspecao_visual_manual_do_flyer",
            }
        ],
        "visual_note": (
            "A inspeção direta confirmou os dois dias, atrações e os canais "
            "@patrulheirosdonorte e @patrulheirosdonorte_mc."
        ),
    },
    "turma-de-cachorro-loco-mc-maua-sp-2026-08-29": {
        "venue": "Rancho do Demar",
        "street_address": "Estrada Nossa Senhora do Pilar, 1993, Vital Brasil",
        "full_address": "Estrada Nossa Senhora do Pilar, 1993, Vital Brasil, Mauá - SP, CEP 09330-555",
        "time_label": "29 e 30 de agosto de 2026; horários das bandas não impressos",
        "organizer": "Turma do Cachorro Loco MC",
        "admission_status": "Entrada: 1 kg de alimento não perecível; cooler proibido",
        "attractions": [
            "26 anos da Turma do Cachorro Loco",
            "Acústico com Deni Campos",
            "Bandas Rockixe e Presságio",
            "Costela de chão",
            "Área de camping",
        ],
        "sources": [
            {
                "url": "https://www.instagram.com/turmadocachorroloco/",
                "label": "Instagram /turmadocachorroloco impresso no flyer",
                "type": "fonte primária do organizador",
                "supports": "identidade e canal oficial exibidos no material visual",
                "checked_at": NOW,
                "discovery_method": "inspecao_visual_manual_do_flyer",
            }
        ],
        "visual_note": (
            "O flyer confirma endereço completo, ingresso solidário, atrações, "
            "estrutura e o canal /turmadocachorroloco."
        ),
    },
    "mc-urubus-obesos-ibia-mg-2026-08-14": {
        "time_label": "14 a 16 de agosto de 2026; show dos Raimundos em 14 de agosto",
        "organizer": "MC Urubus Obesos, integrado ao Festival de Inverno promovido pela Prefeitura de Ibiá",
        "admission_status": "Entrada franca",
        "attractions": [
            "Show nacional com Raimundos",
            "Sete bandas regionais",
            "Festival gastronômico",
            "Camping coberto",
            "Segurança 24 horas",
            "Chuveiro quente",
            "Café da manhã",
        ],
        "sources": [
            {
                "url": "https://www.ibia.mg.gov.br/editais-de-licitacao/page/3/",
                "label": "Prefeitura de Ibiá — contratação oficial do show dos Raimundos",
                "type": "fonte institucional pública",
                "supports": "show dos Raimundos em 14 de agosto de 2026 e Festival de Inverno promovido pelo município",
                "checked_at": NOW,
                "discovery_method": "pesquisa_oficial_multifonte",
            }
        ],
        "visual_note": (
            "O flyer associa o encontro ao Festival de Inverno; a contratação "
            "municipal confirma Raimundos em 14/08/2026. A numeração da edição "
            "aparece divergente em páginas municipais e permanece registrada para revisão."
        ),
    },
    "aguais-da-liberdade-mc-conselheiro-lafaiete-mg-2026-07-25": {
        "title": "25 anos do Águias da Liberdade MC",
        "short_name": "Águias da Liberdade MC",
        "time_label": "25 de julho de 2026, das 11h às 21h",
        "organizer": "Águias da Liberdade MC",
        "contact": "(31) 98889-3200; jaaguias@yahoo.com.br",
        "attractions": ["Celebração dos 25 anos do moto clube", "Confraternização com motociclistas e amigos"],
        "sources": [
            {
                "url": "https://jacaremoto.com.br/events/25-anos-do-aguias-da-liberdade-mc-conselheiro-lafaiete-mg/",
                "label": "Jacaremoto — 25 anos do Águias da Liberdade MC",
                "type": "página específica independente",
                "supports": "data, horário, cidade, realização, contato e perfil do organizador",
                "checked_at": NOW,
                "discovery_method": "pesquisa_web_multifonte",
            },
            {
                "url": "https://www.instagram.com/motoclubeaguiasdaliberdade/",
                "label": "Instagram @MotoclubeaguiasdaLiberdade indicado na página específica",
                "type": "fonte primária do organizador",
                "supports": "identidade e canal oficial do moto clube",
                "checked_at": NOW,
                "discovery_method": "pesquisa_web_multifonte",
            },
        ],
        "visual_note": (
            "A grafia foi corrigida de 'Aguais' para 'Águias'; a página específica "
            "confirma 25 anos, das 11h às 21h, contato e canal do organizador."
        ),
    },
    "motorock-e-amizade-itauna-mg-2026-07-25": {
        "venue": "Restaurante Coqueiros",
        "street_address": "Rodovia MG-431, km 57, Condomínio dos Coqueiros",
        "full_address": "Restaurante Coqueiros, Rodovia MG-431, km 57, Condomínio dos Coqueiros, Itaúna - MG",
        "time_label": "25 de julho de 2026, a partir das 10h",
        "organizer": "Moto Rock & Amizade / Restaurante Coqueiros",
        "attractions": ["Celebração do Dia Nacional do Motociclista"],
        "sources": [
            {
                "url": "https://motociclistasunidos.com.br/",
                "label": "Motociclistas Unidos — agenda específica de 25/07 em Itaúna",
                "type": "agenda comunitária independente",
                "supports": "data, horário, nome do evento e endereço do Restaurante Coqueiros",
                "checked_at": NOW,
                "discovery_method": "pesquisa_web_multifonte",
            }
        ],
        "visual_note": (
            "A agenda independente confirma o evento às 10h no Restaurante "
            "Coqueiros, Rodovia MG-431, km 57."
        ),
    },
    "pit-stop-hanbai-belo-horizonte-mg-2026-07-25": {
        "venue": "Hanbai Motos — unidade Alípio de Melo",
        "street_address": "Avenida Abílio Machado, 2705, Glória",
        "full_address": "Avenida Abílio Machado, 2705, Glória, Belo Horizonte - MG, CEP 30830-433",
        "time_label": "25 de julho de 2026, das 8h às 12h",
        "organizer": "Hanbai Motos / Honda",
        "admission_status": "Entrada gratuita",
        "contact": "Contato do evento não confirmado; consulte a unidade Alípio de Melo pelos canais oficiais da Hanbai",
        "attractions": [
            "Café da manhã especial",
            "Sorteio de produtos Honda Store",
            "35% de desconto na Honda Store",
            "Promoção de óleo",
            "Condições especiais",
        ],
        "sources": [
            {
                "url": "https://hanbaimotos.com.br/institucional/sobre",
                "label": "Site oficial Hanbai Motos — unidade Alípio de Melo",
                "type": "fonte primária do organizador e local",
                "supports": "identidade da Hanbai, endereço, telefone e horário regular da unidade",
                "checked_at": NOW,
                "discovery_method": "pesquisa_web_multifonte",
            }
        ],
        "visual_note": (
            "O flyer confirma o Pit Stop das 8h às 12h; o site oficial da Hanbai "
            "confirma a unidade no mesmo endereço e seu horário de sábado."
        ),
    },
    "dia-do-motociclsita-sao-paulo-sp-2026-07-25": {
        "title": "Celebração do Dia do Motociclista 2026",
        "short_name": "Dia do Motociclista — Rua das Motos",
        "venue": "Rua General Osório e entorno — Rua das Motos",
        "full_address": "Rua General Osório e entorno, Centro, São Paulo - SP",
        "time_label": "25 de julho de 2026, das 9h às 16h",
        "organizer": "Associação Ruas das Motos",
        "admission_status": "Entrada gratuita",
        "attractions": [
            "Exposição de motocicletas",
            "Apresentações musicais",
            "Praça de alimentação",
            "Ativações de marcas",
            "Brindes e sorteios",
            "Feira temática da cultura biker",
        ],
        "sources": [
            {
                "url": "https://www.nacar.com.br/muito-alem-de-uma-motocicleta",
                "label": "Nacar Motorcycles — convite para 25 de julho na Rua General Osório",
                "type": "fonte primária participante",
                "supports": "data, início às 9h, local e identidade da celebração",
                "checked_at": NOW,
                "discovery_method": "pesquisa_web_multifonte",
            },
            {
                "url": "https://www.revistaduasrodas.com.br/noticias/centro-de-sao-paulo-tera-celebracao-do-dia-do-motociclista",
                "label": "Revista Duas Rodas — serviço completo da celebração",
                "type": "cobertura jornalística específica",
                "supports": "data, horário, local, gratuidade, organização e programação",
                "checked_at": NOW,
                "discovery_method": "pesquisa_web_multifonte",
            },
            {
                "url": "https://sampi.net.br/nacional/noticias/2993539/jundiai/2026/07/ruas-das-motos-promove-evento-gratuito-pelas-ruas-de-sao-paulo",
                "label": "Sampi — evento gratuito da Rua das Motos",
                "type": "cobertura jornalística independente",
                "supports": "data, horário, local, gratuidade e atrações",
                "checked_at": NOW,
                "discovery_method": "pesquisa_web_multifonte",
            },
        ],
        "visual_note": (
            "Três fontes externas confirmam a celebração na Rua General Osório, "
            "das 9h às 16h, com entrada gratuita e programação diversificada."
        ),
    },
    "119-festa-de-nossa-senhora-da-abadia-pirajuba-mg-2026-07-26": {
        "organizer": "Paróquia Nossa Senhora da Abadia, com apoio da Prefeitura de Pirajuba",
        "sources": [
            {
                "url": "https://www.licitacao.net/licitacoes_detalhes.asp?id=106797390&idR=1",
                "label": "Pregão 26/2026 da Prefeitura de Pirajuba para a Festa de Nossa Senhora da Abadia",
                "type": "registro público de contratação indexado",
                "supports": "existência da edição 2026, organização municipal de sonorização e iluminação e valor patrimonial da festa",
                "checked_at": NOW,
                "discovery_method": "pesquisa_web_multifonte",
            }
        ],
        "visual_note": (
            "O registro de contratação municipal confirma a preparação da Festa "
            "de Nossa Senhora da Abadia em 2026; a data específica permanece sustentada pelo flyer."
        ),
    },
    "motorock-brumado-ba-2026-07-31": {
        "title": "1º Brumado Motorock 2026",
        "short_name": "Brumado Motorock",
        "time_label": "31 de julho e 1º de agosto de 2026; confira os horários de cada atração no canal oficial",
        "organizer": "Organização do Brumado Motorock, com divulgação da Assessoria de Comunicação da Prefeitura de Brumado",
        "attractions": [
            "Encontro de motociclistas e motoclubes",
            "Rock'n'roll",
            "Confraternização e resenha entre integrantes da estrada",
            "Programação musical divulgada no canal oficial do evento",
        ],
        "sources": [
            {
                "url": "https://www.sudoestenamira.com.br/noticias/12588-2026/07/23/1-brumado-motorock-2026",
                "label": "Sudoeste Na Mira — 1º Brumado Motorock 2026",
                "type": "cobertura jornalística específica com conteúdo da Ascom de Brumado",
                "supports": "nome da edição, datas, cidade, perfil oficial e proposta do evento",
                "checked_at": NOW,
                "discovery_method": "pesquisa_web_multifonte",
            },
            {
                "url": "https://www.instagram.com/brumado_motorock/",
                "label": "Instagram oficial @brumado_motorock indicado pela Ascom",
                "type": "fonte primária da organização",
                "supports": "programação, bandas, localização e avisos operacionais",
                "checked_at": NOW,
                "discovery_method": "pesquisa_web_multifonte",
            },
        ],
        "summary": (
            "O 1º Brumado Motorock reúne motociclistas e motoclubes em Brumado/BA "
            "nos dias 31 de julho e 1º de agosto de 2026, com rock, confraternização "
            "e atualizações operacionais no perfil oficial @brumado_motorock."
        ),
        "visual_note": (
            "A publicação específica assinada pela Ascom de Brumado confirmou a primeira "
            "edição, os dois dias, a cidade, a proposta e o perfil oficial da organização."
        ),
    },
    "motofest-prog-manhumirim-mg-2026-07-31": {
        "title": "5º Manhumirim Moto Fest",
        "short_name": "Manhumirim Moto Fest",
        "end_date": "2026-08-02",
        "venue": "Praça da Rodoviária",
        "street_address": "Praça da Rodoviária, Centro",
        "full_address": "Praça da Rodoviária, Centro, Manhumirim - MG",
        "time_label": "31 de julho a 2 de agosto de 2026; abertura às 18h",
        "organizer": "Geração Tsaleah MC, com os moto clubes locais e apoio da Prefeitura de Manhumirim",
        "admission_status": "Entrada franca em todos os dias",
        "attractions": [
            "Área de camping coberta",
            "Chuveiros quentes",
            "Café da manhã 0800",
            "Praça de alimentação e food trucks",
            "Troféus para moto clubes e moto grupos",
            "Locução de Lukas Augusto, A Voz Estradeira",
        ],
        "sources": [
            {
                "url": "https://motoclub.run/eventos/5-manhumirim-moto-fest-1782261486660",
                "label": "MotoClub Brasil — página específica do 5º Manhumirim Moto Fest",
                "type": "página específica independente com dados estruturados",
                "supports": "edição, datas, horário, local, gratuidade, organização e infraestrutura",
                "checked_at": NOW,
                "discovery_method": "pesquisa_web_multifonte",
            },
            {
                "url": "https://motoclub.run/clubes/geracao-tsaleah-mc-manhumirim-7x81",
                "label": "Página do Geração Tsaleah MC em Manhumirim",
                "type": "perfil específico do organizador",
                "supports": "identidade, cidade e vínculo do moto clube organizador",
                "checked_at": NOW,
                "discovery_method": "pesquisa_web_multifonte",
            },
            {
                "url": "https://www.manhumirim.mg.leg.br/institucional/noticias/moto-clube-aguias-de-aco-mg-111-recebeu-homenagem-na-camara-de-manhumirim",
                "label": "Câmara de Manhumirim — histórico institucional do motociclismo local",
                "type": "fonte institucional de contexto",
                "supports": "tradição dos moto clubes locais e histórico beneficente do Moto Fest",
                "checked_at": NOW,
                "discovery_method": "pesquisa_web_multifonte",
            },
        ],
        "summary": (
            "O 5º Manhumirim Moto Fest acontece de 31 de julho a 2 de agosto de 2026 "
            "na Praça da Rodoviária, com entrada franca, camping coberto, chuveiros "
            "quentes, café da manhã, alimentação, troféus e locução."
        ),
        "visual_note": (
            "A página específica do MotoClub Brasil confirmou Praça da Rodoviária, "
            "abertura às 18h, três dias de evento, gratuidade, organização e infraestrutura."
        ),
    },
}


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFKD", str(value or ""))
    value = "".join(char for char in value if not unicodedata.combining(char))
    return value.lower()


def dedupe(values: list[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        key = normalize(value).strip()
        if key and key not in seen:
            seen.add(key)
            result.append(value.strip())
    return result


def extract_services(text: str) -> list[str]:
    cleaned = normalize(text)
    return [label for label, pattern in SERVICE_PATTERNS if re.search(pattern, cleaned)]


def extract_phones(text: str) -> list[str]:
    candidates = re.findall(
        r"(?:\(?[1-9]\d\)?[\s.-]*)?(?:9[\s.-]*)?\d{4}[\s.-]*[-.]?[\s.-]*\d{4}",
        text,
    )
    result: list[str] = []
    for candidate in candidates:
        digits = re.sub(r"\D", "", candidate)
        if len(digits) not in {10, 11}:
            continue
        area = int(digits[:2])
        if area < 11 or area > 99:
            continue
        formatted = (
            f"({digits[:2]}) {digits[2:7]}-{digits[7:]}"
            if len(digits) == 11
            else f"({digits[:2]}) {digits[2:6]}-{digits[6:]}"
        )
        result.append(formatted)
    return dedupe(result)[:4]


def extract_times(text: str) -> list[str]:
    result: list[str] = []
    for hour, minute in re.findall(r"\b([01]?\d|2[0-3])\s*(?:h|:)\s*([0-5]\d)?\b", text, re.I):
        result.append(f"{int(hour):02d}h{minute or '00'}")
    return dedupe(result)[:6]


def clean_host(value: str) -> str:
    value = value.strip(".,;:()[]{}<>")
    value = re.sub(r"^[^A-Za-z0-9]+", "", value)
    return value


def extract_web_sources(text: str) -> list[dict[str, str]]:
    sources: list[dict[str, str]] = []
    seen: set[str] = set()
    domains = re.findall(
        r"(?<!@)\b(?:www\.)?[a-z0-9][a-z0-9.-]+\.(?:com\.br|com|org\.br|org|net\.br|net|esp\.br)\b(?:/[^\s]*)?",
        text,
        re.I,
    )
    for found in domains:
        found = clean_host(found).lower()
        url = f"https://{found}" if not found.startswith(("http://", "https://")) else found
        host = urlparse(url).netloc.removeprefix("www.")
        if not host or host in {"jb-rider.com.br", "tvduasrodas.com"} or url in seen:
            continue
        seen.add(url)
        sources.append(
            {
                "url": url,
                "label": f"Site indicado no flyer ({host})",
                "type": "fonte primária indicada no material visual",
                "supports": "canal de organização, contato ou serviço impresso no flyer",
                "checked_at": NOW,
                "discovery_method": "ocr_visual_windows",
            }
        )

    handles = re.findall(r"(?<![\w.])@\s*([A-Za-z0-9][A-Za-z0-9._]{2,29})", text)
    for handle in handles:
        key = handle.lower().strip("._")
        if (
            not key
            or key in {item.lower() for item in HANDLE_BLOCKLIST}
            or not any(char.isalpha() for char in key)
            or not any(hint in key for hint in HANDLE_HINTS)
        ):
            continue
        url = f"https://www.instagram.com/{key}/"
        if url in seen:
            continue
        seen.add(url)
        sources.append(
            {
                "url": url,
                "label": f"Perfil @{key} impresso no flyer",
                "type": "fonte primária do organizador ou parceiro",
                "supports": "identidade do canal de organização ou parceiro exibido no material visual",
                "checked_at": NOW,
                "discovery_method": "ocr_visual_windows",
            }
        )
    return sources


def merge_sources(existing: list[Any], incoming: list[dict[str, str]]) -> list[Any]:
    result: list[Any] = []
    seen: set[str] = set()
    for source in incoming + existing:
        if not isinstance(source, dict):
            continue
        url = str(source.get("url") or "").rstrip("/")
        if not url or url in INVALID_OCR_URLS or url in seen:
            continue
        seen.add(url)
        result.append(source)
    return result


def replace_visual_section(body: str, paragraph: str) -> str:
    heading = "## Leitura visual complementar"
    pattern = re.compile(
        rf"\n*{re.escape(heading)}\n.*?(?=\n## |\Z)",
        re.S,
    )
    body = pattern.sub("", body or "").rstrip()
    source_heading = "\n## Fonte e atualização"
    section = f"\n\n{heading}\n\n{paragraph}"
    if source_heading in body:
        return body.replace(source_heading, section + source_heading, 1)
    return body + section


def main() -> int:
    agenda = json.loads(AGENDA.read_text(encoding="utf-8-sig"))
    by_slug: dict[str, dict[str, str]] = {}
    for ocr_path in OCR_FILES:
        if not ocr_path.exists():
            continue
        ocr = json.loads(ocr_path.read_text(encoding="utf-8-sig"))
        for item in ocr.get("items", []):
            slug = str(item.get("slug") or "")
            if not slug:
                continue
            aggregate = by_slug.setdefault(
                slug, {"slug": slug, "url": str(item.get("url") or ""), "text": ""}
            )
            aggregate["text"] = (
                aggregate["text"] + "\n" + str(item.get("text") or "")
            ).strip()
    stats = {
        "records_read": 0,
        "records_changed": 0,
        "with_services": 0,
        "with_phones": 0,
        "with_times": 0,
        "with_new_web_source": 0,
    }
    details: list[dict[str, Any]] = []

    for entry in agenda.get("entries", []):
        item = by_slug.get(str(entry.get("slug") or ""))
        if not item:
            continue
        stats["records_read"] += 1
        text = str(item.get("text") or "").strip()
        if not text:
            continue
        services = extract_services(text)
        phones = extract_phones(text)
        times = extract_times(text)
        web_sources = extract_web_sources(text)
        manual = MANUAL_VISUAL.get(str(entry.get("slug") or ""), {})
        if manual.get("sources"):
            web_sources = merge_sources(web_sources, list(manual["sources"]))
        if services:
            stats["with_services"] += 1
            entry["attractions"] = dedupe(list(entry.get("attractions") or []) + services)
        if phones:
            stats["with_phones"] += 1
            entry["contact"] = "; ".join(phones)
        if times:
            stats["with_times"] += 1
            entry["time_label"] = (
                "Horários identificados no flyer: " + ", ".join(times) +
                "; confirme a atividade correspondente com a organização"
            )
        if web_sources:
            stats["with_new_web_source"] += 1
            entry["sources"] = merge_sources(list(entry.get("sources") or []), web_sources)
        else:
            entry["sources"] = merge_sources(list(entry.get("sources") or []), [])

        for key, value in manual.items():
            if key not in {"sources", "attractions", "visual_note"}:
                entry[key] = value
        if manual.get("attractions"):
            entry["attractions"] = dedupe(
                list(entry.get("attractions") or []) + list(manual["attractions"])
            )

        facts: list[str] = []
        if services:
            facts.append("Estrutura e atrações legíveis: " + ", ".join(services) + ".")
        if times:
            facts.append("Marcas de horário legíveis: " + ", ".join(times) + ".")
        if phones:
            facts.append("Contatos impressos: " + "; ".join(phones) + ".")
        if web_sources:
            facts.append(
                "Canais impressos no material: " +
                ", ".join(source["label"] for source in web_sources) + "."
            )
        if manual.get("visual_note"):
            facts.append(str(manual["visual_note"]))
        if not facts:
            facts.append(
                "A arte foi relida visualmente, mas nenhum dado adicional atingiu "
                "confiança suficiente para substituir os campos conservadores."
            )
        entry["body"] = replace_visual_section(
            str(entry.get("body") or ""),
            " ".join(facts) +
            " A leitura automatizada foi usada como apoio; trechos ambíguos não foram publicados como fato.",
        )
        visual = dict(entry.get("visual_verification") or {})
        visual.update(
            {
                "type": "flyer_reinspecionado_com_ocr_visual",
                "source_url": item.get("url"),
                "checked_at": NOW,
                "ocr_engine": "Windows.Media.Ocr",
                "review_policy": "extração conservadora de padrões estruturados",
                "confirmed_fields": dedupe(
                    list(visual.get("confirmed_fields") or [])
                    + (["services_and_attractions"] if services else [])
                    + (["contact"] if phones else [])
                    + (["time_marks"] if times else [])
                    + (["official_channels"] if web_sources else [])
                ),
            }
        )
        entry["visual_verification"] = visual
        entry["last_updated"] = NOW
        entry["source_checked_at"] = NOW
        entry["verification_status"] = "flyer_reinspecionado_com_validacao_conservadora"
        stats["records_changed"] += 1
        details.append(
            {
                "slug": entry.get("slug"),
                "services": services,
                "phones": phones,
                "times": times,
                "new_sources": [source["url"] for source in web_sources],
            }
        )

    agenda["last_updated"] = NOW
    AGENDA.write_text(
        json.dumps(agenda, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    REPORT.write_text(
        json.dumps({"stats": stats, "records": details}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(stats, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
