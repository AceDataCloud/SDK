/** Search resources. */

import { Transport } from '../runtime/transport';

export type SerpRange =
  | 'h'
  | 'd'
  | 'w'
  | 'm'
  | 'y'
  | 'qdr:h'
  | 'qdr:d'
  | 'qdr:w'
  | 'qdr:m'
  | 'qdr:y';
export type SerpImageSize =
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

const SERP_RANGES = new Set<SerpRange>([
  'h',
  'd',
  'w',
  'm',
  'y',
  'qdr:h',
  'qdr:d',
  'qdr:w',
  'qdr:m',
  'qdr:y',
]);
const SERP_IMAGE_SIZES = new Set<SerpImageSize>([
  'large',
  'medium',
  'icon',
  '2mp',
  '4mp',
  '6mp',
  '8mp',
  '10mp',
  '12mp',
  '15mp',
  '20mp',
  '40mp',
  '70mp',
]);

export interface GoogleSearchOptions {
  query: string;
  type?: string;
  country?: string;
  language?: string;
  page?: number;
  number?: number;
  range?: SerpRange;
  imageSize?: SerpImageSize;
  [key: string]: unknown;
}

function validateGoogleOptions(opts: GoogleSearchOptions): void {
  if (opts.query.trim().length === 0 || opts.query.length > 2048) {
    throw new Error('query must contain 1 to 2048 characters and cannot be blank');
  }
  if (opts.page !== undefined && (!Number.isInteger(opts.page) || opts.page < 1 || opts.page > 100)) {
    throw new Error('page must be an integer between 1 and 100');
  }
  if (opts.number !== undefined && (!Number.isInteger(opts.number) || opts.number < 1 || opts.number > 100)) {
    throw new Error('number must be an integer between 1 and 100');
  }
  if (opts.country !== undefined && (opts.country.length < 1 || opts.country.length > 32)) {
    throw new Error('country must contain 1 to 32 characters');
  }
  if (opts.language !== undefined && (opts.language.length < 1 || opts.language.length > 32)) {
    throw new Error('language must contain 1 to 32 characters');
  }
  if (opts.range !== undefined && !SERP_RANGES.has(opts.range)) {
    throw new Error('range is invalid');
  }
  if (opts.imageSize !== undefined && !SERP_IMAGE_SIZES.has(opts.imageSize)) {
    throw new Error('imageSize is invalid');
  }
}

export class Search {
  constructor(private transport: Transport) {}

  async google(opts: GoogleSearchOptions): Promise<Record<string, unknown>> {
    validateGoogleOptions(opts);
    const {
      query,
      type = 'search',
      country,
      language,
      page = 1,
      number = 10,
      range,
      imageSize,
      ...rest
    } = opts;
    const body: Record<string, unknown> = { query, type, page, number, ...rest };
    if (country !== undefined) body.country = country;
    if (language !== undefined) body.language = language;
    if (range !== undefined) body.range = range;
    if (imageSize !== undefined) body.image_size = imageSize;
    return this.transport.request('POST', '/serp/google', { json: body });
  }
}
