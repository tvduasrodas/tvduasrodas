#!/usr/bin/env python3
"""Monta capas 16:9 de competicoes com foto oficial e marca em destaque."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
ORIGINALS = ROOT / "editorial" / "competition-covers-2026" / "originals"
PREVIEWS = ROOT / "editorial" / "competition-covers-2026" / "previews"

WIDTH, HEIGHT = 1200, 675

COVERS = {
    "arena-cross-brasil-2026": {
        "photo": ROOT / "assets" / "img" / "uploads" / "arenacross-brasil-jundiai-2026-oficial.jpg",
        "logo": ORIGINALS / "logo-arena.png",
        "title": "ARENA CROSS BRASIL",
        "credit": "Arena Cross Brasil / divulgacao",
        "focus": (0.5, 0.45),
    },
    "moto1000gp-2026": {
        "photo": ORIGINALS / "photo-m1gp.webp",
        "logo": ORIGINALS / "logo-m1gp.webp",
        "title": "MOTO1000GP",
        "credit": "MOTO1000GP / divulgacao",
        "focus": (0.55, 0.48),
    },
    "brasil-ride-2026": {
        "photo": ORIGINALS / "photo-brasilride.jpg",
        "logo": ORIGINALS / "logo-brasilride.png",
        "title": "BRASIL RIDE",
        "credit": "Arquivo 2019: Fabio Piva / Brasil Ride",
        "focus": (0.55, 0.5),
    },
    "brasileiro-bmx-racing-2026": {
        "photo": ORIGINALS / "photo-bmx.jpg",
        "logo": ORIGINALS / "logo-cbc.png",
        "title": "BRASILEIRO DE\nBMX RACING",
        "credit": "Thiago Lemos / CBC",
        "focus": (0.5, 0.48),
    },
    "brasileiro-ciclismo-mtb-2026": {
        "photo": ORIGINALS / "photo-mtb.jpg",
        "logo": ORIGINALS / "logo-cbc.png",
        "title": "BRASILEIRO DE\nMOUNTAIN BIKE",
        "credit": "Arquivo 2024: Alan Modesto / CBC",
        "focus": (0.62, 0.5),
    },
    "brasileiro-motocross-2026": {
        "photo": ORIGINALS / "photo-motocross.png",
        "logo": ORIGINALS / "logo-mx1.png",
        "title": "CAMPEONATO BRASILEIRO\nDE MOTOCROSS",
        "credit": "MX1 GP Brasil / divulgacao",
        "focus": (0.58, 0.5),
    },
    "brasileiro-enduro-2026": {
        "photo": ORIGINALS / "photo-enduro.webp",
        "logo": ORIGINALS / "logo-cbm.webp",
        "title": "BRASILEIRO DE ENDURO",
        "credit": "Janjao Santiago / CBM",
        "focus": (0.58, 0.5),
        "logo_crop": (270, 0, 496, 125),
    },
    "motogp-2026": {
        "photo": ORIGINALS / "photo-motogp.jpg",
        "logo": ORIGINALS / "logo-motogp.png",
        "title": "MOTOGP",
        "credit": "Arquivo 2015: Adrian Saxton / CC BY 3.0",
        "focus": (0.58, 0.5),
    },
    "mxgp-2026": {
        "photo": ORIGINALS / "photo-mxgp.jpg",
        "logo": ORIGINALS / "logo-mxgp.png",
        "title": "MUNDIAL DE MOTOCROSS",
        "credit": "MXGP / Infront Moto Racing",
        "focus": (0.58, 0.5),
        "light_logo_plate": True,
    },
    "sertoes-2026": {
        "photo": ORIGINALS / "photo-sertoes.jpg",
        "logo": ORIGINALS / "logo-sertoes.webp",
        "title": "SERTÕES PETROBRAS",
        "credit": "Rapha Rodrigues / Sertoes",
        "focus": (0.62, 0.5),
    },
    "superbike-brasil-2026": {
        "photo": ORIGINALS / "photo-superbike.jpg",
        "logo": ORIGINALS / "logo-superbike.png",
        "title": "SUPERBIKE BRASIL",
        "credit": "SuperBike Brasil / divulgacao",
        "focus": (0.58, 0.5),
    },
    "worldsbk-2026": {
        "photo": ORIGINALS / "photo-worldsbk.jpg",
        "logo": ORIGINALS / "logo-worldsbk.png",
        "title": "WORLD SUPERBIKE",
        "credit": "Arquivo 2024: Jearle / CC BY-SA 4.0",
        "focus": (0.58, 0.5),
    },
}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    name = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(str(Path("C:/Windows/Fonts") / name), size)


def cover_crop(image: Image.Image, focus: tuple[float, float]) -> Image.Image:
    image = ImageOps.exif_transpose(image).convert("RGB")
    scale = max(WIDTH / image.width, HEIGHT / image.height)
    new_size = (round(image.width * scale), round(image.height * scale))
    image = image.resize(new_size, Image.Resampling.LANCZOS)
    left = max(0, min(image.width - WIDTH, round(image.width * focus[0] - WIDTH / 2)))
    top = max(0, min(image.height - HEIGHT, round(image.height * focus[1] - HEIGHT / 2)))
    return image.crop((left, top, left + WIDTH, top + HEIGHT))


def open_logo(path: Path) -> Image.Image:
    return Image.open(path).convert("RGBA")


def fit_logo(logo: Image.Image, max_width: int = 480, max_height: int = 205) -> Image.Image:
    ratio = min(max_width / logo.width, max_height / logo.height, 1)
    size = (max(1, round(logo.width * ratio)), max(1, round(logo.height * ratio)))
    return logo.resize(size, Image.Resampling.LANCZOS) if ratio < 1 else logo.copy()


def make_cover(slug: str, data: dict, output: Path) -> None:
    with Image.open(data["photo"]) as photo:
        base = cover_crop(photo, data["focus"]).convert("RGBA")

    # Gradiente escuro preserva a foto e garante leitura da marca em miniatura.
    shade = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    shade_px = shade.load()
    for x in range(WIDTH):
        alpha = round(205 * max(0, 1 - x / 850) + 35)
        for y in range(HEIGHT):
            vertical = round(42 * abs(y - HEIGHT / 2) / (HEIGHT / 2))
            shade_px[x, y] = (4, 8, 16, min(235, alpha + vertical))
    base.alpha_composite(shade)

    draw = ImageDraw.Draw(base, "RGBA")
    draw.rounded_rectangle((42, 48, 610, 627), radius=30, fill=(5, 10, 20, 145), outline=(255, 255, 255, 40), width=2)
    draw.rounded_rectangle((42, 48, 55, 627), radius=7, fill=(255, 91, 45, 255))

    logo = open_logo(data["logo"])
    if "logo_crop" in data:
        logo = logo.crop(data["logo_crop"])
    logo = fit_logo(logo)
    logo_x = 82 + (480 - logo.width) // 2
    logo_y = 91 + (205 - logo.height) // 2
    if data.get("light_logo_plate"):
        draw.rounded_rectangle(
            (logo_x - 24, logo_y - 18, logo_x + logo.width + 24, logo_y + logo.height + 18),
            radius=18,
            fill=(255, 255, 255, 235),
        )
    shadow = Image.new("RGBA", logo.size, (0, 0, 0, 0))
    shadow.alpha_composite(logo)
    shadow = shadow.filter(ImageFilter.GaussianBlur(8))
    base.alpha_composite(shadow, (logo_x + 5, logo_y + 7))
    base.alpha_composite(logo, (logo_x, logo_y))

    title_font = font(51 if "\n" not in data["title"] else 43, bold=True)
    draw.multiline_text((82, 337), data["title"], font=title_font, fill="white", spacing=7)
    draw.rounded_rectangle((82, 526, 300, 573), radius=22, fill=(255, 91, 45, 235))
    draw.text((105, 537), "TEMPORADA 2026", font=font(20, bold=True), fill="white")
    draw.text((82, 590), f"Foto: {data['credit']}", font=font(16), fill=(225, 230, 238, 220))

    output.parent.mkdir(parents=True, exist_ok=True)
    base.convert("RGB").save(output, "PNG", optimize=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=PREVIEWS)
    args = parser.parse_args()
    for slug, data in COVERS.items():
        make_cover(slug, data, args.output / f"{slug}-capa.png")
        print(slug)


if __name__ == "__main__":
    main()
