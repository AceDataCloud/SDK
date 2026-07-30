import { Fish } from '../src/resources/providers/fish';

describe('Fish provider', () => {
  it('calls fish model read endpoints', async () => {
    const request = jest.fn().mockResolvedValue({ data: [] });
    const fish = new Fish({ request } as any);

    await fish.listModels({ pageSize: 10, pageNumber: 2, self: true });
    await fish.getModel('voice-1');

    expect(request).toHaveBeenNthCalledWith(1, 'GET', '/fish/model', {
      params: {
        page_size: '10',
        page_number: '2',
        self: 'true',
      },
    });
    expect(request).toHaveBeenNthCalledWith(2, 'GET', '/fish/model/voice-1');
  });
});
