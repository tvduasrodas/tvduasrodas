from __future__ import annotations

import math
import subprocess
import textwrap
import wave
from pathlib import Path

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "instagram" / "2026-07-23"
FONT_BOLD = Path(r"C:\Windows\Fonts\arialbd.ttf")
FONT_REGULAR = Path(r"C:\Windows\Fonts\arial.ttf")
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()


PACKAGES = [
    {
        "slug": "pontos-cegos-moto-cidade-como-pilotar-com-margem",
        "label": "PILOTAGEM URBANA",
        "title": "PONTOS CEGOS:\nPILOTE COM MARGEM",
        "subtitle": "Posição, distância e leitura do trânsito reduzem conflitos.",
        "images": [
            "assets/img/uploads/seguranca-urbana-pontos-cegos-capa.webp",
            "assets/img/uploads/seguranca-urbana-espelhos.webp",
            "assets/img/uploads/seguranca-urbana-cruzamento.webp",
        ],
        "scenes": [
            ("VOCÊ FOI VISTO?", "Na cidade, enxergar não garante que o motorista percebeu sua moto."),
            ("EVITE O PONTO CEGO", "Não permaneça ao lado da coluna traseira de carros, ônibus e caminhões."),
            ("CRIE DISTÂNCIA", "Espaço à frente oferece tempo para frear e uma rota de escape."),
            ("LEIA O CRUZAMENTO", "Reduza antes de esquinas, retornos, garagens e conversões."),
            ("SEJA PREVISÍVEL", "Espelho, seta e checagem lateral: comunique antes de mudar de faixa."),
            ("PILOTE COM MARGEM", "Siga @tvduasrodasofc\nAcesse TVDUASRODAS.COM"),
        ],
    },
    {
        "slug": "role-de-rua-23-07-2026-rotas-curtas",
        "label": "ROLÊ DE RUA",
        "title": "ROTAS CURTAS\nSEM IMPROVISO",
        "subtitle": "Moto, scooter ou bicicleta: planeje antes de sair.",
        "images": [
            "assets/img/uploads/role-de-rua-rotas-curtas-capa.webp",
            "assets/img/uploads/role-de-rua-planejamento-bike.webp",
            "assets/img/uploads/role-de-rua-estacionamento-scooter.webp",
        ],
        "scenes": [
            ("CURTO NÃO É AUTOMÁTICO", "Obra, chuva e estacionamento podem mudar um trajeto simples."),
            ("COMPARE DUAS ROTAS", "A via mais previsível pode ser melhor do que a mais curta."),
            ("ESCOLHA O MODO", "Bicicleta, scooter ou moto: use o veículo adequado para o percurso."),
            ("CHEQUE EM 3 MINUTOS", "Pneus, freios, luzes, capacete, trava e condição do tempo."),
            ("PLANEJE ONDE PARAR", "Vaga segura e regular faz parte da rota, não do improviso."),
            ("ROTA BOA É PREVISÍVEL", "Siga @tvduasrodasofc\nAcesse TVDUASRODAS.COM"),
        ],
    },
]


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_BOLD if bold else FONT_REGULAR), size)


def cover_image(path: Path, size: tuple[int, int]) -> Image.Image:
    image = Image.open(path).convert("RGB")
    target_ratio = size[0] / size[1]
    ratio = image.width / image.height
    if ratio > target_ratio:
        new_width = int(image.height * target_ratio)
        left = (image.width - new_width) // 2
        image = image.crop((left, 0, left + new_width, image.height))
    else:
        new_height = int(image.width / target_ratio)
        top = (image.height - new_height) // 2
        image = image.crop((0, top, image.width, top + new_height))
    return image.resize(size, Image.Resampling.LANCZOS)


def gradient_overlay(image: Image.Image, top_alpha: int = 30, bottom_alpha: int = 235) -> Image.Image:
    base = image.convert("RGBA")
    layer = Image.new("RGBA", base.size)
    pixels = layer.load()
    for y in range(base.height):
        alpha = int(top_alpha + (bottom_alpha - top_alpha) * (y / max(1, base.height - 1)))
        for x in range(base.width):
            pixels[x, y] = (5, 12, 18, alpha)
    return Image.alpha_composite(base, layer).convert("RGB")


def draw_brand(draw: ImageDraw.ImageDraw, width: int, y: int) -> None:
    draw.rounded_rectangle((70, y, 480, y + 72), radius=16, fill=(230, 36, 45))
    draw.text((92, y + 15), "TVDUASRODAS", font=font(38, True), fill="white")
    draw.text((width - 360, y + 20), "@tvduasrodasofc", font=font(29, True), fill="white")


