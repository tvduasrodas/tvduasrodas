#!/usr/bin/env python3
"""Normaliza serviço e transparência editorial após a pesquisa cruzada."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import research_all_events as research


ROOT = Path(__file__).resolve().parents[1]
CALENDAR_PATH = ROOT / "content/calendar/cbm-2026.json"
COMPETITIONS_DIR = ROOT / "content/competitions"


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def organizer_for(entry: dict[str, Any]) -> str:
    modality = str(entry.get("modality") or "").lower()
    if any(marker in modality for marker in ("ciclismo", "mtb", "downhill", "bmx", "paraciclismo")):
        return "Organizador local com homologação ou inclusão no calendário da Confederação Brasileira de Ciclismo"
    return "Organizador da etapa com supervisão da entidade esportiva responsável"


def source_labels(entry: dict[str, Any]) -> str:
    labels = [
        str(source.get("label") or "").strip()
        for source in (entry.get("sources") or [])
        if isinstance(source, dict) and source.get("label")
    ]
    return "; ".join(labels[:4]) or "fontes oficiais e específicas registradas nesta página"


def normalize_calendar() -> int:
    payload = load(CALENDAR_PATH)
    changed = 0
    now = datetime.now(timezone.utc).isoformat()
    for entry in payload.get("entries", []):
        if entry.get("title") == "Barras Marathon":
            continue
        city = entry.get("city") or ""
        state = entry.get("state") or ""
        location = entry.get("venue") or entry.get("location") or " · ".join(filter(None, (city, state)))
        if not location:
            location = "Local ainda não definido pela organização"
        entry.setdefault("organizer", organizer_for(entry))
        entry.setdefault("venue", location)
        entry.setdefault("full_address", (
            f"{location}. Rua, número e ponto de referência ainda não foram publicados nas fontes consultadas."
            if city else "Cidade, endereço e ponto de referência ainda não foram publicados nas fontes consultadas."
        ))
        entry.setdefault(
            "time_label",
            "Horários de largada, abertura, credenciamento ou programação ainda não foram publicados nas fontes específicas consultadas.",
        )
        entry.setdefault(
            "admission_status",
            "Inscrição, ingresso ou acesso devem ser confirmados com o organizador; as fontes consultadas ainda não detalham essa condição.",
        )
        entry.setdefault(
            "parking",
            "Estacionamento e guarda de bicicletas/motos ainda não foram detalhados pelas fontes consultadas.",
        )
        entry.setdefault(
            "contact",
            "Use os links de fontes cruzadas abaixo; telefone ou e-mail específico não foi publicado nas páginas consultadas.",
        )
        visual_sources = [
            source for source in (entry.get("sources") or [])
            if any(marker in str(source.get("url") or "") for marker in ("instagram.com", "facebook.com", "youtube.com"))
        ]
        entry.setdefault("visual_verification", {
            "type": "material_visual_indexado" if visual_sources else "fontes_textuais_sem_flyer_publico",
            "source_url": (visual_sources[0].get("url") if visual_sources else entry.get("official_url", "")),
            "checked_at": entry.get("source_checked_at") or now,
            "note": (
                "Canal visual localizado na pesquisa; detalhes devem ser reconferidos quando o regulamento final for publicado."
                if visual_sources
                else "Nenhum flyer público específico foi localizado nos resultados indexados; a ausência foi registrada, sem inventar serviço."
            ),
        })
        stage = entry.get("stage") or "etapa ou prova do calendário"
        modality = entry.get("modality") or "duas rodas"
        entry.setdefault(
            "summary",
            f"{entry.get('title')} está no calendário de 2026 como {stage}, na modalidade {modality}, "
            f"com realização prevista para {entry.get('start_date')}"
            f"{(' a ' + entry.get('end_date')) if entry.get('end_date') else ''}"
            f"{(' em ' + city + '/' + state) if city else ''}. Serviço ainda não publicado permanece sinalizado.",
        )
        entry.setdefault(
            "body",
            f"## Situação verificada\n\n{entry.get('title')} aparece no calendário monitorado para "
            f"{entry.get('start_date')}{(' a ' + entry.get('end_date')) if entry.get('end_date') else ''}. "
            f"O enquadramento divulgado é {stage}, na modalidade {modality}.\n\n"
            f"## Local e serviço\n\nA referência disponível é {location}. As fontes consultadas ainda não "
            f"publicaram um serviço completo com rua, número, horário, estacionamento e contato direto. "
            f"Essas ausências são mantidas de forma explícita para evitar informação inventada.\n\n"
            f"## Inscrições, categorias e regulamento\n\nInscrições, categorias, percurso, premiação, retirada "
            f"de kits e regras técnicas devem ser confirmados nos canais vinculados abaixo. A página será "
            f"atualizada quando o organizador ou a entidade publicar o regulamento específico.\n\n"
            f"## Fontes cruzadas\n\nForam consultadas: {source_labels(entry)}. Links genéricos de calendário "
            f"não são tratados, sozinhos, como confirmação suficiente de serviço.",
        )
        entry["last_updated"] = now
        changed += 1
    payload["last_updated"] = now
    save(CALENDAR_PATH, payload)
    return changed


def normalize_competitions() -> int:
    changed = 0
    now = datetime.now(timezone.utc).isoformat()
    for path in sorted(COMPETITIONS_DIR.glob("*.json")):
        if path.name == "index.json":
            continue
        data = load(path)
        if not data.get("rounds") and data.get("next_stage"):
            stage = data["next_stage"]
            data["rounds"] = [{
                "name": stage.get("name") or "Próxima etapa",
                "start_date": stage.get("start_date"),
                "end_date": stage.get("end_date"),
                "location": " · ".join(filter(None, (stage.get("venue"), stage.get("city"), stage.get("state")))),
                "status": data.get("status") or "agendada",
                "note": stage.get("note", ""),
            }]
        data["calendar_status"] = {
            "status": "publicado" if data.get("rounds") else "aguardando_calendario_oficial",
            "checked_at": data.get("source_checked_at") or now,
            "note": (
                "Etapas disponíveis na tabela da página."
                if data.get("rounds")
                else "A entidade ainda não publicou etapas suficientes para montar uma tabela sem suposições."
            ),
        }
        if data.get("standings") or (data.get("latest_result") or {}).get("classification"):
            data["classification_status"] = {
                "status": "publicada",
                "checked_at": data.get("source_checked_at") or now,
                "note": "Resultados ou classificação oficial disponíveis nos blocos desta página.",
            }
        else:
            data["classification_status"] = {
                "status": "aguardando_publicacao_oficial",
                "checked_at": data.get("source_checked_at") or now,
                "note": "As fontes oficiais consultadas ainda não disponibilizaram classificação consolidada para publicação.",
            }
        if len(str(data.get("body") or "")) < 350:
            next_stage = data.get("next_stage") or {}
            data["body"] = (
                f"## Temporada 2026\n\n{data.get('title')} é acompanhada pela TVDUASRODAS na modalidade "
                f"{data.get('modality') or 'duas rodas'}, sob organização de {data.get('organizer') or 'entidade responsável'}. "
                f"O status registrado é {data.get('status') or 'em verificação'}.\n\n"
                f"## Próxima etapa e calendário\n\nA referência mais recente é "
                f"{next_stage.get('name') or 'a etapa indicada no calendário'}, com data "
                f"{next_stage.get('start_date') or 'a confirmar'} e local "
                f"{' · '.join(filter(None, (next_stage.get('venue'), next_stage.get('city'), next_stage.get('state')))) or 'a confirmar'}. "
                f"Alterações de data e local são conferidas nos canais oficiais.\n\n"
                f"## Classificação e resultados\n\n{data['classification_status']['note']} "
                f"Quando houver documento oficial, atletas, equipes, categorias, posições, tempos e pontos serão "
                f"publicados com páginas relacionadas para os competidores identificados.\n\n"
                f"## Fontes\n\nA apuração registra {source_labels(data)}. Cada link permanece visível na página "
                f"para permitir a conferência dos dados e da data de atualização."
            )
        data["last_updated"] = now
        save(path, data)
        changed += 1
    return changed


def normalize_sources() -> int:
    changed = 0
    for _kind, path, index, data in research.records():
        retained = [
            source for source in (data.get("sources") or [])
            if not (
                isinstance(source, dict)
                and source.get("discovery_method") == "busca_editorial_indexada"
                and not research.indexed_result_is_specific(data, source)
            )
        ]
        source_data = dict(data)
        source_data["sources"] = retained
        normalized = research.deduplicate_sources(research.seed_sources(source_data))
        if normalized != (data.get("sources") or []):
            updated = dict(data)
            updated["sources"] = normalized
            research.save_record(path, index, updated)
            changed += 1
    return changed


def main() -> int:
    calendar_count = normalize_calendar()
    competition_count = normalize_competitions()
    print(json.dumps({
        "calendar_normalized": calendar_count,
        "competitions_normalized": competition_count,
        "sources_normalized": normalize_sources(),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
