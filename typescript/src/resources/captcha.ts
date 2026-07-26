/** Captcha recognition/token resources (`/captcha/*`). */

import { Transport } from '../runtime/transport';
import { TaskHandle } from '../runtime/tasks';

class Recognition {
  constructor(private transport: Transport) {}

  async hcaptcha(opts: {
    queries?: string[];
    question?: string;
    async?: boolean;
    wait?: boolean;
    pollInterval?: number;
    maxWait?: number;
    [key: string]: unknown;
  } = {}): Promise<Record<string, unknown> | TaskHandle> {
    const { queries, question, wait: shouldWait, pollInterval, maxWait, ...rest } = opts;
    const body: Record<string, unknown> = { ...rest };
    if (queries !== undefined) body.queries = queries;
    if (question !== undefined) body.question = question;
    if (opts.async !== undefined) body.async = opts.async;

    const result = await this.transport.request('POST', '/captcha/recognition/hcaptcha', { json: body });
    const taskId = result.task_id as string | undefined;

    if (!taskId || (result.data && !shouldWait)) return result;

    const handle = new TaskHandle(taskId, '/captcha/tasks', this.transport);
    if (shouldWait) return handle.wait({ pollInterval, maxWait });
    return handle;
  }
}

class Token {
  constructor(private transport: Transport) {}

  async hcaptcha(opts: {
    websiteKey: string;
    websiteUrl: string;
    proxy?: string;
    async?: boolean;
    wait?: boolean;
    pollInterval?: number;
    maxWait?: number;
    [key: string]: unknown;
  }): Promise<Record<string, unknown> | TaskHandle> {
    const { websiteKey, websiteUrl, proxy, wait: shouldWait, pollInterval, maxWait, ...rest } = opts;
    const body: Record<string, unknown> = {
      website_key: websiteKey,
      website_url: websiteUrl,
      ...rest,
    };
    if (proxy !== undefined) body.proxy = proxy;
    if (opts.async !== undefined) body.async = opts.async;

    const result = await this.transport.request('POST', '/captcha/token/hcaptcha', { json: body });
    const taskId = result.task_id as string | undefined;

    if (!taskId || (result.token && !shouldWait)) return result;

    const handle = new TaskHandle(taskId, '/captcha/tasks', this.transport);
    if (shouldWait) return handle.wait({ pollInterval, maxWait });
    return handle;
  }
}

export class Captcha {
  readonly recognition: Recognition;
  readonly token: Token;

  constructor(transport: Transport) {
    this.recognition = new Recognition(transport);
    this.token = new Token(transport);
  }
}
