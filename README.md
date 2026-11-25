# Spleeter Local

A Windows command-line workflow maintained by CacheTide for splitting a local audio file or a video's first audio track into vocals and accompaniment. It wraps Deezer's Spleeter 2-stem model and the SpleeterMsvcExe Windows runner.

## Requirements

- Python 3.10 or later.
- [FFmpeg](https://ffmpeg.org/download.html) accessible on PATH, or supply its executable with --ffmpeg.
- [SpleeterMsvcExe](https://github.com/wudicgi/SpleeterMsvcExe/releases). Keep the executable, its DLLs and its models/2stems directory together. Follow the upstream Windows runtime instructions if a DLL is missing.

## Usage

~~~powershell
python separate.py "song or video.mp4" --spleeter "C:/tools/spleeter/Spleeter.exe" --output "stems"
~~~

This creates stems/vocals.wav and stems/accompaniment.wav. Both files are stereo 44.1 kHz PCM WAV. The output directory must be new. FFmpeg validates and normalizes the first audio stream before Spleeter runs. A file without audio produces an error before inference. Clips of up to ten minutes are supported.

Common inputs include WAV, MP3, FLAC, M4A, AAC, Ogg/Opus, MP4, MOV, MKV and WebM when the installed FFmpeg can decode the audio stream. All processing happens locally. If the separation sounds rough, stems can contain residual bleed from the other track.

## Lineage and distribution

The desktop copy that prompted this project is a self-extracting archive containing a localized SpleeterMsvcExe binary, TensorFlow and a 2-stem model. This repository publishes the standalone wrapper and usage documentation. Download upstream binaries and model files from their original distributors.

- [Deezer Spleeter](https://github.com/deezer/spleeter), MIT-licensed source.
- [SpleeterMsvcExe](https://github.com/wudicgi/SpleeterMsvcExe), MIT-licensed source.
- [GMN Bot](https://github.com/frostmoon-rui/gmn_bot) has its own QQ adapter and SILK handling.
