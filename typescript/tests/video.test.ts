import { Video } from '../src/resources/video';

describe('Video resource', () => {
  it('supports gemini provider endpoint and gemini parameters', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'task-gemini' });
    const video = new Video({ request } as any);

    await video.generate({
      provider: 'gemini',
      prompt: 'a short clip',
      model: 'veo-3.0-generate-preview',
      imageUrls: ['https://example.com/input.png'],
      aspectRatio: '16:9',
    });

    expect(request).toHaveBeenCalledWith('POST', '/gemini/videos', {
      json: {
        prompt: 'a short clip',
        model: 'veo-3.0-generate-preview',
        image_urls: ['https://example.com/input.png'],
        aspect_ratio: '16:9',
      },
    });
  });
});
