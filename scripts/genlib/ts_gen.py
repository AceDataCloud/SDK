"""Emit the TypeScript provider classes."""

from __future__ import annotations

import json
from pathlib import Path

from .model import Param, Service, camel, pascal

HEADER = """/**
 * {title} — generated from the platform OpenAPI spec.
 *
 * Do not edit by hand: run `python scripts/generate_providers.py`. Parameter
 * names, types, enums and required-ness all come from the live spec.
 */

import {{ Transport }} from '../../runtime/transport';
{task_import}"""


def _ts_literal(value: object) -> str:
    return json.dumps(value)


def _options_interface(svc: Service, ep) -> tuple[str, str]:
    name = f"{svc.class_name}{pascal(ep.method)}Options"
    lines = [f"export interface {name} {{"]
    for p in ep.callable_params:
        optional = "" if p.required else "?"
        doc = f"  /** {p.description} */\n" if p.description else ""
        lines.append(f"{doc}  {camel(p.name)}{optional}: {p.ts_type()};")
    if ep.pollable:
        lines.append("  /** Submit asynchronously and poll. Defaults to true. */")
        lines.append("  async?: boolean;")
        lines.append("  /** Wait for completion before returning the handle. */")
        lines.append("  wait?: boolean;")
        lines.append("  pollInterval?: number;")
        lines.append("  maxWait?: number;")
    lines.append("  callbackUrl?: string;")
    lines.append("  /** Any parameter added upstream before the SDK is regenerated. */")
    lines.append("  [key: string]: unknown;")
    lines.append("}")
    return name, "\n".join(lines)


def _body(ep, indent: str = "    ") -> list[str]:
    out = [f"{indent}const body: Record<string, unknown> = {{}};"]
    for p in ep.body_params:
        prop = camel(p.name)
        if p.required:
            out.append(f"{indent}body[{json.dumps(p.name)}] = options.{prop};")
            continue
        default = p.default()
        if default is None:
            out.append(f"{indent}if (options.{prop} !== undefined) body[{json.dumps(p.name)}] = options.{prop};")
        else:
            out.append(
                f"{indent}body[{json.dumps(p.name)}] = options.{prop} ?? {_ts_literal(default)};"
            )
    known = {camel(p.name) for p in ep.callable_params} | {
        "async", "wait", "pollInterval", "maxWait", "callbackUrl"
    }
    out.append(f"{indent}for (const [key, value] of Object.entries(options)) {{")
    out.append(f"{indent}  if (!{json.dumps(sorted(known))}.includes(key) && value !== undefined) {{")
    out.append(f"{indent}    body[key] = value;")
    out.append(f"{indent}  }}")
    out.append(f"{indent}}}")
    out.append(f"{indent}if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;")
    return out


def _method(svc: Service, ep) -> str:
    options_name, _ = _options_interface(svc, ep)
    tasks = svc.tasks_path or f"/{svc.alias}/tasks"
    doc = ep.summary or f"Call {ep.path}."
    path_expr = json.dumps(ep.path)
    if ep.path_params:
        path = ep.path
        for p in ep.path_params:
            path = path.replace("{" + p.name + "}", "${options." + camel(p.name) + "}")
        path_expr = "`" + path + "`"

    lines = [f"  /** {doc} */"]
    required_any = any(p.required for p in ep.callable_params)
    arg = f"options: {options_name}" if required_any else f"options: {options_name} = {{}}"
    if ep.pollable:
        lines.append(f"  async {ep.method}({arg}): Promise<TaskHandle> {{")
    else:
        lines.append(f"  async {ep.method}({arg}): Promise<Record<string, unknown>> {{")
    lines.extend(_body(ep))

    if ep.pollable:
        lines.append("    body.async = options.async ?? true;")
        lines.append(
            f"    const result = (await this.transport.request('POST', {path_expr}, {{ json: body }})) as Record<string, unknown>;"
        )
        lines.append(
            f"    const handle = new TaskHandle(taskId(result), {json.dumps(tasks)}, this.transport, result);"
        )
        lines.append("    if (options.wait) {")
        lines.append(
            "      await handle.wait({ pollInterval: options.pollInterval, maxWait: options.maxWait });"
        )
        lines.append("    }")
        lines.append("    return handle;")
    else:
        lines.append(
            f"    return (await this.transport.request('POST', {path_expr}, {{ json: body }})) as Record<string, unknown>;"
        )
    lines.append("  }")
    return "\n".join(lines)


def render(svc: Service) -> str:
    pollable = any(ep.pollable for ep in svc.endpoints)
    task_import = "import { TaskHandle } from '../../runtime/tasks';\n" if pollable else ""
    out = [HEADER.format(title=f"{svc.class_name} ({svc.alias})", task_import=task_import)]
    out.append("")
    if pollable:
        out.append("function taskId(result: Record<string, unknown>): string {")
        out.append("  if (typeof result?.task_id === 'string') return result.task_id;")
        out.append("  const data = result?.data as Record<string, unknown> | undefined;")
        out.append("  if (data && typeof data.task_id === 'string') return data.task_id;")
        out.append("  return typeof result?.id === 'string' ? result.id : '';")
        out.append("}")
        out.append("")

    for ep in svc.endpoints:
        _, block = _options_interface(svc, ep)
        out.append(block)
        out.append("")

    out.append(f"/** {svc.alias} client. */")
    out.append(f"export class {svc.class_name} {{")
    out.append("  constructor(private transport: Transport) {}")
    out.append("")
    for ep in svc.endpoints:
        out.append(_method(svc, ep))
        out.append("")
    out.append("}")
    return "\n".join(out).rstrip() + "\n"


def write_all(services: list[Service], root: Path) -> list[Path]:
    written = []
    target = root / "resources" / "providers"
    target.mkdir(parents=True, exist_ok=True)
    for svc in services:
        path = target / f"{svc.py_module.replace('_', '-')}.ts"
        path.write_text(render(svc))
        written.append(path)

    index = ["/** Provider-axis clients, generated from the platform OpenAPI specs. */", ""]
    for svc in services:
        module = svc.py_module.replace("_", "-")
        index.append(f"export {{ {svc.class_name} }} from './{module}';")
    index.append("")
    index.append("import { Transport } from '../../runtime/transport';")
    for svc in services:
        module = svc.py_module.replace("_", "-")
        index.append(f"import {{ {svc.class_name} }} from './{module}';")
    index.append("")
    index.append("/** Bind every generated provider client onto `client`. */")
    index.append("export function attachProviders(client: Record<string, unknown>, transport: Transport): void {")
    for svc in services:
        index.append(f"  client.{svc.attr.replace('_', '')} = new {svc.class_name}(transport);")
    index.append("}")
    path = target / "index.ts"
    path.write_text("\n".join(index) + "\n")
    written.append(path)
    return written
