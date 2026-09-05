"""Emit the Python provider classes."""

from __future__ import annotations

import json
from pathlib import Path

from .model import Param, Service, pascal, py_param, snake


def _py_literal(value: object) -> str:
    """A Python literal, not a JSON one — json.dumps(True) emits `true`."""
    return repr(value)

HEADER = '''"""{title} — generated from the platform OpenAPI spec.

Do not edit by hand: run ``python scripts/generate_providers.py``. Parameter
names, types, enums and required-ness all come from the live spec, so adding a
model upstream reaches the SDK without anyone retyping it.
"""

from __future__ import annotations

from typing import Any, Literal  # noqa: F401

from ..._runtime.tasks import AsyncTaskHandle, TaskHandle
'''


def _signature(params: list[Param], aliases: dict[str, str], *, pollable: bool) -> str:
    lines = ["self", "*"]
    for p in params:
        name = py_param(p.name)
        annotation = aliases.get(p.name) or p.py_type()
        if p.required:
            lines.append(f"{name}: {annotation}")
        else:
            lines.append(f"{name}: {annotation} | None = None")
    if pollable:
        lines += [
            "async_: bool | None = None",
            "wait: bool = False",
            "poll_interval: float = 3.0",
            "max_wait: float = 600.0",
        ]
    lines.append("callback_url: str | None = None")
    lines.append("**extra: Any")
    return ",\n        ".join(lines)


def _default_consts(svc: Service) -> tuple[dict[str, str], list[str]]:
    """A default too long to inline becomes a module constant.

    Some specs carry a full example prompt as the default; inlining one blows
    past the line limit no matter how it is wrapped.
    """
    mapping: dict[str, str] = {}
    lines: list[str] = []
    for ep in svc.endpoints:
        for p in ep.params:
            if p.is_control or p.required or p.name in mapping:
                continue
            default = p.default()
            if not isinstance(default, str) or len(default) <= 60:
                continue
            const = f"_DEFAULT_{snake(ep.method).upper()}_{p.name.upper()}"
            mapping[f"{ep.method}:{p.name}"] = const
            lines.append(f"{const} = (")
            # Implicit concatenation keeps a long example inside the line limit.
            chunk, width = "", 100
            for word in default.split(" "):
                if chunk and len(chunk) + len(word) + 1 > width:
                    lines.append(f"    {_py_literal(chunk + ' ')}")
                    chunk = word
                else:
                    chunk = f"{chunk} {word}".strip()
            if chunk:
                lines.append(f"    {_py_literal(chunk)}")
            lines.append(")")
    return mapping, lines


def _body(params: list[Param], indent: str = "        ", consts: dict[str, str] | None = None,
          method: str = "") -> str:
    """Build the request body, applying only explicit schema defaults."""
    out: list[str] = [f"{indent}body: dict[str, Any] = {{}}"]
    for p in params:
        name = py_param(p.name)
        if p.required:
            # Required in the signature, so it is always present.
            out.append(f'{indent}body["{p.name}"] = {name}')
            continue
        default = p.default()
        const = (consts or {}).get(f"{method}:{p.name}")
        if const:
            out.append(f'{indent}body["{p.name}"] = {name} if {name} is not None else {const}')
            continue
        if default is None:
            out.append(f"{indent}if {name} is not None:")
            out.append(f'{indent}    body["{p.name}"] = {name}')
        else:
            line = f'{indent}body["{p.name}"] = {name} if {name} is not None else {_py_literal(default)}'
            if len(line) <= 116:
                out.append(line)
            else:
                # ruff caps lines at 120; a long example would otherwise fail lint.
                out.append(f"{indent}body[\"{p.name}\"] = (")
                out.append(f"{indent}    {name} if {name} is not None else {_py_literal(default)}")
                out.append(f"{indent})")
    out.append(f"{indent}body.update(extra)")
    out.append(f"{indent}if callback_url is not None:")
    out.append(f'{indent}    body["callback_url"] = callback_url')
    return "\n".join(out)


def _aliases(svc: Service) -> tuple[dict[str, str], list[str]]:
    """Hoist long enums to module-level type aliases.

    An inline `Literal[...]` of fifteen model names blows past the 120-column
    limit and reads badly; a named alias is both shorter and self-documenting.
    """
    mapping: dict[str, str] = {}
    lines: list[str] = []
    for ep in svc.endpoints:
        for p in ep.params:
            if p.is_control or not p.enum or p.name in mapping:
                continue
            inline = p.py_type()
            if len(inline) <= 40:
                continue
            alias = f"{svc.class_name}{pascal(p.name)}"
            mapping[p.name] = alias
            values = ",\n    ".join(json.dumps(e) for e in p.enum)
            lines.append(f"{alias} = Literal[\n    {values},\n]")
    return mapping, lines


def _docstring(text: str, indent: str = "        ") -> list[str]:
    """Wrap a summary so the emitted line stays inside the 120-column limit."""
    limit = 120 - len(indent) - 6
    if len(text) <= limit:
        return [f'{indent}"""{text}"""']
    words, lines, current = text.split(), [], ""
    for word in words:
        if current and len(current) + len(word) + 1 > limit:
            lines.append(current)
            current = word
        else:
            current = f"{current} {word}".strip()
    if current:
        lines.append(current)
    out = [f'{indent}"""{lines[0]}']
    out.extend(f"{indent}{line}" for line in lines[1:])
    out.append(f'{indent}"""')
    return out


