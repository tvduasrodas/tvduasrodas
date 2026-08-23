#!/usr/bin/env python3
"""Aplica lotes editoriais sem remover eventos nem alterar seus slugs.

Os lotes ficam em ``editorial/review/enrichment-batch-*.json``. A rotina valida
slugs, impede alterações estruturais perigosas e preserva todas as fontes já
registradas antes de regravar a agenda comunitária ou os eventos individuais.
"""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from datetime import date, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
AGENDA_PATH = ROOT / "content" / "events" / "agenda-comunitaria-2026.json"
EVENTS_DIR = ROOT / "content" / "events"
CALENDAR_PATH = ROOT / "content" / "calendar" / "cbm-2026.json"
QUEUE_PATH = ROOT / "editorial" / "review" / "eventos-incompletos.json"
DEFAULT_PATTERN = "editorial/review/enrichment-batch-*.json"
PROTECTED_UPDATE_FIELDS = {
    "slug",
    "sources",
    "research",
    "duplicate_of",
    "reclassified_as",
    "canonical",
    "canonical_url",
    "noindex",
    "robots",
    "url",
    "permalink",
    "redirect",
    "redirects",
    "redirect_to",
}
REQUIRED_EDITORIAL_FIELDS = {
    "summary",
    "body",
    "status",
    "verification_status",
    "last_updated",
    "source_checked_at",
}
RECURSIVELY_BLOCKED_PATCH_KEYS = {
    "duplicate_of",
    "reclassified_as",
    "noindex",
    "no_index",
    "robots",
    "robot",
    "unpublish",
    "unpublished",
    "is_published",
    "hidden",
    "is_hidden",
    "exclude_from_index",
    "excluded_from_index",
}
RECURSIVELY_BLOCKED_PATCH_KEY_PREFIXES = (
    "canonical",
    "redirect",
    "suppress",
    "deindex",
    "noindex",
    "robots",
    "canonic",
    "redirecion",
    "supress",
    "suprim",
    "desindex",
)
TEMPORAL_STATUS_SUMMARY_NOTE = (
    "A classificação como concluída decorre apenas da passagem da data final "
    "e não comprova que o evento tenha sido realizado."
)
TEMPORAL_STATUS_BODY_NOTE = (
    "## Nota de status\n\n"
    "O status foi atualizado para concluída somente porque a data final já passou. "
    "Essa atualização temporal não comprova que o evento tenha sido realizado."
)
TEMPORAL_STATUS_BASIS_MARKER = "Normalização temporal automática"


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError(f"JSON raiz precisa ser objeto: {path}")
    return payload


def merge_queries(current: Any, incoming: Any) -> list[str]:
    merged: list[str] = []
    for value in (current if isinstance(current, list) else []):
        text = str(value).strip()
        if text and text not in merged:
            merged.append(text)
    for value in (incoming if isinstance(incoming, list) else []):
        text = str(value).strip()
        if text and text not in merged:
            merged.append(text)
    return merged


def source_url(source: Any) -> str:
    return str(source.get("url") or "").strip() if isinstance(source, dict) else ""


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFD", value)
    ascii_value = "".join(char for char in normalized if unicodedata.category(char) != "Mn")
    return re.sub(r"(^-+|-+$)", "", re.sub(r"[^a-z0-9]+", "-", ascii_value.lower()))


def normalized_key(value: Any) -> str:
    # Normalize snake_case, kebab-case and camelCase to the same representation so
    # a nested patch cannot bypass the guard by changing only the key spelling.
    text = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", str(value))
    text = unicodedata.normalize("NFD", text)
    ascii_value = "".join(char for char in text if unicodedata.category(char) != "Mn")
    return re.sub(r"[^a-z0-9]+", "_", ascii_value.casefold()).strip("_")


def is_recursively_blocked_patch_key(value: Any) -> bool:
    key = normalized_key(value)
    return key in RECURSIVELY_BLOCKED_PATCH_KEYS or key.startswith(
        RECURSIVELY_BLOCKED_PATCH_KEY_PREFIXES
    )


