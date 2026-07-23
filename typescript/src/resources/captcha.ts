/** Captcha resources (`/captcha/*`). */

import { Transport } from '../runtime/transport';

class RecognitionNamespace {
  constructor(private transport: Transport) {}

  async hcaptcha(opts: {
    queries?: string[];
    question?: string;
    async?: boolean;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
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

class TokenNamespace {
  constructor(private transport: Transport) {}

  async hcaptcha(opts: {
    websiteKey: string;
    websiteUrl: string;
    async?: boolean;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { websiteKey, websiteUrl, ...rest } = opts;
    return this.transport.request('POST', '/captcha/token/hcaptcha', {
      json: {
        website_key: websiteKey,
        website_url: websiteUrl,
        ...rest,
      },
    });
  }

  async recaptcha2(opts: {
    websiteKey: string;
    websiteUrl: string;
    async?: boolean;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { websiteKey, websiteUrl, ...rest } = opts;
    return this.transport.request('POST', '/captcha/token/recaptcha2', {
      json: {
        website_key: websiteKey,
        website_url: websiteUrl,
        ...rest,
      },
    });
  }

  async recaptcha3(opts: {
    pageAction: string;
    websiteKey: string;
    websiteUrl: string;
    async?: boolean;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { pageAction, websiteKey, websiteUrl, ...rest } = opts;
    return this.transport.request('POST', '/captcha/token/recaptcha3', {
      json: {
        page_action: pageAction,
        website_key: websiteKey,
        website_url: websiteUrl,
        ...rest,
      },
    });
  }
}

export class Captcha {
  readonly recognition: RecognitionNamespace;
  readonly token: TokenNamespace;

  constructor(transport: Transport) {
    this.recognition = new RecognitionNamespace(transport);
    this.token = new TokenNamespace(transport);
  }
}