def _method(svc: Service, ep, aliases: dict[str, str], consts: dict[str, str], *, is_async: bool) -> str:
    handle = "AsyncTaskHandle" if is_async else "TaskHandle"
    prefix = "async " if is_async else ""
    await_ = "await " if is_async else ""
    params = ep.callable_params
    doc = ep.summary or f"Call {ep.path}."

    lines = [
        f"    {prefix}def {ep.method}(",
        f"        {_signature(params, aliases, pollable=ep.pollable)},",
    ]
    if ep.pollable:
        lines.append(f"    ) -> {handle}:")
    else:
        lines.append("    ) -> dict[str, Any]:")
    lines.extend(_docstring(doc))
    lines.append(_body(sorted(ep.body_params, key=lambda p: not p.required), consts=consts, method=ep.method))

    header_entries = ", ".join(
        f'"{p.name}": {py_param(p.name)}' for p in ep.header_params
    )
    headers = ", extra_headers=extra_headers" if header_entries else ""
    if header_entries:
        lines.append(f"        extra_headers = {{k: v for k, v in {{{header_entries}}}.items() if v is not None}}")
    if ep.pollable:
        lines.append("        body[\"async\"] = True if async_ is None else async_")
        lines.append(
            f'        result = {await_}self._transport.request("POST", "{ep.path}", json=body{headers})'
        )
        tasks = svc.tasks_path or f"/{svc.alias}/tasks"
        lines.append(
            f'        handle = {handle}(_task_id(result), "{tasks}", self._transport, submitted=result)'
        )
        lines.append("        if wait:")
        lines.append(
            f"            {await_}handle.wait(poll_interval=poll_interval, max_wait=max_wait)"
        )
        lines.append("        return handle")
    else:
        lines.append(
            f'        return {await_}self._transport.request("POST", "{ep.path}", json=body{headers})'
        )
    return "\n".join(lines)


def render(svc: Service) -> str:
    title = f"{svc.class_name} ({svc.alias})"
    aliases, alias_lines = _aliases(svc)
    consts, const_lines = _default_consts(svc)
    out = [HEADER.format(title=title)]
    out.append("")
    if const_lines:
        out.append("")
        out.extend(const_lines)
    if alias_lines:
        out.append("")
        out.extend(alias_lines)
    out.append("")
    out.append("")
    out.append("def _task_id(result: Any) -> str:")
    out.append('    """Task ids appear at the top level or nested under `data`."""')
    out.append("    if not isinstance(result, dict):")
    out.append('        return ""')
    out.append('    if result.get("task_id"):')
    out.append('        return str(result["task_id"])')
    out.append('    data = result.get("data")')
    out.append("    if isinstance(data, dict) and data.get('task_id'):")
    out.append("        return str(data['task_id'])")
    out.append('    return str(result.get("id") or "")')
    out.append("")
    out.append("")

    for is_async in (False, True):
        name = ("Async" if is_async else "") + svc.class_name
        out.append(f"class {name}:")
        out.append(f'    """{"Asynchronous" if is_async else "Synchronous"} {svc.alias} client."""')
        out.append("")
        out.append("    def __init__(self, transport: Any) -> None:")
        out.append("        self._transport = transport")
        out.append("")
        for ep in svc.endpoints:
            out.append(_method(svc, ep, aliases, consts, is_async=is_async))
            out.append("")
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def write_all(services: list[Service], root: Path) -> list[Path]:
    written = []
    for svc in services:
        path = root / "resources" / "providers" / f"{svc.py_module}.py"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render(svc))
        written.append(path)

    init = ['"""Provider-axis clients, generated from the platform OpenAPI specs."""', ""]
    for svc in services:
        init.append(
            f"from .{svc.py_module} import {svc.class_name} as {svc.class_name}, "
            f"Async{svc.class_name} as Async{svc.class_name}"
        )
    init.append("")
    init.append("__all__ = [")
    for svc in services:
        init.append(f'    "{svc.class_name}",')
        init.append(f'    "Async{svc.class_name}",')
    init.append("]")
    index = root / "resources" / "providers" / "__init__.py"
    index.write_text("\n".join(init) + "\n")
    written.append(index)
    return written


MIXIN_HEADER = '''"""Provider-axis attachment — generated, do not edit by hand.

Kept as a mixin rather than inlined into ``_client.py`` so the generator never
has to rewrite a hand-maintained file: adding a service touches only this
module, and the client just calls ``_attach_providers``.
"""

from __future__ import annotations

from typing import Any

'''


def render_mixin(services: list[Service]) -> str:
    out = [MIXIN_HEADER]
    for svc in services:
        out.append(
            f"from .{svc.py_module} import Async{svc.class_name}, {svc.class_name}"
        )
    out.append("")
    out.append("")
    out.append("def attach(client: Any, transport: Any, *, is_async: bool) -> None:")
    out.append('    """Bind every generated provider client onto ``client``."""')
    out.append("    if is_async:")
    for svc in services:
        out.append(f"        client.{svc.attr} = Async{svc.class_name}(transport)")
    out.append("    else:")
    for svc in services:
        out.append(f"        client.{svc.attr} = {svc.class_name}(transport)")
    out.append("")
    return "\n".join(out)


def write_mixin(services: list[Service], root: Path) -> Path:
    path = root / "resources" / "providers" / "_attach.py"
    path.write_text(render_mixin(services))
    return path
