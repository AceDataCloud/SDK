/** Turnstile captcha resource (`/captcha/token/turnstile`). */

import { Transport } from '../runtime/transport';

export class Turnstile {
  constructor(private transport: Transport) {}

  async token(opts: {
    websiteKey: string;
    websiteUrl: string;
    action?: string;
    cdata?: string;
    async?: boolean;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { websiteKey, websiteUrl, action, cdata, ...rest } = opts;
    const body: Record<string, unknown> = { website_key: websiteKey, website_url: websiteUrl, ...rest };
    if (action !== undefined) body.action = action;
    if (cdata !== undefined) body.cdata = cdata;
    return this.transport.request('POST', '/captcha/token/turnstile', { json: body });
  }
}
