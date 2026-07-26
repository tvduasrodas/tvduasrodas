from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
import wave
from pathlib import Path

import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "instagram" / "generated-reel"
FONT = Path(r"C:\Windows\Fonts\arialbd.ttf")
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

W, H = 1080, 1920
FPS = 30
RATE = 44_100
SCENE_SECONDS = 3.25
PEEL_SECONDS = 0.75
PEEL_FRAMES = 8
SCENES: list[dict[str, object]] = []


def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT), size)


def crop_cover(image: Image.Image, focus: tuple[float, float]) -> Image.Image:
    scale = max(W / image.width, H / image.height)
    resized = image.resize(
        (round(image.width * scale), round(image.height * scale)),
        Image.Resampling.LANCZOS,
    )
    excess_x = max(0, resized.width - W)
    excess_y = max(0, resized.height - H)
    left = round(excess_x * focus[0])
    top = round(excess_y * focus[1])
    return resized.crop((left, top, left + W, top + H))


def fit_size(draw: ImageDraw.ImageDraw, text: str, maximum: int, max_width: int) -> int:
    size = maximum
    while size > 30:
        box = draw.textbbox((0, 0), text, font=font(size))
        if box[2] - box[0] <= max_width:
            return size
        size -= 2
    return size


def gradient_overlay() -> Image.Image:
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pixels = np.zeros((H, W, 4), dtype=np.uint8)
    start = 1110
    for y in range(start, H):
        progress = (y - start) / (H - start)
        alpha = round(185 * (progress**1.55))
        pixels[y, :, :3] = (5, 8, 13)
        pixels[y, :, 3] = alpha
    return Image.fromarray(pixels, "RGBA")


def make_scene(index: int, data: dict[str, object]) -> Path:
    with Image.open(data["photo"]) as source:
        scene = crop_cover(source.convert("RGB"), data["focus"])
    scene = ImageEnhance.Contrast(scene).enhance(1.04).convert("RGBA")
    scene.alpha_composite(gradient_overlay())
    draw = ImageDraw.Draw(scene)

    # Identidade pequena: informa sem ocupar a fotografia.
    draw.rounded_rectangle((54, 74, 386, 132), radius=15, fill=(10, 12, 17, 190))
    draw.rectangle((54, 74, 68, 132), fill=(242, 83, 31, 255))
    draw.text((86, 87), "TVDUASRODAS", font=font(31), fill=(255, 255, 255))
    draw.text(
        (904, 88),
        f"{index:02d}/{len(SCENES):02d}",
        font=font(27),
        fill=(255, 255, 255),
    )

    # Etiqueta e textos ficam na zona segura; não há placa preta cobrindo a foto.
    eyebrow = str(data["eyebrow"])
    eyebrow_box = draw.textbbox((0, 0), eyebrow, font=font(26))
    eyebrow_width = eyebrow_box[2] - eyebrow_box[0] + 44
    draw.rounded_rectangle((58, 1240, 58 + eyebrow_width, 1296), radius=14, fill=(242, 83, 31, 235))
    draw.text((80, 1253), eyebrow, font=font(26), fill=(255, 255, 255))

    title = str(data["title"])
    title_size = fit_size(draw, title, 70, 940)
    title_font = font(title_size)
    title_box = draw.textbbox((58, 1320), title, font=title_font, stroke_width=2)
    draw.rounded_rectangle(
        (
            title_box[0] - 16,
            title_box[1] - 10,
            title_box[2] + 16,
            title_box[3] + 10,
        ),
        radius=14,
        fill=(8, 10, 15, 218),
    )
    draw.text(
        (58, 1320),
        title,
        font=title_font,
        fill=(255, 255, 255),
        stroke_width=2,
        stroke_fill=(0, 0, 0, 165),
    )
    detail = str(data["detail"])
    detail_font = font(36)
    detail_box = draw.textbbox((58, 1412), detail, font=detail_font, stroke_width=1)
    draw.rounded_rectangle(
        (
            detail_box[0] - 14,
            detail_box[1] - 9,
            detail_box[2] + 14,
            detail_box[3] + 9,
        ),
        radius=12,
        fill=(8, 10, 15, 205),
    )
    draw.text(
        (58, 1412),
        detail,
        font=detail_font,
        fill=(244, 244, 242),
        stroke_width=1,
        stroke_fill=(0, 0, 0, 150),
    )
    draw.rectangle((58, 1490, 340, 1497), fill=(242, 83, 31, 255))
    draw.text(
        (58, 1520),
        f"Foto: {data['credit']}",
        font=font(22),
        fill=(236, 236, 232),
        stroke_width=1,
        stroke_fill=(0, 0, 0, 150),
    )

    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"scene-{index:02d}.jpg"
    scene.convert("RGB").save(path, "JPEG", quality=93, optimize=True)
    return path


