#!/usr/bin/env python3
"""Monta capas 16:9 de competicoes com foto oficial e marca em destaque."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageFilter, ImageOps


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


def cover_crop(image: Image.Image, focus: tuple[float, float]) -> Image.Image:
    image = ImageOps.exif_transpose(image).convert("RGB")
    scale = max(WIDTH / image.width, HEIGHT / image.height)
    new_size = (round(image.width * scale), round(image.height * scale))
    image = image.resize(new_size, Image.Resampling.LANCZOS)
    left = max(0, min(image.width - WIDTH, round(image.width * focus[0] - WIDTH / 2)))
    top = max(0, min(image.height - HEIGHT, round(image.height * focus[1] - HEIGHT / 2)))
    return image.crop((left, top, left + WIDTH, top + HEIGHT))


def open_logo(path: Path) -> Image.Image:
    logo = Image.open(path).convert("RGBA")
    alpha_bbox = logo.getchannel("A").getbbox()
    return logo.crop(alpha_bbox) if alpha_bbox else logo


def fit_logo(logo: Image.Image, max_width: int = 720, max_height: int = 300) -> Image.Image:
    ratio = min(max_width / logo.width, max_height / logo.height)
    size = (max(1, round(logo.width * ratio)), max(1, round(logo.height * ratio)))
    return logo.resize(size, Image.Resampling.LANCZOS)


def make_cover(slug: str, data: dict, output: Path) -> None:
    with Image.open(data["photo"]) as photo:
        base = cover_crop(photo, data["focus"]).convert("RGBA")

    # Escurecimento leve e uniforme: preserva a foto e dá contraste ao logo.
    base.alpha_composite(Image.new("RGBA", (WIDTH, HEIGHT), (3, 7, 14, 82)))

    logo = open_logo(data["logo"])
    if "logo_crop" in data:
        logo = logo.crop(data["logo_crop"])
        alpha_bbox = logo.getchannel("A").getbbox()
        logo = logo.crop(alpha_bbox) if alpha_bbox else logo
    logo = fit_logo(logo)
    logo_x = (WIDTH - logo.width) // 2
    logo_y = (HEIGHT - logo.height) // 2

    # Um brilho escuro suave substitui painéis, títulos e outros textos.
    glow_pad = 56
    glow = Image.new("RGBA", (logo.width + glow_pad * 2, logo.height + glow_pad * 2), (0, 0, 0, 0))
    glow_alpha = Image.new("L", glow.size, 0)
    glow_alpha.paste(185, (glow_pad, glow_pad, glow_pad + logo.width, glow_pad + logo.height))
    glow_alpha = glow_alpha.filter(ImageFilter.GaussianBlur(34))
    glow.putalpha(glow_alpha)
    base.alpha_composite(glow, (logo_x - glow_pad, logo_y - glow_pad))

    shadow = Image.new("RGBA", logo.size, (0, 0, 0, 210))
    shadow.putalpha(logo.getchannel("A").filter(ImageFilter.GaussianBlur(9)))
    base.alpha_composite(shadow, (logo_x + 7, logo_y + 9))
    base.alpha_composite(logo, (logo_x, logo_y))

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
