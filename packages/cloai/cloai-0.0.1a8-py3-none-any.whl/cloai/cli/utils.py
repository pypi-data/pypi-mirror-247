"""Contains the core business logic of the OpenAI CLI."""
from __future__ import annotations

import math
import pathlib
import uuid
from typing import TYPE_CHECKING

import ffmpeg
import requests

from cloai.core import config

if TYPE_CHECKING:
    from collections.abc import Generator

logger = config.get_logger()


def clip_audio(
    filename: str | pathlib.Path,
    out_dir: str | pathlib.Path,
    target_size: int,
) -> Generator[pathlib.Path, None, None]:
    """Clips the file to the maximum size.

    Args:
        filename: The file to clip.
        out_dir: The directory to save the clipped files to.
        target_size: The target size of the clipped files.
    """
    logger.warning(
        "File too large. Clipping may lead to inaccurate results around the clips.",
    )

    file_size = get_file_size(filename)
    n_files = (file_size // target_size) + 1
    file_duration = get_audio_duration(filename)
    clip_duration = math.ceil(file_duration / n_files)

    uuid_id = uuid.uuid4()
    output_file_pattern = pathlib.Path(out_dir) / f"audio_{uuid_id}_%03d.mp3"
    stream = (
        ffmpeg.input(str(filename))
        .output(
            str(output_file_pattern),
            f="segment",
            segment_time=clip_duration,
        )
        .overwrite_output()
    )

    logger.warning("Running ffmpeg: %s", " ".join(stream.compile()))
    stream.run()

    files = list(pathlib.Path(out_dir).glob(f"*{uuid_id}*.mp3"))
    files.sort()
    yield from files


def download_file(filename: str | pathlib.Path, url: str) -> None:
    """Downloads a file from a URL.

    Args:
        filename: The name of the file to download.
        url: The URL to download the file from.
    """
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    with pathlib.Path(filename).open("wb") as file:
        file.write(response.content)


def get_audio_duration(filename: str | pathlib.Path) -> float:
    """Gets the duration of the audio file.

    Args:
        filename: The name of the audio file.

    Returns:
        float: The duration of the audio file.
    """
    probe = ffmpeg.probe(filename)
    return float(probe["format"]["duration"])


def get_file_size(filename: str | pathlib.Path) -> int:
    """Gets the size of the file.

    Args:
        filename: The name of the file.

    Returns:
        int: The size of the file.
    """
    return pathlib.Path(filename).stat().st_size
