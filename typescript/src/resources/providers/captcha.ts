/**
 * Captcha (captcha) — generated from the platform OpenAPI spec.
 *
 * Do not edit by hand: run `python scripts/generate_providers.py`. Parameter
 * names, types, enums and required-ness all come from the live spec.
 */

import { Transport } from '../../runtime/transport';

class CaptchaRecognition {
  constructor(private transport: Transport) {}

  async hcaptcha(opts: {
    queries?: string[];
    question?: string;
    async?: boolean;
  } = {}): Promise<Record<string, unknown>> {
    const body: Record<string, unknown> = {};
    if (opts.queries !== undefined) body.queries = opts.queries;
    if (opts.question !== undefined) body.question = opts.question;
    if (opts.async !== undefined) body.async = opts.async;
    return (await this.transport.request('POST', '/captcha/recognition/hcaptcha', { json: body })) as Record<string, unknown>;
  }
}

class CaptchaToken {
  constructor(private transport: Transport) {}

  async hcaptcha(opts: {
    websiteKey: string;
    websiteUrl: string;
    proxy?: string;
    async?: boolean;
  }): Promise<Record<string, unknown>> {
    const body: Record<string, unknown> = { website_key: opts.websiteKey, website_url: opts.websiteUrl };
    if (opts.proxy !== undefined) body.proxy = opts.proxy;
    if (opts.async !== undefined) body.async = opts.async;
    return (await this.transport.request('POST', '/captcha/token/hcaptcha', { json: body })) as Record<string, unknown>;
  }
}

export class Captcha {
  readonly recognition: CaptchaRecognition;
  readonly token: CaptchaToken;
  private transport: Transport;

  constructor(transport: Transport) {
    this.transport = transport;
    this.recognition = new CaptchaRecognition(transport);
    this.token = new CaptchaToken(transport);
  }

  async tasks(opts: { taskId: string }): Promise<Record<string, unknown>> {
    return (await this.transport.request('POST', '/captcha/tasks', { json: { task_id: opts.taskId } })) as Record<string, unknown>;
  }
}
