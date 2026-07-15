import { Kling } from '../src/resources/kling';
import { Tasks } from '../src/resources/tasks';
import { Video } from '../src/resources/video';

describe('Video resource', () => {
  it('supports gemini video parameters on /gemini/videos', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'task-gemini' });
    const video = new Video({ request } as any);

    await video.generate({
      prompt: 'hello',
      provider: 'gemini',
      imageUrls: ['https://example.com/1.png'],
      videoUrls: ['https://example.com/1.mp4'],
      aspectRatio: '16:9',
      resolution: '1080p',
      callbackUrl: 'https://example.com/callback',
    });

    expect(request).toHaveBeenCalledWith('POST', '/gemini/videos', {
      json: {
        prompt: 'hello',
        image_urls: ['https://example.com/1.png'],
        video_urls: ['https://example.com/1.mp4'],
        aspect_ratio: '16:9',
        resolution: '1080p',
        callback_url: 'https://example.com/callback',
      },
    });
  });
});

describe('Tasks resource', () => {
  it('uses the gemini tasks endpoint', async () => {
    const request = jest.fn().mockResolvedValue({ id: 'task-gemini' });
    const tasks = new Tasks({ request } as any);

    await tasks.get('task-gemini', { service: 'gemini' });

    expect(request).toHaveBeenCalledWith('POST', '/gemini/tasks', {
      json: { id: 'task-gemini', action: 'retrieve' },
    });
  });
});

describe('Kling resource', () => {
  it('maps imageList and legacy videoList to image_list', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'task-kling' });
    const kling = new Kling({ request } as any);

    await kling.generate({
      action: 'image2video',
      imageList: [{ image_url: 'https://example.com/a.png' }],
    });
    await kling.generate({
      action: 'image2video',
      videoList: [{ image_url: 'https://example.com/b.png' }],
    });

    expect(request).toHaveBeenNthCalledWith(1, 'POST', '/kling/videos', {
      json: {
        action: 'image2video',
        image_list: [{ image_url: 'https://example.com/a.png' }],
      },
    });
    expect(request).toHaveBeenNthCalledWith(2, 'POST', '/kling/videos', {
      json: {
        action: 'image2video',
        image_list: [{ image_url: 'https://example.com/b.png' }],
      },
    });
  });

  it('sends motion model_name and watermark_info', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'task-motion' });
    const kling = new Kling({ request } as any);

    await kling.motion({
      mode: 'pro',
      imageUrl: 'https://example.com/source.png',
      videoUrl: 'https://example.com/driver.mp4',
      characterOrientation: 'image',
      modelName: 'kling-v3',
      watermarkInfo: true,
    });

    expect(request).toHaveBeenCalledWith('POST', '/kling/motion', {
      json: {
        mode: 'pro',
        image_url: 'https://example.com/source.png',
        video_url: 'https://example.com/driver.mp4',
        character_orientation: 'image',
        model_name: 'kling-v3',
        watermark_info: true,
      },
    });
  });
});
