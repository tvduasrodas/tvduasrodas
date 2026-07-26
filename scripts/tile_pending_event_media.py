#!/usr/bin/env python3
"""Cria faixas ampliadas dos flyers para melhorar a leitura de rodapés e contatos."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "output/audit-flyers/manifest.json"
OUT_DIR = ROOT / "output/audit-flyers/tiles"
OUT_MANIFEST = ROOT / "output/audit-flyers/tiles-manifest.json"


def main() -> int:
    payload = json.loads(SOURCE.read_text(encoding="utf-8-sig"))
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    items: list[dict[str, str]] = []
    failures: list[dict[str, str]] = []
    for item in payload.get("items", []):
        source = ROOT / item["path"]
        if source.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
            continue
        try:
            with Image.open(source) as original:
                image = ImageOps.exif_transpose(original).convert("RGB")
                width, height = image.size
                # Três faixas com sobreposição preservam textos que cruzam limites.
                spans = ((0.00, 0.42), (0.29, 0.74), (0.61, 1.00))
                for index, (start, end) in enumerate(spans, 1):
                    tile = image.crop((0, int(height * start), width, int(height * end)))
                    target_width = min(2200, max(1600, tile.width * 2))
                    if tile.width < target_width:
                        target_height = round(tile.height * target_width / tile.width)
                        tile = tile.resize((target_width, target_height), Image.Resampling.LANCZOS)
                    tile = ImageEnhance.Contrast(tile).enhance(1.12)
                    path = OUT_DIR / f"{item['slug']}--tile-{index}.jpg"
                    tile.save(path, "JPEG", quality=94, optimize=True)
                    items.append(
                        {
                            "slug": item["slug"],
                            "url": item["url"],
                            "path": str(path.relative_to(ROOT)),
                            "tile": str(index),
                        }
                    )
        except Exception as exc:
            failures.append(
                {"slug": item["slug"], "path": item["path"], "error": str(exc)}
            )
    report = {
        "requested": len(items),
        "downloaded": len(items),
        "failed": len(failures),
        "items": items,
        "failures": failures,
    }
    OUT_MANIFEST.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"tiles": len(items), "failed": len(failures)}))
    return 0 if not failures else 2


if __name__ == "__main__":
    raise SystemExit(main())
