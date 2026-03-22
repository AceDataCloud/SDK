/** Search resources. */

import { Transport } from '../runtime/transport';

export class Search {
  constructor(private transport: Transport) {}

  async google(opts: {
    query: string;
    type?: string;
    country?: string;
    language?: string;
    page?: number;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { query, type = 'search', country, language, page, ...rest } = opts;
    const body: Record<string, unknown> = { query, type, ...rest };
    if (country !== undefined) body.country = country;
    if (language !== undefined) body.language = language;
    if (page !== undefined) body.page = page;
    return this.transport.request('POST', '/serp/google', { json: body });
  }
}
