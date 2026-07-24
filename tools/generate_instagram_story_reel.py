from __future__ import annotations

import argparse
import math
import subprocess
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

try:
    from imageio_ffmpeg import get_ffmpeg_exe
except ModuleNotFoundError:
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".social-deps"))
    from imageio_ffmpeg import get_ffmpeg_exe


W, H, FPS, RATE = 1080, 1920, 30, 44_100
FONT_BOLD = Path(r"C:\Windows\Fonts\arialbd.ttf")
FONT_REGULAR = Path(r"C:\Windows\Fonts\arial.ttf")


def font(size: int, bold: bool = False):
    return ImageFont.truetype(str(FONT_BOLD if bold else FONT_REGULAR), size)


def crop(image: Image.Image, size: tuple[int, int], focus: float = 0.5) -> Image.Image:
    scale = max(size[0] / image.width, size[1] / image.height)
    resized = image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)
    x = (resized.width - size[0]) // 2
    y = round((resized.height - size[1]) * focus)
    return resized.crop((x, y, x + size[0], y + size[1]))


def lines(draw: ImageDraw.ImageDraw, message: str, face, max_width: int) -> list[str]:
    result, current = [], ""
    for word in message.split():
        proposal = f"{current} {word}".strip()
        if current and draw.textbbox((0, 0), proposal, font=face, stroke_width=2)[2] > max_width:
            result.append(current)
            current = word
        else:
            current = proposal
    if current:
        result.append(current)
    return result


