import { Search } from '../src/resources/search';

describe('Search resource', () => {
  it('sends the documented Google search options', async () => {
    const request = jest.fn().mockResolvedValue({ images: [] });
    const search = new Search({ request } as any);

    await search.google({
      query: 'example',
      type: 'images',
      page: 2,
      range: 'qdr:w',
      number: 20,
      imageSize: '4mp',
    });

    expect(request).toHaveBeenCalledWith('POST', '/serp/google', {
      json: {
        query: 'example',
        type: 'images',
        page: 2,
        range: 'qdr:w',
        number: 20,
        image_size: '4mp',
      },
    });
  });

  it('rejects image filters for non-image searches', async () => {
    const search = new Search({ request: jest.fn() } as any);

    await expect(search.google({ query: 'example', imageSize: '4mp' })).rejects.toThrow(
      "imageSize is only valid when type is 'images'",
    );
  });
});
