import { Kling } from '../src/resources/kling';

describe('Kling resource', () => {
  it('maps newly added generate and motion parameters to API fields', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'task-kling' });
    const kling = new Kling({ request } as any);

    await kling.generate({
      action: 'image2video',
      imageList: [{ image_url: 'https://example.com/start.png', type: 'first_frame' }],
    });

    await kling.motion({
      mode: 'std',
      imageUrl: 'https://example.com/image.png',
      videoUrl: 'https://example.com/video.mp4',
      characterOrientation: 'image',
      modelName: 'kling-v3',
      watermarkInfo: { text: 'demo' },
    });

    expect(request).toHaveBeenNthCalledWith(1, 'POST', '/kling/videos', {
      json: {
        action: 'image2video',
        image_list: [{ image_url: 'https://example.com/start.png', type: 'first_frame' }],
      },
    });
    expect(request).toHaveBeenNthCalledWith(2, 'POST', '/kling/motion', {
      json: {
        mode: 'std',
        image_url: 'https://example.com/image.png',
        video_url: 'https://example.com/video.mp4',
        character_orientation: 'image',
        model_name: 'kling-v3',
        watermark_info: { text: 'demo' },
      },
    });
  });

  it('calls kling lip-sync and talking-photo endpoints', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'task-kling-extra' });
    const kling = new Kling({ request } as any);

    await kling.lipSync({
      mode: 'text2video',
      videoId: 'vid-1',
      text: 'hello',
      voiceLanguage: 'en',
    });

    await kling.talkingPhoto({
      imageUrl: 'https://example.com/photo.png',
      audioUrl: 'https://example.com/audio.mp3',
      model: 'kling-v2-6',
    });

    expect(request).toHaveBeenNthCalledWith(1, 'POST', '/kling/lip-sync', {
      json: {
        mode: 'text2video',
        video_id: 'vid-1',
        text: 'hello',
        voice_language: 'en',
      },
    });
    expect(request).toHaveBeenNthCalledWith(2, 'POST', '/kling/talking-photo', {
      json: {
        image_url: 'https://example.com/photo.png',
        audio_url: 'https://example.com/audio.mp3',
        model: 'kling-v2-6',
      },
    });
  });
});
