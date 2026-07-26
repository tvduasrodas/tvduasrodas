#!/usr/bin/env python3
"""Baixa, em paralelo, as artes dos eventos que ainda exigem auditoria visual."""

from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any
from urllib.parse import urlparse
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
AGENDA = ROOT / "content/events/agenda-comunitaria-2026.json"
AUDIT = ROOT / "output/source-depth-sports-pass4.json"
OUT = ROOT / "output/audit-flyers"
USER_AGENT = "Mozilla/5.0 (compatible; TVDUASRODAS-VisualAudit/1.0)"


def extension(url: str, content_type: str = "") -> str:
    suffix = Path(urlparse(url).path).suffix.lower()
    if suffix in {".jpg", ".jpeg", ".png", ".webp", ".gif", ".mp4"}:
        return suffix
    guessed = mimetypes.guess_extension(content_type.split(";", 1)[0].strip())
    return guessed or ".bin"


def download(item: dict[str, str], timeout: int) -> dict[str, Any]:
    request = Request(item["url"], headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=timeout) as response:
        raw = response.read(15_000_000)
        ext = extension(item["url"], response.headers.get("Content-Type", ""))
    digest = hashlib.sha1(item["url"].encode("utf-8")).hexdigest()[:12]
    path = OUT / f"{item['slug']}--{digest}{ext}"
    path.write_bytes(raw)
    return {**item, "path": str(path.relative_to(ROOT)), "bytes": len(raw)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=10)
    parser.add_argument("--timeout", type=int, default=25)
    args = parser.parse_args()

    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    pending = {
        item["slug"] for item in audit["queue"] if item["kind"] == "agenda"
    }
    agenda = json.loads(AGENDA.read_text(encoding="utf-8-sig"))
    jobs: list[dict[str, str]] = []
    for entry in agenda["entries"]:
        if entry.get("slug") not in pending:
            continue
        candidates = [
            str(entry.get("source_url") or ""),
            *[
                str(source.get("url") or "")
                for source in entry.get("sources", [])
                if isinstance(source, dict)
            ],
        ]
        media = next(
            (
                url
                for url in candidates
                if Path(urlparse(url).path).suffix.lower()
                in {".jpg", ".jpeg", ".png", ".webp", ".gif", ".mp4"}
            ),
            "",
        )
        if media:
            jobs.append({"slug": entry["slug"], "url": media})

    OUT.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, Any]] = []
    failures: list[dict[str, str]] = []
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        futures = {pool.submit(download, job, args.timeout): job for job in jobs}
        for future in as_completed(futures):
            try:
                results.append(future.result())
            except Exception as exc:
                failures.append({**futures[future], "error": str(exc)})

    manifest = {
        "requested": len(jobs),
        "downloaded": len(results),
        "failed": len(failures),
        "items": sorted(results, key=lambda item: item["slug"]),
        "failures": sorted(failures, key=lambda item: item["slug"]),
    }
    (OUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({key: manifest[key] for key in ("requested", "downloaded", "failed")}))
    return 0 if not failures else 2


if __name__ == "__main__":
    raise SystemExit(main())
