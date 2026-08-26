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

  image2text(opts: {
    image: string;
    async?: boolean;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { image, ...rest } = opts;
    const body: Record<string, unknown> = { image, ...rest };
    return this.transport.request('POST', '/captcha/recognition/image2text', { json: body });
  }

  recaptcha2(opts: {
    image: string;
    question: string;
    async?: boolean;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { image, question, ...rest } = opts;
    const body: Record<string, unknown> = { image, question, ...rest };
    return this.transport.request('POST', '/captcha/recognition/recaptcha2', { json: body });
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

  recaptcha2(opts: {
    websiteKey: string;
    websiteUrl: string;
    proxy?: string;
    async?: boolean;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { websiteKey, websiteUrl, proxy, ...rest } = opts;
    const body: Record<string, unknown> = {
      website_key: websiteKey,
      website_url: websiteUrl,
      ...rest,
    };
    if (proxy !== undefined) body.proxy = proxy;
    return this.transport.request('POST', '/captcha/token/recaptcha2', { json: body });
  }

  recaptcha3(opts: {
    pageAction: string;
    websiteKey: string;
    websiteUrl: string;
    async?: boolean;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { pageAction, websiteKey, websiteUrl, ...rest } = opts;
    const body: Record<string, unknown> = {
      page_action: pageAction,
      website_key: websiteKey,
      website_url: websiteUrl,
      ...rest,
    };
    return this.transport.request('POST', '/captcha/token/recaptcha3', { json: body });
  }

  turnstile(opts: {
    websiteKey: string;
    websiteUrl: string;
    action?: string;
    cdata?: string;
    async?: boolean;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { websiteKey, websiteUrl, action, cdata, ...rest } = opts;
    const body: Record<string, unknown> = {
      website_key: websiteKey,
      website_url: websiteUrl,
      ...rest,
    };
    if (action !== undefined) body.action = action;
    if (cdata !== undefined) body.cdata = cdata;
    return this.transport.request('POST', '/captcha/token/turnstile', { json: body });
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
