"""Cria uma cópia WebP leve para publicação editorial.

Uso: python scripts/optimize_image.py origem destino [largura] [qualidade]
"""

from pathlib import Path
import subprocess
import sys


def load_pillow():
    try:
        from PIL import Image, ImageOps
        return Image, ImageOps
    except ModuleNotFoundError:
        bundled_python = (
            Path.home()
            / ".cache"
            / "codex-runtimes"
            / "codex-primary-runtime"
            / "dependencies"
            / "python"
            / "python.exe"
        )
        if bundled_python.exists() and Path(sys.executable).resolve() != bundled_python.resolve():
            result = subprocess.run(
                [str(bundled_python), str(Path(__file__).resolve()), *sys.argv[1:]],
                check=False,
            )
            raise SystemExit(result.returncode)
        raise SystemExit(
            "Pillow não está disponível. Instale Pillow ou execute este script "
            "com o Python incluído no ambiente do Codex."
        )


def main() -> int:
    if len(sys.argv) < 3:
        print("Uso: optimize_image.py origem destino [largura] [qualidade]")
        return 2

    Image, ImageOps = load_pillow()
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
