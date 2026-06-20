import { Images } from '../src/resources/images';

describe('Images resource', () => {
  it('sends flux size/count fields to /flux/images', async () => {
    const request = jest.fn().mockResolvedValue({ data: [{ image_url: 'https://example.com/flux.png' }] });
    const images = new Images({ request } as any);

    await images.generate({
      provider: 'flux',
      prompt: 'A white siamese cat',
      action: 'generate',
      size: '1024x1024',
      count: 2,
    });

    expect(request).toHaveBeenCalledWith('POST', '/flux/images', {
      json: {
        prompt: 'A white siamese cat',
        action: 'generate',
        size: '1024x1024',
        count: 2,
      },
    });
  });
});
