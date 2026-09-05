import { Fish } from '../src/resources/providers/fish';

describe('Fish provider', () => {
  it('lists models with GET query parameters', async () => {
    const request = jest.fn().mockResolvedValue({ data: [] });
    const fish = new Fish({ request } as any);

    await fish.model({ pageSize: 20, self: false, tag: 'demo' });

    expect(request).toHaveBeenCalledWith('GET', '/fish/model', {
      params: {
        page_size: '20',
        page_number: '1',
        self: 'false',
        tag: 'demo',
      },
    });
  });

  it('gets a model by id with an encoded GET path', async () => {
    const request = jest.fn().mockResolvedValue({ _id: 'voice/one' });
    const fish = new Fish({ request } as any);

    await fish.model_by_id({ id: 'voice/one' });

    expect(request).toHaveBeenCalledWith('GET', '/fish/model/voice%2Fone', { params: {} });
  });
});
