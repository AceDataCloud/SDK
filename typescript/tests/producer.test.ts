import { Producer } from '../src/resources/providers/producer';

describe('Producer provider', () => {
  it('serializes the lyrics prompt as a string', async () => {
    const request = jest.fn().mockResolvedValue({ lyrics: 'Verse' });
    const producer = new Producer({ request } as any);

    await producer.lyrics({ prompt: 'Write a summer chorus' });

    expect(request).toHaveBeenCalledWith('POST', '/producer/lyrics', {
      json: { prompt: 'Write a summer chorus' },
    });
  });
});
