/** Captcha recognition and token resources. */

import { Transport } from '../runtime/transport';

class Recognition {
  constructor(private transport: Transport) {}

  async hcaptcha(opts: {
    queries?: Array<Record<string, unknown>>;
    question?: string;
    async?: boolean;
    [key: string]: unknown;
  } = {}): Promise<Record<string, unknown>> {
    return this.transport.request('POST', '/captcha/recognition/hcaptcha', { json: opts });
  }

  async image2text(opts: {
    image: string;
    async?: boolean;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    return this.transport.request('POST', '/captcha/recognition/image2text', { json: opts });
  }

  async recaptcha2(opts: {
    image: string;
    question: string;
    async?: boolean;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    return this.transport.request('POST', '/captcha/recognition/recaptcha2', { json: opts });
  }
}

class Token {
  constructor(private transport: Transport) {}

  async hcaptcha(opts: {
    websiteKey: string;
    websiteUrl: string;
    proxy?: string;
    async?: boolean;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { websiteKey, websiteUrl, proxy, ...rest } = opts;
    const body: Record<string, unknown> = { website_key: websiteKey, website_url: websiteUrl, ...rest };
    if (proxy !== undefined) body.proxy = proxy;
    return this.transport.request('POST', '/captcha/token/hcaptcha', { json: body });
  }

  async recaptcha2(opts: {
    websiteKey: string;
    websiteUrl: string;
    proxy?: string;
    async?: boolean;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { websiteKey, websiteUrl, proxy, ...rest } = opts;
    const body: Record<string, unknown> = { website_key: websiteKey, website_url: websiteUrl, ...rest };
    if (proxy !== undefined) body.proxy = proxy;
    return this.transport.request('POST', '/captcha/token/recaptcha2', { json: body });
  }

  async recaptcha3(opts: {
    pageAction: string;
    websiteKey: string;
    websiteUrl: string;
    async?: boolean;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { pageAction, websiteKey, websiteUrl, ...rest } = opts;
    const body: Record<string, unknown> = { page_action: pageAction, website_key: websiteKey, website_url: websiteUrl, ...rest };
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
