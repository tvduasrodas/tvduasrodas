"""Cria uma cópia WebP leve para publicação editorial.

Uso: python scripts/optimize_image.py origem destino [largura] [qualidade]
"""

from pathlib import Path
import sys

from PIL import Image, ImageOps


def main() -> int:
    if len(sys.argv) < 3:
        print("Uso: optimize_image.py origem destino [largura] [qualidade]")
        return 2

    source = Path(sys.argv[1])
    target = Path(sys.argv[2])
    max_width = int(sys.argv[3]) if len(sys.argv) > 3 else 1600
    quality = int(sys.argv[4]) if len(sys.argv) > 4 else 82

    with Image.open(source) as opened:
        image = ImageOps.exif_transpose(opened).convert("RGB")
        original_size = image.size
        if image.width > max_width:
            new_height = round(image.height * max_width / image.width)
            image = image.resize((max_width, new_height), Image.Resampling.LANCZOS)

        target.parent.mkdir(parents=True, exist_ok=True)
        image.save(target, "WEBP", quality=quality, method=6, optimize=True)

    print(
        f"{source.name}: {original_size[0]}x{original_size[1]} "
        f"({source.stat().st_size} bytes) -> {target.name}: "
        f"{image.width}x{image.height} ({target.stat().st_size} bytes)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
