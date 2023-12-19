from __future__ import annotations

import base64
import io
import os
import sys
from pathlib import Path
from typing import Any, Callable, Dict, List, Literal, Optional, cast, overload

import attr
import sentry_sdk
import tiktoken
from dotenv import load_dotenv
from openai import APIConnectionError, AsyncOpenAI, AsyncStream, AuthenticationError
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionChunk,
    ChatCompletionContentPartParam,
    ChatCompletionMessageParam,
)
from openai.types.chat.completion_create_params import ResponseFormat
from PIL import Image

from mentat.errors import MentatError, UserError
from mentat.session_context import SESSION_CONTEXT
from mentat.utils import mentat_dir_path


def is_test_environment():
    """Returns True if in pytest and not benchmarks"""
    benchmarks_running = os.getenv("MENTAT_BENCHMARKS_RUNNING")
    return (
        "PYTEST_CURRENT_TEST" in os.environ
        and "--benchmark" not in sys.argv
        and (not bool(benchmarks_running) or benchmarks_running == "false")
    )


def api_guard(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator that should be used on any function that calls the OpenAI API

    It does two things:
    1. Raises if the function is called in tests (that aren't benchmarks)
    2. Converts APIConnectionErrors to MentatErrors
    """

    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        assert (
            not is_test_environment()
        ), "OpenAI call attempted in non-benchmark test environment!"
        try:
            return await func(*args, **kwargs)
        except APIConnectionError:
            raise MentatError(
                "API connection error: please check your internet connection and try"
                " again."
            )

    return wrapper


# Ensures that each chunk will have at most one newline character
def chunk_to_lines(chunk: ChatCompletionChunk) -> list[str]:
    content = chunk.choices[0].delta.content
    return ("" if content is None else content).splitlines(keepends=True)


def count_tokens(message: str, model: str, full_message: bool) -> int:
    """
    Calculates the tokens in this message. Will NOT be accurate for a full prompt!
    Use prompt_tokens to get the exact amount of tokens for a prompt.
    If full_message is true, will include the extra 4 tokens used in a chat completion by this message
    if this message is part of a prompt. You do NOT want full_message to be true for a response.
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(message, disallowed_special=())) + (
        4 if full_message else 0
    )


def prompt_tokens(messages: list[ChatCompletionMessageParam], model: str):
    """
    Returns the number of tokens used by a prompt if it was sent to OpenAI for a chat completion.
    Adapted from https://platform.openai.com/docs/guides/text-generation/managing-tokens
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")

    num_tokens = 0
    for message in messages:
        # every message follows <|start|>{role/name}\n{content}<|end|>\n
        # this has 5 tokens (start token, role, \n, end token, \n), but we count the role token later
        num_tokens += 4
        for key, value in message.items():
            if isinstance(value, list) and key == "content":
                value = cast(List[ChatCompletionContentPartParam], value)
                for entry in value:
                    if entry["type"] == "text":
                        num_tokens += len(encoding.encode(entry["text"]))
                    if entry["type"] == "image_url":
                        image_base64: str = entry["image_url"]["url"].split(",")[1]
                        image_bytes: bytes = base64.b64decode(image_base64)
                        image = Image.open(io.BytesIO(image_bytes))
                        size = image.size
                        # As described here: https://platform.openai.com/docs/guides/vision/calculating-costs
                        scale = min(1, 2048 / max(size))
                        size = (int(size[0] * scale), int(size[1] * scale))
                        scale = min(1, 768 / min(size))
                        size = (int(size[0] * scale), int(size[1] * scale))
                        num_tokens += 85 + 170 * ((size[0] + 511) // 512) * (
                            (size[1] + 511) // 512
                        )
            elif isinstance(value, str):
                num_tokens += len(encoding.encode(value))
            if key == "name":  # if there's a name, the role is omitted
                num_tokens -= 1  # role is always required and always 1 token
    num_tokens += 2  # every reply is primed with <|start|>assistant
    return num_tokens


@attr.define
class Model:
    name: str = attr.field()
    context_size: int = attr.field()
    input_cost: float = attr.field()
    output_cost: float = attr.field()
    embedding_model: bool = attr.field(default=False)


known_models: Dict[str, Model] = {
    "gpt-4-1106-preview": Model("gpt-4-1106-preview", 128000, 0.01, 0.03),
    "gpt-4-vision-preview": Model("gpt-4-vision-preview", 128000, 0.01, 0.03),
    "gpt-4": Model("gpt-4", 8192, 0.03, 0.06),
    "gpt-4-32k": Model("gpt-4-32k", 32768, 0.06, 0.12),
    "gpt-4-0613": Model("gpt-4-0613", 8192, 0.03, 0.06),
    "gpt-4-32k-0613": Model("gpt-4-32k-0613", 32768, 0.06, 0.12),
    "gpt-4-0314": Model("gpt-4-0314", 8192, 0.03, 0.06),
    "gpt-4-32k-0314": Model("gpt-4-32k-0314", 32768, 0.06, 0.12),
    "gpt-3.5-turbo-1106": Model("gpt-3.5-turbo-1106", 16385, 0.001, 0.002),
    "gpt-3.5-turbo": Model("gpt-3.5-turbo", 16385, 0.001, 0.002),
    "gpt-3.5-turbo-0613": Model("gpt-3.5-turbo-0613", 4096, 0.0015, 0.002),
    "gpt-3.5-turbo-16k-0613": Model("gpt-3.5-turbo-16k-0613", 16385, 0.003, 0.004),
    "gpt-3.5-turbo-0301": Model("gpt-3.5-turbo-0301", 4096, 0.0015, 0.002),
    "text-embedding-ada-002": Model(
        "text-embedding-ada-002", 8191, 0.0001, 0, embedding_model=True
    ),
}


def model_context_size(model: str) -> Optional[int]:
    if model not in known_models:
        return None
    else:
        return known_models[model].context_size


def model_price_per_1000_tokens(model: str) -> Optional[tuple[float, float]]:
    """Returns (input, output) cost per 1000 tokens in USD"""
    if model not in known_models:
        return None
    else:
        return known_models[model].input_cost, known_models[model].output_cost


def get_max_tokens() -> Optional[int]:
    session_context = SESSION_CONTEXT.get()
    config = session_context.config

    context_size = model_context_size(config.model)
    maximum_context = config.maximum_context
    if maximum_context is not None:
        if context_size:
            return min(context_size, maximum_context)
        else:
            return maximum_context
    else:
        return context_size


class LlmApiHandler:
    """Used for any functions that require calling the external LLM API"""

    def initialize_client(self):
        if not load_dotenv(mentat_dir_path / ".env"):
            load_dotenv()
        key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("OPENAI_API_BASE")
        if not key:
            raise UserError(
                "No OpenAI api key detected.\nEither place your key into a .env"
                " file or export it as an environment variable."
            )

        # We don't have any use for a synchronous client, but if we ever do we can easily make it here
        self.async_client = AsyncOpenAI(api_key=key, base_url=base_url)
        try:
            self.async_client.api_key = key
            self.async_client.models.list()  # Test the key
        except AuthenticationError as e:
            raise UserError(f"OpenAI gave an Authentication Error:\n{e}")

    @overload
    async def call_llm_api(
        self,
        messages: list[ChatCompletionMessageParam],
        model: str,
        stream: Literal[True],
        response_format: ResponseFormat = ResponseFormat(type="text"),
    ) -> AsyncStream[ChatCompletionChunk]: ...

    @overload
    async def call_llm_api(
        self,
        messages: list[ChatCompletionMessageParam],
        model: str,
        stream: Literal[False],
        response_format: ResponseFormat = ResponseFormat(type="text"),
    ) -> ChatCompletion: ...

    @api_guard
    async def call_llm_api(
        self,
        messages: list[ChatCompletionMessageParam],
        model: str,
        stream: bool,
        response_format: ResponseFormat = ResponseFormat(type="text"),
    ) -> ChatCompletion | AsyncStream[ChatCompletionChunk]:
        session_context = SESSION_CONTEXT.get()
        config = session_context.config

        with sentry_sdk.start_span(description="LLM Call") as span:
            span.set_tag("model", model)
            # OpenAI's API is bugged; when gpt-4-vision-preview is used, including the response format
            # at all returns a 400 error. Additionally, gpt-4-vision-preview has a max response of 30 tokens by default.
            # Until this is fixed, we have to use this workaround.
            if model == "gpt-4-vision-preview":
                response = await self.async_client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=config.temperature,
                    stream=stream,
                    max_tokens=4096,
                )
            else:
                response = await self.async_client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=config.temperature,
                    stream=stream,
                    response_format=response_format,
                )

        return response

    @api_guard
    async def call_embedding_api(
        self, input_texts: list[str], model: str = "text-embedding-ada-002"
    ) -> list[list[float]]:
        response = await self.async_client.embeddings.create(
            input=input_texts, model=model
        )
        return [embedding.embedding for embedding in response.data]

    @api_guard
    async def is_model_available(self, model: str) -> bool:
        available_models: list[str] = [
            model.id async for model in self.async_client.models.list()
        ]
        return model in available_models

    @api_guard
    async def call_whisper_api(self, audio_path: Path) -> str:
        audio_file = open(audio_path, "rb")
        transcript = await self.async_client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
        )
        return transcript.text
