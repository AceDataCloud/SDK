import { Images } from '../src/resources/images';

describe('Images resource', () => {
  it('keeps default image providers on /{provider}/images', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'task-image' });
    const images = new Images({ request } as any);

    await images.generate({ provider: 'flux', prompt: 'a cat' });

    expect(request).toHaveBeenCalledWith('POST', '/flux/images', {
      json: { prompt: 'a cat' },
    });
  });

  it('routes image2text provider to captcha recognition endpoint', async () => {
    const request = jest.fn().mockResolvedValue({ data: [{ text: '1234' }] });
    const images = new Images({ request } as any);

    await images.generate({
      provider: 'image2text',
      image: 'base64-image',
      async: true,
    });

    expect(request).toHaveBeenCalledWith('POST', '/captcha/recognition/image2text', {
      json: {
        image: 'base64-image',
        async: true,
      },
    });
  });
});
