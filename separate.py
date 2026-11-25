"""Normalize media and split it with a local Spleeter executable."""

import argparse
from pathlib import Path
import shutil
import subprocess
from tempfile import TemporaryDirectory
import wave


LIMIT_SECONDS = 600


def split(source, output, engine, ffmpeg):
    source, output, engine = source.resolve(), output.resolve(), engine.resolve()
    if not source.is_file() or not engine.is_file():
        raise ValueError("Check the input file and the path to Spleeter.exe.")
    if output.exists():
        raise ValueError("Choose a new output directory.")
    with TemporaryDirectory(prefix="spleeter-local-") as temp:
        track = Path(temp) / "track.wav"
        subprocess.run([
            ffmpeg, "-nostdin", "-v", "error", "-xerror",
            "-protocol_whitelist", "file,pipe",
            "-format_whitelist",
            "aac,aiff,amr,asf,avi,caf,flac,flv,matroska,webm,mov,mp4,m4a,3gp,3g2,mj2,mp3,ogg,wav",
            "-i", str(source), "-map", "0:a:0", "-t", str(LIMIT_SECONDS + 1),
            "-ac", "2", "-ar", "44100", "-c:a", "pcm_s16le", str(track),
        ], check=True, timeout=120)
        with wave.open(str(track)) as audio:
            length = audio.getnframes() / audio.getframerate()
        if not 0 < length <= LIMIT_SECONDS:
            raise ValueError("Expected a readable audio track up to 10 minutes long.")
        subprocess.run([str(engine), "-m", "2stems", str(track)], check=True, timeout=480)
        names = {"vocals": ("vocals", "人声"), "accompaniment": ("accompaniment", "伴奏")}
        results = {}
        for role, names_on_disk in names.items():
            for name in names_on_disk:
                candidate = track.with_suffix(f".{name}.wav")
                if candidate.is_file():
                    with wave.open(str(candidate)) as audio:
                        if abs(audio.getnframes() / audio.getframerate() - length) <= 0.5:
                            results[role] = candidate
                            break
            if role not in results:
                raise ValueError(f"Spleeter did not produce a valid {role} track.")
        output.mkdir(parents=True, exist_ok=False)
        for role, candidate in results.items():
            shutil.copyfile(candidate, output / f"{role}.wav")
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, required=True, help="A new output directory")
    parser.add_argument("--spleeter", type=Path, required=True, help="Path to Spleeter.exe")
    parser.add_argument("--ffmpeg", default="ffmpeg", help="FFmpeg executable or command")
    args = parser.parse_args()
    try:
        print(split(args.source, args.output, args.spleeter, args.ffmpeg))
    except (OSError, ValueError, EOFError, wave.Error, subprocess.SubprocessError) as error:
        parser.exit(1, f"Separation failed: {error}\n")


if __name__ == "__main__":
    main()
