import { Producer } from '../src/resources/providers/producer';

describe('Producer provider', () => {
  it('serializes lyrics prompt as a string', async () => {
    const request = jest.fn().mockResolvedValue({ lyrics: 'snow falls' });
    const producer = new Producer({ request } as any);

    await producer.lyrics({ prompt: 'A song about winter' });

    expect(request).toHaveBeenCalledWith('POST', '/producer/lyrics', {
      json: {
        prompt: 'A song about winter',
      },
    });
  });
});
