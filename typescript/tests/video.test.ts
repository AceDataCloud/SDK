import { Tasks } from '../src/resources/tasks';
import { Video } from '../src/resources/video';

describe('Video resource', () => {
  it('supports gemini video generation parameters', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'task-gemini' });
    const video = new Video({ request } as any);

    await video.generate({
      provider: 'gemini',
      prompt: 'A kitten running through a garden',
      model: 'omni-flash',
      aspectRatio: '16:9',
      imageUrls: ['https://example.com/reference.png'],
      callbackUrl: 'https://example.com/callback',
    });

    expect(request).toHaveBeenCalledWith('POST', '/gemini/videos', {
      json: {
        prompt: 'A kitten running through a garden',
        model: 'omni-flash',
        aspect_ratio: '16:9',
        image_urls: ['https://example.com/reference.png'],
        callback_url: 'https://example.com/callback',
      },
    });
  });
});

describe('Tasks resource', () => {
  it('uses the gemini task endpoint', async () => {
    const request = jest.fn().mockResolvedValue({ response: { status: 'queued' } });
    const tasks = new Tasks({ request } as any);

    await tasks.get('task-gemini', { service: 'gemini' });

    expect(request).toHaveBeenCalledWith('POST', '/gemini/tasks', {
      json: { id: 'task-gemini', action: 'retrieve' },
    });
  });
});
