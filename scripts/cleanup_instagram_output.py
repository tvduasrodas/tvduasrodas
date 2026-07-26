from __future__ import annotations

import argparse
import json
import os
import re
import shutil
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
INSTAGRAM_ROOT = (ROOT / "output" / "instagram").resolve()
DEFAULT_LOG = INSTAGRAM_ROOT / "publication-log.json"
PROTECTED_TOP_LEVEL = {"design-review", "source"}
PUBLICATION_FIELDS = ("asset", "cover", "poster", "copy", "caption")
NOT_APPLICABLE_PREFIXES = ("NAO_APLICAVEL", "NÃO_APLICÁVEL")


def parse_datetime(value: object) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    normalized = value.strip().replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed


def has_publication_confirmation(channel: dict[str, Any]) -> bool:
    permalink = str(channel.get("permalink", "")).strip()
    confirmation = str(channel.get("publicationConfirmation", "")).strip()
    content_id = str(channel.get("metaContentId", "")).strip()
    return permalink.startswith("https://") or bool(confirmation) or bool(content_id)


def channel_publication_time(
    record: dict[str, Any], name: str, *, required: bool
) -> tuple[datetime | None, str | None]:
    channel = record.get(name)
    if not isinstance(channel, dict):
        return (None, f"{name}_ausente") if required else (None, None)

    status = str(channel.get("status", "")).strip().upper()
    if not required and (
        not status or any(status.startswith(prefix) for prefix in NOT_APPLICABLE_PREFIXES)
    ):
        return None, None
    if status != "PUBLICADO":
        return None, f"{name}_status_{status or 'ausente'}"

    published_at = parse_datetime(channel.get("publishedAt"))
    if published_at is None:
        return None, f"{name}_publishedAt_invalido_ou_ausente"
    if not has_publication_confirmation(channel):
        return None, f"{name}_sem_confirmacao"
    return published_at, None


def collect_local_references(record: dict[str, Any]) -> list[Path]:
    references: list[Path] = []
    for channel_name in ("feed", "stories", "reel"):
        channel = record.get(channel_name)
        if not isinstance(channel, dict):
            continue
        for field in PUBLICATION_FIELDS:
            raw = channel.get(field)
            if not isinstance(raw, str) or not raw.strip():
                continue
            normalized = raw.replace("\\", "/").strip()
            if not normalized.startswith("output/instagram/"):
                continue
            references.append((ROOT / normalized).resolve())
    return references


def safe_publication_folder(record: dict[str, Any]) -> tuple[Path | None, str | None]:
    references = collect_local_references(record)
    if not references:
        return None, "sem_arquivos_locais_registrados"

    try:
        common = Path(os.path.commonpath([str(path.parent) for path in references])).resolve()
    except ValueError:
        return None, "referencias_em_unidades_diferentes"

    if common == INSTAGRAM_ROOT or INSTAGRAM_ROOT not in common.parents:
        return None, "pasta_comum_fora_do_escopo_seguro"
    relative = common.relative_to(INSTAGRAM_ROOT)
    if not relative.parts or relative.parts[0] in PROTECTED_TOP_LEVEL:
        return None, "pasta_protegida"
    if common.is_symlink():
        return None, "link_simbolico_nao_permitido"
    if not common.is_dir():
        return None, "pasta_local_ausente"
    return common, None


def folder_stats(folder: Path) -> tuple[int, int]:
    file_count = 0
    total_bytes = 0
    for path in folder.rglob("*"):
        if path.is_file() and not path.is_symlink():
            file_count += 1
            total_bytes += path.stat().st_size
    return file_count, total_bytes


