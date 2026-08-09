/** Search resources. */

import { Transport } from '../runtime/transport';

export type SearchType = 'search' | 'images' | 'news' | 'maps' | 'places' | 'videos';
export type SearchRange = 'h' | 'd' | 'w' | 'm' | 'y' | 'qdr:h' | 'qdr:d' | 'qdr:w' | 'qdr:m' | 'qdr:y';
export type ImageSize =
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

const searchTypes = new Set<SearchType>(['search', 'images', 'news', 'maps', 'places', 'videos']);
const searchRanges = new Set<SearchRange>(['h', 'd', 'w', 'm', 'y', 'qdr:h', 'qdr:d', 'qdr:w', 'qdr:m', 'qdr:y']);
const imageSizes = new Set<ImageSize>(['large', 'medium', 'icon', '2mp', '4mp', '6mp', '8mp', '10mp', '12mp', '15mp', '20mp', '40mp', '70mp']);

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
    imageSize?: ImageSize;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { query, type = 'search', country, language, page, range, number, imageSize, ...rest } = opts;
    if (query.length < 1 || query.length > 2048 || !query.trim()) {
      throw new Error('query must be 1 to 2048 characters and contain at least one non-whitespace character');
    }
    if (!searchTypes.has(type)) throw new Error(`unsupported search type: ${type}`);
    if (page !== undefined && (page < 1 || page > 100)) throw new Error('page must be between 1 and 100');
    if (number !== undefined && (number < 1 || number > 100)) throw new Error('number must be between 1 and 100');
    if (range !== undefined && !searchRanges.has(range)) throw new Error(`unsupported search range: ${range}`);
    if (country !== undefined && (country.length < 1 || country.length > 32)) throw new Error('country must be 1 to 32 characters');
    if (language !== undefined && (language.length < 1 || language.length > 32)) throw new Error('language must be 1 to 32 characters');
    if (imageSize !== undefined && !imageSizes.has(imageSize)) throw new Error(`unsupported image size: ${imageSize}`);
    if (imageSize !== undefined && type !== 'images') throw new Error("imageSize is only valid when type is 'images'");

    const body: Record<string, unknown> = { query, type, ...rest };
    if (country !== undefined) body.country = country;
    if (language !== undefined) body.language = language;
    if (page !== undefined) body.page = page;
    if (range !== undefined) body.range = range;
    if (number !== undefined) body.number = number;
    if (imageSize !== undefined) body.image_size = imageSize;
    return this.transport.request('POST', '/serp/google', { json: body });
  }
}
