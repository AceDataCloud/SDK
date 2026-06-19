import { Tasks } from '../src/resources/tasks';
import { Video } from '../src/resources/video';

describe('Video resource', () => {
  it('maps dreamina request fields to /dreamina/videos', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'task-dreamina' });
    const video = new Video({ request } as any);

    await video.generate({
      provider: 'dreamina',
      prompt: 'Animate this portrait',
      model: 'omnihuman-1.5',
      imageUrl: 'https://cdn.acedata.cloud/image.jpg',
      audioUrl: 'https://cdn.acedata.cloud/audio.mp3',
      maskUrl: ['https://cdn.acedata.cloud/mask.png'],
    });

    expect(request).toHaveBeenCalledWith('POST', '/dreamina/videos', {
      json: {
        prompt: 'Animate this portrait',
        model: 'omnihuman-1.5',
        image_url: 'https://cdn.acedata.cloud/image.jpg',
        audio_url: 'https://cdn.acedata.cloud/audio.mp3',
        mask_url: ['https://cdn.acedata.cloud/mask.png'],
      },
    });
  });

  it('maps grok request fields to /grok/videos', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'task-grok' });
    const video = new Video({ request } as any);

    await video.generate({
      provider: 'grok',
      prompt: 'A city timelapse',
      model: 'grok-imagine-video',
      imageUrl: 'https://cdn.acedata.cloud/image.jpg',
      referenceImageUrls: ['https://cdn.acedata.cloud/ref.jpg'],
      aspectRatio: '16:9',
      resolution: '720p',
      duration: 10,
    });

    expect(request).toHaveBeenCalledWith('POST', '/grok/videos', {
      json: {
        prompt: 'A city timelapse',
        model: 'grok-imagine-video',
        image_url: 'https://cdn.acedata.cloud/image.jpg',
        reference_image_urls: ['https://cdn.acedata.cloud/ref.jpg'],
        aspect_ratio: '16:9',
        resolution: '720p',
        duration: 10,
      },
    });
  });
});

describe('Tasks resource', () => {
  it('uses explicit grok and dreamina task endpoints', async () => {
    const request = jest.fn().mockResolvedValue({ response: { status: 'processing' } });
    const tasks = new Tasks({ request } as any);

    await tasks.get('task-grok', { service: 'grok' });
    await tasks.get('task-dreamina', { service: 'dreamina' });

    expect(request).toHaveBeenNthCalledWith(1, 'POST', '/grok/tasks', {
      json: { id: 'task-grok', action: 'retrieve' },
    });
    expect(request).toHaveBeenNthCalledWith(2, 'POST', '/dreamina/tasks', {
      json: { id: 'task-dreamina', action: 'retrieve' },
    });
  });
});
