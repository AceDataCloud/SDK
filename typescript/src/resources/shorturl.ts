/** Short URL generation resources. */

import { Transport } from '../runtime/transport';

export class ShortUrl {
  constructor(private transport: Transport) {}

  async create(opts: {
    content?: string;
    [key: string]: unknown;
  } = {}): Promise<Record<string, unknown>> {
    const { content, ...rest } = opts;
    const body: Record<string, unknown> = { ...rest };
    if (content !== undefined) body.content = content;
    return this.transport.request('POST', '/shorturl', { json: body });
  }
}
