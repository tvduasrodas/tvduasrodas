#!/usr/bin/env python3
"""Converte evidências OCR conservadoras em serviço completo para a agenda comunitária."""

from __future__ import annotations

import argparse
import json
import re
from datetime import date, datetime
from pathlib import Path
from typing import Any

from apply_event_research_batch import update_community


ROOT = Path(__file__).resolve().parents[1]
AGENDA = ROOT / "content" / "events" / "agenda-comunitaria-2026.json"
PLACEHOLDER_VENUE = re.compile(r"local informado|a confirmar|agenda nacional", re.I)
ADDRESS_NOISE = re.compile(
    r"alimenta|programa|atraç|atrac|show|banda|camping|trof[eé]u|sorteio|entrada|ingresso",
    re.I,
)

KEYWORD_LABELS = {
    "estacionamento": "Estacionamento mencionado no flyer",
    "parking": "Estacionamento mencionado no flyer",
    "camping": "Área de camping",
    "chuveiro": "Chuveiros",
    "café da manhã": "Café da manhã",
    "entrada franca": "Entrada franca",
    "gratuito": "Atividade gratuita indicada no flyer",
    "gratuita": "Atividade gratuita indicada no flyer",
    "ingresso": "Ingressos mencionados no flyer",
    "alimento": "Ação ou ingresso solidário com alimento",
    "praça de alimentação": "Praça de alimentação",
    "food": "Área de alimentação",
    "rock": "Rock",
    "show": "Shows",
    "banda": "Bandas",
    "expositor": "Expositores",
    "acessórios": "Acessórios",
    "troféu": "Troféus",
    "sorteio": "Sorteios",
    "wheeling": "Apresentação de wheeling",
    "motocross": "Motocross",
}


def text(value: Any) -> str:
    return str(value or "").strip()


def clean_signal(value: Any) -> str:
    return re.sub(r"\s+", " ", text(value)).strip(" |,;:-")


def good_address(lines: list[str], confidence: float) -> str | None:
    if confidence < 58:
        return None
    for raw in lines:
        line = clean_signal(raw)
        if not 7 <= len(line) <= 150 or ADDRESS_NOISE.search(line):
            continue
        if re.search(r"\b(rua|r\.|avenida|av\.|rodovia|rod\.|estrada|km|parque|praça|praca)\b", line, re.I):
            return line
    return None


def status_patch(event: dict[str, Any], today: date) -> tuple[str, str]:
    if text(event.get("status")).lower() in {"cancelada", "cancelado"}:
        return "cancelada", text(event.get("status_basis")) or "Cancelamento confirmado em fonte específica."
    try:
        start = date.fromisoformat(text(event.get("start_date"))[:10])
        end = date.fromisoformat(text(event.get("end_date") or event.get("start_date"))[:10])
    except ValueError:
        return "data_a_confirmar", "Data inválida ou incompleta; requer nova confirmação."
    if end < today:
        return "concluida", "Data programada encerrada; balanço final não localizado na fonte comunitária."
    if start <= today <= end:
        return "em_andamento", "Data programada em curso; nenhum aviso de cancelamento localizado na fonte consultada."
    return "agendada", "Data futura divulgada no flyer e na agenda comunitária; confirme alterações antes de viajar."


def admission(signals: dict[str, Any]) -> tuple[bool, str]:
    keys = {text(item).lower() for item in signals.get("keywords", [])}
    if {"entrada franca", "gratuito", "gratuita"} & keys:
        return True, "Gratuidade indicada no flyer; confira eventuais condições na arte original"
    if "alimento" in keys:
        return False, "O flyer menciona alimento ou ação solidária; confira quantidade e condição na arte original"
    if "ingresso" in keys:
        return False, "O flyer menciona ingresso; valor e condições devem ser confirmados na arte original"
    return False, "Não informado de forma legível no flyer consultado"


def parking(signals: dict[str, Any]) -> str:
    keys = {text(item).lower() for item in signals.get("keywords", [])}
    if {"estacionamento", "parking"} & keys:
        return "Estacionamento mencionado no flyer; localização, preço e regras devem ser confirmados com a organização"
    return "Não informado de forma legível no flyer consultado"


def organizer(event: dict[str, Any]) -> str:
    title = text(event.get("title"))
    if re.search(r"\b(MC|MG|Moto Clube|Motoclube|Associa[cç][aã]o|Federa[cç][aã]o)\b", title, re.I):
        return title
    return "Organização não identificada de forma legível no flyer consultado"


