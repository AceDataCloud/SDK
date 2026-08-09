/** Search resources. */

import { Transport } from '../runtime/transport';

export type SearchType = 'search' | 'images' | 'news' | 'maps' | 'places' | 'videos';
export type SearchRange = 'h' | 'd' | 'w' | 'm' | 'y' | 'qdr:h' | 'qdr:d' | 'qdr:w' | 'qdr:m' | 'qdr:y';
export type SearchImageSize =
  | 'large'
  | 'medium'
  | 'icon'
  | '2mp'
  | '4mp'
  | '6mp'
  | '8mp'
  | '10mp'
  | '12mp'
  | '15mp'
  | '20mp'
  | '40mp'
  | '70mp';

export class Search {
  constructor(private transport: Transport) {}

  async google(opts: {
    query: string;
    type?: SearchType;
    country?: string;
    language?: string;
    page?: number;
    range?: SearchRange;
    number?: number;
    image_size?: SearchImageSize;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { query, type = 'search', country, language, page, range, number, image_size, ...rest } = opts;
    const body: Record<string, unknown> = { query, type, ...rest };
    if (country !== undefined) body.country = country;
    if (language !== undefined) body.language = language;
    if (page !== undefined) body.page = page;
    if (range !== undefined) body.range = range;
    if (number !== undefined) body.number = number;
    if (image_size !== undefined) body.image_size = image_size;
    return this.transport.request('POST', '/serp/google', { json: body });
  }
}
