"""Tripo (tripo) — generated from the platform OpenAPI spec.

Do not edit by hand: run ``python scripts/generate_providers.py``. Parameter
names, types, enums and required-ness all come from the live spec, so adding a
model upstream reaches the SDK without anyone retyping it.
"""

from __future__ import annotations

from typing import Any, Literal  # noqa: F401

from ..._runtime.tasks import AsyncTaskHandle, TaskHandle

TripoModel = Literal[
    "v3.1-20260211",
    "v3.0-20250812",
    "v2.5-20250123",
    "P1-20260311",
    "P2-20260801",
]
TripoTextureQuality = Literal[
    "fast",
    "standard",
    "detailed",
    "extreme",
]
TripoFormat = Literal[
    "GLTF",
    "FBX",
    "USDZ",
    "OBJ",
    "STL",
    "3MF",
]
TripoFbxPreset = Literal[
    "blender",
    "3dsmax",
    "mixamo",
    "bake_scale",
]
TripoRigType = Literal[
    "biped",
    "quadruped",
    "hexapod",
    "octopod",
    "avian",
    "serpentine",
    "aquatic",
    "others",
]
TripoSpec = Literal[
    "tripo",
    "mixamo",
    "actorcore",
    "unity",
    "unreal",
    "vrm",
]


def _task_id(result: Any) -> str:
    """Task ids appear at the top level or nested under `data`."""
    if not isinstance(result, dict):
        return ""
    if result.get("task_id"):
        return str(result["task_id"])
    data = result.get("data")
    if isinstance(data, dict) and data.get("task_id"):
        return str(data["task_id"])
    return str(result.get("id") or "")