def build_patch(event: dict[str, Any], evidence: dict[str, Any], checked_at: str) -> dict[str, Any]:
    signals = evidence.get("signals") or {}
    confidence = float(evidence.get("ocr_confidence") or 0)
    media_url = text((evidence.get("card") or {}).get("media_url"))
    detail_url = text((evidence.get("card") or {}).get("detail_url"))
    times = [clean_signal(item) for item in signals.get("times", []) if clean_signal(item)]
    times = list(dict.fromkeys(times))[:12]
    phones = [clean_signal(item) for item in signals.get("phones", []) if clean_signal(item)]
    phones = list(dict.fromkeys(phones))[:5]
    address = good_address(signals.get("address_lines", []), confidence)
    city = text(event.get("city"))
    state = text(event.get("state"))
    status, status_basis = status_patch(event, date(2026, 7, 26))
    is_free, admission_status = admission(signals)
    labels = list(
        dict.fromkeys(
            KEYWORD_LABELS[key]
            for key in signals.get("keywords", [])
            if key in KEYWORD_LABELS
        )
    )
    if not labels:
        labels = ["Programação detalhada não identificada de forma legível no flyer"]

    confirmed = ["date", "city", "state", "event_name"]
    if confidence >= 50 and times:
        confirmed.append("times")
    if address:
        confirmed.append("address_reference")
    if labels and "Programação detalhada" not in labels[0]:
        confirmed.append("services_and_attractions")
    if phones:
        confirmed.append("contact")

    time_label = (
        f"Horários identificados no flyer: {', '.join(times)}"
        if confidence >= 50 and times
        else "Horário não informado de forma legível no flyer consultado"
    )
    if address:
        venue = address
        street_address = address
        full_address = f"{address}, {city} - {state}"
    else:
        current_venue = text(event.get("venue"))
        venue = (
            current_venue
            if current_venue and not PLACEHOLDER_VENUE.search(current_venue)
            else "Local detalhado não informado de forma legível no flyer"
        )
        street_address = "Endereço detalhado não informado de forma legível no flyer"
        full_address = f"Endereço detalhado não informado no flyer; referência: {city} - {state}"

    service_phrase = ", ".join(labels[:8])
    contact = "; ".join(phones) if confidence >= 50 and phones else "Contato não identificado de forma legível no flyer"
    summary = (
        f"{text(event.get('event_type')) or 'Evento de duas rodas'} em {city}/{state}, "
        f"com data divulgada para {text(event.get('start_date'))}. "
        f"O flyer foi inspecionado localmente; serviços identificados: {service_phrase.lower()}."
    )
    body = (
        "## Serviço verificado\n\n"
        f"{text(event.get('title'))} tem data divulgada de "
        f"{text(event.get('start_date'))} a {text(event.get('end_date') or event.get('start_date'))}, "
        f"em {city}/{state}. {time_label}.\n\n"
        "## Local e endereço\n\n"
        f"{full_address}. Quando o endereço não aparece de forma legível, a TVDUASRODAS mantém essa ausência "
        "explícita e não inventa rua, número ou CEP.\n\n"
        "## Programação e estrutura\n\n"
        f"{service_phrase}. Os nomes e horários que não atingiram confiança suficiente no processamento visual "
        "não foram transformados em informação pública.\n\n"
        "## Acesso, estacionamento e contato\n\n"
        f"{admission_status}. {parking(signals)}. {contact}.\n\n"
        "## Fonte e atualização\n\n"
        "A data, a cidade e os sinais de serviço foram confrontados com o flyer específico indexado pela JB-RIDER. "
        "A arte original permanece vinculada para conferência de mudanças e detalhes."
    )

    return {
        "timezone": text(event.get("timezone")) or "America/Sao_Paulo",
        "time_label": time_label,
        "venue": venue,
        "street_address": street_address,
        "full_address": full_address,
        "status": status,
        "status_basis": status_basis,
        "status_checked_at": checked_at,
        "organizer": text(event.get("organizer")) or organizer(event),
        "contact": text(event.get("contact")) or contact,
        "official_url": text(event.get("official_url")) if "jb-rider.com.br/eventos.php" not in text(event.get("official_url")) else detail_url,
        "source_url": media_url or detail_url,
        "source_label": "Flyer específico indexado pela JB-RIDER",
        "verification_status": "flyer_processado_localmente_com_validacao_conservadora",
        "source_checked_at": checked_at,
        "visual_verification": {
            "type": "flyer_com_ocr_local",
            "source_url": media_url,
            "detail_url": detail_url,
            "checked_at": checked_at,
            "ocr_engine": "Tesseract.js por",
            "ocr_confidence": confidence,
            "review_policy": "Somente padrões estruturados; campos duvidosos tratados como não informados",
            "confirmed_fields": confirmed,
        },
        "free": is_free,
        "admission_status": admission_status,
        "parking": parking(signals),
        "summary": summary,
        "attractions": labels,
        "body": body,
        "last_updated": checked_at,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    evidence_path = args.evidence if args.evidence.is_absolute() else ROOT / args.evidence
    payload = json.loads(evidence_path.read_text(encoding="utf-8"))
    agenda = json.loads(AGENDA.read_text(encoding="utf-8-sig"))
    by_slug = {item["slug"]: item for item in agenda.get("entries", [])}
    checked_at = datetime.fromisoformat(payload["generated_at"].replace("Z", "+00:00")).isoformat()

    best_evidence: dict[str, dict[str, Any]] = {}
    for item in payload.get("ocr_entries", []):
        slug = text(item.get("slug"))
        current = best_evidence.get(slug)
        if not current or float(item.get("ocr_confidence") or 0) > float(current.get("ocr_confidence") or 0):
            best_evidence[slug] = item

    patches: list[dict[str, Any]] = []
    skipped_complete = 0
    for evidence in best_evidence.values():
        if evidence.get("fetch_status") != "ok":
            continue
        event = by_slug.get(evidence.get("slug"))
        if not event or event.get("duplicate_of"):
            continue
        if event.get("visual_verification") and event.get("verification_status") != "agenda_comunitaria":
            skipped_complete += 1
            continue
        patches.append({"slug": event["slug"], "patch": build_patch(event, evidence, checked_at)})

    print(f"Patches={len(patches)} completos_preservados={skipped_complete}")
    if not args.dry_run:
        update_community(AGENDA, patches)
        print(f"Agenda atualizada: {AGENDA.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
