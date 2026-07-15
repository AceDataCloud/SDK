import { Kling } from '../src/resources/kling';

describe('Kling resource', () => {
  it('includes model_name and watermark_info in motion payload', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'task-kling-motion' });
    const kling = new Kling({ request } as any);

    await kling.motion({
      mode: 'std',
      imageUrl: 'https://example.com/image.png',
      videoUrl: 'https://example.com/video.mp4',
      characterOrientation: 'image',
      modelName: 'kling-v3',
      watermarkInfo: { text: 'ace' },
    });

    expect(request).toHaveBeenCalledWith('POST', '/kling/motion', {
      json: {
        mode: 'std',
        image_url: 'https://example.com/image.png',
        video_url: 'https://example.com/video.mp4',
        character_orientation: 'image',
        model_name: 'kling-v3',
        watermark_info: { text: 'ace' },
      },
    });
  });

  it('calls /kling/lip-sync with mapped payload fields', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'task-kling-lipsync' });
    const kling = new Kling({ request } as any);

    await kling.lipSync({
      mode: 'text2video',
      videoId: 'video-1',
      text: 'hello',
      voiceLanguage: 'en',
      voiceSpeed: 1.2,
      callbackUrl: 'https://example.com/callback',
    });

    expect(request).toHaveBeenCalledWith('POST', '/kling/lip-sync', {
      json: {
        mode: 'text2video',
        video_id: 'video-1',
        text: 'hello',
        voice_language: 'en',
        voice_speed: 1.2,
        callback_url: 'https://example.com/callback',
      },
    });
  });

  it('calls /kling/talking-photo with required fields', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'task-kling-talking-photo' });
    const kling = new Kling({ request } as any);

    await kling.talkingPhoto({
      imageUrl: 'https://example.com/image.png',
      audioUrl: 'https://example.com/audio.mp3',
      mode: 'pro',
      duration: 10,
    });

    expect(request).toHaveBeenCalledWith('POST', '/kling/talking-photo', {
      json: {
        image_url: 'https://example.com/image.png',
        audio_url: 'https://example.com/audio.mp3',
        mode: 'pro',
        duration: 10,
      },
    });
  });
});
