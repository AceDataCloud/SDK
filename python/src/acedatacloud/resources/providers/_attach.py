"""Provider-axis attachment — generated, do not edit by hand.

Kept as a mixin rather than inlined into ``_client.py`` so the generator never
has to rewrite a hand-maintained file: adding a service touches only this
module, and the client just calls ``_attach_providers``.
"""

from __future__ import annotations

from typing import Any

from .captcha import AsyncCaptcha, Captcha
from .digitalhuman import AsyncDigitalhuman, Digitalhuman
from .drawai import AsyncDrawAI, DrawAI
from .dreamina import AsyncDreamina, Dreamina
from .fish import AsyncFish, Fish
from .flux import AsyncFlux, Flux
from .gemini import AsyncGemini, Gemini
from .grok import AsyncGrok, Grok
from .hailuo import AsyncHailuo, Hailuo
from .happyhorse import AsyncHappyhorse, Happyhorse
from .localization import AsyncLocalization, Localization
from .luma import AsyncLuma, Luma
from .maestro import AsyncMaestro, Maestro
from .midjourney import AsyncMidjourney, Midjourney
from .nano_banana import AsyncNanoBanana, NanoBanana
from .producer import AsyncProducer, Producer
from .qrart import AsyncQRart, QRart
from .seedance import AsyncSeedance, Seedance
from .seedream import AsyncSeedream, Seedream
from .sora import AsyncSora, Sora
from .suno import AsyncSuno, Suno
from .wan import AsyncWan, Wan


def attach(client: Any, transport: Any, *, is_async: bool) -> None:
    """Bind every generated provider client onto ``client``."""
    if is_async:
        client.captcha = AsyncCaptcha(transport)
        client.digitalhuman = AsyncDigitalhuman(transport)
        client.drawai = AsyncDrawAI(transport)
        client.dreamina = AsyncDreamina(transport)
        client.fish = AsyncFish(transport)
        client.flux = AsyncFlux(transport)
        client.gemini = AsyncGemini(transport)
        client.grok = AsyncGrok(transport)
        client.hailuo = AsyncHailuo(transport)
        client.happyhorse = AsyncHappyhorse(transport)
        client.localization = AsyncLocalization(transport)
        client.luma = AsyncLuma(transport)
        client.maestro = AsyncMaestro(transport)
        client.midjourney = AsyncMidjourney(transport)
        client.nano_banana = AsyncNanoBanana(transport)
        client.producer = AsyncProducer(transport)
        client.qrart = AsyncQRart(transport)
        client.seedance = AsyncSeedance(transport)
        client.seedream = AsyncSeedream(transport)
        client.sora = AsyncSora(transport)
        client.suno = AsyncSuno(transport)
        client.wan = AsyncWan(transport)
    else:
        client.captcha = Captcha(transport)
        client.digitalhuman = Digitalhuman(transport)
        client.drawai = DrawAI(transport)
        client.dreamina = Dreamina(transport)
        client.fish = Fish(transport)
        client.flux = Flux(transport)
        client.gemini = Gemini(transport)
        client.grok = Grok(transport)
        client.hailuo = Hailuo(transport)
        client.happyhorse = Happyhorse(transport)
        client.localization = Localization(transport)
        client.luma = Luma(transport)
        client.maestro = Maestro(transport)
        client.midjourney = Midjourney(transport)
        client.nano_banana = NanoBanana(transport)
        client.producer = Producer(transport)
        client.qrart = QRart(transport)
        client.seedance = Seedance(transport)
        client.seedream = Seedream(transport)
        client.sora = Sora(transport)
        client.suno = Suno(transport)
        client.wan = Wan(transport)
