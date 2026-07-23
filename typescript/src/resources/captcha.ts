/** Captcha recognition and token resources (`/captcha/*`). */

import { Transport } from '../runtime/transport';

class Recognition {
  constructor(private transport: Transport) {}

  async hcaptcha(opts: {
    queries?: string[];
    question?: string;
    async?: boolean;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { async: isAsync, ...rest } = opts;
    const body: Record<string, unknown> = { ...rest };
    if (isAsync !== undefined) body.async = isAsync;
    return this.transport.request('POST', '/captcha/recognition/hcaptcha', { json: body });
  }

  async image2text(opts: {
    image: string;
    async?: boolean;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { image, async: isAsync, ...rest } = opts;
    const body: Record<string, unknown> = { image, ...rest };
    if (isAsync !== undefined) body.async = isAsync;
    return this.transport.request('POST', '/captcha/recognition/image2text', { json: body });
  }

  async recaptcha2(opts: {
    image: string;
    question: string;
    async?: boolean;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { image, question, async: isAsync, ...rest } = opts;
    const body: Record<string, unknown> = { image, question, ...rest };
    if (isAsync !== undefined) body.async = isAsync;
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
    const { websiteKey, websiteUrl, async: isAsync, ...rest } = opts;
    const body: Record<string, unknown> = {
      website_key: websiteKey,
      website_url: websiteUrl,
      ...rest,
    };
    if (isAsync !== undefined) body.async = isAsync;
    return this.transport.request('POST', '/captcha/token/hcaptcha', { json: body });
  }

  async recaptcha2(opts: {
    websiteKey: string;
    websiteUrl: string;
    async?: boolean;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { websiteKey, websiteUrl, async: isAsync, ...rest } = opts;
    const body: Record<string, unknown> = {
      website_key: websiteKey,
      website_url: websiteUrl,
      ...rest,
    };
    if (isAsync !== undefined) body.async = isAsync;
    return this.transport.request('POST', '/captcha/token/recaptcha2', { json: body });
  }

  async recaptcha3(opts: {
    pageAction: string;
    websiteKey: string;
    websiteUrl: string;
    async?: boolean;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { pageAction, websiteKey, websiteUrl, async: isAsync, ...rest } = opts;
    const body: Record<string, unknown> = {
      page_action: pageAction,
      website_key: websiteKey,
      website_url: websiteUrl,
      ...rest,
    };
    if (isAsync !== undefined) body.async = isAsync;
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
