"""Emit the Go provider clients."""

from __future__ import annotations

import json
from pathlib import Path

from .model import Service, pascal

HEADER = """// Code generated from the platform OpenAPI spec. DO NOT EDIT.
// Regenerate with: python scripts/generate_providers.py

package acedatacloud
"""


def _go_literal(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, str):
        return json.dumps(value)
    return str(value)


def _field_name(name: str) -> str:
    """Go exports by capitalising, and prefers URL/ID over Url/Id."""
    out = pascal(name)
    for word, fixed in (("Url", "URL"), ("Id", "ID"), ("Api", "API")):
        if out.endswith(word):
            out = out[: -len(word)] + fixed
        out = out.replace(word + "s", fixed + "s")
    return out


def _request_struct(svc: Service, ep) -> str:
    name = f"{svc.class_name}{pascal(ep.method)}Request"
    lines = [f"// {name} is the input to {svc.attr}.{ep.method.title()}."]
    lines.append(f"type {name} struct {{")
    for p in ep.callable_params:
        comment = p.description or ("required" if p.required else "optional")
        lines.append(f"\t// {comment[:110].rstrip()}")
        lines.append(f"\t{_field_name(p.name)} {p.go_type()}")
    if ep.pollable:
        lines.append("\t// Async submits without blocking; poll the returned handle. Defaults true.")
        lines.append("\tAsync *bool")
    lines.append("\t// CallbackURL optionally receives the completion webhook.")
    lines.append("\tCallbackURL string")
    lines.append("\t// Extra fields merged into the request body.")
    lines.append("\tExtra map[string]any")
    lines.append("}")
    return name, "\n".join(lines)


def _to_body(struct: str, svc: Service, ep) -> str:
    lines = [f"func (r {struct}) toBody() map[string]any {{"]
    lines.append("\tbody := map[string]any{}")
    for p in ep.body_params:
        field = _field_name(p.name)
        key = json.dumps(p.name)
        default = p.default()
        go_type = p.go_type()
        zero = {"string": '""', "int": "0", "float64": "0"}.get(go_type)

        if p.required:
            lines.append(f"\tbody[{key}] = r.{field}")
            continue
        if default is not None:
            if zero:
                lines.append(f"\tif r.{field} != {zero} {{")
                lines.append(f"\t\tbody[{key}] = r.{field}")
                lines.append("\t} else {")
                lines.append(f"\t\tbody[{key}] = {_go_literal(default)}")
                lines.append("\t}")
            else:
                # bool and composite types have no distinguishable zero value.
                lines.append(f"\tbody[{key}] = r.{field}")
        elif zero:
            lines.append(f"\tif r.{field} != {zero} {{")
            lines.append(f"\t\tbody[{key}] = r.{field}")
            lines.append("\t}")
        elif go_type.startswith("[]") or go_type.startswith("map["):
            lines.append(f"\tif r.{field} != nil {{")
            lines.append(f"\t\tbody[{key}] = r.{field}")
            lines.append("\t}")
        else:
            lines.append(f"\tbody[{key}] = r.{field}")

    if ep.pollable:
        lines.append('\tbody["async"] = true')
        lines.append("\tif r.Async != nil {")
        lines.append('\t\tbody["async"] = *r.Async')
        lines.append("\t}")
    lines.append('\tif r.CallbackURL != "" {')
    lines.append('\t\tbody["callback_url"] = r.CallbackURL')
    lines.append("\t}")
    lines.append("\tfor k, v := range r.Extra {")
    lines.append("\t\tif _, exists := body[k]; !exists {")
    lines.append("\t\t\tbody[k] = v")
    lines.append("\t\t}")
    lines.append("\t}")
    lines.append("\treturn body")
    lines.append("}")
    return "\n".join(lines)


def _imports(svc: Service) -> str:
    imports = ["context"]
    if any(ep.path_params or ep.query_params for ep in svc.endpoints):
        imports.extend(["fmt", "net/url"])
    if any(ep.path_params for ep in svc.endpoints):
        imports.append("strings")
    if len(imports) == 1:
        return '\nimport "context"\n'
    lines = ["", "import ("]
    for name in imports:
        lines.append(f"\t{json.dumps(name)}")
    lines.append(")")
    return "\n".join(lines) + "\n"


def _query_method(struct: str, ep) -> str:
    if not ep.query_params:
        return ""
    lines = [f"func (r {struct}) toQuery() url.Values {{"]
    lines.append("\tquery := url.Values{}")
    for p in ep.query_params:
        field = _field_name(p.name)
        key = json.dumps(p.name)
        default = p.default()
        zero = {"string": '""', "int": "0", "float64": "0"}.get(p.go_type())
        if p.required:
            lines.append(f"\tquery.Set({key}, fmt.Sprint(r.{field}))")
        elif default is not None:
            if zero:
                lines.append(f"\tif r.{field} != {zero} {{")
                lines.append(f"\t\tquery.Set({key}, fmt.Sprint(r.{field}))")
                lines.append("\t} else {")
                lines.append(f"\t\tquery.Set({key}, fmt.Sprint({_go_literal(default)}))")
                lines.append("\t}")
            else:
                lines.append(f"\tquery.Set({key}, fmt.Sprint(r.{field}))")
        elif zero:
            lines.append(f"\tif r.{field} != {zero} {{")
            lines.append(f"\t\tquery.Set({key}, fmt.Sprint(r.{field}))")
            lines.append("\t}")
        else:
            lines.append(f"\tquery.Set({key}, fmt.Sprint(r.{field}))")
    lines.append("\treturn query")
    lines.append("}")
    return "\n".join(lines)