class Tripo:
    """Synchronous tripo client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def generate(
        self,
        *,
        action: Literal["generate"] | None = None,
        model: TripoModel | None = None,
        texture: Literal["none", "standard"] | None = None,
        prompt: str | None = None,
        image_url: str | None = None,
        image_urls: list[str | None] | None = None,
        idempotency_key: str | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> TaskHandle:
        """Tripo Generations"""
        body: dict[str, Any] = {}
        body["action"] = action if action is not None else "generate"
        body["model"] = model if model is not None else "v3.1-20260211"
        body["texture"] = texture if texture is not None else "standard"
        if prompt is not None:
            body["prompt"] = prompt
        if image_url is not None:
            body["image_url"] = image_url
        if image_urls is not None:
            body["image_urls"] = image_urls
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        extra_headers = {k: v for k, v in {"Idempotency-Key": idempotency_key}.items() if v is not None}
        body["async"] = True if async_ is None else async_
        result = self._transport.request("POST", "/tripo/generations", json=body, extra_headers=extra_headers)
        handle = TaskHandle(_task_id(result), "/tripo/tasks", self._transport, submitted=result)
        if wait:
            handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    def models(
        self,
        *,
        action: Literal["import", "texture", "convert"],
        model_url: str | None = None,
        model_id: str | None = None,
        model: TripoModel | None = None,
        texture_quality: TripoTextureQuality | None = None,
        texture_alignment: Literal["original_image", "geometry"] | None = None,
        texture_seed: int | None = None,
        pbr: bool | None = None,
        bake: bool | None = None,
        delight: bool | None = None,
        part_names: list[str] | None = None,
        compress: Literal["geometry"] | None = None,
        prompt: str | None = None,
        image_url: str | None = None,
        image_urls: list[str | None] | None = None,
        style_image_url: str | None = None,
        format: TripoFormat | None = None,
        quad: bool | None = None,
        force_symmetry: bool | None = None,
        flatten_bottom: bool | None = None,
        pack_uv: bool | None = None,
        export_vertex_colors: bool | None = None,
        pivot_to_center_bottom: bool | None = None,
        with_animation: bool | None = None,
        animate_in_place: bool | None = None,
        face_limit: int | None = None,
        flatten_bottom_threshold: float | None = None,
        texture_size: int | None = None,
        texture_format: Literal["JPEG", "PNG", "WEBP", "BMP"] | None = None,
        scale_factor: float | None = None,
        export_orientation: Literal["+x", "-x", "+y", "-y"] | None = None,
        fbx_preset: TripoFbxPreset | None = None,
        texture_packaging: Literal["embedded", "zip"] | None = None,
        idempotency_key: str | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> TaskHandle:
        """Tripo Models"""
        body: dict[str, Any] = {}
        body["action"] = action
        if model_url is not None:
            body["model_url"] = model_url
        if model_id is not None:
            body["model_id"] = model_id
        if model is not None:
            body["model"] = model
        if texture_quality is not None:
            body["texture_quality"] = texture_quality
        if texture_alignment is not None:
            body["texture_alignment"] = texture_alignment
        if texture_seed is not None:
            body["texture_seed"] = texture_seed
        if pbr is not None:
            body["pbr"] = pbr
        if bake is not None:
            body["bake"] = bake
        if delight is not None:
            body["delight"] = delight
        if part_names is not None:
            body["part_names"] = part_names
        if compress is not None:
            body["compress"] = compress
        if prompt is not None:
            body["prompt"] = prompt
        if image_url is not None:
            body["image_url"] = image_url
        if image_urls is not None:
            body["image_urls"] = image_urls
        if style_image_url is not None:
            body["style_image_url"] = style_image_url
        if format is not None:
            body["format"] = format
        if quad is not None:
            body["quad"] = quad
        if force_symmetry is not None:
            body["force_symmetry"] = force_symmetry
        if flatten_bottom is not None:
            body["flatten_bottom"] = flatten_bottom
        if pack_uv is not None:
            body["pack_uv"] = pack_uv
        if export_vertex_colors is not None:
            body["export_vertex_colors"] = export_vertex_colors
        if pivot_to_center_bottom is not None:
            body["pivot_to_center_bottom"] = pivot_to_center_bottom
        if with_animation is not None:
            body["with_animation"] = with_animation
        if animate_in_place is not None:
            body["animate_in_place"] = animate_in_place
        if face_limit is not None:
            body["face_limit"] = face_limit
        if flatten_bottom_threshold is not None:
            body["flatten_bottom_threshold"] = flatten_bottom_threshold
        if texture_size is not None:
            body["texture_size"] = texture_size
        if texture_format is not None:
            body["texture_format"] = texture_format
        if scale_factor is not None:
            body["scale_factor"] = scale_factor
        if export_orientation is not None:
            body["export_orientation"] = export_orientation
        if fbx_preset is not None:
            body["fbx_preset"] = fbx_preset
        if texture_packaging is not None:
            body["texture_packaging"] = texture_packaging
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        extra_headers = {k: v for k, v in {"Idempotency-Key": idempotency_key}.items() if v is not None}
        body["async"] = True if async_ is None else async_
        result = self._transport.request("POST", "/tripo/models", json=body, extra_headers=extra_headers)
        handle = TaskHandle(_task_id(result), "/tripo/tasks", self._transport, submitted=result)
        if wait:
            handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    def animations(
        self,
        *,
        action: Literal["rig_check", "rig", "retarget"],
        model_id: str | None = None,
        model_url: str | None = None,
        model: TripoModel | None = None,
        rig_type: TripoRigType | None = None,
        spec: TripoSpec | None = None,
        format: TripoFormat | None = None,
        animation: str | None = None,
        animations: list[str] | None = None,
        export_with_geometry: bool | None = None,
        animate_in_place: bool | None = None,
        idempotency_key: str | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> TaskHandle:
        """Tripo Animations"""
        body: dict[str, Any] = {}
        body["action"] = action
        if model_id is not None:
            body["model_id"] = model_id
        if model_url is not None:
            body["model_url"] = model_url
        if model is not None:
            body["model"] = model
        if rig_type is not None:
            body["rig_type"] = rig_type
        if spec is not None:
            body["spec"] = spec
        if format is not None:
            body["format"] = format
        if animation is not None:
            body["animation"] = animation
        if animations is not None:
            body["animations"] = animations
        if export_with_geometry is not None:
            body["export_with_geometry"] = export_with_geometry
        if animate_in_place is not None:
            body["animate_in_place"] = animate_in_place
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        extra_headers = {k: v for k, v in {"Idempotency-Key": idempotency_key}.items() if v is not None}
        body["async"] = True if async_ is None else async_
        result = self._transport.request("POST", "/tripo/animations", json=body, extra_headers=extra_headers)
        handle = TaskHandle(_task_id(result), "/tripo/tasks", self._transport, submitted=result)
        if wait:
            handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    def tasks(
        self,
        *,
        action: Literal["retrieve", "retrieve_batch"] | None = None,
        id: str | None = None,
        trace_id: str | None = None,
        ids: list[str] | None = None,
        trace_ids: list[str] | None = None,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Tripo tasks"""
        body: dict[str, Any] = {}
        body["action"] = action if action is not None else "retrieve"
        if id is not None:
            body["id"] = id
        if trace_id is not None:
            body["trace_id"] = trace_id
        if ids is not None:
            body["ids"] = ids
        if trace_ids is not None:
            body["trace_ids"] = trace_ids
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return self._transport.request("POST", "/tripo/tasks", json=body)


