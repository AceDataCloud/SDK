"""OpenAI-compatible facade resources."""

from __future__ import annotations

import json as _json
from collections.abc import Iterator
from typing import Any

from acedatacloud._runtime.transport import _map_error


def _multipart_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


class _Completions:
    """Namespace for openai.chat.completions."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def create(
        self,
        *,
        model: str,
        messages: list[dict[str, Any]],
        stream: bool = False,
        **kwargs: Any,
    ) -> dict[str, Any] | Iterator[dict[str, Any]]:
        body = {"model": model, "messages": messages, **kwargs}
        if stream:
            body["stream"] = True
            return self._stream(body)
        return self._transport.request("POST", "/openai/chat/completions", json=body)

    def _stream(self, body: dict[str, Any]) -> Iterator[dict[str, Any]]:
        for chunk in self._transport.request_stream("POST", "/openai/chat/completions", json=body):
            yield _json.loads(chunk)


class _AsyncCompletions:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def create(
        self,
        *,
        model: str,
        messages: list[dict[str, Any]],
        stream: bool = False,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body = {"model": model, "messages": messages, **kwargs}
        if stream:
            body["stream"] = True
            return self._stream(body)
        return await self._transport.request("POST", "/openai/chat/completions", json=body)

    async def _stream(self, body: dict[str, Any]):
        async for chunk in self._transport.request_stream("POST", "/openai/chat/completions", json=body):
            yield _json.loads(chunk)


class _ChatNamespace:
    def __init__(self, transport: Any) -> None:
        self.completions = _Completions(transport)


class _AsyncChatNamespace:
    def __init__(self, transport: Any) -> None:
        self.completions = _AsyncCompletions(transport)


class _Models:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def list(self) -> dict[str, Any]:
        return self._transport.request("GET", "/openai/models")


class _AsyncModels:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def list(self) -> dict[str, Any]:
        return await self._transport.request("GET", "/openai/models")


class _Responses:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def create(
        self,
        *,
        model: str,
        input: str | list[dict[str, Any]],
        stream: bool = False,
        **kwargs: Any,
    ) -> dict[str, Any] | Iterator[dict[str, Any]]:
        body = {"model": model, "input": input, **kwargs}
        if stream:
            body["stream"] = True
            return self._stream(body)
        return self._transport.request("POST", "/openai/responses", json=body)

    def _stream(self, body: dict[str, Any]) -> Iterator[dict[str, Any]]:
        for chunk in self._transport.request_stream("POST", "/openai/responses", json=body):
            yield _json.loads(chunk)


class _AsyncResponses:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def create(
        self,
        *,
        model: str,
        input: str | list[dict[str, Any]],
        stream: bool = False,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body = {"model": model, "input": input, **kwargs}
        if stream:
            body["stream"] = True
            return self._stream(body)
        return await self._transport.request("POST", "/openai/responses", json=body)

    async def _stream(self, body: dict[str, Any]):
        async for chunk in self._transport.request_stream("POST", "/openai/responses", json=body):
            yield _json.loads(chunk)


class _Images:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def generate(
        self,
        *,
        prompt: str,
        model: str,
        background: str | None = None,
        moderation: str | None = None,
        n: int | None = None,
        output_compression: int | None = None,
        output_format: str | None = None,
        partial_images: int | None = None,
        size: str | None = None,
        quality: str | None = None,
        response_format: str | None = None,
        style: str | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"prompt": prompt, "model": model, **kwargs}
        if background is not None:
            body["background"] = background
        if moderation is not None:
            body["moderation"] = moderation
        if n is not None:
            body["n"] = n
        if output_compression is not None:
            body["output_compression"] = output_compression
        if output_format is not None:
            body["output_format"] = output_format
        if partial_images is not None:
            body["partial_images"] = partial_images
        if size is not None:
            body["size"] = size
        if quality is not None:
            body["quality"] = quality
        if response_format is not None:
            body["response_format"] = response_format
        if style is not None:
            body["style"] = style
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_
        return self._transport.request("POST", "/openai/images/generations", json=body)

    def edit(
        self,
        *,
        image: str | list[str],
        prompt: str,
        model: str | None = None,
        n: int | None = None,
        background: str | None = None,
        input_fidelity: str | None = None,
        mask: str | None = None,
        output_format: str | None = None,
        output_compression: int | None = None,
        partial_images: int | None = None,
        quality: str | None = None,
        size: str | None = None,
        response_format: str | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"image": image, "prompt": prompt, **kwargs}
        if model is not None:
            body["model"] = model
        if n is not None:
            body["n"] = n
        if background is not None:
            body["background"] = background
        if input_fidelity is not None:
            body["input_fidelity"] = input_fidelity
        if mask is not None:
            body["mask"] = mask
        if output_format is not None:
            body["output_format"] = output_format
        if output_compression is not None:
            body["output_compression"] = output_compression
        if partial_images is not None:
            body["partial_images"] = partial_images
        if quality is not None:
            body["quality"] = quality
        if size is not None:
            body["size"] = size
        if response_format is not None:
            body["response_format"] = response_format
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_
        return self._transport.request("POST", "/openai/images/edits", json=body)


class _AsyncImages:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def generate(
        self,
        *,
        prompt: str,
        model: str,
        background: str | None = None,
        moderation: str | None = None,
        n: int | None = None,
        output_compression: int | None = None,
        output_format: str | None = None,
        partial_images: int | None = None,
        size: str | None = None,
        quality: str | None = None,
        response_format: str | None = None,
        style: str | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"prompt": prompt, "model": model, **kwargs}
        if background is not None:
            body["background"] = background
        if moderation is not None:
            body["moderation"] = moderation
        if n is not None:
            body["n"] = n
        if output_compression is not None:
            body["output_compression"] = output_compression
        if output_format is not None:
            body["output_format"] = output_format
        if partial_images is not None:
            body["partial_images"] = partial_images
        if size is not None:
            body["size"] = size
        if quality is not None:
            body["quality"] = quality
        if response_format is not None:
            body["response_format"] = response_format
        if style is not None:
            body["style"] = style
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_
        return await self._transport.request("POST", "/openai/images/generations", json=body)

    async def edit(
        self,
        *,
        image: str | list[str],
        prompt: str,
        model: str | None = None,
        n: int | None = None,
        background: str | None = None,
        input_fidelity: str | None = None,
        mask: str | None = None,
        output_format: str | None = None,
        output_compression: int | None = None,
        partial_images: int | None = None,
        quality: str | None = None,
        size: str | None = None,
        response_format: str | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"image": image, "prompt": prompt, **kwargs}
        if model is not None:
            body["model"] = model
        if n is not None:
            body["n"] = n
        if background is not None:
            body["background"] = background
        if input_fidelity is not None:
            body["input_fidelity"] = input_fidelity
        if mask is not None:
            body["mask"] = mask
        if output_format is not None:
            body["output_format"] = output_format
        if output_compression is not None:
            body["output_compression"] = output_compression
        if partial_images is not None:
            body["partial_images"] = partial_images
        if quality is not None:
            body["quality"] = quality
        if size is not None:
            body["size"] = size
        if response_format is not None:
            body["response_format"] = response_format
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_
        return await self._transport.request("POST", "/openai/images/edits", json=body)


class _Embeddings:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def create(
        self,
        *,
        model: str,
        input: str | list[str],
        encoding_format: str | None = None,
        dimensions: int | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"model": model, "input": input, **kwargs}
        if encoding_format is not None:
            body["encoding_format"] = encoding_format
        if dimensions is not None:
            body["dimensions"] = dimensions
        return self._transport.request("POST", "/openai/embeddings", json=body)


class _AsyncEmbeddings:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def create(
        self,
        *,
        model: str,
        input: str | list[str],
        encoding_format: str | None = None,
        dimensions: int | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"model": model, "input": input, **kwargs}
        if encoding_format is not None:
            body["encoding_format"] = encoding_format
        if dimensions is not None:
            body["dimensions"] = dimensions
        return await self._transport.request("POST", "/openai/embeddings", json=body)


class _Speech:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def create(
        self,
        *,
        input: str,
        model: str | None = None,
        voice: str | None = None,
        response_format: str | None = None,
        speed: float | None = None,
        **kwargs: Any,
    ) -> bytes:
        body: dict[str, Any] = {"input": input, **kwargs}
        if model is not None:
            body["model"] = model
        if voice is not None:
            body["voice"] = voice
        if response_format is not None:
            body["response_format"] = response_format
        if speed is not None:
            body["speed"] = speed
        response = self._transport._client.request(
            "POST",
            f"{self._transport._base_url}/v1/audio/speech",
            json=body,
            headers=self._transport._headers,
            timeout=self._transport._timeout,
        )
        if response.status_code >= 400:
            try:
                error_body = response.json()
            except Exception:
                error_body = {"error": {"code": "unknown", "message": response.text}}
            raise _map_error(response.status_code, error_body)
        return response.content


class _AsyncSpeech:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def create(
        self,
        *,
        input: str,
        model: str | None = None,
        voice: str | None = None,
        response_format: str | None = None,
        speed: float | None = None,
        **kwargs: Any,
    ) -> bytes:
        body: dict[str, Any] = {"input": input, **kwargs}
        if model is not None:
            body["model"] = model
        if voice is not None:
            body["voice"] = voice
        if response_format is not None:
            body["response_format"] = response_format
        if speed is not None:
            body["speed"] = speed
        response = await self._transport._client.request(
            "POST",
            f"{self._transport._base_url}/v1/audio/speech",
            json=body,
            headers=self._transport._headers,
            timeout=self._transport._timeout,
        )
        if response.status_code >= 400:
            try:
                error_body = response.json()
            except Exception:
                error_body = {"error": {"code": "unknown", "message": response.text}}
            raise _map_error(response.status_code, error_body)
        return response.content


class _Transcriptions:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def create(
        self,
        *,
        file: bytes,
        filename: str = "audio",
        model: str | None = None,
        language: str | None = None,
        prompt: str | None = None,
        response_format: str | None = None,
        temperature: float | None = None,
        timestamp_granularities: list[str] | None = None,
        stream: bool | None = None,
        languages: list[str] | None = None,
        keywords: list[str] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any] | str | Iterator[str]:
        data = _transcription_data(
            model=model,
            language=language,
            prompt=prompt,
            response_format=response_format,
            temperature=temperature,
            timestamp_granularities=timestamp_granularities,
            stream=stream,
            languages=languages,
            keywords=keywords,
            extra=kwargs,
        )
        if stream:
            return self._stream(file=file, filename=filename, data=data)
        response = self._transport._client.post(
            f"{self._transport._base_url}/v1/audio/transcriptions",
            files={"file": (filename, file)},
            data=data,
            headers={k: v for k, v in self._transport._headers.items() if k != "content-type"},
            timeout=self._transport._timeout,
        )
        if response.status_code >= 400:
            try:
                error_body = response.json()
            except Exception:
                error_body = {"error": {"code": "unknown", "message": response.text}}
            raise _map_error(response.status_code, error_body)
        if response.headers.get("content-type", "").startswith("text/plain"):
            return response.text
        return response.json()

    def _stream(self, *, file: bytes, filename: str, data: dict[str, Any]) -> Iterator[str]:
        with self._transport._client.stream(
            "POST",
            f"{self._transport._base_url}/v1/audio/transcriptions",
            files={"file": (filename, file)},
            data=data,
            headers={k: v for k, v in self._transport._headers.items() if k != "content-type"},
            timeout=self._transport._timeout,
        ) as response:
            if response.status_code >= 400:
                body_bytes = response.read()
                try:
                    error_body = _json.loads(body_bytes)
                except Exception:
                    error_body = {"error": {"code": "unknown", "message": body_bytes.decode(errors="replace")}}
                raise _map_error(response.status_code, error_body)
            for line in response.iter_lines():
                if line.startswith("data: "):
                    data_line = line[6:]
                    if data_line == "[DONE]":
                        return
                    yield data_line


class _AsyncTranscriptions:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def create(
        self,
        *,
        file: bytes,
        filename: str = "audio",
        model: str | None = None,
        language: str | None = None,
        prompt: str | None = None,
        response_format: str | None = None,
        temperature: float | None = None,
        timestamp_granularities: list[str] | None = None,
        stream: bool | None = None,
        languages: list[str] | None = None,
        keywords: list[str] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any] | str | Any:
        data = _transcription_data(
            model=model,
            language=language,
            prompt=prompt,
            response_format=response_format,
            temperature=temperature,
            timestamp_granularities=timestamp_granularities,
            stream=stream,
            languages=languages,
            keywords=keywords,
            extra=kwargs,
        )
        if stream:
            return self._stream(file=file, filename=filename, data=data)
        response = await self._transport._client.post(
            f"{self._transport._base_url}/v1/audio/transcriptions",
            files={"file": (filename, file)},
            data=data,
            headers={k: v for k, v in self._transport._headers.items() if k != "content-type"},
            timeout=self._transport._timeout,
        )
        if response.status_code >= 400:
            try:
                error_body = response.json()
            except Exception:
                error_body = {"error": {"code": "unknown", "message": response.text}}
            raise _map_error(response.status_code, error_body)
        if response.headers.get("content-type", "").startswith("text/plain"):
            return response.text
        return response.json()

    async def _stream(self, *, file: bytes, filename: str, data: dict[str, Any]):
        async with self._transport._client.stream(
            "POST",
            f"{self._transport._base_url}/v1/audio/transcriptions",
            files={"file": (filename, file)},
            data=data,
            headers={k: v for k, v in self._transport._headers.items() if k != "content-type"},
            timeout=self._transport._timeout,
        ) as response:
            if response.status_code >= 400:
                body_bytes = await response.aread()
                try:
                    error_body = _json.loads(body_bytes)
                except Exception:
                    error_body = {"error": {"code": "unknown", "message": body_bytes.decode(errors="replace")}}
                raise _map_error(response.status_code, error_body)
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data_line = line[6:]
                    if data_line == "[DONE]":
                        return
                    yield data_line


def _transcription_data(
    *,
    model: str | None,
    language: str | None,
    prompt: str | None,
    response_format: str | None,
    temperature: float | None,
    timestamp_granularities: list[str] | None,
    stream: bool | None,
    languages: list[str] | None,
    keywords: list[str] | None,
    extra: dict[str, Any],
) -> dict[str, Any]:
    data: dict[str, Any] = {key: _multipart_value(value) for key, value in extra.items()}
    if model is not None:
        data["model"] = model
    if language is not None:
        data["language"] = language
    if prompt is not None:
        data["prompt"] = prompt
    if response_format is not None:
        data["response_format"] = response_format
    if temperature is not None:
        data["temperature"] = _multipart_value(temperature)
    if stream is not None:
        data["stream"] = _multipart_value(stream)
    if timestamp_granularities is not None:
        data["timestamp_granularities[]"] = [_multipart_value(item) for item in timestamp_granularities]
    if languages is not None:
        data["languages[]"] = [_multipart_value(item) for item in languages]
    if keywords is not None:
        data["keywords[]"] = [_multipart_value(item) for item in keywords]
    return data


class _Audio:
    def __init__(self, transport: Any) -> None:
        self.speech = _Speech(transport)
        self.transcriptions = _Transcriptions(transport)


class _AsyncAudio:
    def __init__(self, transport: Any) -> None:
        self.speech = _AsyncSpeech(transport)
        self.transcriptions = _AsyncTranscriptions(transport)


class _Realtime:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def connect(self) -> dict[str, Any]:
        return self._transport.request("GET", "/v1/realtime")


class _AsyncRealtime:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def connect(self) -> dict[str, Any]:
        return await self._transport.request("GET", "/v1/realtime")


class _Tasks:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def retrieve(
        self,
        *,
        id: str | None = None,
        trace_id: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"action": "retrieve", **kwargs}
        if id is not None:
            body["id"] = id
        if trace_id is not None:
            body["trace_id"] = trace_id
        return self._transport.request("POST", "/openai/tasks", json=body)

    def retrieve_batch(
        self,
        *,
        ids: list[str] | None = None,
        trace_ids: list[str] | None = None,
        application_id: str | None = None,
        user_id: str | None = None,
        type: str | None = None,
        offset: int | None = None,
        limit: int | None = None,
        created_at_min: float | None = None,
        created_at_max: float | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"action": "retrieve_batch", **kwargs}
        if ids is not None:
            body["ids"] = ids
        if trace_ids is not None:
            body["trace_ids"] = trace_ids
        if application_id is not None:
            body["application_id"] = application_id
        if user_id is not None:
            body["user_id"] = user_id
        if type is not None:
            body["type"] = type
        if offset is not None:
            body["offset"] = offset
        if limit is not None:
            body["limit"] = limit
        if created_at_min is not None:
            body["created_at_min"] = created_at_min
        if created_at_max is not None:
            body["created_at_max"] = created_at_max
        return self._transport.request("POST", "/openai/tasks", json=body)


class _AsyncTasks:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def retrieve(
        self,
        *,
        id: str | None = None,
        trace_id: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"action": "retrieve", **kwargs}
        if id is not None:
            body["id"] = id
        if trace_id is not None:
            body["trace_id"] = trace_id
        return await self._transport.request("POST", "/openai/tasks", json=body)

    async def retrieve_batch(
        self,
        *,
        ids: list[str] | None = None,
        trace_ids: list[str] | None = None,
        application_id: str | None = None,
        user_id: str | None = None,
        type: str | None = None,
        offset: int | None = None,
        limit: int | None = None,
        created_at_min: float | None = None,
        created_at_max: float | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"action": "retrieve_batch", **kwargs}
        if ids is not None:
            body["ids"] = ids
        if trace_ids is not None:
            body["trace_ids"] = trace_ids
        if application_id is not None:
            body["application_id"] = application_id
        if user_id is not None:
            body["user_id"] = user_id
        if type is not None:
            body["type"] = type
        if offset is not None:
            body["offset"] = offset
        if limit is not None:
            body["limit"] = limit
        if created_at_min is not None:
            body["created_at_min"] = created_at_min
        if created_at_max is not None:
            body["created_at_max"] = created_at_max
        return await self._transport.request("POST", "/openai/tasks", json=body)


class OpenAI:
    """Synchronous OpenAI-compatible facade."""

    def __init__(self, transport: Any) -> None:
        self.chat = _ChatNamespace(transport)
        self.models = _Models(transport)
        self.responses = _Responses(transport)
        self.images = _Images(transport)
        self.embeddings = _Embeddings(transport)
        self.audio = _Audio(transport)
        self.realtime = _Realtime(transport)
        self.tasks = _Tasks(transport)


class AsyncOpenAI:
    """Async OpenAI-compatible facade."""

    def __init__(self, transport: Any) -> None:
        self.chat = _AsyncChatNamespace(transport)
        self.models = _AsyncModels(transport)
        self.responses = _AsyncResponses(transport)
        self.images = _AsyncImages(transport)
        self.embeddings = _AsyncEmbeddings(transport)
        self.audio = _AsyncAudio(transport)
        self.realtime = _AsyncRealtime(transport)
        self.tasks = _AsyncTasks(transport)
