/** Captcha resources. */

import { Transport } from '../runtime/transport';

class Recognition {
  constructor(private transport: Transport) {}

  async hcaptcha(opts: {
    question?: string;
    queries?: string;
    async?: boolean;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { question, queries, async, ...rest } = opts;
    const body: Record<string, unknown> = { ...rest };
    if (question !== undefined) body.question = question;
    if (queries !== undefined) body.queries = queries;
    if (async !== undefined) body.async = async;
    return this.transport.request('POST', '/captcha/recognition/hcaptcha', { json: body });
  }

  async image2text(opts: {
    image: string;
    async?: boolean;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { image, async, ...rest } = opts;
    const body: Record<string, unknown> = { image, ...rest };
    if (async !== undefined) body.async = async;
    return this.transport.request('POST', '/captcha/recognition/image2text', { json: body });
  }

  async recaptcha2(opts: {
    image: string;
    question: string;
    async?: boolean;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { image, question, async, ...rest } = opts;
    const body: Record<string, unknown> = { image, question, ...rest };
    if (async !== undefined) body.async = async;
    return this.transport.request('POST', '/captcha/recognition/recaptcha2', { json: body });
  }
}

class Token {
  constructor(private transport: Transport) {}

  async hcaptcha(opts: {
    websiteKey: string;
    websiteUrl: string;
    async?: boolean;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { websiteKey, websiteUrl, async, ...rest } = opts;
    const body: Record<string, unknown> = {
      website_key: websiteKey,
      website_url: websiteUrl,
      ...rest,
    };
    if (async !== undefined) body.async = async;
    return this.transport.request('POST', '/captcha/token/hcaptcha', { json: body });
  }

  async recaptcha2(opts: {
    websiteKey: string;
    websiteUrl: string;
    async?: boolean;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { websiteKey, websiteUrl, async, ...rest } = opts;
    const body: Record<string, unknown> = {
      website_key: websiteKey,
      website_url: websiteUrl,
      ...rest,
    };
    if (async !== undefined) body.async = async;
    return this.transport.request('POST', '/captcha/token/recaptcha2', { json: body });
  }

  async recaptcha3(opts: {
    websiteKey: string;
    websiteUrl: string;
    pageAction: string;
    async?: boolean;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { websiteKey, websiteUrl, pageAction, async, ...rest } = opts;
    const body: Record<string, unknown> = {
      website_key: websiteKey,
      website_url: websiteUrl,
      page_action: pageAction,
      ...rest,
    };
    if (async !== undefined) body.async = async;
    return this.transport.request('POST', '/captcha/token/recaptcha3', { json: body });
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