def centered(draw: ImageDraw.ImageDraw, message: str, y: int, size: int, color=(255, 255, 255), width=900) -> int:
    face = font(size, True)
    for line in lines(draw, message, face, width):
        box = draw.textbbox((0, 0), line, font=face, stroke_width=2)
        draw.text(((W - (box[2] - box[0])) // 2, y), line, font=face, fill=color, stroke_width=2, stroke_fill=(0, 0, 0))
        y += box[3] - box[1] + 15
    return y


def canvas(source: Path, eyebrow: str, headline: str, detail: str, credit: str) -> Image.Image:
    with Image.open(source) as original:
        photo = crop(original.convert("RGB"), (W, 970), 0.48).convert("RGBA")
        background = crop(original.convert("RGB"), (W, H), 0.48).filter(ImageFilter.GaussianBlur(26))
    result = ImageEnhance.Brightness(background).enhance(0.30).convert("RGBA")
    result.alpha_composite(photo, (0, 275))
    dark = ImageDraw.Draw(result)
    dark.rectangle((0, 0, W, 280), fill=(2, 13, 19, 220))
    dark.rounded_rectangle((55, 1150, 1025, 1740), 42, fill=(2, 13, 19, 235), outline=(0, 215, 185), width=4)
    mark = "TVDUASRODAS"
    mark_face = font(47, True)
    mark_box = dark.textbbox((0, 0), mark, font=mark_face)
    dark.text(((W - (mark_box[2] - mark_box[0])) // 2, 83), mark, font=mark_face, fill=(235, 255, 252))
    badge_face = font(29, True)
    badge_box = dark.textbbox((0, 0), eyebrow, font=badge_face)
    badge_width = badge_box[2] - badge_box[0] + 58
    dark.rounded_rectangle(((W - badge_width) // 2, 203, (W + badge_width) // 2, 260), 28, fill=(0, 215, 185))
    dark.text(((W - (badge_box[2] - badge_box[0])) // 2, 214), eyebrow, font=badge_face, fill=(0, 27, 30))
    y = centered(dark, headline, 1230, 66, width=850)
    dark.rounded_rectangle((410, y + 8, 670, y + 17), 5, fill=(0, 215, 185))
    centered(dark, detail, y + 46, 35, (210, 240, 238), 830)
    dark.text((54, 1803), credit, font=font(22), fill=(203, 215, 215))
    return result


def audio(path: Path, duration: float) -> None:
    samples = int(RATE * duration)
    t = np.arange(samples) / RATE
    waveform = np.zeros(samples)
    chords = ((110, 165, 220), (98, 147, 196), (87, 131, 175), (123, 185, 247))
    for i, start in enumerate(np.arange(0, duration, 2.0)):
        mask = (t >= start) & (t < min(start + 2.0, duration))
        local = t[mask] - start
        chord = chords[i % len(chords)]
        waveform[mask] += sum(np.sin(2 * math.pi * freq * local) for freq in chord) / len(chord) * 0.13
    for start in np.arange(0, duration, 0.5):
        position = int(start * RATE)
        local = np.arange(min(int(.16 * RATE), samples - position)) / RATE
        waveform[position:position + len(local)] += np.sin(2 * math.pi * (76 - 35 * local) * local) * np.exp(-24 * local) * .18
    waveform /= max(float(np.max(np.abs(waveform))), 1e-6)
    waveform *= .45
    fade = int(.35 * RATE)
    waveform[:fade] *= np.linspace(0, 1, fade)
    waveform[-fade:] *= np.linspace(1, 0, fade)
    pcm = np.int16(waveform * 32767)
    stereo = np.column_stack((pcm, pcm)).ravel()
    with wave.open(str(path), "wb") as output:
        output.setnchannels(2); output.setsampwidth(2); output.setframerate(RATE); output.writeframes(stereo.tobytes())


def make_video(images: list[Path], output: Path, seconds: float, transitions: bool) -> float:
    track = output.with_suffix(".original-track.wav")
    total = seconds * len(images) - (0.45 * (len(images) - 1) if transitions else 0)
    audio(track, total)
    command = [get_ffmpeg_exe(), "-y"]
    for image in images:
        command += ["-loop", "1", "-t", str(seconds), "-i", str(image)]
    command += ["-i", str(track)]
    if transitions:
        filters = []
        for i in range(len(images)):
            filters.append(f"[{i}:v]scale={W}:{H},zoompan=z='min(zoom+0.0007,1.06)':d={round(seconds*FPS)}:s={W}x{H}:fps={FPS},setsar=1[v{i}]")
        previous = "v0"
        for i in range(1, len(images)):
            label = "out" if i == len(images) - 1 else f"x{i}"
            filters.append(f"[{previous}][v{i}]xfade=transition=fade:duration=0.45:offset={i*(seconds-.45):.2f}[{label}]")
            previous = label
        command += ["-filter_complex", ";".join(filters), "-map", "[out]"]
    else:
        command += ["-map", "0:v"]
    command += ["-map", f"{len(images)}:a", "-t", f"{total:.2f}", "-r", str(FPS), "-c:v", "libx264", "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(output)]
    subprocess.run(command, check=True)
    track.unlink(missing_ok=True)
    return total


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--images", nargs="+", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--badge", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--details", nargs=5, required=True)
    parser.add_argument("--credit", required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    scenes = []
    for i, detail in enumerate(args.details, 1):
        item = canvas(args.images[(i - 1) % len(args.images)], args.badge, args.title if i == 1 else detail.split(" | ")[0], detail.split(" | ")[-1], args.credit)
        path = args.out / f"reel-scene-{i:02d}.jpg"
        item.convert("RGB").save(path, "JPEG", quality=92, optimize=True)
        scenes.append(path)
    (args.out / "reel-cover.jpg").write_bytes(scenes[0].read_bytes())
    story = canvas(args.images[0], args.badge, args.title, "Leia a matéria completa em TVDUASRODAS.COM", args.credit)
    story_poster = args.out / "story-poster.jpg"
    story.convert("RGB").save(story_poster, "JPEG", quality=92, optimize=True)
    story_duration = make_video([story_poster], args.out / "story.mp4", 14.0, False)
    reel_duration = make_video(scenes, args.out / "reel.mp4", 5.0, True)
    print(f"STORY_DURATION={story_duration:.2f}\nREEL_DURATION={reel_duration:.2f}")


if __name__ == "__main__":
    main()
