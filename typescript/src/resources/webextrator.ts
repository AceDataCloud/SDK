/** WebExtrator web render & extract resources. */

import { Transport } from '../runtime/transport';

class Tasks {
  constructor(private transport: Transport) {}

  async retrieve(opts: {
    id?: string;
    traceId?: string;
    [key: string]: unknown;
  } = {}): Promise<Record<string, unknown>> {
    const { id, traceId, ...rest } = opts;
    const body: Record<string, unknown> = { action: 'retrieve', ...rest };
    if (id !== undefined) body.id = id;
    if (traceId !== undefined) body.trace_id = traceId;
    return this.transport.request('POST', '/webextrator/tasks', { json: body });
  }

  async retrieveBatch(opts: {
    ids?: string[];
    traceIds?: string[];
    offset?: number;
    limit?: number;
    [key: string]: unknown;
  } = {}): Promise<Record<string, unknown>> {
    const { ids, traceIds, offset, limit, ...rest } = opts;
    const body: Record<string, unknown> = { action: 'retrieve_batch', ...rest };
    if (ids !== undefined) body.ids = ids;
    if (traceIds !== undefined) body.trace_ids = traceIds;
    if (offset !== undefined) body.offset = offset;
    if (limit !== undefined) body.limit = limit;
    return this.transport.request('POST', '/webextrator/tasks', { json: body });
  }
}

export class WebExtrator {
  readonly tasks: Tasks;

  constructor(private transport: Transport) {
    this.tasks = new Tasks(transport);
  }

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
    async?: boolean;
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
    async?: boolean;
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
}
