import { Images } from '../src/resources/images';

describe('Images resource', () => {
  it('normalizes nano-banana requests to the docs schema', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'task-image' });
    const images = new Images({ request } as any);

    await images.generate({
      prompt: 'A cat',
      imageUrl: 'https://example.com/reference.png',
      count: 2,
    });

    expect(request).toHaveBeenCalledWith('POST', '/nano-banana/images', {
      json: {
        prompt: 'A cat',
        action: 'generate',
        image_urls: ['https://example.com/reference.png'],
        count: 2,
      },
    });
  });

  it('keeps non-nano-banana image payloads unchanged', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'task-image' });
    const images = new Images({ request } as any);

    await images.generate({
      provider: 'flux',
      prompt: 'A cat',
      imageUrl: 'https://example.com/reference.png',
    });

    expect(request).toHaveBeenCalledWith('POST', '/flux/images', {
      json: {
        prompt: 'A cat',
        image_url: 'https://example.com/reference.png',
      },
    });
  });
});
