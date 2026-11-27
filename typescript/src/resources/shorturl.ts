/** Short URL resource (`/shorturl`). */

import { Transport } from '../runtime/transport';

export class ShortUrl {
  constructor(private transport: Transport) {}

  async create(opts: { url: string; slug?: string; [key: string]: unknown }): Promise<Record<string, unknown>> {
    const { url, slug, ...rest } = opts;
    const body: Record<string, unknown> = { url, ...rest };
    if (slug !== undefined) body.slug = slug;
    return this.transport.request('POST', '/shorturl', { json: body });
  }
}
