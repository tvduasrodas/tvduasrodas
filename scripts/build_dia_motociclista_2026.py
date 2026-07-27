from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

from PIL import Image, ImageDraw, ImageFilter, ImageFont


UPLOADS = ROOT / "assets" / "img" / "uploads"
OUT = ROOT / "output" / "instagram" / "2026-07-27" / "dia-do-motociclista-2026"
LOGO = ROOT / "assets" / "img" / "logotv.png"
FONT_BOLD = Path(r"C:\Windows\Fonts\arialbd.ttf")
FONT_REGULAR = Path(r"C:\Windows\Fonts\arial.ttf")

INK = (8, 11, 16)
ASPHALT = (18, 22, 28)
ORANGE = (245, 85, 28)
AMBER = (255, 181, 36)
CREAM = (247, 241, 229)
MINT = (78, 225, 197)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_BOLD if bold else FONT_REGULAR), size)


def gradient(size: tuple[int, int], top: tuple[int, int, int], bottom: tuple[int, int, int]) -> Image.Image:
    width, height = size
    image = Image.new("RGB", size)
    draw = ImageDraw.Draw(image)
    for y in range(height):
        ratio = y / max(1, height - 1)
        color = tuple(round(top[i] * (1 - ratio) + bottom[i] * ratio) for i in range(3))
        draw.line((0, y, width, y), fill=color)
    return image


def paste_logo(canvas: Image.Image, width: int, y: int, center: bool = True) -> None:
    with Image.open(LOGO) as source:
        logo = source.convert("RGBA")
    ratio = width / logo.width
    logo = logo.resize((width, round(logo.height * ratio)), Image.Resampling.LANCZOS)
    x = (canvas.width - logo.width) // 2 if center else 60
    glow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    glow.alpha_composite(logo, (x, y))
    glow = glow.filter(ImageFilter.GaussianBlur(12))
    canvas.alpha_composite(glow)
    canvas.alpha_composite(logo, (x, y))


