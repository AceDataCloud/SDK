import { Search } from '../src/resources/search';

describe('SERP search contract', () => {
  it('serializes defaults and new filters', async () => {
    const request = jest.fn().mockResolvedValue({ organic_results: [] });
    const search = new Search({ request } as any);

    await search.google({
      query: 'SDK examples',
      country: 'US',
      language: 'en',
      range: 'qdr:w',
      imageSize: '10mp',
    });

    expect(request).toHaveBeenCalledWith('POST', '/serp/google', {
      json: {
        query: 'SDK examples',
        type: 'search',
        page: 1,
        number: 10,
        country: 'US',
        language: 'en',
        range: 'qdr:w',
        image_size: '10mp',
      },
    });
  });

  it.each([
    [{ query: '   ' }, 'query'],
    [{ query: 'test', page: 0 }, 'page'],
    [{ query: 'test', number: 101 }, 'number'],
    [{ query: 'test', country: '' }, 'country'],
    [{ query: 'test', language: 'x'.repeat(33) }, 'language'],
    [{ query: 'test', range: 'invalid' } as any, 'range'],
    [{ query: 'test', imageSize: 'huge' } as any, 'imageSize'],
  ])('rejects invalid options', async (options, message) => {
    const request = jest.fn();
    const search = new Search({ request } as any);

    await expect(search.google(options)).rejects.toThrow(message);
    expect(request).not.toHaveBeenCalled();
  });
});
