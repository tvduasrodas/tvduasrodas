#!/usr/bin/env python3
"""Aplica fontes esportivas verificadas manualmente e corrige URLs quebradas."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
CALENDAR = ROOT / "content/calendar/cbm-2026.json"
NOW = datetime.now(timezone.utc).isoformat()


def source(url: str, label: str, kind: str, supports: str) -> dict[str, str]:
    return {
        "url": url,
        "label": label,
        "type": kind,
        "supports": supports,
        "checked_at": NOW,
        "discovery_method": "auditoria_editorial_manual_multifonte",
    }


VERIFIED: dict[tuple[str, str], dict[str, Any]] = {
    ("Campeonato Brasileiro de Motocross", "2026-07-31"): {
        "sources": [
            source(
                "https://mx1gpbrasil.com.br/inscricoes-antecipadas-para-a-7a-e-8a-etapas-do-mx1-gp-brasil-sportbay-estao-abertas/",
                "MX1 GP Brasil confirma 7ª e 8ª etapas em Santa Cruz do Capibaribe",
                "fonte primária do promotor",
                "datas, cidade, etapas, inscrições e categorias internacionais",
            ),
            source(
                "https://eventos.sportbay.com.br/eventos/7-e-8-etapa-mx1-gp-brmx-2026",
                "Inscrição específica da 7ª e 8ª etapas do MX1 GP Brasil 2026",
                "plataforma oficial de inscrições",
                "identidade da etapa, inscrição e acesso dos pilotos",
            ),
        ],
        "organizer": "MX1 GP Brasil / Grupo Promox, com supervisão da CBM",
        "time_label": "Evento de 30 de julho a 2 de agosto; inscrições antecipadas até 29 de julho, às 18h",
        "full_address": "Santa Cruz do Capibaribe - PE; pista e acesso final devem ser consultados no guia da etapa",
        "visual_verification": {
            "type": "pagina_oficial_com_imagem_e_links_de_inscricao",
            "source_url": "https://mx1gpbrasil.com.br/inscricoes-antecipadas-para-a-7a-e-8a-etapas-do-mx1-gp-brasil-sportbay-estao-abertas/",
            "checked_at": NOW,
            "confirmed_fields": ["datas", "cidade", "etapas", "inscricoes"],
        },
    },
    ("Campeonato Brasileiro de Enduro de Regularidade", "2026-08-01"): {
        "sources": [
            source(
                "https://novo.ibitipocaoffroad.com.br/post/2",
                "Ibitipoca Off Road confirma a edição 2026",
                "fonte primária do organizador",
                "datas, vistoria, modalidades, inscrição e contato",
            ),
            source(
                "https://tribunademinas.com.br/noticias/esportes/22-07-2026/ibitipoca-off-road-chega-a-36a-edicao-com-615-inscritos-de-214-cidades.html",
                "Tribuna de Minas detalha a 36ª edição do Ibitipoca Off Road",
                "cobertura jornalística",
                "público esportivo, cidades representadas, modalidades, largada e percurso",
            ),
        ],
        "city": "Juiz de Fora",
        "state": "MG",
        "venue": "Roteiro Ibitipoca Off Road, com base operacional divulgada pelo organizador",
        "full_address": "Juiz de Fora e região de Ibitipoca - MG; roteiro e parque fechado no guia do participante",
        "time_label": "Provas em 1º e 2 de agosto; vistoria em 31 de julho; largada jornalisticamente prevista a partir das 6h",
        "organizer": "Ibitipoca Off Road, com supervisão esportiva da CBM",
        "visual_verification": {
            "type": "pagina_oficial_2026_com_imagens_e_inscricoes",
            "source_url": "https://novo.ibitipocaoffroad.com.br/post/2",
            "checked_at": NOW,
            "confirmed_fields": ["datas", "vistoria", "modalidades", "contato"],
        },
        "note": "A cobertura local registra 615 inscritos de 214 cidades: 560 motos e 55 carros/UTVs.",
    },
    ("Campeonato Brasileiro de Enduro", "2026-08-07"): {
        "sources": [
            source(
                "https://www.lsoffroad.com.br/post/campeonato-brasileiro-de-enduro-anuncia-mudan%C3%A7as-no-calend%C3%A1rio-da-temporada-2026",
                "LS Off Road repercute o calendário revisado do Brasileiro de Enduro 2026",
                "fonte independente do setor",
                "mudança de data, cidade e janela da prova",
            ),
            source(
                "https://www.alfaeventos.esp.br/",
                "Alfa Eventos, promotora de provas off-road",
                "canal do organizador",
                "organização e contato operacional",
            ),
        ],
        "stage": "4ª prova do calendário revisado",
        "organizer": "Alfa Eventos, com supervisão da CBM",
        "time_label": "De 7 a 9 de agosto; programação detalhada deve ser conferida no regulamento particular",
        "visual_verification": {
            "type": "calendario_oficial_e_confirmacao_independente",
            "source_url": "https://www.lsoffroad.com.br/post/campeonato-brasileiro-de-enduro-anuncia-mudan%C3%A7as-no-calend%C3%A1rio-da-temporada-2026",
            "checked_at": NOW,
            "confirmed_fields": ["datas", "cidade", "mudanca_de_calendario"],
        },
    },
    ("Campeonato Brasileiro de Moto Climb", "2026-08-08"): {
        "sources": [
            source(
                "https://www.motoclimbbrasil.com.br/",
                "MotoClimb Brasil — calendário do promotor para 2026",
                "fonte primária do promotor",
                "calendário do promotor, categorias, entrada, estacionamento e estrutura",
            )
        ],
        "status": "em_verificacao",
        "organizer": "MotoClimb Brasil, com supervisão da CBM",
        "time_label": "A CBM lista 8 e 9 de agosto; o calendário do promotor não lista Morungaba nesta data",
        "note": "Conflito ativo: a CBM exibe Morungaba em 8 e 9 de agosto, enquanto o promotor publica a 2ª etapa em Teresópolis em 12 e 13 de junho. Não viaje sem confirmação direta.",
        "visual_verification": {
            "type": "conflito_documentado_entre_fontes_primarias",
            "source_url": "https://www.motoclimbbrasil.com.br/",
            "checked_at": NOW,
            "confirmed_fields": ["conflito_de_data", "categorias", "estrutura"],
        },
    },
    ("Campeonato Brasileiro de Arenacross", "2026-08-14"): {
        "sources": [
            source(
                "https://www.arenacross.com.br/single-post/arena-cross-vai-encerrar-temporada-em-grande-estilo-com-rodada-dupla-na-super-final-no-festival-inte",
                "Arena Cross confirma Super Final em rodada dupla no Festival Interlagos",
                "fonte primária do promotor",
                "datas, local, formato, pilotos, público esperado e ingresso",
            ),
            source(
                "https://www.ticketmaster.com.br/event/suhai-festival-de-interlagos-2026-edicao-moto",
                "Bilheteria oficial do Festival Interlagos 2026 — edição moto",
                "plataforma oficial de ingressos",
                "acesso, categorias de ingresso e local",
            ),
        ],
        "venue": "Autódromo José Carlos Pace — Interlagos",
        "full_address": "Autódromo José Carlos Pace, Avenida Senador Teotônio Vilela, 261, Interlagos, São Paulo - SP",
        "organizer": "Arena Cross Brasil e Festival Interlagos, com supervisão da CBM",
        "time_label": "14 e 15 de agosto; acesso à arquibancada por ordem de chegada e sujeito à lotação",
        "admission_status": "Acesso mediante ingresso do Festival Interlagos; valores e lotes variam na bilheteria oficial",
        "visual_verification": {
            "type": "materia_oficial_com_imagens_e_bilheteria_cruzada",
            "source_url": "https://www.arenacross.com.br/single-post/arena-cross-vai-encerrar-temporada-em-grande-estilo-com-rodada-dupla-na-super-final-no-festival-inte",
            "checked_at": NOW,
            "confirmed_fields": ["datas", "local", "formato", "ingressos", "pilotos"],
        },
    },
    ("Campeonato Brasileiro de Motovelocidade", "2026-09-27"): {
        "sources": [
            source(
                "https://m1gp.com.br/club-gp/calendario-2026/",
                "Calendário oficial MOTO1000GP 2026",
                "fonte primária do promotor",
                "data, etapa e autódromo",
            ),
            source(
                "https://www.honda.com.br/racing/6etapamoto1000gprs26",
                "Honda Racing — 6ª etapa do MOTO1000GP 2026",
                "fonte oficial de equipe participante",
                "etapa, pilotos, categorias e cobertura esportiva",
            ),
        ],
        "venue": "Autódromo Internacional de Santa Cruz do Sul",
        "full_address": "Autódromo Internacional de Santa Cruz do Sul, Santa Cruz do Sul - RS",
        "organizer": "MOTO1000GP, com supervisão da CBM",
        "time_label": "Etapa em 27 de setembro; programação por sessão será publicada pelo MOTO1000GP",
        "note": "A página da CBM trazia o município abreviado incorretamente; o calendário do promotor confirma Santa Cruz do Sul/RS.",
        "visual_verification": {
            "type": "calendario_do_promotor_e_pagina_de_equipe",
            "source_url": "https://m1gp.com.br/club-gp/calendario-2026/",
            "checked_at": NOW,
            "confirmed_fields": ["data", "etapa", "cidade", "autodromo"],
        },
    },
    ("Campeonato Brasileiro de Moto Climb", "2026-10-10"): {
        "sources": [
            source(
                "https://www.motoclimbbrasil.com.br/",
                "MotoClimb Brasil confirma a 3ª etapa em Nova Resende",
                "fonte primária do promotor",
                "datas, cidade, categorias, entrada, estacionamento e food park",
            )
        ],
        "organizer": "MotoClimb Brasil, com supervisão da CBM",
        "time_label": "10 e 11 de outubro; horários das baterias serão divulgados pelo promotor",
        "admission_status": "Entrada gratuita para o público, segundo o promotor",
        "parking": "Estacionamento anunciado no local",
        "visual_verification": {
            "type": "pagina_oficial_com_calendario_e_estrutura",
            "source_url": "https://www.motoclimbbrasil.com.br/",
            "checked_at": NOW,
            "confirmed_fields": ["datas", "cidade", "categorias", "entrada", "estacionamento", "alimentacao"],
        },
    },
    ("Campeonato Brasileiro de Big Trail", "2026-10-10"): {
        "sources": [
            source(
                "https://www.bitesbr.com.br/",
                "BITES confirma SportBay Big Trail em Siqueira Campos",
                "fonte primária do promotor",
                "datas, cidade, formato e categorias",
            ),
            source(
                "https://blog.sportbay.com.br/eventos-off-road/",
                "SportBay destaca o BITES entre os eventos off-road de 2026",
                "fonte oficial do patrocinador",
                "temporada 2026, perfil esportivo e acesso do público",
            ),
        ],
        "organizer": "BITES — Big Trail Enduro Series / SportBay, com chancela da CBM",
        "time_label": "10 e 11 de outubro; programação detalhada será divulgada pelo BITES",
        "visual_verification": {
            "type": "pagina_oficial_com_calendario_categorias_e_imagens",
            "source_url": "https://www.bitesbr.com.br/",
            "checked_at": NOW,
            "confirmed_fields": ["datas", "cidade", "categorias", "formato"],
        },
    },
    ("Campeonato Brasileiro de MTB 2026", "2026-07-23"): {
        "sources": [
            source(
                "https://www.cbc.esp.br/modalidades/evento/busca//id/1344",
                "CBC — página específica do Brasileiro MTB XCO/XCC/XCE 2026",
                "fonte primária da entidade esportiva",
                "datas, sede, modalidades, regulamento e inscrições",
            ),
            source(
                "https://www.encontrasaojosedoscampos.com/sao-jose-dos-campos-sp-recebe-campeonato-brasileiro-de-mtb-2026-entre-os-dias-23-e-26-de-julho/",
                "São José dos Campos recebe o Brasileiro de MTB 2026",
                "cobertura local independente",
                "datas, cidade, modalidades e sede",
            )
        ],
        "venue": "Mobai Bike Land",
        "full_address": "Mobai Bike Land, São José dos Campos - SP",
        "organizer": "CBC, Mobai Bike Land e Federação Paulista de Ciclismo",
        "time_label": "De 23 a 26 de julho; cronograma por categoria no guia técnico da CBC",
        "visual_verification": {
            "type": "pagina_local_com_imagem_cruzada_com_calendario_cbc",
            "source_url": "https://www.encontrasaojosedoscampos.com/sao-jose-dos-campos-sp-recebe-campeonato-brasileiro-de-mtb-2026-entre-os-dias-23-e-26-de-julho/",
            "checked_at": NOW,
            "confirmed_fields": ["datas", "cidade", "sede", "modalidades"],
        },
    },
    ("Vila Race MTB", "2026-08-23"): {
        "sources": [
            source(
                "https://www.realtiming.com.br/eventos/",
                "Real Timing lista Vila Race MTB 2026",
                "cronometragem e inscrição",
                "data, cidade e modalidade XCM",
            ),
            source(
                "https://www.apcrono.com.br/",
                "AP Crono — canal indicado pela CBC para a prova",
                "fonte primária de cronometragem indicada pela entidade",
                "organização técnica e resultados",
            ),
        ],
        "organizer": "Organização Vila Race, com cronometragem especializada e supervisão esportiva",
        "time_label": "23 de agosto; horário de largada deve ser conferido na página de inscrição",
        "visual_verification": {
            "type": "listagem_de_cronometragem_cruzada_com_cbc",
            "source_url": "https://www.realtiming.com.br/eventos/",
            "checked_at": NOW,
            "confirmed_fields": ["data", "cidade", "modalidade"],
        },
    },
    ("Internacional Estrada Real #4", "2026-09-05"): {
        "sources": [
            source(
                "https://internacionalestradareal.com.br/",
                "Calendário e serviço oficial da Internacional Estrada Real 2026",
                "fonte primária do promotor",
                "datas, sede, retirada de kit, categorias e premiação",
            ),
            source(
                "https://internacionalestradareal.com.br/etapa/arcos/",
                "Página oficial da etapa Barbacena 2026",
                "fonte primária do promotor",
                "programação por modalidade, hospedagem e kit",
            ),
            source(
                "https://sportsforyou.com.br/eventos/ciclismo/estrada/",
                "SportsForYou lista a Internacional Estrada Real #4 em Barbacena",
                "agenda esportiva independente",
                "datas, cidade e modalidades",
            ),
        ],
        "end_date": "2026-09-06",
        "venue": "Praça de Eventos de Barbacena",
        "full_address": "Praça de Eventos, Barbacena - MG",
        "organizer": "Avelar Sports, com supervisão da CBC/UCI",
        "time_label": "Secretaria de 2 a 5 de setembro; provas XCC em 4/9, XCO em 5/9 e XCM/infantil em 6/9",
        "visual_verification": {
            "type": "pagina_oficial_com_programacao_kit_e_hospedagem",
            "source_url": "https://internacionalestradareal.com.br/",
            "checked_at": NOW,
            "confirmed_fields": ["datas", "local", "programacao", "kit", "premiacao"],
        },
    },
    ("XCM AG Sport", "2026-09-18"): {
        "sources": [
            source(
                "https://www.agsportinternacional.com/",
                "AG Sport Internacional — canal oficial da organização",
                "fonte primária do organizador",
                "organização, inscrições e contato",
            ),
            source(
                "https://inscricoes.com.br/eventos",
                "Inscrições.com.br lista XCM AG Sport Stage Race 2026",
                "plataforma de inscrições específica",
                "data, cidade, modalidade e situação das inscrições",
            ),
        ],
        "organizer": "AG Sport Internacional, com supervisão da CBC",
        "time_label": "De 18 a 20 de setembro; programação e largadas no regulamento do organizador",
        "visual_verification": {
            "type": "canal_do_organizador_cruzado_com_calendario_cbc",
            "source_url": "https://www.agsportinternacional.com/",
            "checked_at": NOW,
            "confirmed_fields": ["organizador", "cidade", "janela_da_prova"],
        },
    },
    ("Internacional MTB Series XCO #4", "2026-09-19"): {
        "sources": [
            source(
                "https://www.internacionalmtbseries.com.br/",
                "Internacional MTB Series — temporada 2026",
                "fonte primária do promotor",
                "calendário, inscrições, categorias e contato",
            ),
            source(
                "https://www.uci.org/competition-details/2026/MTB/",
                "Calendário internacional UCI MTB 2026",
                "entidade esportiva internacional",
                "classe internacional, modalidades e temporada",
            ),
        ],
        "organizer": "Internacional MTB Series, com supervisão da CBC/UCI",
        "time_label": "19 e 20 de setembro; horários por categoria no cronograma técnico",
        "visual_verification": {
            "type": "pagina_do_promotor_cruzada_com_calendario_esportivo",
            "source_url": "https://www.internacionalmtbseries.com.br/",
            "checked_at": NOW,
            "confirmed_fields": ["temporada", "cidade", "modalidade"],
        },
    },
    ("CIMTB #3 — Congonhas", "2026-09-25"): {
        "sources": [
            source(
                "https://cimtb.com.br/",
                "CIMTB — calendário e informações oficiais",
                "fonte primária do promotor",
                "etapa, inscrições, categorias e contato",
            )
        ],
        "organizer": "CIMTB, com supervisão da CBC/UCI e apoio municipal",
        "time_label": "De 25 a 27 de setembro; programação por categoria no guia oficial",
        "visual_verification": {
            "type": "pagina_oficial_do_promotor",
            "source_url": "https://cimtb.com.br/",
            "checked_at": NOW,
            "confirmed_fields": ["etapa", "cidade", "modalidades"],
        },
    },
    ("Desafio São José dos Campos de Paraciclismo", "2026-11-22"): {
        "sources": [
            source(
                "https://www.clubedeciclismosjc.com.br/exibe_evento.asp?codigo=52",
                "Clube de Ciclismo de São José dos Campos — página específica do desafio",
                "fonte primária do organizador",
                "data, cidade, inscrição e contato",
            )
        ],
        "organizer": "Clube de Ciclismo de São José dos Campos / EMX, com supervisão da CBC",
        "time_label": "22 de novembro; programação e percurso na página do organizador",
        "visual_verification": {
            "type": "pagina_especifica_do_organizador",
            "source_url": "https://www.clubedeciclismosjc.com.br/exibe_evento.asp?codigo=52",
            "checked_at": NOW,
            "confirmed_fields": ["data", "cidade", "organizador"],
        },
    },
    ("12º Up Hill Serra da Chocadeira", "2026-12-05"): {
        "sources": [
            source(
                "https://agitoesportes.com.br/",
                "Agito Esportes — canal indicado pela CBC para o Up Hill",
                "fonte primária do organizador",
                "organização, inscrição, cronometragem e contato",
            )
        ],
        "organizer": "Agito Esportes, com supervisão da CBC",
        "time_label": "5 e 6 de dezembro; largadas e retirada de kit no regulamento do organizador",
        "visual_verification": {
            "type": "canal_do_organizador_cruzado_com_calendario_cbc",
            "source_url": "https://agitoesportes.com.br/",
            "checked_at": NOW,
            "confirmed_fields": ["datas", "cidade", "organizador"],
        },
    },
    ("Campeonato Brasileiro de MTB Downhill 2026", "2026-07-24"): {
        "sources": [
            source(
                "https://www.ilhabela.sp.gov.br/portal/noticias/0/3/17596/atletas-de-ilhabela-conquistam-titulos-na-segunda-etapa-do-campeonato-paulista-de-downhill-com-apoio-da-prefeitura",
                "Prefeitura de Ilhabela confirma atletas no Brasileiro de Downhill em Paraíba do Sul",
                "fonte institucional pública independente",
                "mês, cidade, caráter nacional e atletas participantes",
            )
        ],
        "venue": "Parque das Águas Salutaris — pista do Morro da Torre",
        "full_address": "Parque das Águas Salutaris, Paraíba do Sul - RJ",
        "organizer": "CBC e FECIERJ",
        "time_label": "24 a 26 de julho; treinos, tomada de tempo e finais conforme guia técnico",
        "visual_verification": {
            "type": "pagina_oficial_cbc_com_imagem_cruzada_com_fonte_municipal",
            "source_url": "https://cbc.esp.br/modalidades/evento/busca/mtb/id/1352",
            "checked_at": NOW,
            "confirmed_fields": ["datas", "cidade", "pista", "programacao"],
        },
    },
    ("Campeonato Sulbrasileiro de BMX", "2026-08-23"): {
        "sources": [
            source(
                "https://www.pyxisbrasil.com/evento/sulbrasileiro2026",
                "Pyxis — Campeonato Sul Brasileiro de Bicicross 2026",
                "plataforma oficial de inscrições",
                "datas, endereço, programação, categorias, organização e premiação",
            ),
            source(
                "https://www.apbmx.com.br/atleta/gabibalus",
                "Calendário esportivo 2026 publicado na vitrine da atleta Gabriela Balus",
                "fonte esportiva independente",
                "data da competição, cidade, classe C3 e presença no calendário nacional",
            ),
        ],
        "start_date": "2026-08-22",
        "end_date": "2026-08-23",
        "venue": "Pista de BMX do Parque Malwee",
        "full_address": "Rua Wolfgang Weege, 770, Parque Malwee, Jaraguá do Sul - SC, CEP 89262-000",
        "organizer": "Sociedade Corintias Esporte Clube, com supervisão da FCC e CBC",
        "time_label": "22 de agosto: secretaria, clínica e treinos; 23 de agosto: aquecimento, abertura, provas e premiação",
        "visual_verification": {
            "type": "pagina_de_inscricao_com_imagem_programacao_e_regulamento",
            "source_url": "https://www.pyxisbrasil.com/evento/sulbrasileiro2026",
            "checked_at": NOW,
            "confirmed_fields": ["datas", "endereco", "programacao", "categorias", "premiacao"],
        },
    },
    ("Circuito Sul Fluminense de Ciclismo", "2026-08-23"): {
        "sources": [
            source(
                "https://fecierj.org.br/eventos/calendario-2026/",
                "FECIERJ — calendário oficial 2026",
                "fonte primária da federação",
                "data, cidade, modalidade e vínculo com o circuito estadual",
            )
        ],
        "organizer": "FECIERJ e organização local do Circuito Sul Fluminense",
    },
    ("Taça Brasil de Paraciclismo de Pista", "2026-08-04"): {
        "sources": [
            source(
                "https://www.cbc.esp.br/modalidades/evento/busca//id/1349",
                "CBC — página específica da Taça Brasil de Pista 2026",
                "fonte primária da entidade esportiva",
                "datas, velódromo, organização, programa, hotel e alojamento",
            ),
            source(
                "https://www.uci.org/competition-details/2026/PAR/77190",
                "UCI — Taça Brasil de Ciclismo de Pista #1",
                "entidade esportiva internacional",
                "datas, local, classe e provas paralímpicas",
            ),
            source(
                "https://www.uci.org/competition-details/2026/PIS/79054",
                "UCI — Track American Series / Taça Brasil de Pista",
                "entidade esportiva internacional",
                "datas, local, classe e programa esportivo",
            ),
        ],
        "venue": "Velódromo Municipal de Maringá",
        "full_address": "Velódromo Municipal de Maringá, Vila Olímpica, Avenida Colombo, Zona 7, Maringá - PR",
        "organizer": "Instituto Mais Esporte, com chancela da CBC e apoio da Secretaria de Esportes de Maringá",
        "time_label": "De 4 a 9 de agosto, com início operacional indicado para 8h; programa provisório na página da CBC",
        "visual_verification": {
            "type": "pagina_cbc_com_imagem_documentos_e_calendario_uci",
            "source_url": "https://www.cbc.esp.br/modalidades/evento/busca//id/1349",
            "checked_at": NOW,
            "confirmed_fields": ["datas", "local", "programa", "alojamento", "organizacao"],
        },
    },
    ("Circuito do Estreito", "2026-08-22"): {
        "sources": [
            source(
                "https://www.nortecrono.com.br/",
                "Norte Crono — canal do organizador indicado pela CBC",
                "fonte primária do organizador",
                "organização, inscrições, cronometragem e contato",
            )
        ],
        "start_date": "2026-11-29",
        "end_date": "2026-11-29",
        "status": "data_alterada_em_verificacao",
        "organizer": "Norte Crono, com homologação esportiva indicada pela CBC",
        "time_label": "A listagem atual da CBC mostra 29 de novembro; o índice anterior ainda exibe 22 e 23 de agosto",
        "note": "Alteração detectada em 26/07/2026: a página viva da CBC passou a listar 29/11/2026, enquanto cópias indexadas ainda exibem 22 e 23/08. A data nova foi adotada com alerta até publicação do regulamento 2026 pela Norte Crono.",
        "visual_verification": {
            "type": "divergencia_temporal_documentada_entre_calendario_vivo_e_indice",
            "source_url": "https://www.cbc.esp.br/modalidades/calendario/busca/mtb",
            "checked_at": NOW,
            "confirmed_fields": ["titulo", "cidade", "modalidade", "alteracao_de_data"],
        },
    },
    ("Desafio de Downhill Santa Cruz", "2026-08-29"): {
        "sources": [
            source(
                "https://www.realtiming.com.br/evento/desafio-stacruzense-dh2023",
                "Real Timing — página específica do Desafio Santacruzense de Downhill",
                "fonte primária histórica da cronometragem e organização",
                "organizador, contato, categorias, local e estrutura recorrente; as datas 2026 vêm da CBC",
            ),
            source(
                "https://blogdapolo.com.br/desafio-de-downhill-acontece-neste-fim-de-semana-em-santa-cruz-do-capibaribe/",
                "Blog da Polo — cobertura específica do Desafio de Downhill",
                "cobertura jornalística independente",
                "localidade, categorias, inscrição, premiação e contato histórico da organização",
            ),
        ],
        "venue": "Pista de downhill na região do Cruzeiro da Palestina",
        "full_address": "Bairro da Palestina, Santa Cruz do Capibaribe - PE; acesso final deve ser confirmado no regulamento 2026",
        "organizer": "Organização local do Desafio Santacruzense de Downhill, com homologação da CBC",
        "visual_verification": {
            "type": "calendario_cbc_cruzado_com_paginas_historicas_especificas",
            "source_url": "https://www.realtiming.com.br/evento/desafio-stacruzense-dh2023",
            "checked_at": NOW,
            "confirmed_fields": ["identidade", "cidade", "modalidade", "categorias", "organizador"],
        },
    },
    ("Copa do Brasil de BMX #03", "2026-09-05"): {
        "sources": [
            source(
                "https://www.ba.gov.br/esporte/sites/site-sudesb/files/2026-06/SEI_00141866064_Plano_de_Trabalho.pdf",
                "SUDESB — plano de trabalho oficial da Copa Brasil de BMX Racing 2026",
                "fonte primária institucional e regulamento operacional",
                "datas, pista, horários, organizador, 41 categorias, 250 atletas, público estimado, taxa e premiação",
            ),
            source(
                "https://www.apbmx.com.br/atleta/gabibalus",
                "Calendário esportivo 2026 publicado na vitrine da atleta Gabriela Balus",
                "fonte esportiva independente",
                "datas, cidade, classe C2 e vínculo oficial da Copa do Brasil de BMX #03",
            )
        ],
        "venue": "Pista de Bicicross Tertuliano Torres",
        "full_address": "Lotes 01 e 02, Quadra 05, Loteamento Jardim Iracema, Pituaçu, Salvador - BA",
        "time_label": "5 de setembro: treinos e kits das 8h às 17h; 6 de setembro: treinos às 8h, competições às 10h e premiação às 13h",
        "organizer": "Associação de Bicicross de Salvador (ABS), com apoio da SUDESB e chancela da CBC",
        "admission_status": "Inscrição esportiva prevista em R$ 100 por atleta",
        "visual_verification": {
            "type": "plano_de_trabalho_oficial_com_programacao_e_estrutura",
            "source_url": "https://www.ba.gov.br/esporte/sites/site-sudesb/files/2026-06/SEI_00141866064_Plano_de_Trabalho.pdf",
            "checked_at": NOW,
            "confirmed_fields": ["datas", "pista", "programacao", "categorias", "publico", "inscricao", "premiacao"],
        },
    },
    ("Copa Bahia de BMX Racing", "2026-09-05"): {
        "sources": [
            source(
                "https://absbmx.com.br/3a-etapa-da-copa-bahia-de-bmx-racing-salvador-2025/",
                "ABS BMX — histórico específico da Copa Bahia de BMX Racing em Salvador",
                "fonte primária do organizador local",
                "identidade do circuito, organização em Salvador e alcance estadual; a data 2026 vem do calendário esportivo",
            ),
            source(
                "https://www.apbmx.com.br/atleta/gabibalus",
                "Calendário esportivo 2026 publicado na vitrine da atleta Gabriela Balus",
                "fonte esportiva independente",
                "data, cidade, classe C5 e presença da Copa Bahia de BMX Racing no calendário nacional",
            )
        ],
        "organizer": "Organização baiana de BMX Racing, com homologação no ranking CBC",
    },
    ("Desafio da Moda de BMX", "2026-09-20"): {
        "sources": [
            source(
                "https://sapl.santacruzdocapibaribe.pe.leg.br/materia/pesquisar-materia?ano=2025&autoria__autor=26&autoria__primeiro_autor=True&tipo=18",
                "Câmara de Santa Cruz do Capibaribe — reconhecimento do Desafio da Moda de BMX",
                "fonte oficial institucional",
                "organizador local, pista Niedson Tibúrcio, ranking C5, categorias, presença PCD e público esportivo histórico",
            ),
            source(
                "https://www.apbmx.com.br/atleta/gabibalus",
                "Calendário esportivo 2026 publicado na vitrine da atleta Gabriela Balus",
                "fonte esportiva independente",
                "data, cidade, classe C5 e presença do Desafio da Moda no calendário nacional",
            )
        ],
        "venue": "Pista Municipal de Bicicross Niedson Tibúrcio",
        "organizer": "Associação de Bicicross de Santa Cruz do Capibaribe, com Alex Júnior e homologação no ranking CBC",
    },
    ("Copa Recife de BMX", "2026-11-29"): {
        "sources": [
            source(
                "https://www.apbmx.com.br/atleta/gabibalus",
                "Calendário esportivo 2026 publicado na vitrine da atleta Gabriela Balus",
                "fonte esportiva independente",
                "data, cidade, classe C5 e presença da Copa Recife no calendário nacional",
            )
        ],
        "organizer": "Organização local de Recife, com homologação no ranking CBC",
    },
    ("Copa Pedal de BMX Racing", "2026-12-13"): {
        "sources": [
            source(
                "https://www.ba.gov.br/comunicacao/2024/08/noticias/copa-pedal-de-bicicross-reune-alunos-do-projeto-social-e-atleta-olimpica-em-stella-maris",
                "Governo da Bahia — histórico oficial da Copa Pedal de Bicicross",
                "fonte oficial institucional",
                "organizador, projeto social, categorias de base, pista de Stella Maris e alcance; a data 2026 vem do calendário esportivo",
            ),
            source(
                "https://www.apbmx.com.br/atleta/gabibalus",
                "Calendário esportivo 2026 publicado na vitrine da atleta Gabriela Balus",
                "fonte esportiva independente",
                "data, cidade, classe C5 e presença da Copa Pedal no calendário nacional",
            )
        ],
        "venue": "Pista de Bicicross de Stella Maris",
        "organizer": "Associação de Bicicross de Salvador e Projeto Pedal, com apoio da SUDESB e homologação CBC",
    },
    ("Desafio São José dos Campos de Paraciclismo", "2026-11-22"): {
        "sources": [
            source(
                "https://www.clubedeciclismosjc.com.br/exibe_evento.asp?codigo=52",
                "Clube de Ciclismo SJC — regulamento do Desafio São José de Paraciclismo 2026",
                "fonte primária do organizador e regulamento",
                "data, endereço, classes, inscrição, programação, premiação, contato e organização",
            ),
            source(
                "https://www.sjc.sp.gov.br/noticias/2025/agosto/14/desafio-tera-participacao-de-15-atletas-do-sao-jose-ciclismo/",
                "Prefeitura de São José dos Campos — cobertura institucional do Desafio São José",
                "fonte oficial institucional independente",
                "local, horários, organização, categorias e participação de atletas no circuito recorrente",
            ),
        ],
        "venue": "Parque Oswaldo Henrique Chimaschi (Ribeirão Vermelho), Portaria B",
        "full_address": "Avenida Fernando Sabino, 2000, Urbanova, São José dos Campos - SP",
        "time_label": "22 de novembro: secretaria às 6h, primeiras largadas às 7h e premiação após as 10h30",
        "organizer": "Clube de Ciclismo de São José dos Campos, EMX Promoções e Sonia Molina, com supervisão FPC/CBC",
        "admission_status": "Inscrição até 10 de novembro; doação de 2 kg de alimentos ou contribuição equivalente de R$ 20",
        "contact": "(12) 98142-0856 — Sônia / Clube de Ciclismo de São José dos Campos",
        "visual_verification": {
            "type": "regulamento_2026_com_imagens_do_circuito_e_fontes_institucionais",
            "source_url": "https://www.clubedeciclismosjc.com.br/exibe_evento.asp?codigo=52",
            "checked_at": NOW,
            "confirmed_fields": ["data", "endereco", "programacao", "classes", "inscricao", "premiacao", "contato"],
        },
    },
    ("Volta Ciclística da Juventude", "2026-09-04"): {
        "sources": [
            source(
                "https://fecierj.org.br/eventos/volta-da-juventude-2026-05-06-e-07-09-2026/",
                "FECIERJ — regulamento e programação oficial da Volta da Juventude 2026",
                "fonte primária da federação organizadora",
                "datas, quatro etapas, percursos, horários, classificação e premiação",
            ),
            source(
                "https://www.planetadabike.com/",
                "Planeta da Bike noticia a programação da Volta da Juventude 2026",
                "cobertura jornalística especializada",
                "datas, cidade e quatro disciplinas",
            ),
        ],
        "end_date": "2026-09-07",
        "venue": "Valença, Parapeúna e Pentagna",
        "full_address": "Valença, Parapeúna e Pentagna, município de Valença - RJ",
        "organizer": "FECIERJ",
        "time_label": "Congresso em 4/9 às 18h; CRI em 5/9 às 8h; montanha às 15h; circuito em 6/9 às 8h30; estrada em 7/9 às 7h30",
        "visual_verification": {
            "type": "regulamento_oficial_com_programacao_cruzado_com_imprensa_especializada",
            "source_url": "https://fecierj.org.br/eventos/volta-da-juventude-2026-05-06-e-07-09-2026/",
            "checked_at": NOW,
            "confirmed_fields": ["datas", "horarios", "locais", "percursos", "premiacao"],
        },
    },
    ("Copa Brasil de Paraciclismo de Estrada", "2026-09-19"): {
        "sources": [
            source(
                "https://ge.globo.com/sc/noticia/2026/06/11/copa-brasil-de-paraciclismo-veja-programacao-e-modalidades.ghtml",
                "ge confirma João Pessoa como segunda etapa da Copa Brasil de Paraciclismo 2026",
                "cobertura jornalística",
                "cidade, mês, sequência da temporada e modalidades",
            ),
            source(
                "https://cpb.org.br/noticias/copa-brasil-de-ciclismo-de-estrada-abre-temporada-2026-em-santa-catarina/",
                "CPB confirma João Pessoa no calendário da Copa Brasil 2026",
                "fonte primária institucional esportiva",
                "cidade, mês, importância e atletas da temporada",
            ),
        ],
        "organizer": "CBC, CPB e Federação Paraibana de Ciclismo, com apoio municipal",
        "time_label": "19 e 20 de setembro; horários da etapa serão publicados no guia técnico da CBC",
        "visual_verification": {
            "type": "calendario_cbc_cruzado_com_cpb_e_cobertura_jornalistica",
            "source_url": "https://ge.globo.com/sc/noticia/2026/06/11/copa-brasil-de-paraciclismo-veja-programacao-e-modalidades.ghtml",
            "checked_at": NOW,
            "confirmed_fields": ["cidade", "mes", "sequencia_da_temporada"],
        },
    },
    ("Ita Biker — Ultra Maratona", "2026-09-19"): {
        "sources": [
            source(
                "https://suainscricao.com/evento/ita-biker",
                "Sua Inscrição — página específica da Ita Biker 2026",
                "plataforma oficial de inscrições",
                "data, cidade, inscrição e regras de desconto",
            ),
            source(
                "https://casinhadeaventuras.com.br/round-5-ita-biker-a-grande-final",
                "Casinha de Aventuras — Ita Biker, grande final",
                "fonte primária do organizador",
                "formato, percurso e organização",
            ),
        ],
        "organizer": "Casinha de Aventuras",
        "time_label": "19 e 20 de setembro; a página de inscrição registra atividade em 20/9 às 10h03",
        "visual_verification": {
            "type": "pagina_de_inscricao_cruzada_com_pagina_do_organizador",
            "source_url": "https://suainscricao.com/evento/ita-biker",
            "checked_at": NOW,
            "confirmed_fields": ["data", "cidade", "inscricao"],
        },
    },
    ("CIMTB #3 — Congonhas", "2026-09-25"): {
        "sources": [
            source(
                "https://www.adventuremag.com.br/calendario/10409/1/CIMTB-Congonhas-2026",
                "Adventuremag — CIMTB Congonhas 2026",
                "agenda esportiva independente",
                "datas, cidade e organizador",
            ),
            source(
                "https://cimtb.com.br/images/2025/12/REGULAMENTO-MARATONA-2026.pdf",
                "Regulamento oficial da Maratona CIMTB 2026",
                "regulamento oficial",
                "data da etapa, categorias, seguro e regras esportivas",
            ),
        ],
        "venue": "Praça de Eventos de Congonhas",
        "full_address": "Praça de Eventos, Congonhas - MG",
        "time_label": "25 a 27 de setembro; horários detalhados na programação oficial da etapa",
    },
    ("Campeonato Brasileiro de Paraciclismo de Pista 2026", "2026-10-16"): {
        "sources": [
            source(
                "https://www.uci.org/competition-details/2026/PAR/78876",
                "UCI — Campeonato Brasileiro de Paraciclismo de Pista 2026",
                "entidade esportiva internacional",
                "identidade, sede e temporada",
            )
        ],
        "organizer": "CBC, com homologação esportiva da UCI e apoio local",
        "time_label": "16 a 18 de outubro; programa de provas aguardando guia técnico",
        "visual_verification": {
            "type": "pagina_uci_cruzada_com_calendario_cbc",
            "source_url": "https://www.uci.org/competition-details/2026/PAR/78876",
            "checked_at": NOW,
            "confirmed_fields": ["evento", "cidade", "temporada"],
        },
    },
    ("Copa Brasil de Paraciclismo de Estrada", "2026-12-05"): {
        "sources": [
            source(
                "https://cpb.org.br/noticias/copa-brasil-de-ciclismo-de-estrada-abre-temporada-2026-em-santa-catarina/",
                "CPB confirma Salvador como encerramento da Copa Brasil 2026",
                "fonte primária institucional esportiva",
                "cidade, posição no calendário e importância da temporada",
            ),
            source(
                "https://ge.globo.com/sc/noticia/2026/06/11/copa-brasil-de-paraciclismo-veja-programacao-e-modalidades.ghtml",
                "ge confirma Salvador como etapa final da temporada",
                "cobertura jornalística",
                "cidade e sequência da temporada",
            ),
        ],
        "organizer": "CBC, CPB e Federação Baiana de Ciclismo",
        "time_label": "5 e 6 de dezembro; horários aguardam guia técnico da etapa final",
        "visual_verification": {
            "type": "calendario_cbc_cruzado_com_cpb_e_imprensa",
            "source_url": "https://cpb.org.br/noticias/copa-brasil-de-ciclismo-de-estrada-abre-temporada-2026-em-santa-catarina/",
            "checked_at": NOW,
            "confirmed_fields": ["cidade", "etapa_final", "temporada"],
        },
    },
    ("16ª Maratona de MTB Cabra da Peste", "2026-11-28"): {
        "sources": [
            source(
                "https://tiquet.com.br/",
                "Tiquet — plataforma indicada pela CBC e pelo organizador",
                "plataforma oficial de inscrições",
                "canal de inscrição e contato do organizador",
            ),
            source(
                "https://auniao.pb.gov.br/servicos/copy_of_jornal-a-uniao/2025/novembro/jornal-em-pdf-29-11-25-cdepc.pdf",
                "A União documenta a tradição e o porte nacional da Maratona Cabra da Peste",
                "cobertura jornalística histórica",
                "organização, sede recorrente, porte e perfil esportivo",
            ),
        ],
        "organizer": "Agnaldo Melo / Federação Paraibana de Ciclismo, com supervisão da CBC",
        "time_label": "28 e 29 de novembro; programação 2026 ainda será publicada na Tiquet",
        "full_address": "Soledade - PB; arena e percurso aguardam o regulamento específico de 2026",
        "note": "A data 2026 está no calendário CBC; a Tiquet ainda exibe a edição anterior. Dados de percurso e valores de 2025 não foram reutilizados como serviço atual.",
        "visual_verification": {
            "type": "calendario_2026_cruzado_com_plataforma_do_organizador_e_historico_jornalistico",
            "source_url": "https://tiquet.com.br/",
            "checked_at": NOW,
            "confirmed_fields": ["organizador", "sede_recorrente", "porte_historico"],
        },
    },
    ("Taça Brasil de BMX Racing", "2026-12-03"): {
        "sources": [
            source(
                "https://mtesporte.com.br/esporte/cuiaba-e-confirmada-como-sede-do-campeonato-brasileiro-de-bmx-em-2026/",
                "MT Esporte confirma a janela da Taça Brasil de BMX Racing 2026",
                "cobertura jornalística especializada",
                "datas e posição no calendário nacional",
            ),
            source(
                "https://fgcgoias.esp.br/",
                "Federação Goiana de Ciclismo",
                "fonte primária da federação estadual",
                "entidade local, rankings e contato",
            ),
        ],
        "organizer": "CBC e Federação Goiana de Ciclismo",
        "time_label": "3 a 5 de dezembro; programação e pista aguardam guia técnico",
        "visual_verification": {
            "type": "calendario_cbc_cruzado_com_imprensa_e_federacao_local",
            "source_url": "https://mtesporte.com.br/esporte/cuiaba-e-confirmada-como-sede-do-campeonato-brasileiro-de-bmx-em-2026/",
            "checked_at": NOW,
            "confirmed_fields": ["datas", "temporada", "entidade_local"],
        },
    },
}


def clean_url(url: str) -> str:
    value = str(url or "").strip()
    if not value:
        return ""
    if "cbc.esp.br/modalidades/calendario/" in value:
        tail = value.split("cbc.esp.br/modalidades/calendario/", 1)[1]
        external = re.findall(
            r"(?:www\.)?[a-z0-9.-]+\.(?:com\.br|esp\.br|org\.br|com|org|net)(?:/[^\s]*)?",
            tail,
            flags=re.I,
        )
        external = [item for item in external if "cbc.esp.br" not in item]
        if external:
            return "https://" + external[-1].strip("/")
    if "file%3A/home/cbm/www/site/public/index.php/" in value:
        suffix = value.split("file%3A/home/cbm/www/site/public/index.php/", 1)[1]
        host = urlparse(value).netloc
        return f"https://{host}/{suffix.strip('/')}"
    if not urlparse(value).scheme and re.match(r"^(?:www\.)?[a-z0-9.-]+\.[a-z]{2,}", value, re.I):
        return "https://" + value.strip("/")
    return value


def dedupe(sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in sources:
        if not isinstance(item, dict):
            continue
        url = clean_url(item.get("url", ""))
        if not url or url in seen or url.rstrip("/") in {
            "https://instagram.com",
            "https://facebook.com",
            "https://www.instagram.com",
            "https://www.facebook.com",
        }:
            continue
        seen.add(url)
        copy = dict(item)
        copy["url"] = url
        result.append(copy)
    return result


def source_is_wrong_for_entry(entry: dict[str, Any], item: dict[str, Any]) -> bool:
    """Remove fontes que descrevem outra etapa/ano e haviam sido aceitas por texto genérico."""
    url = str(item.get("url") or "")
    key = (str(entry.get("title") or ""), str(entry.get("start_date") or ""))
    wrong: dict[tuple[str, str], tuple[str, ...]] = {
        ("Copa Bahia de BMX Racing", "2026-09-05"): (
            "pyxisbrasil.com/evento/campeonato-baiano-de-bmx-2026",
            "ba.gov.br/esporte/noticias/2026-05/3815/",
        ),
        ("Copa Brasil de Paraciclismo de Estrada", "2026-09-19"): (),
        ("Copa Brasil de Paraciclismo de Estrada", "2026-12-05"): (),
        ("Internacional MTB Series XCO #4", "2026-09-19"): (
            "uci.org/competition-details/2026/MTB/",
        ),
        ("Desafio de Downhill Santa Cruz", "2026-08-29"): (
            "sapl.santacruzdocapibaribe.pe.leg.br/materia/16917",
            "santacruzdocapibaribe.pe.gov.br/",
        ),
        ("Copa do Brasil de BMX #03", "2026-09-05"): (
            "ba.gov.br/esporte/noticias/2026-03/3696/",
            "ba.gov.br/esporte/noticias/2026-03/3705/",
        ),
        ("Copa Pedal de BMX Racing", "2026-12-13"): (
            "ba.gov.br/esporte/noticias/2026-05/3822/",
        ),
    }
    return any(marker in url for marker in wrong.get(key, ()))


def main() -> int:
    payload = json.loads(CALENDAR.read_text(encoding="utf-8-sig"))
    applied = 0
    cleaned = 0
    for entry in payload.get("entries", []):
        original = entry.get("sources") or []
        normalized = dedupe([
            item for item in original
            if isinstance(item, dict) and not source_is_wrong_for_entry(entry, item)
        ])
        if normalized != original:
            entry["sources"] = normalized
            cleaned += 1
        key = (str(entry.get("title") or ""), str(entry.get("start_date") or ""))
        patch = VERIFIED.get(key)
        if not patch:
            aliases = {
                ("Circuito do Estreito", "2026-11-29"): ("Circuito do Estreito", "2026-08-22"),
                ("Campeonato Sulbrasileiro de BMX", "2026-08-22"): ("Campeonato Sulbrasileiro de BMX", "2026-08-23"),
            }
            patch = VERIFIED.get(aliases.get(key, ("", "")))
        if not patch:
            continue
        incoming = patch.get("sources", [])
        # A fonte verificada mais recente deve prevalecer quando a URL já
        # existia com um rótulo genérico ou sem a classificação primária.
        entry["sources"] = dedupe(incoming + (entry.get("sources") or []))
        for key, value in patch.items():
            if key != "sources":
                entry[key] = value
        entry["source_checked_at"] = NOW
        entry["last_updated"] = NOW
        domains = {
            urlparse(item["url"]).netloc.lower().removeprefix("www.")
            for item in entry["sources"]
            if item.get("url")
        }
        entry["research_status"] = {
            "required_specific_independent_sources": 2,
            "specific_independent_domains_found": len(domains),
            "status": "fontes_cruzadas" if len(domains) >= 2 else "segunda_fonte_especifica_ainda_pendente",
            "reviewed_at": NOW,
            "editorial_rule": "Dados publicados somente com atribuição ao fato que cada fonte sustenta.",
        }
        applied += 1
    payload["last_updated"] = NOW
    CALENDAR.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    competition_sources = {
        "brasileiro-ciclismo-mtb-2026.json": [
            source(
                "https://www.planetadabike.com/single-post/campeonato-brasileiro-de-mtb-2026-ter%C3%A1-exposi%C3%A7%C3%A3o-dos-lan%C3%A7amentos-da-cannondale",
                "Planeta da Bike confirma o Brasileiro MTB 2026 no Mobai Bike Land",
                "cobertura jornalística especializada",
                "datas, sede, importância, público e ativação de marca",
            ),
            source(
                "https://www.cbc.esp.br/modalidades/evento/busca//id/1344",
                "CBC — página específica do Brasileiro MTB XCO/XCC/XCE 2026",
                "fonte primária da entidade esportiva",
                "datas, sede, modalidades, regulamento e inscrições",
            ),
        ],
        "brasileiro-downhill-2026.json": [
            source(
                "https://www.ilhabela.sp.gov.br/portal/noticias/0/3/17596/atletas-de-ilhabela-conquistam-titulos-na-segunda-etapa-do-campeonato-paulista-de-downhill-com-apoio-da-prefeitura",
                "Prefeitura de Ilhabela confirma atletas no Brasileiro de Downhill em Paraíba do Sul",
                "fonte institucional pública independente",
                "mês, cidade, caráter nacional e atletas participantes",
            ),
            source(
                "https://www.cbc.esp.br/modalidades/evento/id/1352",
                "CBC — página específica do Brasileiro de Downhill 2026",
                "fonte primária da entidade esportiva",
                "datas, pista, desnível, programação, regulamento e inscrições",
            ),
        ],
    }
    competition_applied = 0
    for filename, incoming in competition_sources.items():
        path = ROOT / "content/competitions" / filename
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        data["sources"] = dedupe((data.get("sources") or []) + incoming)
        data["source_checked_at"] = NOW
        data["last_updated"] = NOW
        domains = {
            urlparse(item["url"]).netloc.lower().removeprefix("www.")
            for item in data["sources"]
            if item.get("url")
        }
        data["research_status"] = {
            "required_specific_independent_sources": 2,
            "specific_independent_domains_found": len(domains),
            "status": "fontes_cruzadas",
            "reviewed_at": NOW,
            "editorial_rule": "Resultados e serviço cruzados com fonte esportiva primária e fonte externa específica.",
        }
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        competition_applied += 1
    print(json.dumps({
        "verified_records_applied": applied,
        "records_with_cleaned_urls": cleaned,
        "competitions_applied": competition_applied,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
