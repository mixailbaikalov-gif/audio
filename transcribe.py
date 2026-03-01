#!/usr/bin/env python3
"""CLI tool to transcribe audio files into text using OpenAI Audio Transcriptions API."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import TYPE_CHECKING, Iterable

if TYPE_CHECKING:
    from openai import OpenAI

AUDIO_EXTENSIONS = {
    ".mp3",
    ".wav",
    ".m4a",
    ".mp4",
    ".mpeg",
    ".mpga",
    ".webm",
    ".ogg",
    ".flac",
}


def find_audio_files(path: Path) -> Iterable[Path]:
    if path.is_file():
        if path.suffix.lower() not in AUDIO_EXTENSIONS:
            raise ValueError(f"Unsupported audio extension: {path.suffix}")
        return [path]

    if not path.exists():
        raise FileNotFoundError(f"Path does not exist: {path}")

    files = sorted(
        p for p in path.rglob("*") if p.is_file() and p.suffix.lower() in AUDIO_EXTENSIONS
    )
    if not files:
        raise FileNotFoundError(f"No audio files found in directory: {path}")

    return files


def transcribe_file(
    client: "OpenAI",
    audio_path: Path,
    output_path: Path,
    model: str,
    language: str | None,
    prompt: str | None,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with audio_path.open("rb") as audio_file:
        response = client.audio.transcriptions.create(
            model=model,
            file=audio_file,
            language=language,
            prompt=prompt,
        )

    output_path.write_text(response.text.strip() + "\n", encoding="utf-8")


def target_output_path(audio_path: Path, input_root: Path, output_root: Path | None) -> Path:
    if output_root is None:
        return audio_path.with_suffix(".txt")

    if input_root.is_file():
        return output_root / (audio_path.stem + ".txt")

    relative = audio_path.relative_to(input_root)
    return (output_root / relative).with_suffix(".txt")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Transcribe one audio file or all audio files in a directory into .txt files"
    )
    parser.add_argument("input", type=Path, help="Path to audio file or folder with audio files")
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=None,
        help="Directory for output .txt files (default: next to source audio)",
    )
    parser.add_argument(
        "-m",
        "--model",
        default="gpt-4o-mini-transcribe",
        help="Transcription model name (default: gpt-4o-mini-transcribe)",
    )
    parser.add_argument(
        "-l",
        "--language",
        default=None,
        help="Language hint in ISO-639-1 format, e.g. ru, en",
    )
    parser.add_argument(
        "-p",
        "--prompt",
        default=None,
        help="Optional prompt/instruction to improve transcription quality",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source_path = args.input.resolve()

    audio_files = find_audio_files(source_path)
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise SystemExit(
            "Package 'openai' is not installed. Install it first: pip install openai"
        ) from exc

    client = OpenAI()

    for audio_file in audio_files:
        destination = target_output_path(audio_file, source_path, args.output_dir)
        print(f"Transcribing: {audio_file} -> {destination}")
        transcribe_file(
            client=client,
            audio_path=audio_file,
            output_path=destination,
            model=args.model,
            language=args.language,
            prompt=args.prompt,
        )

    print(f"Done. Transcribed {len(audio_files)} file(s).")


if __name__ == "__main__":
    main()
