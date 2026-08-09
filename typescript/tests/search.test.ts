import { Search } from '../src/resources/search';

describe('Search resource', () => {
  it('sends new SERP parameters to /serp/google', async () => {
    const request = jest.fn().mockResolvedValue({ ok: true });
    const search = new Search({ request } as any);

    await search.google({
      query: 'example',
      type: 'images',
      range: 'qdr:d',
      number: 20,
      image_size: '4mp',
    });

    expect(request).toHaveBeenCalledWith('POST', '/serp/google', {
      json: {
        query: 'example',
        type: 'images',
        range: 'qdr:d',
        number: 20,
        image_size: '4mp',
      },
    });
  });
});