def find_recursively_blocked_patch_keys(value: Any, path: str = "patch") -> list[str]:
    blocked: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if is_recursively_blocked_patch_key(key):
                blocked.append(child_path)
            blocked.extend(find_recursively_blocked_patch_keys(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            blocked.extend(find_recursively_blocked_patch_keys(child, f"{path}[{index}]"))
    return blocked


def parse_iso_date(value: Any) -> date | None:
    text = str(value or "").strip()
    if not text:
        return None
    try:
        return date.fromisoformat(text[:10])
    except ValueError:
        return None


def append_once(current: Any, addition: str, separator: str) -> str:
    text = str(current or "").strip()
    if addition in text:
        return text
    return f"{text}{separator if text else ''}{addition}"


def normalize_elapsed_scheduled_events(
    by_slug: dict[str, dict[str, Any]],
    touched: list[str],
    now: datetime | None = None,
) -> list[str]:
    checked_at = (now or datetime.now().astimezone()).replace(microsecond=0)
    today = checked_at.date()
    timestamp = checked_at.isoformat()
    normalized: list[str] = []

    for slug in touched:
        target = by_slug[slug]
        status = str(target.get("status") or "").strip().casefold()
        if status != "agendada":
            # Estados cancelados e todos os demais estados permanecem intocados.
            continue
        end_date = parse_iso_date(target.get("end_date"))
        if end_date is None or end_date >= today:
            continue

        target["status"] = "concluida"
        target["summary"] = append_once(
            target.get("summary"), TEMPORAL_STATUS_SUMMARY_NOTE, " "
        )
        target["body"] = append_once(
            target.get("body"), TEMPORAL_STATUS_BODY_NOTE, "\n\n"
        )
        temporal_basis = (
            f"{TEMPORAL_STATUS_BASIS_MARKER} em {today.isoformat()}: a data final "
            f"{end_date.isoformat()} já passou; isso não comprova a realização do evento."
        )
        target["status_basis"] = append_once(
            target.get("status_basis"), temporal_basis, " "
        )
        target["status_checked_at"] = timestamp
        target["last_updated"] = timestamp
        normalized.append(slug)

    return normalized


def require_exact_queue_order(touched: list[str], queue_slugs: list[str]) -> None:
    if touched == queue_slugs:
        return

    touched_members = set(touched)
    missing = [slug for slug in queue_slugs if slug not in touched_members]
    first_mismatch = next(
        (
            index
            for index, (actual, expected) in enumerate(
                zip(touched, queue_slugs, strict=False)
            )
            if actual != expected
        ),
        min(len(touched), len(queue_slugs)),
    )
    details = [
        f"recebidos {len(touched)} de {len(queue_slugs)}",
        f"primeira divergência no índice {first_mismatch}",
    ]
    if missing:
        details.append(f"faltam {len(missing)} página(s): {', '.join(missing[:10])}")
    raise ValueError(
        "Com --require-full-queue, os slugs tocados devem ser idênticos "
        "à fila e estar na mesma ordem; " + "; ".join(details)
    )


def load_event_inventory() -> tuple[
    dict[str, Any],
    dict[str, Any],
    dict[str, dict[str, Any]],
    dict[str, Path],
    list[str],
]:
    agenda = load_json(AGENDA_PATH)
    entries = agenda.get("entries")
    if not isinstance(entries, list):
        raise ValueError("A agenda não contém uma lista 'entries'.")

    agenda_slugs = [str(entry.get("slug") or "") for entry in entries]
    if not all(agenda_slugs) or len(agenda_slugs) != len(set(agenda_slugs)):
        raise ValueError("A agenda contém slug vazio ou duplicado antes da aplicação.")
    by_slug: dict[str, dict[str, Any]] = {}
    locations: dict[str, Path] = {}

    # O gerador prioriza arquivos individuais e só depois incorpora a agenda.
    # Replicar essa precedência garante que um lote atualize o registro canônico.
    for path in sorted(EVENTS_DIR.glob("*.json")):
        if path.name in {AGENDA_PATH.name, "index.json"}:
            continue
        payload = load_json(path)
        slug = str(payload.get("slug") or path.stem).strip()
        if not slug:
            raise ValueError(f"Evento individual sem slug: {path}")
        if slug in by_slug:
            raise ValueError(f"Slug duplicado entre eventos individuais: {slug}")
        by_slug[slug] = payload
        locations[slug] = path

    for entry in entries:
        if entry.get("duplicate_of") or entry.get("reclassified_as") == "competition":
            continue
        slug = str(entry.get("slug") or "").strip()
        if slug in by_slug:
            continue
        by_slug[slug] = entry
        locations[slug] = AGENDA_PATH

    calendar = load_json(CALENDAR_PATH)
    calendar_entries = calendar.get("entries")
    if not isinstance(calendar_entries, list):
        raise ValueError("O calendário CBM não contém uma lista 'entries'.")
    for entry in calendar_entries:
        if entry.get("competition_slug"):
            continue
        slug = slugify(f"{entry.get('title', '')}-{entry.get('start_date', '')}")
        if not slug or slug in by_slug:
            continue
        by_slug[slug] = entry
        locations[slug] = CALENDAR_PATH

    original_slugs = list(by_slug)
    return agenda, calendar, by_slug, locations, original_slugs


def apply_batches(
    by_slug: dict[str, dict[str, Any]],
    batch_paths: list[Path],
) -> list[str]:

    touched: list[str] = []
    touched_set: set[str] = set()
    for path in batch_paths:
        payload = load_json(path)
        patches = payload.get("entries")
        if not isinstance(patches, list):
            raise ValueError(f"Lote sem lista 'entries': {path}")
        batch_name = str(payload.get("batch") or path.stem)

        for patch in patches:
            if not isinstance(patch, dict):
                raise ValueError(f"Entrada inválida em {path}")
            blocked_paths = find_recursively_blocked_patch_keys(patch)
            if blocked_paths:
                raise ValueError(
                    "Chaves de supressão, redirecionamento ou canônica são proibidas "
                    f"em qualquer nível do patch ({', '.join(blocked_paths)}): {path}"
                )
            slug = str(patch.get("slug") or "").strip()
            if slug not in by_slug:
                raise ValueError(f"Slug do lote não existe no inventário de eventos: {slug} ({path})")
            if slug in touched_set:
                raise ValueError(f"Slug aparece em mais de um lote: {slug}")
            touched_set.add(slug)
            touched.append(slug)
            target = by_slug[slug]

            updates = patch.get("updates") or {}
            if not isinstance(updates, dict):
                raise ValueError(f"'updates' precisa ser objeto: {slug}")
            protected = PROTECTED_UPDATE_FIELDS.intersection(updates)
            if protected:
                fields = ", ".join(sorted(protected))
                raise ValueError(f"Campos protegidos em updates ({fields}): {slug}")
            missing_editorial = sorted(
                field
                for field in REQUIRED_EDITORIAL_FIELDS
                if not str(updates.get(field) or target.get(field) or "").strip()
            )
            if missing_editorial:
                raise ValueError(
                    f"Campos editoriais ausentes ({', '.join(missing_editorial)}): {slug}"
                )
            final_body = updates.get("body") or target.get("body") or ""
            if len(str(final_body).strip()) < 350:
                raise ValueError(f"Conteúdo aprofundado abaixo de 350 caracteres: {slug}")
            for key, value in updates.items():
                if value is not None:
                    target[key] = value

            existing_sources = target.get("sources")
            if not isinstance(existing_sources, list):
                existing_sources = []
            known_urls = {source_url(source) for source in existing_sources if source_url(source)}
            additional_sources = patch.get("additional_sources") or []
            if not isinstance(additional_sources, list):
                raise ValueError(f"'additional_sources' precisa ser lista: {slug}")
            for source in additional_sources:
                url = source_url(source)
                if not url:
                    raise ValueError(f"Fonte sem URL: {slug} ({path})")
                if not str(source.get("label") or "").strip():
                    raise ValueError(f"Fonte sem rótulo: {slug} ({url})")
                if not str(source.get("type") or "").strip():
                    raise ValueError(f"Fonte sem tipo: {slug} ({url})")
                if not str(source.get("supports") or "").strip():
                    raise ValueError(f"Fonte sem rastreabilidade 'supports': {slug} ({url})")
                if url not in known_urls:
                    existing_sources.append(source)
                    known_urls.add(url)
            target["sources"] = existing_sources

            research_patch = patch.get("research") or {}
            if not isinstance(research_patch, dict):
                raise ValueError(f"'research' precisa ser objeto: {slug}")
            research = target.get("research")
            if not isinstance(research, dict):
                research = {}
            if "query" in research_patch:
                research["query"] = merge_queries(research.get("query"), research_patch.get("query"))
            for key, value in research_patch.items():
                if key != "query" and value is not None:
                    research[key] = value
            target["research"] = research

            provenance = target.get("editorial_enrichment_batches")
            if not isinstance(provenance, list):
                provenance = []
            if batch_name not in provenance:
                provenance.append(batch_name)
            target["editorial_enrichment_batches"] = provenance

    return touched


def write_inventory(
    agenda: dict[str, Any],
    calendar: dict[str, Any],
    by_slug: dict[str, dict[str, Any]],
    locations: dict[str, Path],
    touched: list[str],
) -> None:
    agenda_touched = any(locations[slug] == AGENDA_PATH for slug in touched)
    if agenda_touched:
        AGENDA_PATH.write_text(
            json.dumps(agenda, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    calendar_touched = any(locations[slug] == CALENDAR_PATH for slug in touched)
    if calendar_touched:
        CALENDAR_PATH.write_text(
            json.dumps(calendar, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    for slug in touched:
        path = locations[slug]
        if path in {AGENDA_PATH, CALENDAR_PATH}:
            continue
        path.write_text(
            json.dumps(by_slug[slug], ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--pattern",
        default=DEFAULT_PATTERN,
        help="Padrão de lotes relativo à raiz do projeto.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Grava a agenda; sem esta opção, apenas valida os lotes.",
    )
    parser.add_argument(
        "--require-full-queue",
        action="store_true",
        help="Recusa a aplicação se os lotes não cobrirem exatamente a fila editorial atual.",
    )
    args = parser.parse_args()

    batch_paths = sorted(ROOT.glob(args.pattern))
    if not batch_paths:
        raise SystemExit(f"Nenhum lote encontrado para: {args.pattern}")
    agenda, calendar, by_slug, locations, original_slugs = load_event_inventory()
    touched = apply_batches(by_slug, batch_paths)
    temporally_normalized = normalize_elapsed_scheduled_events(by_slug, touched)
    if list(by_slug) != original_slugs:
        raise ValueError("A aplicação alterou a quantidade, a ordem ou os slugs dos eventos.")
    queue_total = None
    if QUEUE_PATH.exists():
        queue = load_json(QUEUE_PATH).get("queue")
        if not isinstance(queue, list):
            raise ValueError("A fila editorial não contém uma lista 'queue'.")
        queue_slugs = [str(item.get("slug") or "").strip() for item in queue]
        if not all(queue_slugs) or len(queue_slugs) != len(set(queue_slugs)):
            raise ValueError("A fila editorial contém slug vazio ou duplicado.")
        queue_total = len(queue_slugs)
        outside_queue = sorted(set(touched) - set(queue_slugs))
        if outside_queue:
            raise ValueError(
                "Lotes contêm páginas fora da fila editorial: "
                + ", ".join(outside_queue[:10])
            )
        if args.require_full_queue:
            require_exact_queue_order(touched, queue_slugs)
    elif args.require_full_queue:
        raise ValueError("--require-full-queue exige a fila editorial existente.")
    if args.apply:
        write_inventory(agenda, calendar, by_slug, locations, touched)
    mode = "aplicado" if args.apply else "validado"
    print(
        f"Lotes: {len(batch_paths)} | eventos {mode}s: {len(touched)} | "
        f"inventário preservado: {len(by_slug)}"
        + (f" | cobertura da fila: {len(touched)}/{queue_total}" if queue_total is not None else "")
        + f" | status vencido normalizado: {len(temporally_normalized)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
