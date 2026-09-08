/** Short URL resource (`/shorturl`). */

import { Transport } from '../runtime/transport';

export class ShortUrl {
  constructor(private transport: Transport) {}

  async create(opts: { content?: string; url?: string; slug?: string; [key: string]: unknown }): Promise<Record<string, unknown>> {
    const { content, url, slug, ...rest } = opts;
    const bodyContent = content ?? url;
    if (bodyContent === undefined) {
      throw new Error('Either `content` or legacy `url` must be provided.');
    }
    const body: Record<string, unknown> = { content: bodyContent, ...rest };
    if (slug !== undefined) body.slug = slug;
    return this.transport.request('POST', '/shorturl', { json: body });
  }
}
