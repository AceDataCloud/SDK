/** HTTP transport for AceDataCloud SDK. Uses native fetch (Node 18+). */

import {
  APIError,
  AuthenticationError,
  InsufficientBalanceError,
  ModerationError,
  RateLimitError,
  ResourceDisabledError,
  TimeoutError,
  TokenMismatchError,
  TransportError,
  ValidationError,
} from './errors';
import type {
  PaymentHandler,
  PaymentRequiredBody,
} from './payment';

const ERROR_CODE_MAP: Record<string, typeof APIError> = {
  invalid_token: AuthenticationError,
  token_expired: AuthenticationError,
  no_token: AuthenticationError,
  token_mismatched: TokenMismatchError,
  used_up: InsufficientBalanceError,
  disabled: ResourceDisabledError,
  too_many_requests: RateLimitError,
  bad_request: ValidationError,
};

const RETRY_STATUS_CODES = new Set([408, 409, 429, 500, 502, 503, 504]);

export function mapError(statusCode: number, body: Record<string, unknown>): APIError {
  // The server occasionally returns ``error`` as a bare string (e.g. x402
  // facilitator diagnostics) or omits/nulls it entirely. Normalize to an
  // object so downstream property access is always safe and the message
  // is preserved verbatim.
  let errorData: Record<string, unknown>;
  if (typeof body.error === 'string') {
    errorData = { message: body.error };
  } else if (body.error && typeof body.error === 'object' && !Array.isArray(body.error)) {
    errorData = body.error as Record<string, unknown>;
  } else {
    errorData = {};
  }
  const code = (errorData.code ?? '') as string;
  const message = (errorData.message ?? '') as string;
  const traceId = body.trace_id as string | undefined;

  let ErrorClass = ERROR_CODE_MAP[code];
  if (!ErrorClass) {
    if (statusCode === 403) ErrorClass = ModerationError;
    else if (statusCode === 401) ErrorClass = AuthenticationError;
    else if (statusCode === 429) ErrorClass = RateLimitError;
    else if (statusCode === 400) ErrorClass = ValidationError;
    else ErrorClass = APIError;
  }

  return new ErrorClass({ message, statusCode, code, traceId, body });
}

