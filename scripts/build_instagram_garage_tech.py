from __future__ import annotations

import math
import subprocess
import wave
from pathlib import Path

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "instagram" / "2026-07-24" / "garage-tech-corrente-moto-limpeza-lubrificacao"
IMAGES = [
    ROOT / "assets/img/uploads/garage-tech-corrente-capa.jpg",
    ROOT / "assets/img/uploads/garage-tech-corrente-limpeza.jpg",
    ROOT / "assets/img/uploads/garage-tech-corrente-lubrificacao.jpg",
]
SCENES = [
    ("CORRENTE SEGURA", "Antes de lubrificar, pare a moto e confira o conjunto."),
    ("OLHE OS ELOS", "Ferrugem, elos travados e desgaste pedem atenção."),
    ("FOLGA É DO MANUAL", "Cada modelo tem a medida e o método recomendados."),
    ("LIMPE COM CUIDADO", "Evite solventes agressivos e mantenha o motor desligado."),
    ("LUBRIFIQUE SEM EXCESSO", "Produto demais acumula sujeira e pode ser arremessado."),
    ("MANUTENÇÃO COM MARGEM", "Siga @tvduasrodasofc\nAcesse TVDUASRODAS.COM"),
]
SIZE = (1080, 1920)
FONT_BOLD = Path(r"C:\Windows\Fonts\arialbd.ttf")
FONT_REGULAR = Path(r"C:\Windows\Fonts\arial.ttf")


def fit(path: Path) -> Image.Image:
    image = Image.open(path).convert("RGB")
    ratio = SIZE[0] / SIZE[1]
    if image.width / image.height > ratio:
        width = int(image.height * ratio)
        image = image.crop(((image.width - width) // 2, 0, (image.width + width) // 2, image.height))
    else:
        height = int(image.width / ratio)
        image = image.crop((0, (image.height - height) // 2, image.width, (image.height + height) // 2))
    return image.resize(SIZE, Image.Resampling.LANCZOS)


def card(path: Path, heading: str, copy: str, output: Path) -> None:
    image = fit(path).convert("RGBA")
    overlay = Image.new("RGBA", SIZE, (4, 12, 18, 0))
    pixels = overlay.load()
    for y in range(SIZE[1]):
        alpha = int(30 + 220 * y / SIZE[1])
        for x in range(SIZE[0]):
            pixels[x, y] = (4, 12, 18, alpha)
    image = Image.alpha_composite(image, overlay).convert("RGB")
    draw = ImageDraw.Draw(image)
    bold = lambda size: ImageFont.truetype(str(FONT_BOLD), size)
    regular = lambda size: ImageFont.truetype(str(FONT_REGULAR), size)
    draw.rounded_rectangle((70, 70, 500, 145), radius=16, fill=(230, 36, 45))
    draw.text((92, 88), "TVDUASRODAS", font=bold(38), fill="white")
    draw.text((690, 94), "@tvduasrodasofc", font=bold(28), fill="white")
    draw.rounded_rectangle((70, 1190, 1010, 1740), radius=30, fill=(4, 12, 18))
    draw.text((110, 1250), heading, font=bold(62), fill=(245, 180, 0))
    draw.multiline_text((110, 1370), copy, font=regular(45), fill="white", spacing=14)
    draw.text((110, 1665), "GARAGE TECH  •  TVDUASRODAS.COM", font=bold(27), fill=(215, 225, 235))
    image.save(output, quality=92, optimize=True, subsampling=1)


def audio(output: Path, seconds: float) -> None:
    rate = 44100
    with wave.open(str(output), "w") as wav:
        wav.setnchannels(2); wav.setsampwidth(2); wav.setframerate(rate)
        frames = bytearray(); notes = (110.0, 146.83, 164.81, 196.0)
        for i in range(int(rate * seconds)):
            t = i / rate; note = notes[int(t / 2) % len(notes)]
            value = (math.sin(2 * math.pi * note * t) + 0.3 * math.sin(4 * math.pi * note * t)) * 0.1
            sample = int(max(-1, min(1, value)) * 32767)
            frames.extend(sample.to_bytes(2, "little", signed=True) * 2)
        wav.writeframes(frames)


def video(images: list[Path], sound: Path, output: Path, seconds_per_scene: float) -> None:
    manifest = output.with_suffix(".concat.txt")
    manifest.write_text("\n".join(sum(([f"file '{path.as_posix()}'", f"duration {seconds_per_scene:.3f}"] for path in images), []) + [f"file '{images[-1].as_posix()}'"]), encoding="utf-8")
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-f", "concat", "-safe", "0", "-i", str(manifest), "-i", str(sound), "-shortest", "-r", "30", "-vf", "scale=1080:1920,format=yuv420p", "-c:v", "libx264", "-crf", "20", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(output)], check=True)
    manifest.unlink(missing_ok=True)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    scene_paths = []
    for index, (heading, copy) in enumerate(SCENES, 1):
        output = OUT / f"reel-scene-{index:02d}.jpg"
        card(IMAGES[(index - 1) % len(IMAGES)], heading, copy, output)
        scene_paths.append(output)
    (OUT / "reel-cover.jpg").write_bytes(scene_paths[0].read_bytes())
    card(IMAGES[0], "CORRENTE: CUIDE COM SEGURANÇA", "Inspeção, limpeza e lubrificação sempre com a moto parada.", OUT / "story-base.jpg")
    soundtrack = OUT / "trilha-original.wav"
    audio(soundtrack, 24)
    video([OUT / "story-base.jpg"], soundtrack, OUT / "story.mp4", 14)
    video(scene_paths, soundtrack, OUT / "reel.mp4", 4)
    soundtrack.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
