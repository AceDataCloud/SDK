import re

# Update Python transport.py
py_file = 'python/src/acedatacloud/_runtime/transport.py'
with open(py_file, 'r') as f:
    py_content = f.read()

# Fix _map_error signature and body
py_content = py_content.replace(
    'def _map_error(status_code: int, body: dict[str, Any]) -> APIError:',
    'def _map_error(status_code: int, body: Any) -> APIError:'
)
py_content = py_content.replace(
    '    error_data = body.get("error", {})',
    '    error_data = (body or {}).get("error", {}) if isinstance(body, dict) else {}'
)
py_content = py_content.replace(
    '    trace_id = body.get("trace_id")',
    '    trace_id = (body or {}).get("trace_id") if isinstance(body, dict) else None'
)

with open(py_file, 'w') as f:
    f.write(py_content)

# Update TypeScript transport.ts
ts_file = 'typescript/src/runtime/transport.ts'
with open(ts_file, 'r') as f:
    ts_content = f.read()

# Export mapError
ts_content = ts_content.replace(
    'function mapError(statusCode: number, body: Record<string, unknown>): APIError {',
    'export function mapError(statusCode: number, body: any): APIError {'
)

# Fix mapError body
ts_content = ts_content.replace(
    '  const errorData = (body.error ?? {}) as Record<string, unknown>;',
    '  const errorData = (body && typeof body === "object" ? (body.error ?? {}) : {}) as Record<string, unknown>;'
)
ts_content = ts_content.replace(
    '  const traceId = body.trace_id as string | undefined;',
    '  const traceId = (body && typeof body === "object" ? body.trace_id : undefined) as string | undefined;'
)

with open(ts_file, 'w') as f:
    f.write(ts_content)