def draw_wrapped(draw: ImageDraw.ImageDraw, text: str, xy: tuple[int, int], width_chars: int, size: int,
                 fill: str = "white", bold: bool = False, spacing: int = 12) -> int:
    wrapped = "\n".join(textwrap.wrap(text, width=width_chars, break_long_words=False))
    draw.multiline_text(xy, wrapped, font=font(size, bold), fill=fill, spacing=spacing)
    box = draw.multiline_textbbox(xy, wrapped, font=font(size, bold), spacing=spacing)
    return box[3]


def make_card(pkg: dict, image_path: Path, output: Path, size: tuple[int, int], scene=None) -> None:
    image = gradient_overlay(cover_image(image_path, size))
    draw = ImageDraw.Draw(image)
    draw_brand(draw, size[0], 70)
    if scene is None:
        draw.rounded_rectangle((70, size[1] - 620, 520, size[1] - 560), radius=14, fill=(245, 180, 0))
        draw.text((92, size[1] - 610), pkg["label"], font=font(30, True), fill=(10, 18, 24))
        draw.multiline_text((70, size[1] - 520), pkg["title"], font=font(78, True), fill="white", spacing=8)
        draw_wrapped(draw, pkg["subtitle"], (70, size[1] - 290), 40, 38, fill=(235, 240, 245))
        draw.text((70, size[1] - 105), "TVDUASRODAS.COM", font=font(35, True), fill=(245, 180, 0))
    else:
        heading, copy = scene
        draw.rounded_rectangle((70, size[1] - 680, size[0] - 70, size[1] - 170), radius=28, fill=(5, 12, 18, 205))
        draw.text((105, size[1] - 630), heading, font=font(64, True), fill=(245, 180, 0))
        draw_wrapped(draw, copy, (105, size[1] - 510), 34, 43, fill="white", spacing=14)
        draw.text((105, size[1] - 235), f"{pkg['label']}  •  TVDUASRODAS.COM", font=font(27, True), fill=(210, 220, 228))
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output, quality=92, optimize=True, subsampling=1)


def make_audio(path: Path, duration: float) -> None:
    rate = 44100
    with wave.open(str(path), "w") as wav:
        wav.setnchannels(2)
        wav.setsampwidth(2)
        wav.setframerate(rate)
        frames = bytearray()
        notes = [110.0, 146.83, 164.81, 196.0]
        for i in range(int(rate * duration)):
            t = i / rate
            beat = int(t / 2.0) % len(notes)
            envelope = 0.55 + 0.45 * math.sin(math.pi * ((t % 2.0) / 2.0))
            value = (
                math.sin(2 * math.pi * notes[beat] * t)
                + 0.35 * math.sin(2 * math.pi * notes[beat] * 2 * t)
                + 0.18 * math.sin(2 * math.pi * 55 * t)
            )
            sample = int(max(-1, min(1, value * envelope * 0.12)) * 32767)
            frames.extend(sample.to_bytes(2, "little", signed=True) * 2)
        wav.writeframes(frames)


def make_video(images: list[Path], audio: Path, output: Path, seconds_each: float) -> None:
    concat = output.with_suffix(".concat.txt")
    lines = []
    for image in images:
        lines.extend([f"file '{image.as_posix()}'", f"duration {seconds_each:.3f}"])
    lines.append(f"file '{images[-1].as_posix()}'")
    concat.write_text("\n".join(lines), encoding="utf-8")
    command = [
        FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", str(concat),
        "-i", str(audio), "-shortest", "-r", "30",
        "-vf", "scale=1080:1920,format=yuv420p",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(output),
    ]
    subprocess.run(command, check=True)
    concat.unlink(missing_ok=True)


def main() -> None:
    for pkg in PACKAGES:
        folder = OUT / pkg["slug"]
        sources = [ROOT / path for path in pkg["images"]]
        make_card(pkg, sources[0], folder / "feed.jpg", (1080, 1350))
        make_card(pkg, sources[0], folder / "story-base.jpg", (1080, 1920))
        reel_scenes = []
        for index, scene in enumerate(pkg["scenes"], 1):
            scene_path = folder / f"reel-scene-{index:02d}.jpg"
            make_card(pkg, sources[(index - 1) % len(sources)], scene_path, (1080, 1920), scene=scene)
            reel_scenes.append(scene_path)
        (folder / "reel-cover.jpg").write_bytes(reel_scenes[0].read_bytes())
        audio = folder / "trilha-original.wav"
        make_audio(audio, 30)
        make_video([folder / "story-base.jpg"], audio, folder / "story.mp4", 14.0)
        make_video(reel_scenes, audio, folder / "reel.mp4", 4.0)
        audio.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
