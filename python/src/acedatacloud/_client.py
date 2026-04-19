"""Top-level client for AceDataCloud SDK."""

from __future__ import annotations

from typing import Any

from acedatacloud._runtime.payment import (
    PaymentHandler,
    SyncPaymentHandler,
)
from acedatacloud._runtime.transport import AsyncTransport, SyncTransport
from acedatacloud.resources.audio import AsyncAudio, Audio
from acedatacloud.resources.chat import AsyncChat, Chat
from acedatacloud.resources.files import AsyncFiles, Files
from acedatacloud.resources.images import AsyncImages, Images
from acedatacloud.resources.openai_compat import AsyncOpenAI, OpenAI
from acedatacloud.resources.platform import AsyncPlatform, Platform
from acedatacloud.resources.search import AsyncSearch, Search
from acedatacloud.resources.tasks import AsyncTasks, Tasks
from acedatacloud.resources.video import AsyncVideo, Video

_API_BASE = "https://api.acedata.cloud"
_PLATFORM_BASE = "https://platform.acedata.cloud"


class AceDataCloud:
    """Synchronous AceDataCloud client."""

    def __init__(
        self,
        api_token: str | None = None,
        *,
        base_url: str = _API_BASE,
        platform_base_url: str = _PLATFORM_BASE,
        timeout: float = 300.0,
        max_retries: int = 2,
        headers: dict[str, str] | None = None,
        payment_handler: SyncPaymentHandler | None = None,
    ) -> None:
        self._transport = SyncTransport(
            api_token=api_token,
            base_url=base_url,
            platform_base_url=platform_base_url,
            timeout=timeout,
            max_retries=max_retries,
            extra_headers=headers or {},
            payment_handler=payment_handler,
        )
        self.chat = Chat(self._transport)
        self.images = Images(self._transport)
        self.audio = Audio(self._transport)
        self.video = Video(self._transport)
        self.search = Search(self._transport)
        self.tasks = Tasks(self._transport)
        self.files = Files(self._transport)
        self.platform = Platform(self._transport)
        self.openai = OpenAI(self._transport)

    def close(self) -> None:
        self._transport.close()

    def __enter__(self) -> AceDataCloud:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()


class AsyncAceDataCloud:
    """Asynchronous AceDataCloud client."""

    def __init__(
        self,
        api_token: str | None = None,
        *,
        base_url: str = _API_BASE,
        platform_base_url: str = _PLATFORM_BASE,
        timeout: float = 300.0,
        max_retries: int = 2,
        headers: dict[str, str] | None = None,
        payment_handler: PaymentHandler | None = None,
    ) -> None:
        self._transport = AsyncTransport(
            api_token=api_token,
            base_url=base_url,
            platform_base_url=platform_base_url,
            timeout=timeout,
            max_retries=max_retries,
            extra_headers=headers or {},
            payment_handler=payment_handler,
        )
        self.chat = AsyncChat(self._transport)
        self.images = AsyncImages(self._transport)
        self.audio = AsyncAudio(self._transport)
        self.video = AsyncVideo(self._transport)
        self.search = AsyncSearch(self._transport)
        self.tasks = AsyncTasks(self._transport)
        self.files = AsyncFiles(self._transport)
        self.platform = AsyncPlatform(self._transport)
        self.openai = AsyncOpenAI(self._transport)

    async def close(self) -> None:
        await self._transport.close()

    async def __aenter__(self) -> AsyncAceDataCloud:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()