function backoffDelay(attempt: number): number {
  const base = Math.min(2 ** attempt, 8);
  return base + Math.random() * 0.5;
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function isAbortError(error: unknown): boolean {
  return typeof error === 'object' && error !== null && 'name' in error && error.name === 'AbortError';
}

function timeoutError(error: unknown): TimeoutError {
  return new TimeoutError({
    message: `Request timed out${error instanceof Error && error.message ? `: ${error.message}` : ''}`,
    statusCode: 0,
    code: 'timeout',
  });
}

export interface TransportOptions {
  apiToken?: string;
  baseURL?: string;
  platformBaseURL?: string;
  timeout?: number;
  maxRetries?: number;
  headers?: Record<string, string>;
  /**
   * Optional handler invoked when a request returns `402 Payment Required`.
   * The handler receives the parsed `accepts` list and must return the extra
   * headers (typically `X-Payment`) to attach to the automatic retry.
   *
   * See `@acedatacloud/x402-client` for a drop-in implementation.
   */
  paymentHandler?: PaymentHandler;
}

export class Transport {
  private baseURL: string;
  private platformBaseURL: string;
  private timeout: number;
  private maxRetries: number;
  private headers: Record<string, string>;
  private paymentHandler?: PaymentHandler;

  constructor(opts: TransportOptions = {}) {
    const token = opts.apiToken ?? process.env.ACEDATACLOUD_API_TOKEN ?? '';
    if (!token && !opts.paymentHandler) {
      throw new AuthenticationError({
        message:
          'apiToken is required (or provide a paymentHandler, e.g. from @acedatacloud/x402-client). ' +
          'Pass it to the client or set ACEDATACLOUD_API_TOKEN.',
        statusCode: 0,
        code: 'no_token',
      });
    }
    this.baseURL = (opts.baseURL ?? 'https://x402.acedata.cloud').replace(/\/+$/, '');
    this.platformBaseURL = (opts.platformBaseURL ?? 'https://platform.acedata.cloud').replace(/\/+$/, '');
    this.timeout = opts.timeout ?? 300_000;
    this.maxRetries = opts.maxRetries ?? 2;
    this.paymentHandler = opts.paymentHandler;
    const baseHeaders: Record<string, string> = {
      accept: 'application/json',
      'content-type': 'application/json',
      'user-agent': 'acedatacloud-node/0.1.0',
      ...(opts.headers ?? {}),
    };
    if (token) {
      baseHeaders.authorization = `Bearer ${token}`;
    }
    this.headers = baseHeaders;
  }

  async request(
    method: string,
    path: string,
    opts: {
      json?: Record<string, unknown>;
      params?: Record<string, string>;
      platform?: boolean;
      timeout?: number;
      headers?: Record<string, string>;
    } = {}
  ): Promise<Record<string, unknown>> {
    const base = opts.platform ? this.platformBaseURL : this.baseURL;
    let url = `${base}${path}`;
    if (opts.params) {
      const qs = new URLSearchParams(opts.params).toString();
      url += `?${qs}`;
    }
    const headers = { ...this.headers, ...(opts.headers ?? {}) };
    const timeoutMs = opts.timeout ?? this.timeout;

    let lastError: Error | null = null;
    let paymentAttempted = false;
    let extraHeaders: Record<string, string> = {};
    let attempt = 0;
    while (true) {
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), timeoutMs);
      try {
        const resp = await fetch(url, {
          method,
          headers: { ...headers, ...extraHeaders },
          body: opts.json ? JSON.stringify(opts.json) : undefined,
          signal: controller.signal,
        });
        clearTimeout(timer);

        if (resp.status === 402 && this.paymentHandler && !paymentAttempted) {
          const text = await resp.text();
          let body: unknown;
          try {
            body = JSON.parse(text);
          } catch {
            throw mapError(402, { error: { code: 'invalid_402', message: text } });
          }
          if (
            !body ||
            typeof body !== 'object' ||
            !Array.isArray((body as PaymentRequiredBody).accepts) ||
            !(body as PaymentRequiredBody).accepts.length ||
            !(body as PaymentRequiredBody).accepts.every(
              (requirement) => requirement !== null && typeof requirement === 'object'
            )
          ) {
            throw mapError(402, { error: { code: 'invalid_402', message: 'No payment requirements' } });
          }
          const paymentRequired = body as PaymentRequiredBody;
          const result = await this.paymentHandler({
            url,
            method,
            body: opts.json,
            accepts: paymentRequired.accepts,
          });
          extraHeaders = { ...extraHeaders, ...result.headers };
          paymentAttempted = true;
          continue;
        }

        if (resp.status >= 400) {
          const text = await resp.text();
          let body: Record<string, unknown>;
          try {
            body = JSON.parse(text) as Record<string, unknown>;
          } catch {
            body = { error: { code: 'unknown', message: text } };
          }
          if (!paymentAttempted && RETRY_STATUS_CODES.has(resp.status) && attempt < this.maxRetries) {
            await sleep(backoffDelay(attempt) * 1000);
            attempt += 1;
            continue;
          }
          throw mapError(resp.status, body);
        }

        return (await resp.json()) as Record<string, unknown>;
      } catch (err) {
        clearTimeout(timer);
        if (err instanceof APIError) throw err;
        if (isAbortError(err)) {
          lastError = timeoutError(err);
        } else {
          lastError = err as Error;
        }
        if (!paymentAttempted && attempt < this.maxRetries) {
          await sleep(backoffDelay(attempt) * 1000);
          attempt += 1;
          continue;
        }
        throw lastError;
      }
    }
  }

  async *requestStream(
    method: string,
    path: string,
    opts: { json?: Record<string, unknown>; timeout?: number } = {}
  ): AsyncGenerator<string, void, unknown> {
    const url = `${this.baseURL}${path}`;
    const headers = { ...this.headers, accept: 'text/event-stream' };
    let paymentAttempted = false;
    let extraHeaders: Record<string, string> = {};

    while (true) {
      const controller = new AbortController();
      const timeoutMs = opts.timeout ?? this.timeout;
      const connectionTimer = setTimeout(() => controller.abort(), timeoutMs);
      try {
        let resp: Response;
        try {
          resp = await fetch(url, {
            method,
            headers: { ...headers, ...extraHeaders },
            body: opts.json ? JSON.stringify(opts.json) : undefined,
            signal: controller.signal,
          });
        } catch (error) {
          if (isAbortError(error)) throw timeoutError(error);
          throw error;
        } finally {
          clearTimeout(connectionTimer);
        }

        if (resp.status === 402 && this.paymentHandler && !paymentAttempted) {
          const text = await resp.text();
          let body: unknown;
          try {
            body = JSON.parse(text);
          } catch {
            throw mapError(402, { error: { code: 'invalid_402', message: text } });
          }
          if (
            !body ||
            typeof body !== 'object' ||
            !Array.isArray((body as PaymentRequiredBody).accepts) ||
            !(body as PaymentRequiredBody).accepts.length ||
            !(body as PaymentRequiredBody).accepts.every(
              (requirement) => requirement !== null && typeof requirement === 'object'
            )
          ) {
            throw mapError(402, { error: { code: 'invalid_402', message: 'No payment requirements' } });
          }
          const paymentRequired = body as PaymentRequiredBody;
          const result = await this.paymentHandler({
            url,
            method,
            body: opts.json,
            accepts: paymentRequired.accepts,
          });
          extraHeaders = { ...extraHeaders, ...result.headers };
          paymentAttempted = true;
          continue;
        }

        if (resp.status >= 400) {
          const text = await resp.text();
          let body: Record<string, unknown>;
          try {
            body = JSON.parse(text) as Record<string, unknown>;
          } catch {
            body = { error: { code: 'unknown', message: text } };
          }
          throw mapError(resp.status, body);
        }

        if (!resp.body) throw new TransportError('No response body for stream');

        const reader = resp.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';

        try {
          while (true) {
            const idleTimer = setTimeout(() => controller.abort(), timeoutMs);
            let result: Awaited<ReturnType<typeof reader.read>>;
            try {
              result = await reader.read();
            } catch (error) {
              if (isAbortError(error)) throw timeoutError(error);
              throw error;
            } finally {
              clearTimeout(idleTimer);
            }
            const { done, value } = result;
            if (done) break;
            buffer += decoder.decode(value, { stream: true });

            const lines = buffer.split('\n');
            buffer = lines.pop() ?? '';

            for (const line of lines) {
              if (line.startsWith('data: ')) {
                const data = line.slice(6);
                if (data === '[DONE]') return;
                yield data;
              }
            }
          }
        } finally {
          try {
            await reader.cancel();
          } catch {
            // Preserve the original stream error, especially SDK TimeoutError.
          }
        }
        return;
      } finally {
        clearTimeout(connectionTimer);
      }
    }
  }

  async upload(
    path: string,
    fileData: Buffer | Uint8Array,
    filename: string,
    opts: { timeout?: number } = {}
  ): Promise<Record<string, unknown>> {
    const url = `${this.platformBaseURL}${path}`;
    const boundary = `----AceDataCloudBoundary${Date.now()}`;
    const headers = {
      ...this.headers,
      'content-type': `multipart/form-data; boundary=${boundary}`,
    };
    delete (headers as Record<string, string>)['content-type'];

    const body = new FormData();
    body.append('file', new Blob([fileData]), filename);

    const authHeaders: Record<string, string> = {
      authorization: this.headers.authorization,
      'user-agent': this.headers['user-agent'],
    };

    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), opts.timeout ?? this.timeout);
    try {
      let resp: Response;
      try {
        resp = await fetch(url, {
          method: 'POST',
          headers: authHeaders,
          body,
          signal: controller.signal,
        });
      } catch (error) {
        if (isAbortError(error)) throw timeoutError(error);
        throw error;
      }
      clearTimeout(timer);

      if (resp.status >= 400) {
        const text = await resp.text();
        let respBody: Record<string, unknown>;
        try {
          respBody = JSON.parse(text) as Record<string, unknown>;
        } catch {
          respBody = { error: { code: 'unknown', message: text } };
        }
        throw mapError(resp.status, respBody);
      }
      return (await resp.json()) as Record<string, unknown>;
    } finally {
      clearTimeout(timer);
    }
  }
}
