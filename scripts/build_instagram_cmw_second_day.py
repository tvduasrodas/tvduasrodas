from __future__ import annotations

import math
import subprocess
import textwrap
import wave
from pathlib import Path

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageEnhance, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "instagram" / "2026-07-25" / "capital-moto-week-2026-segundo-dia-dicas"
SOURCE = OUT / "arte-editorial-ia.png"
FONT_BOLD = Path(r"C:\Windows\Fonts\arialbd.ttf")
FONT_REGULAR = Path(r"C:\Windows\Fonts\arial.ttf")
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

SCENES = [
    ("SEGUNDO DIA", "O festival segue em Bras\u00edlia. Planeje a visita antes de sair."),
    ("CONFIRA O ACESSO", "Ingressos, hor\u00e1rios e regras devem ser vistos nos canais oficiais."),
    ("V\u00c1 DE EQUIPAMENTO", "Capacete, hidrata\u00e7\u00e3o e itens de chuva ajudam a curtir com margem."),
    ("ENCONTRE O RITMO", "Combine ponto de encontro e retorno antes de a programa\u00e7\u00e3o come\u00e7ar."),
    ("SERVI\u00c7O ATUALIZADO", "Acompanhe a cobertura e confirme o que mudou no dia."),
    ("CAPITAL MOTO WEEK", "Siga @tvduasrodasofc\nAcesse TVDUASRODAS.COM"),
]


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_BOLD if bold else FONT_REGULAR), size)


def base_image(size: tuple[int, int]) -> Image.Image:
    image = Image.open(SOURCE).convert("RGB")
    ratio = size[0] / size[1]
    if image.width / image.height > ratio:
        width = int(image.height * ratio)
        left = (image.width - width) // 2
        image = image.crop((left, 0, left + width, image.height))
    else:
        height = int(image.width / ratio)
        top = (image.height - height) // 2
        image = image.crop((0, top, image.width, top + height))
    image = image.resize(size, Image.Resampling.LANCZOS)
    return ImageEnhance.Brightness(image).enhance(0.78)


def brand(draw: ImageDraw.ImageDraw, width: int) -> None:
    draw.rounded_rectangle((64, 64, 474, 136), radius=16, fill=(230, 36, 45))
    draw.text((86, 79), "TVDUASRODAS", font=font(38, True), fill="white")
    draw.text((width - 380, 85), "@tvduasrodasofc", font=font(29, True), fill="white")


def wrap(draw: ImageDraw.ImageDraw, value: str, xy: tuple[int, int], chars: int, size: int) -> None:
    draw.multiline_text(xy, "\n".join(textwrap.wrap(value, width=chars)), font=font(size), fill="white", spacing=13)


def card(path: Path, scene: tuple[str, str] | None = None) -> None:
    image = base_image((1080, 1920)).convert("RGBA")
    shade = Image.new("RGBA", image.size, (3, 11, 22, 0))
    shade_draw = ImageDraw.Draw(shade)
    shade_draw.rectangle((0, 1100, 1080, 1920), fill=(3, 11, 22, 220))
    image = Image.alpha_composite(image, shade).convert("RGB")
    draw = ImageDraw.Draw(image)
    brand(draw, 1080)
    if scene is None:
        draw.rounded_rectangle((64, 1200, 760, 1262), radius=14, fill=(245, 180, 0))
        draw.text((87, 1213), "EVENTOS", font=font(31, True), fill=(5, 12, 18))
        draw.multiline_text((64, 1310), "CAPITAL MOTO WEEK\nSEGUNDO DIA", font=font(72, True), fill="white", spacing=7)
        wrap(draw, "Dicas para curtir o festival com planejamento e margem.", (64, 1515), 38, 39)
        draw.text((64, 1810), "ACESSE TVDUASRODAS.COM", font=font(33, True), fill=(245, 180, 0))
    else:
        heading, copy = scene
        draw.rounded_rectangle((64, 1220, 1016, 1758), radius=28, fill=(3, 11, 22, 212))
        draw.text((100, 1275), heading, font=font(62, True), fill=(245, 180, 0))
        wrap(draw, copy, (100, 1400), 35, 44)
        draw.text((100, 1688), "EVENTOS  •  TVDUASRODAS.COM", font=font(27, True), fill=(215, 223, 230))
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, quality=92, optimize=True)


def audio(path: Path, duration: float) -> None:
    rate = 44100
    with wave.open(str(path), "w") as wav:
        wav.setnchannels(2); wav.setsampwidth(2); wav.setframerate(rate)
        frames = bytearray(); notes = [110.0, 146.83, 164.81, 196.0]
        for i in range(int(rate * duration)):
            t = i / rate; note = notes[int(t / 2) % len(notes)]
            value = (math.sin(2 * math.pi * note * t) + 0.25 * math.sin(4 * math.pi * note * t)) * 0.11
            frames.extend(int(value * 32767).to_bytes(2, "little", signed=True) * 2)
        wav.writeframes(frames)


def video(images: list[Path], soundtrack: Path, out: Path, seconds_each: float) -> None:
    concat = out.with_suffix(".concat.txt")
    concat.write_text("\n".join([item for image in images for item in (f"file '{image.as_posix()}'", f"duration {seconds_each:.3f}")] + [f"file '{images[-1].as_posix()}'"]), encoding="utf-8")
    subprocess.run([FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", str(concat), "-i", str(soundtrack), "-shortest", "-r", "30", "-vf", "scale=1080:1920,format=yuv420p", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(out)], check=True)
    concat.unlink(missing_ok=True)


def main() -> None:
    story_base = OUT / "story-poster.jpg"
    card(story_base)
    scenes = []
    for index, scene in enumerate(SCENES, 1):
        path = OUT / f"reel-scene-{index:02d}.jpg"; card(path, scene); scenes.append(path)
    (OUT / "reel-cover.jpg").write_bytes(scenes[0].read_bytes())
    soundtrack = OUT / "trilha-original.wav"; audio(soundtrack, 30)
    video([story_base], soundtrack, OUT / "story.mp4", 14)
    video(scenes, soundtrack, OUT / "reel.mp4", 4)
    soundtrack.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