def make_page_peel(old_path: Path, new_path: Path, transition_index: int) -> list[Path]:
    with Image.open(old_path) as old_image, Image.open(new_path) as new_image:
        old = np.asarray(old_image.convert("RGB"), dtype=np.float32)
        new = np.asarray(new_image.convert("RGB"), dtype=np.float32)

    yy, xx = np.mgrid[0:H, 0:W]
    diagonal = xx + yy
    maximum = W + H
    band = 155.0
    frames: list[Path] = []

    for frame_index in range(PEEL_FRAMES):
        progress = (frame_index + 1) / (PEEL_FRAMES + 1)
        eased = 0.5 - 0.5 * math.cos(math.pi * progress)
        threshold = maximum * (1.0 - eased)
        distance = diagonal - threshold

        reveal = np.clip((distance + band * 0.32) / (band * 0.64), 0.0, 1.0)[..., None]
        frame = old * (1.0 - reveal) + new * reveal

        # Sombra e brilho formam a dobra do papel.
        shadow = np.clip(1.0 - np.abs(distance + 58.0) / 90.0, 0.0, 1.0)[..., None]
        frame *= 1.0 - shadow * 0.28
        fold = np.clip(1.0 - np.abs(distance - 18.0) / 78.0, 0.0, 1.0)[..., None]
        fold_color = np.array([246.0, 239.0, 226.0], dtype=np.float32)
        frame = frame * (1.0 - fold * 0.68) + fold_color * (fold * 0.68)

        # Linha quente na borda reforça a identidade visual sem virar uma tarja.
        edge = np.clip(1.0 - np.abs(distance - 72.0) / 6.0, 0.0, 1.0)[..., None]
        orange = np.array([242.0, 83.0, 31.0], dtype=np.float32)
        frame = frame * (1.0 - edge * 0.8) + orange * (edge * 0.8)

        path = OUT / f"peel-{transition_index:02d}-{frame_index + 1:02d}.jpg"
        Image.fromarray(np.uint8(np.clip(frame, 0, 255)), "RGB").save(
            path, "JPEG", quality=91, optimize=True
        )
        frames.append(path)
    return frames


def rock_track(path: Path, duration: float) -> None:
    samples = round(RATE * duration)
    t = np.arange(samples, dtype=np.float64) / RATE
    mix = np.zeros(samples, dtype=np.float64)
    rng = np.random.default_rng(20260725)
    progression = (82.41, 73.42, 65.41, 98.00)  # E2, D2, C2, G2

    for bar, start in enumerate(np.arange(0.0, duration, 2.0)):
        stop = min(start + 2.0, duration)
        mask = (t >= start) & (t < stop)
        local = t[mask] - start
        root = progression[bar % len(progression)]

        guitar = (
            np.sin(2 * np.pi * root * local)
            + 0.72 * np.sin(2 * np.pi * root * 1.5 * local)
            + 0.50 * np.sin(2 * np.pi * root * 2.0 * local)
        )
        chug = 0.50 + 0.50 * np.square(np.sin(2 * np.pi * 4.0 * local))
        mix[mask] += np.tanh(guitar * 1.85) * chug * 0.16
        mix[mask] += np.sin(2 * np.pi * (root / 2) * local) * 0.09

    for beat in np.arange(0.0, duration, 0.5):
        start = round(beat * RATE)
        length = min(round(0.18 * RATE), samples - start)
        if length <= 0:
            continue
        local = np.arange(length) / RATE
        kick = np.sin(2 * np.pi * (92 - 55 * local) * local) * np.exp(-24 * local)
        mix[start : start + length] += kick * (0.28 if int(beat * 2) % 4 in (0, 2) else 0.10)

    for beat in np.arange(0.5, duration, 1.0):
        start = round(beat * RATE)
        length = min(round(0.16 * RATE), samples - start)
        if length <= 0:
            continue
        local = np.arange(length) / RATE
        snare = rng.normal(0.0, 1.0, length) * np.exp(-19 * local)
        mix[start : start + length] += snare * 0.14

    for beat in np.arange(0.0, duration, 0.25):
        start = round(beat * RATE)
        length = min(round(0.045 * RATE), samples - start)
        if length <= 0:
            continue
        local = np.arange(length) / RATE
        hat = rng.normal(0.0, 1.0, length) * np.exp(-75 * local)
        mix[start : start + length] += hat * 0.032

    fade = round(0.45 * RATE)
    mix[:fade] *= np.linspace(0.0, 1.0, fade)
    mix[-fade:] *= np.linspace(1.0, 0.0, fade)
    mix /= max(float(np.max(np.abs(mix))), 1e-9)
    pcm = np.int16(np.clip(mix * 0.72, -1.0, 1.0) * 32767)
    stereo = np.column_stack((pcm, pcm)).ravel()

    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(2)
        wav.setsampwidth(2)
        wav.setframerate(RATE)
        wav.writeframes(stereo.tobytes())