def wrap(draw: ImageDraw.ImageDraw, text: str, max_width: int, size: int) -> list[str]:
    face = font(size, True)
    lines: list[str] = []
    current = ""
    for word in text.split():
        candidate = f"{current} {word}".strip()
        if current and draw.textbbox((0, 0), candidate, font=face)[2] > max_width:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def centered_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    y: int,
    size: int,
    max_width: int,
    fill: tuple[int, int, int] = CREAM,
    spacing: int = 10,
) -> int:
    face = font(size, True)
    for line in wrap(draw, text, max_width, size):
        box = draw.textbbox((0, 0), line, font=face, stroke_width=2)
        width = box[2] - box[0]
        draw.text(
            ((draw._image.width - width) // 2, y),
            line,
            font=face,
            fill=fill,
            stroke_width=2,
            stroke_fill=INK,
        )
        y += box[3] - box[1] + spacing
    return y


def road(draw: ImageDraw.ImageDraw, width: int, height: int, horizon: int) -> None:
    draw.polygon(
        [(width * 0.36, horizon), (width * 0.64, horizon), (width * 0.94, height), (width * 0.06, height)],
        fill=ASPHALT,
    )
    draw.line((width * 0.5, horizon + 40, width * 0.5, height), fill=AMBER, width=max(8, width // 90))
    for offset in (-0.19, 0.19):
        draw.line(
            (width * (0.5 + offset * 0.18), horizon, width * (0.5 + offset), height),
            fill=(230, 230, 220),
            width=max(4, width // 180),
        )


def motorcycle(draw: ImageDraw.ImageDraw, cx: int, cy: int, scale: float = 1.0) -> None:
    r = round(53 * scale)
    line = max(8, round(15 * scale))
    draw.ellipse((cx - 130 * scale, cy, cx - 130 * scale + 2 * r, cy + 2 * r), outline=CREAM, width=line)
    draw.ellipse((cx + 35 * scale, cy, cx + 35 * scale + 2 * r, cy + 2 * r), outline=CREAM, width=line)
    rear = (cx - 130 * scale + r, cy + r)
    front = (cx + 35 * scale + r, cy + r)
    seat = (cx - 28 * scale, cy - 8 * scale)
    engine = (cx - 24 * scale, cy + 65 * scale)
    draw.line((rear, seat, front, engine, rear), fill=ORANGE, width=line, joint="curve")
    draw.line((seat[0], seat[1], seat[0] + 58 * scale, seat[1] - 70 * scale), fill=CREAM, width=line)
    draw.line((seat[0] + 58 * scale, seat[1] - 70 * scale, front[0] - 20 * scale, front[1] - 30 * scale), fill=CREAM, width=line)
    draw.ellipse(
        (seat[0] - 20 * scale, seat[1] - 116 * scale, seat[0] + 56 * scale, seat[1] - 40 * scale),
        fill=CREAM,
        outline=ORANGE,
        width=max(5, round(7 * scale)),
    )


def save_webp(image: Image.Image, path: Path, quality: int = 82) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(path, "WEBP", quality=quality, method=6)


def build_cover() -> Path:
    size = (1600, 900)
    base = gradient(size, (39, 15, 10), INK).convert("RGBA")
    draw = ImageDraw.Draw(base)
    road(draw, *size, horizon=320)
    motorcycle(draw, 800, 525, 1.2)
    paste_logo(base, 780, 45)
    draw.rounded_rectangle((430, 690, 1170, 770), radius=36, fill=ORANGE)
    label = "27 DE JULHO"
    face = font(42, True)
    box = draw.textbbox((0, 0), label, font=face)
    draw.text(((1600 - (box[2] - box[0])) // 2, 708), label, font=face, fill=CREAM)
    centered_text(draw, "DIA DO MOTOCICLISTA", 790, 54, 1360)
    path = UPLOADS / "dia-do-motociclista-2026-capa.webp"
    save_webp(base, path)
    return path


def build_respect() -> Path:
    size = (1400, 788)
    base = gradient(size, (10, 34, 39), INK).convert("RGBA")
    draw = ImageDraw.Draw(base)
    draw.rounded_rectangle((70, 80, 1330, 708), radius=42, fill=(15, 21, 28), outline=MINT, width=5)
    draw.line((700, 120, 700, 668), fill=AMBER, width=10)
    motorcycle(draw, 405, 365, 0.9)
    draw.rounded_rectangle((820, 325, 1130, 510), radius=50, outline=CREAM, width=15)
    draw.ellipse((850, 470, 925, 545), outline=CREAM, width=14)
    draw.ellipse((1025, 470, 1100, 545), outline=CREAM, width=14)
    centered_text(draw, "RESPEITO É VIA DE MÃO DUPLA", 115, 48, 1180)
    centered_text(draw, "distância • visibilidade • previsibilidade", 635, 30, 1180, MINT)
    path = UPLOADS / "dia-do-motociclista-2026-respeito.webp"
    save_webp(base, path, 80)
    return path


def build_checklist() -> Path:
    size = (1400, 788)
    base = gradient(size, (46, 18, 9), INK).convert("RGBA")
    draw = ImageDraw.Draw(base)
    centered_text(draw, "ANTES DE GIRAR A CHAVE", 78, 55, 1200)
    labels = (("PNEUS", "pressão e desgaste"), ("FREIOS", "resposta e fluido"), ("LUZES", "ver e ser visto"), ("CAPACETE", "ajuste e afivelamento"))
    for index, (title, detail) in enumerate(labels):
        x = 70 + index * 330
        draw.rounded_rectangle((x, 245, x + 290, 640), radius=34, fill=(15, 20, 27), outline=ORANGE, width=5)
        draw.ellipse((x + 95, 295, x + 195, 395), outline=CREAM, width=12)
        draw.text((x + 32, 455), title, font=font(35, True), fill=CREAM)
        detail_lines = wrap(draw, detail, 230, 25)
        y = 520
        for line in detail_lines:
            draw.text((x + 32, y), line, font=font(25), fill=MINT)
            y += 32
    path = UPLOADS / "dia-do-motociclista-2026-checklist.webp"
    save_webp(base, path, 80)
    return path


def social_card(index: int, eyebrow: str, title: str, detail: str) -> Path:
    size = (1080, 1920)
    hues = [
        ((62, 18, 7), INK),
        ((9, 48, 52), INK),
        ((54, 23, 8), (7, 17, 25)),
        ((20, 37, 65), INK),
        ((55, 12, 19), INK),
        ((7, 44, 38), INK),
    ]
    base = gradient(size, *hues[index - 1]).convert("RGBA")
    draw = ImageDraw.Draw(base)
    road(draw, *size, horizon=510)
    motorcycle(draw, 540, 790 + index * 8, 1.0)
    paste_logo(base, 880, 85)
    draw.rounded_rectangle((60, 1210, 1020, 1760), radius=44, fill=(7, 10, 15, 238), outline=ORANGE, width=5)
    draw.rounded_rectangle((100, 1260, 560, 1330), radius=30, fill=ORANGE)
    draw.text((130, 1277), eyebrow, font=font(30, True), fill=CREAM)
    y = centered_text(draw, title, 1380, 66, 860)
    centered_text(draw, detail, y + 35, 34, 840, MINT)
    draw.text((78, 1818), "Arte editorial original: TVDUASRODAS", font=font(24), fill=(210, 214, 218))
    path = OUT / f"base-scene-{index:02d}.jpg"
    path.parent.mkdir(parents=True, exist_ok=True)
    base.convert("RGB").save(path, "JPEG", quality=92, optimize=True)
    return path


def reel_source(index: int) -> Path:
    size = (1080, 1920)
    hues = [
        ((62, 18, 7), INK),
        ((9, 48, 52), INK),
        ((54, 23, 8), (7, 17, 25)),
        ((20, 37, 65), INK),
        ((55, 12, 19), INK),
        ((7, 44, 38), INK),
    ]
    base = gradient(size, *hues[index - 1]).convert("RGBA")
    draw = ImageDraw.Draw(base)
    horizon = 420 + index * 18
    road(draw, *size, horizon=horizon)
    motorcycle(draw, 540 + (index - 3) * 20, 825 + index * 24, 1.0 + index * 0.025)
    paste_logo(base, 860, 80)
    draw.ellipse((70 + index * 21, 1110, 210 + index * 21, 1250), outline=MINT, width=10)
    draw.line((140 + index * 21, 1180, 900 - index * 18, 1180), fill=ORANGE, width=10)
    path = OUT / f"reel-source-{index:02d}.jpg"
    path.parent.mkdir(parents=True, exist_ok=True)
    base.convert("RGB").save(path, "JPEG", quality=92, optimize=True)
    return path


def build_social() -> list[Path]:
    cards = [
        ("27 DE JULHO", "DIA DO MOTOCICLISTA", "Uma homenagem a quem vive sobre duas rodas."),
        ("NA CIDADE", "RESPEITO TAMBÉM PROTEGE", "Distância e previsibilidade abrem espaço para a vida."),
        ("ANTES DE SAIR", "A VOLTA COMEÇA NA REVISÃO", "Pneus, freios, luzes e capacete."),
        ("NA RUA", "SER VISTO MUDA O TRAJETO", "Posicionamento e sinalização com antecedência."),
        ("NA ESTRADA", "RITMO COM MARGEM", "A melhor viagem é aquela que termina bem."),
        ("NOSSA HOMENAGEM", "ACELERE A CONSCIÊNCIA", "Leia a matéria em TVDUASRODAS.COM"),
    ]
    story_cards = [social_card(index, *content) for index, content in enumerate(cards, 1)]
    reel_sources = [reel_source(index) for index in range(1, 7)]
    return [*story_cards, *reel_sources]


def main() -> None:
    files = [build_cover(), build_respect(), build_checklist(), *build_social()]
    receipt = {
        "created_for": "Dia do Motociclista — 27/07/2026",
        "rights_verified": True,
        "rights_basis": "Artes editoriais originais TVDUASRODAS com o logotipo próprio do portal.",
        "files": [str(path.relative_to(ROOT)).replace("\\", "/") for path in files],
    }
    (OUT / "art-build.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
