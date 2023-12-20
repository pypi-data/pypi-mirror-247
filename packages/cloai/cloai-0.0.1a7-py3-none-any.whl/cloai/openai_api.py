"""This module contains interactions with OpenAI models."""
from __future__ import annotations

import abc
import logging
import pathlib
from typing import Any, Literal, TypedDict

import openai

from cloai.core import config

settings = config.get_settings()
OPENAI_API_KEY = settings.OPENAI_API_KEY
LOGGER_NAME = settings.LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)


class Message(TypedDict):
    """A message object."""

    role: Literal["assistant", "system", "user"]
    content: str


class OpenAIBaseClass(abc.ABC):
    """An abstract base class for OpenAI models.

    This class initializes the OpenAI client and requires a run method to be
    implemented.

    Attributes:
        client: The OpenAI client used to interact with the model.
    """

    def __init__(self) -> None:
        """Initializes a new instance of the OpenAIBaseClass class."""
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY.get_secret_value())

    @abc.abstractmethod
    async def run(self, *_args: Any, **_kwargs: Any) -> Any:  # noqa: ANN401
        """Runs the model."""
        ...


class TextToSpeech(OpenAIBaseClass):
    """A class for running the Text-To-Speech models."""

    async def run(
        self,
        text: str,
        output_file: pathlib.Path | str,
        model: str = "tts-1",
        voice: Literal["alloy", "echo", "fable", "onyx", "nova", "shimmer"] = "onyx",
    ) -> None:
        """Runs the Text-To-Speech model.

        Args:
            text: The text to convert to speech.
            output_file: The name of the output file.
            model: The name of the Text-To-Speech model to use.
            voice: The voice to use.

        Returns:
            The model's response.
        """
        response = self.client.audio.speech.create(
            model=model,
            voice=voice,
            input=text,
        )
        response.stream_to_file(output_file)


class SpeechToText(OpenAIBaseClass):
    """A class for running the Speech-To-Text models."""

    async def run(
        self,
        audio_file: pathlib.Path | str,
        model: str = "whisper-1",
    ) -> str:
        """Runs the Speech-To-Text model.

        Args:
            audio_file: The audio to convert to text.
            model: The name of the Speech-To-Text model to use.

        Returns:
            The model's response.
        """
        with pathlib.Path(audio_file).open("rb") as audio:
            return self.client.audio.transcriptions.create(
                model=model,
                file=audio,
                response_format="text",
            )  # type: ignore[return-value] # response_format overrides output type.


class ImageGeneration(OpenAIBaseClass):
    """A class for running the Image Generation models."""

    async def run(  # noqa: PLR0913
        self,
        prompt: str,
        model: str = "dall-e-3",
        size: Literal["256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"]
        | None = None,
        quality: Literal["standard", "hd"] = "standard",
        n: int | None = None,
    ) -> list[str | None]:
        """Runs the Image Generation model.

        Args:
            prompt: The prompt to generate an image from.
            model: The name of the Image Generation model to use.
            size: The size of the generated image.
            quality: The quality of the generated image.
            n: The number of images to generate.

        Returns:
            str: The image urls.
        """
        response = self.client.images.generate(
            model=model,
            prompt=prompt,
            size=size,
            quality=quality,
            n=n,
        )

        return [data.url for data in response.data]
