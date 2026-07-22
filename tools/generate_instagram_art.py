from __future__ import annotations

import argparse
from pathlib import Path
from textwrap import wrap

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


FONT_BOLD = Path(r"C:\Windows\Fonts\arialbd.ttf")
FONT_REGULAR = Path(r"C:\Windows\Fonts\arial.ttf")


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_BOLD if bold else FONT_REGULAR), size=size)


def cover_image(source: Image.Image, size: tuple[int, int], focus_y: float = 0.5) -> Image.Image:
    target_w, target_h = size
    scale = max(target_w / source.width, target_h / source.height)
    resized = source.resize((round(source.width * scale), round(source.height * scale)), Image.Resampling.LANCZOS)
    left = max(0, (resized.width - target_w) // 2)
    max_top = max(0, resized.height - target_h)
    top = round(max_top * focus_y)
    return resized.crop((left, top, left + target_w, top + target_h))


def add_gradient(canvas: Image.Image, start_y: int, end_y: int, max_alpha: int = 245) -> None:
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    span = max(1, end_y - start_y)
    for y in range(start_y, end_y):
        ratio = (y - start_y) / span
        alpha = round(max_alpha * ratio)
        draw.line((0, y, canvas.width, y), fill=(4, 10, 14, alpha))
    canvas.alpha_composite(overlay)


def paste_logo(canvas: Image.Image, logo: Image.Image, width: int, x: int, y: int) -> None:
    ratio = width / logo.width
    resized = logo.resize((width, round(logo.height * ratio)), Image.Resampling.LANCZOS)
    shadow = Image.new("RGBA", resized.size, (0, 0, 0, 0))
    shadow.alpha_composite(resized)
    shadow = shadow.filter(ImageFilter.GaussianBlur(7))
    canvas.alpha_composite(shadow, (x + 2, y + 4))
    canvas.alpha_composite(resized, (x, y))


def draw_badge(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, size: int) -> int:
    badge_font = font(size, True)
    x, y = xy
    box = draw.textbbox((0, 0), text, font=badge_font)
    width = box[2] - box[0] + 44
    height = box[3] - box[1] + 26
    draw.rounded_rectangle((x, y, x + width, y + height), radius=height // 2, fill=(0, 215, 185, 255))
    draw.text((x + 22, y + 10), text, font=badge_font, fill=(0, 20, 25, 255))
    return y + height


def draw_multiline(draw: ImageDraw.ImageDraw, text: str, box: tuple[int, int, int, int], size: int, spacing: int) -> int:
    x1, y1, x2, _ = box
    title_font = font(size, True)
    max_width = x2 - x1
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        bounds = draw.textbbox((0, 0), candidate, font=title_font, stroke_width=2)
        if current and bounds[2] - bounds[0] > max_width:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    y = y1
    for line in lines:
        draw.text((x1, y), line, font=title_font, fill="white", stroke_width=2, stroke_fill=(0, 0, 0, 170))
        bbox = draw.textbbox((x1, y), line, font=title_font, stroke_width=2)
        y = bbox[3] + spacing
    return y


def make_feed(source: Image.Image, logo: Image.Image, output: Path) -> None:
    canvas = cover_image(source, (1080, 1350), focus_y=0.42).convert("RGBA")
    canvas = ImageEnhance.Contrast(canvas).enhance(1.06)
    add_gradient(canvas, 650, 1350)
    draw = ImageDraw.Draw(canvas)
    paste_logo(canvas, logo, 520, 44, 42)
    badge_bottom = draw_badge(draw, (55, 825), "ELECTRIC ZONE", 34)
    title_bottom = draw_multiline(draw, "COMO FUNCIONA UMA MOTO ELÉTRICA", (55, badge_bottom + 38, 1025, 1275), 74, 6)
    draw.rectangle((55, title_bottom + 12, 310, title_bottom + 20), fill=(0, 215, 185, 255))
    draw.text((55, 1280), "BATERIA • BMS • INVERSOR • REGENERAÇÃO", font=font(28, True), fill=(205, 240, 237, 255))
    canvas.convert("RGB").save(output, "JPEG", quality=92, optimize=True, progressive=True)


def make_story(source: Image.Image, logo: Image.Image, output: Path) -> None:
    blurred = cover_image(source, (1080, 1920), focus_y=0.42).convert("RGB").filter(ImageFilter.GaussianBlur(24))
    blurred = ImageEnhance.Brightness(blurred).enhance(0.46).convert("RGBA")
    canvas = blurred
    photo = cover_image(source, (1080, 1080), focus_y=0.5).convert("RGBA")
    canvas.alpha_composite(photo, (0, 300))
    add_gradient(canvas, 980, 1920)
    draw = ImageDraw.Draw(canvas)
    paste_logo(canvas, logo, 620, 60, 80)
    badge_bottom = draw_badge(draw, (60, 1270), "NOVO PROGRAMA", 32)
    title_bottom = draw_multiline(draw, "COMO FUNCIONA UMA MOTO ELÉTRICA", (60, badge_bottom + 34, 1020, 1770), 72, 5)
    draw.text((60, min(title_bottom + 28, 1740)), "Bateria, BMS, inversor e regeneração", font=font(34), fill=(217, 238, 238, 255))
    link_y = 1810
    draw.rounded_rectangle((60, link_y, 1020, link_y + 78), radius=38, fill=(0, 215, 185, 255))
    label = "LINK CLICÁVEL NO PERFIL"
    label_font = font(34, True)
    bbox = draw.textbbox((0, 0), label, font=label_font)
    draw.text(((1080 - (bbox[2] - bbox[0])) // 2, link_y + 20), label, font=label_font, fill=(0, 20, 25, 255))
    canvas.convert("RGB").save(output, "JPEG", quality=92, optimize=True, progressive=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--logo", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    with Image.open(args.source) as source_image, Image.open(args.logo) as logo_image:
        make_feed(source_image.convert("RGB"), logo_image.convert("RGBA"), args.output_dir / "feed-electric-zone.jpg")
        make_story(source_image.convert("RGB"), logo_image.convert("RGBA"), args.output_dir / "stories-electric-zone.jpg")


if __name__ == "__main__":
    main()
