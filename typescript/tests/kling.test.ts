import { Kling } from '../src/resources/kling';

describe('Kling resource', () => {
  it('forwards motion-specific optional fields to /kling/motion', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'task-motion' });
    const kling = new Kling({ request } as any);

    await kling.motion({
      modelName: 'kling-v3',
      mode: 'pro',
      watermarkInfo: { enabled: true },
      imageUrl: 'https://example.com/image.png',
      videoUrl: 'https://example.com/video.mp4',
      characterOrientation: 'image',
      keepOriginalSound: 'yes',
      callbackUrl: 'https://example.com/callback',
      async: true,
    });

    expect(request).toHaveBeenCalledWith('POST', '/kling/motion', {
      json: {
        model_name: 'kling-v3',
        mode: 'pro',
        watermark_info: { enabled: true },
        image_url: 'https://example.com/image.png',
        video_url: 'https://example.com/video.mp4',
        character_orientation: 'image',
        keep_original_sound: 'yes',
        callback_url: 'https://example.com/callback',
        async: true,
      },
    });
  });

  it('calls the lip-sync and talking-photo endpoints with mapped fields', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'task-kling' });
    const kling = new Kling({ request } as any);

    await kling.lipSync({
      mode: 'text2video',
      videoUrl: 'https://example.com/source.mp4',
      text: 'Hello world',
      voiceLanguage: 'en',
      voiceSpeed: 1.2,
      callbackUrl: 'https://example.com/lip-sync',
      async: true,
    });

    await kling.talkingPhoto({
      imageUrl: 'https://example.com/portrait.png',
      audioUrl: 'https://example.com/audio.mp3',
      prompt: 'Speak naturally',
      model: 'kling-v2-6',
      duration: 10,
      mode: 'pro',
      callbackUrl: 'https://example.com/talking-photo',
      async: true,
    });

    expect(request).toHaveBeenNthCalledWith(1, 'POST', '/kling/lip-sync', {
      json: {
        mode: 'text2video',
        video_url: 'https://example.com/source.mp4',
        text: 'Hello world',
        voice_language: 'en',
        voice_speed: 1.2,
        callback_url: 'https://example.com/lip-sync',
        async: true,
      },
    });
    expect(request).toHaveBeenNthCalledWith(2, 'POST', '/kling/talking-photo', {
      json: {
        image_url: 'https://example.com/portrait.png',
        audio_url: 'https://example.com/audio.mp3',
        prompt: 'Speak naturally',
        model: 'kling-v2-6',
        duration: 10,
        mode: 'pro',
        callback_url: 'https://example.com/talking-photo',
        async: true,
      },
    });
  });
});
