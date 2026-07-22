from __future__ import annotations

import argparse
import math
import subprocess
import wave
from pathlib import Path

import numpy as np
from imageio_ffmpeg import get_ffmpeg_exe


SAMPLE_RATE = 44_100
DURATION = 15.0


def synthesize_original_track(output: Path) -> None:
    """Create a short, original electronic instrumental loop."""
    count = int(SAMPLE_RATE * DURATION)
    t = np.arange(count, dtype=np.float64) / SAMPLE_RATE
    audio = np.zeros(count, dtype=np.float64)

    # Original four-chord pad and bass progression at 120 BPM.
    chords = ((110.00, 164.81, 220.00), (87.31, 130.81, 174.61),
              (98.00, 146.83, 196.00), (82.41, 123.47, 164.81))
    bar = 2.0
    for index, chord in enumerate(chords * 2):
        start = index * bar
        if start >= DURATION:
            break
        mask = (t >= start) & (t < min(start + bar, DURATION))
        local = t[mask] - start
        envelope = np.minimum(local / 0.18, 1.0) * np.minimum((bar - local) / 0.25, 1.0)
        pad = sum(np.sin(2 * math.pi * frequency * local) for frequency in chord) / len(chord)
        bass = np.sin(2 * math.pi * (chord[0] / 2) * local)
        audio[mask] += envelope * (0.16 * pad + 0.10 * bass)

    # Soft kick, clap and hi-hat pattern, synthesized from noise and sine waves.
    rng = np.random.default_rng(20260722)
    for beat in np.arange(0, DURATION, 0.5):
        start = int(beat * SAMPLE_RATE)
        length = min(int(0.18 * SAMPLE_RATE), count - start)
        local = np.arange(length) / SAMPLE_RATE
        kick = np.sin(2 * math.pi * (72 - 35 * local) * local) * np.exp(-24 * local)
        audio[start:start + length] += 0.22 * kick
    for beat in np.arange(0.25, DURATION, 0.25):
        start = int(beat * SAMPLE_RATE)
        length = min(int(0.045 * SAMPLE_RATE), count - start)
        local = np.arange(length) / SAMPLE_RATE
        hat = rng.normal(0, 1, length) * np.exp(-70 * local)
        audio[start:start + length] += 0.035 * hat

    fade = int(0.35 * SAMPLE_RATE)
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    wav_path = args.output.with_suffix(".original-track.wav")
    synthesize_original_track(wav_path)
    command = [
        get_ffmpeg_exe(), "-y", "-loop", "1", "-i", str(args.image),
        "-i", str(wav_path), "-t", str(DURATION), "-r", "30",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
        "-ar", str(SAMPLE_RATE), "-movflags", "+faststart", str(args.output),
    ]
    subprocess.run(command, check=True)
    wav_path.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
