from __future__ import annotations

import argparse
import math
import subprocess
import textwrap
import wave
from pathlib import Path

import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw, ImageFont


WIDTH, HEIGHT = 1080, 1920
FPS = 30
SAMPLE_RATE = 44_100
DURATION = 14
FONT_BOLD = Path(r"C:\Windows\Fonts\arialbd.ttf")
FONT_REGULAR = Path(r"C:\Windows\Fonts\arial.ttf")
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_BOLD if bold else FONT_REGULAR), size)


def crop_cover(image: Image.Image) -> Image.Image:
    scale = max(WIDTH / image.width, HEIGHT / image.height)
    resized = image.resize(
        (round(image.width * scale), round(image.height * scale)),
        Image.Resampling.LANCZOS,
    )
    left = max(0, (resized.width - WIDTH) // 2)
    top = max(0, (resized.height - HEIGHT) // 2)
    return resized.crop((left, top, left + WIDTH, top + HEIGHT))


def wrapped(draw: ImageDraw.ImageDraw, value: str, max_width: int, size: int) -> str:
    words = value.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        box = draw.textbbox((0, 0), candidate, font=font(size, True))
        if box[2] - box[0] <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return "\n".join(lines)


def build_poster(
    image_path: Path,
    output_path: Path,
    title: str,
    subtitle: str,
    cta: str,
    credit: str,
) -> None:
    with Image.open(image_path) as source:
        image = crop_cover(source.convert("RGB")).convert("RGBA")

    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    pixels = np.zeros((HEIGHT, WIDTH, 4), dtype=np.uint8)
    for y in range(HEIGHT):
        if y < 930:
            alpha = round(175 * (1 - y / 930) ** 1.7)
        else:
            alpha = round(210 * ((y - 930) / (HEIGHT - 930)) ** 1.4)
        pixels[y, :, :3] = (4, 8, 13)
        pixels[y, :, 3] = alpha
    overlay = Image.fromarray(pixels, "RGBA")
    image.alpha_composite(overlay)
    draw = ImageDraw.Draw(image)

    draw.rounded_rectangle((58, 72, 440, 142), radius=18, fill=(9, 13, 18, 215))
    draw.rectangle((58, 72, 76, 142), fill=(242, 83, 31, 255))
    draw.text((98, 90), "TVDUASRODAS", font=font(35, True), fill="white")

    title_text = wrapped(draw, title.upper(), 930, 78)
    draw.multiline_text(
        (60, 245),
        title_text,
        font=font(78, True),
        fill="white",
        spacing=10,
        stroke_width=2,
        stroke_fill=(0, 0, 0),
    )

    subtitle_text = "\n".join(textwrap.wrap(subtitle, width=38))
    draw.rounded_rectangle((58, 1325, 1022, 1665), radius=30, fill=(5, 10, 16, 218))
    draw.multiline_text(
        (92, 1370),
        subtitle_text,
        font=font(42),
        fill=(240, 242, 244),
        spacing=14,
    )
    draw.rounded_rectangle((92, 1570, 760, 1642), radius=18, fill=(242, 83, 31, 245))
    draw.text((122, 1587), cta.upper(), font=font(34, True), fill="white")
    draw.text((60, 1815), f"Imagem: {credit}", font=font(22), fill=(220, 225, 230))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(output_path, "JPEG", quality=93, optimize=True)


def build_audio(path: Path) -> None:
    samples = DURATION * SAMPLE_RATE
    t = np.arange(samples, dtype=np.float64) / SAMPLE_RATE
    mix = np.zeros(samples, dtype=np.float64)
    progression = (110.0, 146.83, 164.81, 130.81)
    for index, start in enumerate(np.arange(0.0, DURATION, 2.0)):
        mask = (t >= start) & (t < min(start + 2.0, DURATION))
        local = t[mask] - start
        root = progression[index % len(progression)]
        pad = (
            np.sin(2 * math.pi * root * local)
            + 0.45 * np.sin(2 * math.pi * root * 1.5 * local)
            + 0.25 * np.sin(2 * math.pi * root * 2.0 * local)
        )
        mix[mask] += pad * 0.12
    for beat in np.arange(0.0, DURATION, 0.5):
        start = round(beat * SAMPLE_RATE)
        length = min(round(0.12 * SAMPLE_RATE), samples - start)
        local = np.arange(length) / SAMPLE_RATE
        mix[start : start + length] += (
            np.sin(2 * math.pi * (86 - 45 * local) * local)
            * np.exp(-22 * local)
            * 0.18
        )
    fade = np.minimum(np.clip(t / 0.5, 0, 1), np.clip((DURATION - t) / 0.7, 0, 1))
    pcm = np.int16(np.clip(mix * fade, -0.95, 0.95) * 32767)
    with wave.open(str(path), "wb") as target:
        target.setnchannels(1)
        target.setsampwidth(2)
        target.setframerate(SAMPLE_RATE)
        target.writeframes(pcm.tobytes())


def encode(poster: Path, output: Path) -> None:
    audio = output.with_suffix(".wav")
    build_audio(audio)
    subprocess.run(
        [
            FFMPEG,
            "-y",
            "-loop",
            "1",
            "-framerate",
            str(FPS),
            "-i",
            str(poster),
            "-i",
            str(audio),
            "-t",
            str(DURATION),
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "19",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "160k",
            "-movflags",
            "+faststart",
            str(output),
        ],
        check=True,
    )
    audio.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Gera Story vertical TVDUASRODAS.")
    parser.add_argument("--image", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--title", required=True)
    parser.add_argument("--subtitle", required=True)
    parser.add_argument("--cta", default="Acesse TVDUASRODAS.COM")
    parser.add_argument("--credit", default="TVDUASRODAS")
    args = parser.parse_args()

    output_dir = args.output_dir.resolve()
    poster = output_dir / "story-poster.jpg"
    video = output_dir / "story.mp4"
    build_poster(
        args.image.resolve(),
        poster,
        args.title,
        args.subtitle,
        args.cta,
        args.credit,
    )
    encode(poster, video)
    print(f"POSTER={poster}")
    print(f"VIDEO={video}")
    print(f"DURATION={DURATION}")


if __name__ == "__main__":
    main()
