from __future__ import annotations

import math
import subprocess
import textwrap
import wave
from pathlib import Path

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "instagram" / "2026-07-25" / "estrada-aberta-25-07-2026-ritmo-planejamento"
SOURCE = OUT / "arte-editorial-ia.png"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
FONT_BOLD = Path(r"C:\Windows\Fonts\arialbd.ttf")
FONT_REGULAR = Path(r"C:\Windows\Fonts\arial.ttf")

SCENES = [
    ("VIAGEM NÃO É CRONÔMETRO", "Ritmo seguro começa com margem para mudar o plano."),
    ("DIVIDA O TRAJETO", "Serra, chuva, obras e tráfego mudam o tempo real de cada trecho."),
    ("PARE ANTES DA FADIGA", "Planeje combustível, água e descanso em locais seguros."),
    ("REVISE A MOTO", "Bagagem firme, pneus, luzes e clima: confira tudo sem pressa."),
    ("MARGEM É SEGURANÇA", "Siga @tvduasrodasofc\nAcesse TVDUASRODAS.COM"),
]


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_BOLD if bold else FONT_REGULAR), size)


def crop_portrait(source: Path) -> Image.Image:
    image = Image.open(source).convert("RGB")
    ratio = 1080 / 1920
    current = image.width / image.height
    if current > ratio:
        width = int(image.height * ratio)
        left = (image.width - width) // 2
        image = image.crop((left, 0, left + width, image.height))
    else:
        height = int(image.width / ratio)
        top = max(0, (image.height - height) // 2)
        image = image.crop((0, top, image.width, top + height))
    return image.resize((1080, 1920), Image.Resampling.LANCZOS)


def card(heading: str, copy: str, path: Path) -> None:
    image = crop_portrait(SOURCE).convert("RGBA")
    shade = Image.new("RGBA", image.size)
    pixels = shade.load()
    for y in range(1920):
        alpha = int(24 + 210 * (y / 1919))
        for x in range(1080):
            pixels[x, y] = (3, 12, 23, alpha)
    image = Image.alpha_composite(image, shade).convert("RGB")
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((64, 65, 470, 135), radius=18, fill=(225, 42, 49))
    draw.text((88, 82), "TVDUASRODAS", font=font(35, True), fill="white")
    draw.text((730, 86), "@tvduasrodasofc", font=font(28, True), fill="white")
    draw.rounded_rectangle((64, 1200, 1016, 1765), radius=30, fill=(4, 13, 25, 218))
    draw.text((104, 1260), heading, font=font(64, True), fill=(248, 183, 35), spacing=8)
    wrapped = "\n".join(textwrap.wrap(copy, width=32, break_long_words=False))
    draw.multiline_text((104, 1415), wrapped, font=font(45, False), fill="white", spacing=14)
    draw.text((104, 1698), "ESTRADA ABERTA  •  TVDUASRODAS.COM", font=font(27, True), fill=(218, 228, 235))
    image.save(path, quality=92, optimize=True)


def audio(path: Path, seconds: float) -> None:
    rate = 44100
    notes = [110.0, 146.83, 164.81, 196.0]
    with wave.open(str(path), "w") as wav:
        wav.setnchannels(2); wav.setsampwidth(2); wav.setframerate(rate)
        frames = bytearray()
        for i in range(int(rate * seconds)):
            t = i / rate
            note = notes[int(t / 2) % len(notes)]
            envelope = 0.5 + 0.5 * math.sin(math.pi * ((t % 2) / 2))
            sample = int((math.sin(2 * math.pi * note * t) + 0.25 * math.sin(4 * math.pi * note * t)) * envelope * 0.10 * 32767)
            frames.extend(sample.to_bytes(2, "little", signed=True) * 2)
        wav.writeframes(frames)


def video(images: list[Path], sound: Path, output: Path, seconds_each: float) -> None:
    manifest = output.with_suffix(".concat.txt")
    rows = []
    for image in images:
        rows.extend([f"file '{image.as_posix()}'", f"duration {seconds_each:.3f}"])
    rows.append(f"file '{images[-1].as_posix()}'")
    manifest.write_text("\n".join(rows), encoding="utf-8")
    subprocess.run([FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", str(manifest), "-i", str(sound), "-shortest", "-r", "30", "-vf", "scale=1080:1920,format=yuv420p", "-c:v", "libx264", "-crf", "20", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(output)], check=True)
    manifest.unlink(missing_ok=True)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    cards = []
    for index, (heading, copy) in enumerate(SCENES, 1):
        target = OUT / f"reel-scene-{index:02d}.jpg"
        card(heading, copy, target)
        cards.append(target)
    (OUT / "reel-cover.jpg").write_bytes(cards[0].read_bytes())
    card("PARE COM MARGEM", "Planeje o ritmo, a parada e a revisão da moto antes de seguir.", OUT / "story-poster.jpg")
    sound = OUT / "trilha-original.wav"
    audio(sound, 25)
    video([OUT / "story-poster.jpg"], sound, OUT / "story.mp4", 14)
    video(cards, sound, OUT / "reel.mp4", 4.8)
    sound.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
