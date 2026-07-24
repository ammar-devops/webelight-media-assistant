import os
import subprocess
from pathlib import Path

from app.core.config import settings


def extract_audio(video_path: str) -> str:
    """
    Extract audio from a video file and save it as WAV.

    Args:
        video_path (str): Path to input video

    Returns:
        str: Path to extracted WAV file
    """

    output_dir = Path(settings.OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)

    input_path = Path(video_path)

    output_file = output_dir / f"{input_path.stem}.wav"

    command = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_path),
        "-vn",
        "-acodec",
        "pcm_s16le",
        "-ar",
        "16000",
        "-ac",
        "1",
        str(output_file),
    ]

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"FFmpeg failed:\n{result.stderr}"
        )

    if not output_file.exists():
        raise FileNotFoundError("Audio extraction failed.")

    return str(output_file)


def is_ffmpeg_installed() -> bool:
    """
    Check if FFmpeg is installed.
    """

    try:
        subprocess.run(
            ["ffmpeg", "-version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        return True
    except Exception:
        return False