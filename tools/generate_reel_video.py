from __future__ import annotations

import argparse
import math
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

try:
    from imageio_ffmpeg import get_ffmpeg_exe
except ModuleNotFoundError:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".reel-deps"))
    from imageio_ffmpeg import get_ffmpeg_exe


WIDTH = 1080
HEIGHT = 1920
FPS = 30
SCENE_SECONDS = 4.0
TRANSITION_SECONDS = 0.45
SAMPLE_RATE = 44_100
FONT_BOLD = Path(r"C:\Windows\Fonts\arialbd.ttf")
FONT_REGULAR = Path(r"C:\Windows\Fonts\arial.ttf")


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_BOLD if bold else FONT_REGULAR), size=size)


def cover(source: Image.Image, size: tuple[int, int], focus_y: float = 0.5) -> Image.Image:
    target_w, target_h = size
    scale = max(target_w / source.width, target_h / source.height)
    resized = source.resize((round(source.width * scale), round(source.height * scale)), Image.Resampling.LANCZOS)
    left = max(0, (resized.width - target_w) // 2)
    top = round(max(0, resized.height - target_h) * focus_y)
    return resized.crop((left, top, left + target_w, top + target_h))


def fit_logo(logo: Image.Image, width: int) -> Image.Image:
    ratio = width / logo.width
    return logo.resize((width, round(logo.height * ratio)), Image.Resampling.LANCZOS)


def wrap_lines(draw: ImageDraw.ImageDraw, text: str, typeface: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    lines: list[str] = []
    for paragraph in text.split("\n"):
        current = ""
        for word in paragraph.split():
            candidate = f"{current} {word}".strip()
            bounds = draw.textbbox((0, 0), candidate, font=typeface, stroke_width=2)
            if current and bounds[2] - bounds[0] > max_width:
                lines.append(current)
                current = word
            else:
                current = candidate
        if current:
            lines.append(current)
    return lines


def draw_centered_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    y: int,
    size: int,
    max_width: int = 940,
    fill: tuple[int, int, int] = (255, 255, 255),
    spacing: int = 14,
) -> int:
    typeface = font(size, True)
    for line in wrap_lines(draw, text, typeface, max_width):
        bounds = draw.textbbox((0, 0), line, font=typeface, stroke_width=2)
        line_w = bounds[2] - bounds[0]
        draw.text(((WIDTH - line_w) // 2, y), line, font=typeface, fill=fill,
                  stroke_width=2, stroke_fill=(0, 0, 0))
        y += bounds[3] - bounds[1] + spacing
    return y


def make_scene(
    source_path: Path,
    logo: Image.Image,
    output: Path,
    eyebrow: str,
    headline: str,
    detail: str,
    accent: str = "⚡",
) -> None:
    with Image.open(source_path) as source:
        source = source.convert("RGB")
        background = cover(source, (WIDTH, HEIGHT), 0.45).filter(ImageFilter.GaussianBlur(28))
        background = ImageEnhance.Brightness(background).enhance(0.32).convert("RGBA")
        canvas = background
        photo = cover(source, (WIDTH, 960), 0.48).convert("RGBA")
        canvas.alpha_composite(photo, (0, 280))

    dark = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    shade = ImageDraw.Draw(dark)
    for y in range(1020, 1920):
        alpha = min(248, round(248 * (y - 1020) / 500))
        shade.line((0, y, WIDTH, y), fill=(3, 10, 14, alpha))
    shade.rectangle((0, 0, WIDTH, 285), fill=(3, 10, 14, 205))
    canvas.alpha_composite(dark)
    draw = ImageDraw.Draw(canvas)

    logo_img = fit_logo(logo, 520)
    canvas.alpha_composite(logo_img, ((WIDTH - logo_img.width) // 2, 70))

    eyebrow_font = font(31, True)
    eyebrow_bounds = draw.textbbox((0, 0), eyebrow, font=eyebrow_font)
    pill_w = eyebrow_bounds[2] - eyebrow_bounds[0] + 56
    draw.rounded_rectangle(((WIDTH - pill_w) // 2, 205, (WIDTH + pill_w) // 2, 262), 28, fill=(0, 215, 185))
    draw.text(((WIDTH - (eyebrow_bounds[2] - eyebrow_bounds[0])) // 2, 216), eyebrow,
              font=eyebrow_font, fill=(0, 24, 28))

    draw.rounded_rectangle((55, 1165, 1025, 1745), 38, fill=(3, 10, 14, 232), outline=(0, 215, 185), width=4)
    draw.text((90, 1215), accent, font=font(58, True), fill=(0, 215, 185))
    y = draw_centered_text(draw, headline, 1280, 66, 860)
    draw.rounded_rectangle((410, y + 8, 670, y + 17), 5, fill=(0, 215, 185))
    draw_centered_text(draw, detail, y + 42, 36, 860, (207, 238, 237), 11)

    credit_font = font(24)
    draw.text((54, 1782), "Foto: Honda Motor Europe / divulgação", font=credit_font, fill=(190, 204, 207))
    draw.text((54, 1822), "Dados europeus da fabricante • não é teste presencial", font=credit_font, fill=(190, 204, 207))
    canvas.convert("RGB").save(output, "JPEG", quality=93, optimize=True, progressive=True)


def make_cta(source_path: Path, logo: Image.Image, output: Path) -> None:
    with Image.open(source_path) as source:
        canvas = cover(source.convert("RGB"), (WIDTH, HEIGHT), 0.45).filter(ImageFilter.GaussianBlur(22))
    canvas = ImageEnhance.Brightness(canvas).enhance(0.30).convert("RGBA")
    overlay = Image.new("RGBA", canvas.size, (2, 10, 14, 165))
    canvas.alpha_composite(overlay)
    draw = ImageDraw.Draw(canvas)
    logo_img = fit_logo(logo, 690)
    canvas.alpha_composite(logo_img, ((WIDTH - logo_img.width) // 2, 185))
    draw.rounded_rectangle((75, 610, 1005, 1425), 48, fill=(3, 10, 14, 232), outline=(0, 215, 185), width=5)
    y = draw_centered_text(draw, "ENTENDA O SISTEMA COMPLETO", 700, 72, 820)
    y = draw_centered_text(draw, "Bateria • BMS • inversor • motor • regeneração • recarga", y + 40, 37, 800, (210, 238, 237))
    draw.rounded_rectangle((165, y + 70, 915, y + 165), 48, fill=(0, 215, 185))
    follow = "SIGA @TVDUASRODASOFC"
    follow_font = font(38, True)
    bounds = draw.textbbox((0, 0), follow, font=follow_font)
    draw.text(((WIDTH - (bounds[2] - bounds[0])) // 2, y + 95), follow, font=follow_font, fill=(0, 22, 27))
    draw_centered_text(draw, "TVDUASRODAS.COM", y + 220, 54, 800, (255, 255, 255))
    draw.text((54, 1782), "Foto: Honda Motor Europe / divulgação", font=font(24), fill=(190, 204, 207))
    canvas.convert("RGB").save(output, "JPEG", quality=93, optimize=True, progressive=True)


def synthesize_track(output: Path, duration: float) -> None:
    count = int(SAMPLE_RATE * duration)
    t = np.arange(count, dtype=np.float64) / SAMPLE_RATE
    audio = np.zeros(count, dtype=np.float64)
    chords = ((110.00, 164.81, 220.00), (87.31, 130.81, 174.61),
              (98.00, 146.83, 196.00), (82.41, 123.47, 164.81))
    bar = 2.0
    for index in range(math.ceil(duration / bar)):
        chord = chords[index % len(chords)]
        start = index * bar
        mask = (t >= start) & (t < min(start + bar, duration))
        local = t[mask] - start
        envelope = np.minimum(local / 0.15, 1.0) * np.minimum((bar - local) / 0.25, 1.0)
        pad = sum(np.sin(2 * math.pi * frequency * local) for frequency in chord) / len(chord)
        bass = np.sin(2 * math.pi * chord[0] / 2 * local)
        audio[mask] += envelope * (0.16 * pad + 0.10 * bass)

    rng = np.random.default_rng(20260722)
    for beat in np.arange(0, duration, 0.5):
        start = int(beat * SAMPLE_RATE)
        length = min(int(0.18 * SAMPLE_RATE), count - start)
        local = np.arange(length) / SAMPLE_RATE
        audio[start:start + length] += 0.22 * np.sin(2 * math.pi * (72 - 35 * local) * local) * np.exp(-24 * local)
    for beat in np.arange(0.25, duration, 0.25):
        start = int(beat * SAMPLE_RATE)
        length = min(int(0.045 * SAMPLE_RATE), count - start)
        local = np.arange(length) / SAMPLE_RATE
        audio[start:start + length] += 0.035 * rng.normal(0, 1, length) * np.exp(-70 * local)

    fade = int(0.4 * SAMPLE_RATE)
    audio[:fade] *= np.linspace(0, 1, fade)
    audio[-fade:] *= np.linspace(1, 0, fade)
    peak = max(float(np.max(np.abs(audio))), 1e-9)
    pcm = np.int16(np.clip(audio / peak * 0.55, -1, 1) * 32767)
    stereo = np.column_stack((pcm, pcm)).ravel()
    with wave.open(str(output), "wb") as wav:
        wav.setnchannels(2)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        wav.writeframes(stereo.tobytes())


def render_video(scenes: list[Path], output: Path) -> float:
    total = SCENE_SECONDS * len(scenes) - TRANSITION_SECONDS * (len(scenes) - 1)
    track = output.with_suffix(".original-track.wav")
    synthesize_track(track, total)
    command = [get_ffmpeg_exe(), "-y"]
    for scene in scenes:
        command += ["-loop", "1", "-t", str(SCENE_SECONDS), "-i", str(scene)]
    command += ["-i", str(track)]

    filters: list[str] = []
    frames = round(SCENE_SECONDS * FPS)
    for index in range(len(scenes)):
        direction = 1 if index % 2 == 0 else -1
        zoom = "min(zoom+0.0007,1.065)" if direction == 1 else "if(eq(on,1),1.065,max(zoom-0.00055,1.0))"
        filters.append(
            f"[{index}:v]scale={WIDTH}:{HEIGHT},zoompan=z='{zoom}':d={frames}:s={WIDTH}x{HEIGHT}:fps={FPS},"
            f"setsar=1,format=yuv420p[v{index}]"
        )
    previous = "v0"
    for index in range(1, len(scenes)):
        output_label = "vout" if index == len(scenes) - 1 else f"x{index}"
        offset = index * (SCENE_SECONDS - TRANSITION_SECONDS)
        transition = "fade" if index % 2 else "fadeblack"
        filters.append(
            f"[{previous}][v{index}]xfade=transition={transition}:duration={TRANSITION_SECONDS}:offset={offset:.2f}[{output_label}]"
        )
        previous = output_label

    command += [
        "-filter_complex", ";".join(filters), "-map", "[vout]", "-map", f"{len(scenes)}:a",
        "-t", f"{total:.2f}", "-r", str(FPS), "-c:v", "libx264", "-preset", "medium", "-crf", "19",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", str(SAMPLE_RATE),
        "-movflags", "+faststart", str(output),
    ]
    subprocess.run(command, check=True)
    track.unlink(missing_ok=True)
    return total


def make_contact_sheet(scenes: list[Path], output: Path) -> None:
    thumbs = []
    for scene in scenes:
        with Image.open(scene) as image:
            thumbs.append(image.resize((270, 480), Image.Resampling.LANCZOS))
    sheet = Image.new("RGB", (270 * 4, 480 * 2), (8, 12, 16))
    for index, thumb in enumerate(thumbs):
        sheet.paste(thumb, ((index % 4) * 270, (index // 4) * 480))
    sheet.save(output, "JPEG", quality=90, optimize=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--assets-dir", required=True, type=Path)
    parser.add_argument("--logo", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    image_names = [
        "electric-zone-componentes-eletricos-capa.webp",
        "electric-zone-painel-tft.webp",
        "electric-zone-bateria-motor.webp",
        "electric-zone-bateria-motor.webp",
        "electric-zone-conector-recarga.webp",
        "electric-zone-componentes-eletricos-capa.webp",
    ]
    content = [
        ("ELECTRIC ZONE", "DA TOMADA ATÉ A RODA", "O que acontece dentro de uma moto elétrica?", "01"),
        ("BATERIA + BMS", "9,3 kWh", "Energia monitorada célula a célula", "02"),
        ("INVERSOR + MOTOR", "50 kW • 100 Nm", "A corrente elétrica é controlada e vira torque", "03"),
        ("REGENERAÇÃO", "ENERGIA DE VOLTA", "Ao desacelerar, o motor também pode atuar como gerador", "04"),
        ("RECARGA CCS2", "20% → 80%", "Cerca de 30 minutos em condições especificadas", "05"),
        ("HONDA WN7", "EXEMPLO OFICIAL", "Dados da versão europeia; não é teste presencial", "06"),
    ]
    with Image.open(args.logo) as logo_source:
        logo = logo_source.convert("RGBA")
        scenes: list[Path] = []
        for index, (image_name, copy) in enumerate(zip(image_names, content), 1):
            scene_path = args.output_dir / f"reel-scene-{index:02d}.jpg"
            make_scene(args.assets_dir / image_name, logo, scene_path, *copy)
            scenes.append(scene_path)
        cta_path = args.output_dir / "reel-scene-07.jpg"
        make_cta(args.assets_dir / image_names[0], logo, cta_path)
        scenes.append(cta_path)

    cover_path = args.output_dir / "reel-electric-zone-capa.jpg"
    cover_path.write_bytes(scenes[0].read_bytes())
    video_path = args.output_dir / "reel-electric-zone-como-funciona.mp4"
    duration = render_video(scenes, video_path)
    make_contact_sheet(scenes, args.output_dir / "reel-electric-zone-contato.jpg")
    print(f"VIDEO={video_path}")
    print(f"COVER={cover_path}")
    print(f"DURATION={duration:.2f}")


if __name__ == "__main__":
    main()