def _path_lines(ep, struct: str) -> list[str]:
    if not ep.path_params:
        return []
    lines = [f"\tpath := {json.dumps(ep.path)}"]
    for p in ep.path_params:
        lines.append(
            f"\tpath = strings.ReplaceAll(path, {json.dumps('{'+p.name+'}')}, "
            f"url.PathEscape(fmt.Sprint(req.{_field_name(p.name)})))"
        )
    return lines


def _method(svc: Service, ep, struct: str) -> str:
    receiver = svc.class_name
    method = pascal(ep.method)
    tasks = svc.tasks_path or f"/{svc.alias}/tasks"
    doc = (ep.summary or f"Call {ep.path}.").replace("\n", " ")

    lines = [f"// {method} {doc[:150]}"]
    request_path = "path" if ep.path_params else json.dumps(ep.path)
    if ep.pollable:
        lines.append(
            f"func (c *{receiver}) {method}(ctx context.Context, req {struct}) (*TaskHandle, error) {{"
        )
        lines.extend(_path_lines(ep, struct))
        lines.append("\tresult, err := c.t.do(ctx, requestOpts{")
        lines.append('\t\tMethod: "POST",')
        lines.append(f"\t\tPath:   {request_path},")
        lines.append("\t\tBody:   req.toBody(),")
        if ep.query_params:
            lines.append("\t\tQuery:  req.toQuery(),")
        lines.append("\t})")
        lines.append("\tif err != nil {")
        lines.append("\t\treturn nil, err")
        lines.append("\t}")
        lines.append(
            f"\treturn newTaskHandle(taskIDFrom(result), {json.dumps(tasks)}, c.t, result), nil"
        )
    else:
        lines.append(
            f"func (c *{receiver}) {method}(ctx context.Context, req {struct}) (map[string]any, error) {{"
        )
        lines.extend(_path_lines(ep, struct))
        lines.append("\treturn c.t.do(ctx, requestOpts{")
        lines.append('\t\tMethod: "POST",')
        lines.append(f"\t\tPath:   {request_path},")
        lines.append("\t\tBody:   req.toBody(),")
        if ep.query_params:
            lines.append("\t\tQuery:  req.toQuery(),")
        lines.append("\t})")
    lines.append("}")
    return "\n".join(lines)


def render(svc: Service) -> str:
    out = [HEADER + _imports(svc), ""]
    out.append(f"// {svc.class_name} is the {svc.alias} provider client.")
    out.append(f"type {svc.class_name} struct {{")
    out.append("\tt *transport")
    out.append("}")
    out.append("")

    for ep in svc.endpoints:
        struct, block = _request_struct(svc, ep)
        out.append(block)
        out.append("")
        out.append(_to_body(struct, svc, ep))
        out.append("")
        query = _query_method(struct, ep)
        if query:
            out.append(query)
            out.append("")
        out.append(_method(svc, ep, struct))
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def write_all(services: list[Service], root: Path) -> list[Path]:
    written = []
    target = root / "providers"
    target.mkdir(parents=True, exist_ok=True)
    for svc in services:
        path = root / f"provider_{svc.py_module}.go"
        path.write_text(render(svc))
        written.append(path)

    # One place that binds every provider onto the client.
    # This file has no request methods, so it must not import context.
    lines = [HEADER, ""]
    lines.append("// taskIDFrom pulls a task id out of a submission response.")
    lines.append("func taskIDFrom(result map[string]any) string {")
    lines.append('\tif s, ok := result["task_id"].(string); ok && s != "" {')
    lines.append("\t\treturn s")
    lines.append("\t}")
    lines.append('\tif data, ok := result["data"].(map[string]any); ok {')
    lines.append('\t\tif s, ok := data["task_id"].(string); ok && s != "" {')
    lines.append("\t\t\treturn s")
    lines.append("\t\t}")
    lines.append("\t}")
    lines.append('\tif s, ok := result["id"].(string); ok {')
    lines.append("\t\treturn s")
    lines.append("\t}")
    lines.append('\treturn ""')
    lines.append("}")
    lines.append("")
    lines.append("// providers holds the provider-axis clients, one per service.")
    lines.append("type providers struct {")
    for svc in services:
        lines.append(f"\t{svc.attr.replace('_', '')} *{svc.class_name}")
    lines.append("}")
    lines.append("")
    lines.append("func newProviders(tr *transport) *providers {")
    lines.append("\treturn &providers{")
    for svc in services:
        lines.append(f"\t\t{svc.attr.replace('_', '')}: &{svc.class_name}{{t: tr}},")
    lines.append("\t}")
    lines.append("}")
    lines.append("")
    for svc in services:
        attr = svc.attr.replace("_", "")
        lines.append(f"// {svc.class_name} returns the {svc.alias} provider client.")
        lines.append(f"func (c *Client) {svc.class_name}() *{svc.class_name} {{ return c.providers.{attr} }}")
        lines.append("")
    path = root / "providers_attach.go"
    path.write_text("\n".join(lines).rstrip() + "\n")
    written.append(path)
    target.rmdir()
    return written