def build_video(scenes: list[Path], transitions: list[list[Path]]) -> float:
    concat = OUT / "timeline.txt"
    lines: list[str] = []
    peel_frame_seconds = PEEL_SECONDS / PEEL_FRAMES

    for index, scene in enumerate(scenes):
        lines.extend((f"file '{scene.as_posix()}'", f"duration {SCENE_SECONDS:.5f}"))
        if index < len(transitions):
            for frame in transitions[index]:
                lines.extend((f"file '{frame.as_posix()}'", f"duration {peel_frame_seconds:.5f}"))
    lines.append(f"file '{scenes[-1].as_posix()}'")
    concat.write_text("\n".join(lines), encoding="utf-8")

    duration = SCENE_SECONDS * len(scenes) + PEEL_SECONDS * len(transitions)
    audio = OUT / "trilha-rock-original.wav"
    rock_track(audio, duration)
    video = OUT / "reel.mp4"

    subprocess.run(
        [
            FFMPEG,
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat),
            "-i",
            str(audio),
            "-t",
            f"{duration:.3f}",
            "-r",
            str(FPS),
            "-vf",
            f"scale={W}:{H},format=yuv420p",
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "19",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-movflags",
            "+faststart",
            str(video),
        ],
        check=True,
    )
    concat.unlink(missing_ok=True)
    audio.unlink(missing_ok=True)
    return duration


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_manifest(path: Path) -> tuple[dict[str, object], list[dict[str, object]]]:
    manifest = json.loads(path.read_text(encoding="utf-8"))
    if manifest.get("rights_verified") is not True:
        raise ValueError("O manifesto deve confirmar rights_verified=true.")

    raw_scenes = manifest.get("scenes")
    if not isinstance(raw_scenes, list) or not 5 <= len(raw_scenes) <= 7:
        raise ValueError("O Reel exige de 5 a 7 cenas com imagens diferentes.")

    scenes: list[dict[str, object]] = []
    hashes: set[str] = set()
    required = ("image", "context", "title", "detail", "credit", "source_url")
    for index, raw in enumerate(raw_scenes, 1):
        if not isinstance(raw, dict):
            raise ValueError(f"Cena {index}: estrutura inválida.")
        missing = [field for field in required if not str(raw.get(field, "")).strip()]
        if missing:
            raise ValueError(f"Cena {index}: campos obrigatórios ausentes: {', '.join(missing)}.")

        photo = Path(str(raw["image"]))
        if not photo.is_absolute():
            photo = (path.parent / photo).resolve()
        if not photo.is_file():
            raise FileNotFoundError(f"Cena {index}: imagem inexistente: {photo}")

        image_hash = file_sha256(photo)
        if image_hash in hashes:
            raise ValueError(
                f"Cena {index}: imagem repetida. Cortes diferentes do mesmo arquivo não são permitidos."
            )
        hashes.add(image_hash)

        focus = raw.get("focus", [0.5, 0.5])
        if (
            not isinstance(focus, list)
            or len(focus) != 2
            or any(not isinstance(value, (int, float)) for value in focus)
            or any(value < 0 or value > 1 for value in focus)
        ):
            raise ValueError(f"Cena {index}: focus deve conter dois números entre 0 e 1.")

        scenes.append(
            {
                "photo": photo,
                "focus": (float(focus[0]), float(focus[1])),
                "eyebrow": str(raw["context"]).upper(),
                "title": str(raw["title"]).upper(),
                "detail": str(raw["detail"]),
                "credit": str(raw["credit"]),
                "source_url": str(raw["source_url"]),
                "sha256": image_hash,
            }
        )
    return manifest, scenes


def main() -> None:
    global OUT, SCENES

    parser = argparse.ArgumentParser(
        description="Gera o Reel padrão TVDUASRODAS a partir de 5 a 7 fotos distintas."
    )
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    manifest_path = args.manifest.resolve()
    manifest, SCENES = load_manifest(manifest_path)
    OUT = args.output_dir.resolve()
    OUT.mkdir(parents=True, exist_ok=True)

    scene_paths = [make_scene(index, data) for index, data in enumerate(SCENES, 1)]
    transitions = [
        make_page_peel(scene_paths[index], scene_paths[index + 1], index + 1)
        for index in range(len(scene_paths) - 1)
    ]
    duration = build_video(scene_paths, transitions)
    (OUT / "reel-cover.jpg").write_bytes(scene_paths[0].read_bytes())
    receipt = {
        "format": "1080x1920",
        "video_codec": "H.264",
        "audio_codec": "AAC",
        "transition": "page_peel_diagonal",
        "soundtrack": "rock_instrumental_original",
        "scene_count": len(SCENES),
        "nominal_duration_seconds": round(duration, 2),
        "rights_verified": True,
        "source_manifest": str(manifest_path),
        "content_url": manifest.get("content_url", ""),
        "scenes": [
            {
                "image": str(scene["photo"]),
                "sha256": scene["sha256"],
                "credit": scene["credit"],
                "source_url": scene["source_url"],
            }
            for scene in SCENES
        ],
    }
    (OUT / "reel-build.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"OUTPUT={OUT}")
    print(f"VIDEO={OUT / 'reel.mp4'}")
    print(f"SCENES={len(SCENES)}")
    print(f"DURATION={duration:.2f}")


if __name__ == "__main__":
    main()
