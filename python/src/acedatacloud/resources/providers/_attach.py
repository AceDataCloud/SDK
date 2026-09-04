"""Provider-axis attachment — generated, do not edit by hand.

Kept as a mixin rather than inlined into ``_client.py`` so the generator never
has to rewrite a hand-maintained file: adding a service touches only this
module, and the client just calls ``_attach_providers``.
"""

from __future__ import annotations

from typing import Any

from .digitalhuman import AsyncDigitalhuman, Digitalhuman
from .dreamina import AsyncDreamina, Dreamina
from .fish import AsyncFish, Fish
from .flux import AsyncFlux, Flux
from .gemini import AsyncGemini, Gemini
from .hailuo import AsyncHailuo, Hailuo
from .happyhorse import AsyncHappyhorse, Happyhorse
from .localization import AsyncLocalization, Localization
from .luma import AsyncLuma, Luma
from .maestro import AsyncMaestro, Maestro
from .minimax import AsyncMinimax, Minimax
from .nano_banana import AsyncNanoBanana, NanoBanana
from .producer import AsyncProducer, Producer
from .qwen_image import AsyncQwenImage, QwenImage
from .seedance import AsyncSeedance, Seedance
from .seedream import AsyncSeedream, Seedream
from .suno import AsyncSuno, Suno
from .wan import AsyncWan, Wan


def attach(client: Any, transport: Any, *, is_async: bool) -> None:
    """Bind every generated provider client onto ``client``."""
    if is_async:
        client.digitalhuman = AsyncDigitalhuman(transport)
        client.dreamina = AsyncDreamina(transport)
        client.fish = AsyncFish(transport)
        client.flux = AsyncFlux(transport)
        client.gemini = AsyncGemini(transport)
        client.hailuo = AsyncHailuo(transport)
        client.happyhorse = AsyncHappyhorse(transport)
        client.localization = AsyncLocalization(transport)
        client.luma = AsyncLuma(transport)
        client.maestro = AsyncMaestro(transport)
        client.minimax = AsyncMinimax(transport)
        client.nano_banana = AsyncNanoBanana(transport)
        client.producer = AsyncProducer(transport)
        client.qwen_image = AsyncQwenImage(transport)
        client.seedance = AsyncSeedance(transport)
        client.seedream = AsyncSeedream(transport)
        client.suno = AsyncSuno(transport)
        client.wan = AsyncWan(transport)
    else:
        client.digitalhuman = Digitalhuman(transport)
        client.dreamina = Dreamina(transport)
        client.fish = Fish(transport)
        client.flux = Flux(transport)
        client.gemini = Gemini(transport)
        client.hailuo = Hailuo(transport)
        client.happyhorse = Happyhorse(transport)
        client.localization = Localization(transport)
        client.luma = Luma(transport)
        client.maestro = Maestro(transport)
        client.minimax = Minimax(transport)
        client.nano_banana = NanoBanana(transport)
        client.producer = Producer(transport)
        client.qwen_image = QwenImage(transport)
        client.seedance = Seedance(transport)
        client.seedream = Seedream(transport)
        client.suno = Suno(transport)
        client.wan = Wan(transport)