def build_plan(
    records: list[dict[str, Any]], now: datetime, retention: timedelta
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    candidates: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    folder_owners: dict[Path, list[int]] = {}

    for index, record in enumerate(records):
        title = str(record.get("title", f"registro_{index + 1}"))
        if isinstance(record.get("localCleanup"), dict):
            skipped.append({"index": index, "title": title, "reason": "limpeza_ja_registrada"})
            continue

        publication_times: list[datetime] = []
        reasons: list[str] = []
        for channel_name, required in (("stories", True), ("reel", True), ("feed", False)):
            published_at, reason = channel_publication_time(
                record, channel_name, required=required
            )
            if published_at is not None:
                publication_times.append(published_at)
            if reason:
                reasons.append(reason)
        if reasons:
            skipped.append(
                {"index": index, "title": title, "reason": ",".join(reasons)}
            )
            continue

        latest_publication = max(publication_times)
        eligible_at = latest_publication + retention
        if now < eligible_at:
            skipped.append(
                {
                    "index": index,
                    "title": title,
                    "reason": "prazo_24h_nao_cumprido",
                    "eligibleAt": eligible_at.isoformat(),
                }
            )
            continue

        folder, reason = safe_publication_folder(record)
        if folder is None:
            skipped.append({"index": index, "title": title, "reason": reason})
            continue

        file_count, total_bytes = folder_stats(folder)
        candidate = {
            "index": index,
            "title": title,
            "folder": folder,
            "latestPublishedAt": latest_publication.isoformat(),
            "eligibleAt": eligible_at.isoformat(),
            "fileCount": file_count,
            "bytes": total_bytes,
        }
        candidates.append(candidate)
        folder_owners.setdefault(folder, []).append(index)

    shared_folders = {folder for folder, owners in folder_owners.items() if len(owners) > 1}
    if shared_folders:
        retained: list[dict[str, Any]] = []
        for candidate in candidates:
            if candidate["folder"] in shared_folders:
                skipped.append(
                    {
                        "index": candidate["index"],
                        "title": candidate["title"],
                        "reason": "pasta_compartilhada_por_varios_registros",
                    }
                )
            else:
                retained.append(candidate)
        candidates = retained
    return candidates, skipped


def write_log_atomically(path: Path, records: list[dict[str, Any]]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    temporary.replace(path)


def apply_cleanup(
    candidates: list[dict[str, Any]],
    records: list[dict[str, Any]],
    log_path: Path,
    now: datetime,
    retention_hours: float,
) -> None:
    for candidate in candidates:
        folder = Path(candidate["folder"]).resolve()
        if folder == INSTAGRAM_ROOT or INSTAGRAM_ROOT not in folder.parents:
            raise RuntimeError(f"Destino inseguro recusado durante a aplicação: {folder}")
        relative = folder.relative_to(INSTAGRAM_ROOT)
        if not relative.parts or relative.parts[0] in PROTECTED_TOP_LEVEL:
            raise RuntimeError(f"Pasta protegida recusada durante a aplicação: {folder}")

        shutil.rmtree(folder)
        parent = folder.parent
        if (
            parent != INSTAGRAM_ROOT
            and parent.parent == INSTAGRAM_ROOT
            and re.fullmatch(r"\d{4}-\d{2}-\d{2}", parent.name)
            and not any(parent.iterdir())
        ):
            parent.rmdir()

        record = records[int(candidate["index"])]
        record["localCleanup"] = {
            "status": "EXCLUIDO_APOS_PUBLICACAO",
            "deletedAt": now.isoformat(),
            "retentionHours": retention_hours,
            "folder": folder.relative_to(ROOT).as_posix(),
            "fileCount": candidate["fileCount"],
            "bytesFreed": candidate["bytes"],
            "latestPublishedAt": candidate["latestPublishedAt"],
            "reason": "Story e Reel confirmados no Instagram há pelo menos 24 horas.",
        }
    write_log_atomically(log_path, records)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Remove arquivos locais de publicações do Instagram confirmadas há pelo "
            "menos 24 horas. O padrão é apenas simulação."
        )
    )
    parser.add_argument("--apply", action="store_true", help="Aplica as exclusões elegíveis.")
    parser.add_argument("--retention-hours", type=float, default=24.0)
    parser.add_argument("--log", type=Path, default=DEFAULT_LOG)
    parser.add_argument(
        "--now",
        help="Data/hora ISO 8601 para teste; quando omitida, usa o relógio atual.",
    )
    args = parser.parse_args()

    if args.retention_hours < 24:
        raise ValueError("A retenção nunca pode ser inferior a 24 horas.")
    log_path = args.log.resolve()
    if log_path != DEFAULT_LOG.resolve() and INSTAGRAM_ROOT not in log_path.parents:
        raise ValueError("O registro de publicação deve ficar dentro de output/instagram.")
    now = parse_datetime(args.now) if args.now else datetime.now().astimezone()
    if now is None:
        raise ValueError("--now deve usar ISO 8601 com fuso horário.")

    data = json.loads(log_path.read_text(encoding="utf-8"))
    if not isinstance(data, list) or any(not isinstance(item, dict) for item in data):
        raise ValueError("publication-log.json deve conter uma lista de registros.")

    retention = timedelta(hours=args.retention_hours)
    candidates, skipped = build_plan(data, now, retention)
    total_bytes = sum(int(item["bytes"]) for item in candidates)
    summary = {
        "mode": "apply" if args.apply else "dry-run",
        "now": now.isoformat(),
        "retentionHours": args.retention_hours,
        "eligibleCount": len(candidates),
        "eligibleBytes": total_bytes,
        "eligibleFolders": [
            {
                **{key: value for key, value in item.items() if key != "folder"},
                "folder": Path(item["folder"]).relative_to(ROOT).as_posix(),
            }
            for item in candidates
        ],
        "skipped": skipped,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))

    if args.apply and candidates:
        apply_cleanup(candidates, data, log_path, now, args.retention_hours)
        print(f"CLEANUP_APPLIED={len(candidates)}")
        print(f"BYTES_FREED={total_bytes}")
    elif args.apply:
        print("CLEANUP_APPLIED=0")


if __name__ == "__main__":
    main()