class AsyncTripo:
    """Asynchronous tripo client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def generate(
        self,
        *,
        action: Literal["generate"] | None = None,
        model: TripoModel | None = None,
        texture: Literal["none", "standard"] | None = None,
        prompt: str | None = None,
        image_url: str | None = None,
        image_urls: list[str | None] | None = None,
        idempotency_key: str | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> AsyncTaskHandle:
        """Tripo Generations"""
        body: dict[str, Any] = {}
        body["action"] = action if action is not None else "generate"
        body["model"] = model if model is not None else "v3.1-20260211"
        body["texture"] = texture if texture is not None else "standard"
        if prompt is not None:
            body["prompt"] = prompt
        if image_url is not None:
            body["image_url"] = image_url
        if image_urls is not None:
            body["image_urls"] = image_urls
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        extra_headers = {k: v for k, v in {"Idempotency-Key": idempotency_key}.items() if v is not None}
        body["async"] = True if async_ is None else async_
        result = await self._transport.request("POST", "/tripo/generations", json=body, extra_headers=extra_headers)
        handle = AsyncTaskHandle(_task_id(result), "/tripo/tasks", self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    async def models(
        self,
        *,
        action: Literal["import", "texture", "convert"],
        model_url: str | None = None,
        model_id: str | None = None,
        model: TripoModel | None = None,
        texture_quality: TripoTextureQuality | None = None,
        texture_alignment: Literal["original_image", "geometry"] | None = None,
        texture_seed: int | None = None,
        pbr: bool | None = None,
        bake: bool | None = None,
        delight: bool | None = None,
        part_names: list[str] | None = None,
        compress: Literal["geometry"] | None = None,
        prompt: str | None = None,
        image_url: str | None = None,
        image_urls: list[str | None] | None = None,
        style_image_url: str | None = None,
        format: TripoFormat | None = None,
        quad: bool | None = None,
        force_symmetry: bool | None = None,
        flatten_bottom: bool | None = None,
        pack_uv: bool | None = None,
        export_vertex_colors: bool | None = None,
        pivot_to_center_bottom: bool | None = None,
        with_animation: bool | None = None,
        animate_in_place: bool | None = None,
        face_limit: int | None = None,
        flatten_bottom_threshold: float | None = None,
        texture_size: int | None = None,
        texture_format: Literal["JPEG", "PNG", "WEBP", "BMP"] | None = None,
        scale_factor: float | None = None,
        export_orientation: Literal["+x", "-x", "+y", "-y"] | None = None,
        fbx_preset: TripoFbxPreset | None = None,
        texture_packaging: Literal["embedded", "zip"] | None = None,
        idempotency_key: str | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> AsyncTaskHandle:
        """Tripo Models"""
        body: dict[str, Any] = {}
        body["action"] = action
        if model_url is not None:
            body["model_url"] = model_url
        if model_id is not None:
            body["model_id"] = model_id
        if model is not None:
            body["model"] = model
        if texture_quality is not None:
            body["texture_quality"] = texture_quality
        if texture_alignment is not None:
            body["texture_alignment"] = texture_alignment
        if texture_seed is not None:
            body["texture_seed"] = texture_seed
        if pbr is not None:
            body["pbr"] = pbr
        if bake is not None:
            body["bake"] = bake
        if delight is not None:
            body["delight"] = delight
        if part_names is not None:
            body["part_names"] = part_names
        if compress is not None:
            body["compress"] = compress
        if prompt is not None:
            body["prompt"] = prompt
        if image_url is not None:
            body["image_url"] = image_url
        if image_urls is not None:
            body["image_urls"] = image_urls
        if style_image_url is not None:
            body["style_image_url"] = style_image_url
        if format is not None:
            body["format"] = format
        if quad is not None:
            body["quad"] = quad
        if force_symmetry is not None:
            body["force_symmetry"] = force_symmetry
        if flatten_bottom is not None:
            body["flatten_bottom"] = flatten_bottom
        if pack_uv is not None:
            body["pack_uv"] = pack_uv
        if export_vertex_colors is not None:
            body["export_vertex_colors"] = export_vertex_colors
        if pivot_to_center_bottom is not None:
            body["pivot_to_center_bottom"] = pivot_to_center_bottom
        if with_animation is not None:
            body["with_animation"] = with_animation
        if animate_in_place is not None:
            body["animate_in_place"] = animate_in_place
        if face_limit is not None:
            body["face_limit"] = face_limit
        if flatten_bottom_threshold is not None:
            body["flatten_bottom_threshold"] = flatten_bottom_threshold
        if texture_size is not None:
            body["texture_size"] = texture_size
        if texture_format is not None:
            body["texture_format"] = texture_format
        if scale_factor is not None:
            body["scale_factor"] = scale_factor
        if export_orientation is not None:
            body["export_orientation"] = export_orientation
        if fbx_preset is not None:
            body["fbx_preset"] = fbx_preset
        if texture_packaging is not None:
            body["texture_packaging"] = texture_packaging
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        extra_headers = {k: v for k, v in {"Idempotency-Key": idempotency_key}.items() if v is not None}
        body["async"] = True if async_ is None else async_
        result = await self._transport.request("POST", "/tripo/models", json=body, extra_headers=extra_headers)
        handle = AsyncTaskHandle(_task_id(result), "/tripo/tasks", self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    async def animations(
        self,
        *,
        action: Literal["rig_check", "rig", "retarget"],
        model_id: str | None = None,
        model_url: str | None = None,
        model: TripoModel | None = None,
        rig_type: TripoRigType | None = None,
        spec: TripoSpec | None = None,
        format: TripoFormat | None = None,
        animation: str | None = None,
        animations: list[str] | None = None,
        export_with_geometry: bool | None = None,
        animate_in_place: bool | None = None,
        idempotency_key: str | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> AsyncTaskHandle:
        """Tripo Animations"""
        body: dict[str, Any] = {}
        body["action"] = action
        if model_id is not None:
            body["model_id"] = model_id
        if model_url is not None:
            body["model_url"] = model_url
        if model is not None:
            body["model"] = model
        if rig_type is not None:
            body["rig_type"] = rig_type
        if spec is not None:
            body["spec"] = spec
        if format is not None:
            body["format"] = format
        if animation is not None:
            body["animation"] = animation
        if animations is not None:
            body["animations"] = animations
        if export_with_geometry is not None:
            body["export_with_geometry"] = export_with_geometry
        if animate_in_place is not None:
            body["animate_in_place"] = animate_in_place
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        extra_headers = {k: v for k, v in {"Idempotency-Key": idempotency_key}.items() if v is not None}
        body["async"] = True if async_ is None else async_
        result = await self._transport.request("POST", "/tripo/animations", json=body, extra_headers=extra_headers)
        handle = AsyncTaskHandle(_task_id(result), "/tripo/tasks", self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    async def tasks(
        self,
        *,
        action: Literal["retrieve", "retrieve_batch"] | None = None,
        id: str | None = None,
        trace_id: str | None = None,
        ids: list[str] | None = None,
        trace_ids: list[str] | None = None,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Tripo tasks"""
        body: dict[str, Any] = {}
        body["action"] = action if action is not None else "retrieve"
        if id is not None:
            body["id"] = id
        if trace_id is not None:
            body["trace_id"] = trace_id
        if ids is not None:
            body["ids"] = ids
        if trace_ids is not None:
            body["trace_ids"] = trace_ids
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return await self._transport.request("POST", "/tripo/tasks", json=body)
