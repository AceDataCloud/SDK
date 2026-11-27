/** Captcha resources (`/captcha/*`). */

import { Transport } from '../runtime/transport';

class Recognition {
  constructor(private transport: Transport) {}

  hcaptcha(opts: {
    queries?: string[];
    question?: string;
    async?: boolean;
    [key: string]: unknown;
  } = {}): Promise<Record<string, unknown>> {
    const { queries, question, ...rest } = opts;
    const body: Record<string, unknown> = { ...rest };
    if (queries !== undefined) body.queries = queries;
    if (question !== undefined) body.question = question;
    return this.transport.request('POST', '/captcha/recognition/hcaptcha', { json: body });
  }
}

class Token {
  constructor(private transport: Transport) {}

  hcaptcha(opts: {
    websiteKey: string;
    websiteUrl: string;
    rqdata?: string;
    proxy?: string;
    async?: boolean;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { websiteKey, websiteUrl, rqdata, proxy, ...rest } = opts;
    const body: Record<string, unknown> = {
      website_key: websiteKey,
      website_url: websiteUrl,
      ...rest,
    };
    if (rqdata !== undefined) body.rqdata = rqdata;
    if (proxy !== undefined) body.proxy = proxy;
    return this.transport.request('POST', '/captcha/token/hcaptcha', { json: body });
  }
}

class Tasks {
  constructor(private transport: Transport) {}

  retrieve(opts: { taskId: string; [key: string]: unknown }): Promise<Record<string, unknown>> {
    const { taskId, ...rest } = opts;
    return this.transport.request('POST', '/captcha/tasks', {
      json: { task_id: taskId, ...rest },
    });
  }
}

export class Captcha {
  readonly recognition: Recognition;
  readonly token: Token;
  readonly tasks: Tasks;

  constructor(transport: Transport) {
    this.recognition = new Recognition(transport);
    this.token = new Token(transport);
    this.tasks = new Tasks(transport);
  }
}
