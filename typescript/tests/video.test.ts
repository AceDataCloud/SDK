import { Tasks } from '../src/resources/tasks';
import { Video } from '../src/resources/video';

describe('Video resource', () => {
  it('supports gemini video params on /gemini/videos', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'task-gemini' });
    const video = new Video({ request } as any);

    await video.generate({
      provider: 'gemini',
      prompt: 'hello',
      model: 'omni-flash',
      imageUrls: ['https://example.com/1.png'],
      aspectRatio: '16:9',
      callbackUrl: 'https://example.com/callback',
    });

    expect(request).toHaveBeenCalledWith('POST', '/gemini/videos', {
      json: {
        prompt: 'hello',
        model: 'omni-flash',
        image_urls: ['https://example.com/1.png'],
        aspect_ratio: '16:9',
        callback_url: 'https://example.com/callback',
      },
    });
  });
});

describe('Tasks resource', () => {
  it('uses the gemini task endpoint', async () => {
    const request = jest.fn().mockResolvedValue({ id: 'task-gemini' });
    const tasks = new Tasks({ request } as any);

    await tasks.get('task-gemini', { service: 'gemini' });

    expect(request).toHaveBeenCalledWith('POST', '/gemini/tasks', {
      json: { id: 'task-gemini', action: 'retrieve' },
    });
  });
});
