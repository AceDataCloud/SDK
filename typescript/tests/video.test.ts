import { Video } from '../src/resources/video';

describe('Video resource', () => {
  it('supports gemini endpoint and gemini video parameters', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'task-video' });
    const video = new Video({ request } as any);

    await video.generate({
      provider: 'gemini',
      prompt: 'A cat running in a garden',
      model: 'gemini-2.5-flash-image-preview',
      imageUrls: ['https://example.com/input.png'],
      aspectRatio: '16:9',
      callbackUrl: 'https://example.com/callback',
    });

    expect(request).toHaveBeenCalledWith('POST', '/gemini/videos', {
      json: {
        prompt: 'A cat running in a garden',
        model: 'gemini-2.5-flash-image-preview',
        image_urls: ['https://example.com/input.png'],
        aspect_ratio: '16:9',
        callback_url: 'https://example.com/callback',
      },
    });
  });
});
