/** WebExtrator web render & extract resources. */

import { Transport } from '../runtime/transport';

export class WebExtrator {
  constructor(private transport: Transport) {}

  async extract(opts: {
    url: string;
    expectedType?: 'product' | 'article' | 'general';
    enableLlm?: boolean;
    waitUntil?: 'load' | 'domcontentloaded' | 'networkidle' | 'commit';
    timeout?: number;
    delay?: number;
    waitForSelector?: string;
    blockResources?: string[];
    headers?: Record<string, string>;
    userAgent?: string;
    callbackUrl?: string;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { url, expectedType, enableLlm, waitUntil, timeout, delay, waitForSelector, blockResources, headers, userAgent, callbackUrl, ...rest } = opts;
    const body: Record<string, unknown> = { url, ...rest };
    if (expectedType !== undefined) body.expected_type = expectedType;
    if (enableLlm !== undefined) body.enable_llm = enableLlm;
    if (waitUntil !== undefined) body.wait_until = waitUntil;
    if (timeout !== undefined) body.timeout = timeout;
    if (delay !== undefined) body.delay = delay;
    if (waitForSelector !== undefined) body.wait_for_selector = waitForSelector;
    if (blockResources !== undefined) body.block_resources = blockResources;
    if (headers !== undefined) body.headers = headers;
    if (userAgent !== undefined) body.user_agent = userAgent;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    return this.transport.request('POST', '/webextrator/extract', { json: body });
  }

  async render(opts: {
    url: string;
    waitUntil?: 'load' | 'domcontentloaded' | 'networkidle' | 'commit';
    timeout?: number;
    delay?: number;
    waitForSelector?: string;
    blockResources?: string[];
    headers?: Record<string, string>;
    userAgent?: string;
    callbackUrl?: string;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { url, waitUntil, timeout, delay, waitForSelector, blockResources, headers, userAgent, callbackUrl, ...rest } = opts;
    const body: Record<string, unknown> = { url, ...rest };
    if (waitUntil !== undefined) body.wait_until = waitUntil;
    if (timeout !== undefined) body.timeout = timeout;
    if (delay !== undefined) body.delay = delay;
    if (waitForSelector !== undefined) body.wait_for_selector = waitForSelector;
    if (blockResources !== undefined) body.block_resources = blockResources;
    if (headers !== undefined) body.headers = headers;
    if (userAgent !== undefined) body.user_agent = userAgent;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    return this.transport.request('POST', '/webextrator/render', { json: body });
  }

  async tasks(opts: {
    action: 'retrieve' | 'retrieve_batch';
    id?: string;
    traceId?: string;
    ids?: string[];
    traceIds?: string[];
    offset?: number;
    limit?: number;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { action, id, traceId, ids, traceIds, offset, limit, ...rest } = opts;
    const body: Record<string, unknown> = { action, ...rest };
    if (id !== undefined) body.id = id;
    if (traceId !== undefined) body.trace_id = traceId;
    if (ids !== undefined) body.ids = ids;
    if (traceIds !== undefined) body.trace_ids = traceIds;
    if (offset !== undefined) body.offset = offset;
    if (limit !== undefined) body.limit = limit;
    return this.transport.request('POST', '/webextrator/tasks', { json: body });
  }
}
