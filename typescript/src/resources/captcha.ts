/** Captcha recognition and token resources (`/captcha/*`). */

import { Transport } from '../runtime/transport';

class RecognitionNamespace {
  constructor(private transport: Transport) {}

  hcaptcha(opts: {
    queries?: unknown[];
    question?: string;
    async?: boolean;
    [key: string]: unknown;
  } = {}): Promise<Record<string, unknown>> {
    const { queries, question, async: asyncFlag, ...rest } = opts;
    const body: Record<string, unknown> = { ...rest };
    if (queries !== undefined) body.queries = queries;
    if (question !== undefined) body.question = question;
    if (asyncFlag !== undefined) body.async = asyncFlag;
    return this.transport.request('POST', '/captcha/recognition/hcaptcha', { json: body });
  }

  image2text(opts: {
    image: string;
    async?: boolean;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { image, async: asyncFlag, ...rest } = opts;
    const body: Record<string, unknown> = { image, ...rest };
    if (asyncFlag !== undefined) body.async = asyncFlag;
    return this.transport.request('POST', '/captcha/recognition/image2text', { json: body });
  }

  recaptcha2(opts: {
    image: string;
    question: string;
    async?: boolean;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { image, question, async: asyncFlag, ...rest } = opts;
    const body: Record<string, unknown> = { image, question, ...rest };
    if (asyncFlag !== undefined) body.async = asyncFlag;
    return this.transport.request('POST', '/captcha/recognition/recaptcha2', { json: body });
  }
}

class TokenNamespace {
  constructor(private transport: Transport) {}

  hcaptcha(opts: {
    websiteKey: string;
    websiteUrl: string;
    proxy?: string;
    async?: boolean;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { websiteKey, websiteUrl, proxy, async: asyncFlag, ...rest } = opts;
    const body: Record<string, unknown> = { website_key: websiteKey, website_url: websiteUrl, ...rest };
    if (proxy !== undefined) body.proxy = proxy;
    if (asyncFlag !== undefined) body.async = asyncFlag;
    return this.transport.request('POST', '/captcha/token/hcaptcha', { json: body });
  }

  recaptcha2(opts: {
    websiteKey: string;
    websiteUrl: string;
    proxy?: string;
    async?: boolean;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { websiteKey, websiteUrl, proxy, async: asyncFlag, ...rest } = opts;
    const body: Record<string, unknown> = { website_key: websiteKey, website_url: websiteUrl, ...rest };
    if (proxy !== undefined) body.proxy = proxy;
    if (asyncFlag !== undefined) body.async = asyncFlag;
    return this.transport.request('POST', '/captcha/token/recaptcha2', { json: body });
  }

  recaptcha3(opts: {
    websiteKey: string;
    websiteUrl: string;
    pageAction: string;
    async?: boolean;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { websiteKey, websiteUrl, pageAction, async: asyncFlag, ...rest } = opts;
    const body: Record<string, unknown> = {
      website_key: websiteKey,
      website_url: websiteUrl,
      page_action: pageAction,
      ...rest,
    };
    if (asyncFlag !== undefined) body.async = asyncFlag;
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
    const { websiteKey, websiteUrl, action, cdata, async: asyncFlag, ...rest } = opts;
    const body: Record<string, unknown> = { website_key: websiteKey, website_url: websiteUrl, ...rest };
    if (action !== undefined) body.action = action;
    if (cdata !== undefined) body.cdata = cdata;
    if (asyncFlag !== undefined) body.async = asyncFlag;
    return this.transport.request('POST', '/captcha/token/turnstile', { json: body });
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
