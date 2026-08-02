#!/usr/bin/env python3
"""Gera capas editoriais 16:9 com identidade dos programas da Revista."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
UPLOADS = ROOT / "assets" / "img" / "uploads"
FONT_BOLD = Path("C:/Windows/Fonts/arialbd.ttf")
FONT_REGULAR = Path("C:/Windows/Fonts/arial.ttf")

PROGRAMS = {
    "role-de-rua": {"label": "ROLÊ DE RUA", "accent": "#ffcf00", "tag": "MOBILIDADE URBANA"},
    "estrada-aberta": {"label": "ESTRADA ABERTA", "accent": "#ff6a1a", "tag": "ROTAS E VIAGENS"},
    "garage-tech": {"label": "GARAGE TECH", "accent": "#00b7ff", "tag": "MECÂNICA E TECNOLOGIA"},
    "electric-zone": {"label": "ELECTRIC ZONE", "accent": "#63e600", "tag": "MOBILIDADE ELÉTRICA"},
}

EDICOES = [
    ("role-de-rua", "role-de-rua-rotas-curtas-capa.webp", "role-de-rua-23-07-2026-capa-edicao.webp", "EDIÇÃO 23.07.2026", "ROTAS CURTAS SEM IMPROVISO"),
    ("role-de-rua", "role-de-rua-cruzamentos-capa.webp", "role-de-rua-27-07-2026-capa-edicao.webp", "EDIÇÃO 27.07.2026", "CRUZAMENTOS: LEIA ANTES DA ESQUINA"),
    ("estrada-aberta", "estrada-aberta-25-07-2026-capa.webp", "estrada-aberta-25-07-2026-capa-edicao.webp", "EDIÇÃO 25.07.2026", "VIAJAR COM RITMO E MARGEM"),
    ("estrada-aberta", "estrada-aberta-graciosa-capa.webp", "estrada-aberta-01-08-2026-capa-edicao.webp", "EDIÇÃO 01.08.2026", "ESTRADA DA GRACIOSA EM UM DIA"),
    ("garage-tech", "garage-tech-corrente-capa.jpg", "garage-tech-corrente-capa-edicao.webp", "EDIÇÃO 22.07.2026", "CORRENTE: INSPEÇÃO, LIMPEZA E LUBRIFICAÇÃO"),
    ("electric-zone", "electric-zone-componentes-eletricos-capa.webp", "electric-zone-componentes-capa-edicao.webp", "EDIÇÃO 21.07.2026", "COMO FUNCIONA UMA MOTO ELÉTRICA"),
    ("electric-zone", "electric-zone-dc-dc-capa.webp", "electric-zone-26-07-2026-capa-edicao.webp", "EDIÇÃO 26.07.2026", "DA BATERIA PRINCIPAL À REDE DE 12 V"),
]

CARDS = [
    ("role-de-rua", "programa-role-de-rua-capa.webp", "programa-role-de-rua-identidade.webp"),
    ("estrada-aberta", "programa-estrada-aberta-capa.webp", "programa-estrada-aberta-identidade.webp"),
    ("garage-tech", "programa-garage-tech-capa.webp", "programa-garage-tech-identidade.webp"),
    ("electric-zone", "electric-zone-componentes-eletricos-capa.webp", "programa-electric-zone-identidade.webp"),
]


def font(size: int, bold: bool = False):
    return ImageFont.truetype(str(FONT_BOLD if bold else FONT_REGULAR), size)


def fit_cover(source: Image.Image, size=(1600, 900)) -> Image.Image:
    source = source.convert("RGB")
    ratio = max(size[0] / source.width, size[1] / source.height)
    resized = source.resize((round(source.width * ratio), round(source.height * ratio)), Image.Resampling.LANCZOS)
    left = (resized.width - size[0]) // 2
    top = (resized.height - size[1]) // 2
    return resized.crop((left, top, left + size[0], top + size[1]))


def wrap(draw, text, face, max_width):
    words, lines, current = text.split(), [], ""
    for word in words:
        trial = f"{current} {word}".strip()
        if draw.textbbox((0, 0), trial, font=face)[2] <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_logo_mark(draw, program, accent):
    """Símbolo simples e reproduzível que acompanha o nome de cada programa."""
    box = (76, 184, 168, 276)
    draw.rounded_rectangle(box, radius=18, fill=accent)
    ink = "#071019"
    if program == "role-de-rua":
        draw.ellipse((101, 200, 143, 242), outline=ink, width=8)
        draw.polygon([(122, 268), (105, 236), (139, 236)], fill=ink)
        draw.line((91, 255, 153, 255), fill=ink, width=7)
    elif program == "estrada-aberta":
        draw.polygon([(122, 195), (151, 264), (93, 264)], fill=ink)
        draw.line((122, 207, 122, 223), fill=accent, width=5)
        draw.line((119, 235, 115, 252), fill=accent, width=5)
        draw.line((125, 235, 129, 252), fill=accent, width=5)
    elif program == "garage-tech":
        draw.ellipse((93, 201, 151, 259), outline=ink, width=9)
        draw.ellipse((111, 219, 133, 241), fill=ink)
        for x1, y1, x2, y2 in [(119,191,125,209),(119,251,125,269),(83,227,101,233),(143,227,161,233)]:
            draw.rectangle((x1, y1, x2, y2), fill=ink)
    else:
        draw.polygon([(130, 194), (99, 234), (119, 234), (105, 267), (148, 220), (127, 220)], fill=ink)


def render(program, source_name, output_name, edition, headline=None):
    meta = PROGRAMS[program]
    image = fit_cover(Image.open(UPLOADS / source_name))
    image = ImageEnhance.Contrast(image).enhance(1.06)
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    accent = meta["accent"]

    draw.rectangle((0, 0, 1600, 900), fill=(0, 0, 0, 28))
    draw.polygon([(0, 0), (1060, 0), (790, 900), (0, 900)], fill=(5, 10, 18, 210))
    draw.rectangle((0, 0, 30, 900), fill=accent)
    draw.rectangle((75, 92, 330, 101), fill=accent)
    draw.text((75, 122), "TVDUASRODAS  |  REVISTA", font=font(25, True), fill="white")
    draw_logo_mark(draw, program, accent)
    draw.text((192, 192), meta["label"], font=font(76, True), fill=accent, stroke_width=1, stroke_fill=(0, 0, 0, 100))
    draw.text((194, 292), meta["tag"], font=font(27, True), fill="white")

    if headline:
        y = 515
        for line in wrap(draw, headline, font(42, True), 680):
            draw.text((78, y), line, font=font(42, True), fill="white")
            y += 51
    draw.rounded_rectangle((76, 765, 505, 828), radius=10, fill=accent)
    draw.text((101, 779), edition, font=font(28, True), fill="#071019")
    draw.text((1288, 817), "TVDUASRODAS.COM", font=font(22, True), fill="white", anchor="ra")

    final = Image.alpha_composite(image.convert("RGBA"), overlay).convert("RGB")
    final.save(UPLOADS / output_name, "WEBP", quality=82, method=6)


def main():
    for item in EDICOES:
        render(*item)
    for program, source, output in CARDS:
        render(program, source, output, "PROGRAMA DA REVISTA", PROGRAMS[program]["tag"])


if __name__ == "__main__":
    main()
