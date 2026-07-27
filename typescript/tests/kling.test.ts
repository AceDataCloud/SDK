import { Kling } from '../src/resources/kling';

describe('Kling resource', () => {
  it('serializes canonical Omni references and async polling', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'task-kling' });
    const kling = new Kling({ request } as any);

    await kling.generate({
      action: 'text2video',
      model: 'kling-o1',
      prompt: 'Use the references',
      mode: 'std',
      duration: 5,
      async: true,
      timeout: 600,
      imageList: [{ imageUrl: 'https://example.com/ref.jpg' }],
      videoList: [
        {
          videoUrl: 'https://example.com/ref.mp4',
          referType: 'feature',
          keepOriginalSound: 'yes',
        },
      ],
    });

    expect(request).toHaveBeenCalledWith('POST', '/kling/videos', {
      json: {
        action: 'text2video',
        model: 'kling-o1',
        prompt: 'Use the references',
        mode: 'std',
        duration: 5,
        async: true,
        timeout: 600,
        image_list: [{ image_url: 'https://example.com/ref.jpg' }],
        video_list: [
          {
            video_url: 'https://example.com/ref.mp4',
            refer_type: 'feature',
            keep_original_sound: 'yes',
          },
        ],
      },
    });
  });

  it('rejects references on non-Omni models before transport', async () => {
    const request = jest.fn();
    const kling = new Kling({ request } as any);

    await expect(
      kling.generate({
        action: 'text2video',
        model: 'kling-v3',
        prompt: 'test',
        imageList: [{ imageUrl: 'https://example.com/ref.jpg' }],
      })
    ).rejects.toThrow('Omni references require');
    expect(request).not.toHaveBeenCalled();
  });

  it('rejects an unknown runtime model before transport', async () => {
    const request = jest.fn();
    const kling = new Kling({ request } as any);

    await expect(
      kling.generate({
        action: 'text2video',
        model: 'unknown-model',
        prompt: 'test',
      } as any)
    ).rejects.toThrow('model must be one of');
    expect(request).not.toHaveBeenCalled();
  });

  it('rejects invalid O1 duration and duplicate first frames', async () => {
    const kling = new Kling({ request: jest.fn() } as any);

    await expect(
      kling.generate({
        action: 'text2video',
        model: 'kling-o1',
        prompt: 'test',
        duration: 10,
      })
    ).rejects.toThrow('only 5-second');

    await expect(
      kling.generate({
        action: 'image2video',
        model: 'kling-v3-omni',
        prompt: 'test',
        startImageUrl: 'https://example.com/start.jpg',
        imageList: [{ imageUrl: 'https://example.com/other.jpg', type: 'first_frame' }],
      })
    ).rejects.toThrow('Only one first frame');
  });

  it('rejects extend on unsupported models', async () => {
    const kling = new Kling({ request: jest.fn() } as any);

    await expect(
      kling.generate({
        action: 'extend',
        model: 'kling-v3',
        videoId: 'video-1',
      })
    ).rejects.toThrow('extend requires');
  });

  it('rejects a base reference video combined with frames', async () => {
    const kling = new Kling({ request: jest.fn() } as any);

    await expect(
      kling.generate({
        action: 'image2video',
        model: 'kling-v3-omni',
        prompt: 'test',
        startImageUrl: 'https://example.com/start.jpg',
        videoList: [{ videoUrl: 'https://example.com/base.mp4', referType: 'base' }],
      })
    ).rejects.toThrow('base reference video');
  });

  it('rejects explicit empty reference arrays before transport', async () => {
    const request = jest.fn();
    const kling = new Kling({ request } as any);

    await expect(
      kling.generate({
        action: 'text2video',
        model: 'kling-o1',
        prompt: 'test',
        imageList: [],
      })
    ).rejects.toThrow('imageList must be non-empty');
    await expect(
      kling.generate({
        action: 'text2video',
        model: 'kling-o1',
        prompt: 'test',
        videoList: [],
      })
    ).rejects.toThrow('videoList must be non-empty');
    expect(request).not.toHaveBeenCalled();
  });

  it('serializes motion from an explicit closed contract', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'task-motion' });
    const kling = new Kling({ request } as any);

    await kling.motion({
      mode: 'pro',
      imageUrl: 'https://example.com/subject.jpg',
      videoUrl: 'https://example.com/motion.mp4',
      characterOrientation: 'image',
      keepOriginalSound: 'yes',
      prompt: 'follow the motion',
      async: true,
    });

    expect(request).toHaveBeenCalledWith('POST', '/kling/motion', {
      json: {
        mode: 'pro',
        image_url: 'https://example.com/subject.jpg',
        video_url: 'https://example.com/motion.mp4',
        character_orientation: 'image',
        keep_original_sound: 'yes',
        prompt: 'follow the motion',
        async: true,
      },
    });
  });

  it('rejects malformed motion and callback URLs before transport', async () => {
    const request = jest.fn();
    const kling = new Kling({ request } as any);

    await expect(
      kling.motion({
        mode: 'std',
        imageUrl: 'https://example.com/subject.jpg',
        videoUrl: 'file:///tmp/motion.mp4',
        characterOrientation: 'video',
      })
    ).rejects.toThrow('videoUrl must be an HTTP URL');
    await expect(
      kling.generate({
        action: 'text2video',
        model: 'kling-v3',
        prompt: 'test',
        callbackUrl: 'not-a-url',
      })
    ).rejects.toThrow('callbackUrl must be an HTTP URL');
    expect(request).not.toHaveBeenCalled();
  });

  it('rejects invalid reference enums and audio with video before transport', async () => {
    const request = jest.fn();
    const kling = new Kling({ request } as any);

    await expect(
      kling.generate({
        action: 'text2video',
        model: 'kling-o1',
        prompt: 'test',
        imageList: [{ imageUrl: 'https://example.com/ref.jpg', type: 'invalid' }],
      } as any)
    ).rejects.toThrow('type must be first_frame or end_frame');
    await expect(
      kling.generate({
        action: 'text2video',
        model: 'kling-o1',
        prompt: 'test',
        videoList: [{ videoUrl: 'https://example.com/ref.mp4', referType: 'invalid' }],
      } as any)
    ).rejects.toThrow('referType must be base or feature');
    await expect(
      kling.generate({
        action: 'text2video',
        model: 'kling-o1',
        prompt: 'test',
        videoList: [{ videoUrl: 'https://example.com/ref.mp4', referType: 'feature', keepOriginalSound: 'invalid' }],
      } as any)
    ).rejects.toThrow('keepOriginalSound must be yes or no');
    await expect(
      kling.generate({
        action: 'text2video',
        model: 'kling-v3-omni',
        prompt: 'test',
        generateAudio: true,
        videoList: [{ videoUrl: 'https://example.com/ref.mp4', referType: 'feature' }],
      })
    ).rejects.toThrow('generateAudio cannot be used with videoList');
    expect(request).not.toHaveBeenCalled();
  });

  it('serializes motion with modelName and watermarkInfo', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'task-motion' });
    const kling = new Kling({ request } as any);

    await kling.motion({
      mode: 'pro',
      imageUrl: 'https://example.com/subject.jpg',
      videoUrl: 'https://example.com/motion.mp4',
      characterOrientation: 'image',
      modelName: 'kling-v3',
      watermarkInfo: { enabled: true },
      async: true,
    });

    expect(request).toHaveBeenCalledWith('POST', '/kling/motion', {
      json: {
        mode: 'pro',
        image_url: 'https://example.com/subject.jpg',
        video_url: 'https://example.com/motion.mp4',
        character_orientation: 'image',
        model_name: 'kling-v3',
        watermark_info: { enabled: true },
        async: true,
      },
    });
  });

  it('serializes lipSync to /kling/lip-sync', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'task-lipsync' });
    const kling = new Kling({ request } as any);

    await kling.lipSync({
      mode: 'audio2video',
      videoUrl: 'https://example.com/video.mp4',
      audioUrl: 'https://example.com/audio.mp3',
      voiceLanguage: 'zh',
      async: true,
    });

    expect(request).toHaveBeenCalledWith('POST', '/kling/lip-sync', {
      json: {
        mode: 'audio2video',
        video_url: 'https://example.com/video.mp4',
        audio_url: 'https://example.com/audio.mp3',
        voice_language: 'zh',
        async: true,
      },
    });
  });

  it('rejects invalid lipSync mode before transport', async () => {
    const request = jest.fn();
    const kling = new Kling({ request } as any);

    await expect(
      kling.lipSync({ mode: 'invalid' as any })
    ).rejects.toThrow('mode must be audio2video or text2video');
    expect(request).not.toHaveBeenCalled();
  });

  it('serializes talkingPhoto to /kling/talking-photo', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'task-talking-photo' });
    const kling = new Kling({ request } as any);

    await kling.talkingPhoto({
      imageUrl: 'https://example.com/photo.jpg',
      audioUrl: 'https://example.com/audio.mp3',
      model: 'kling-v1-6',
      duration: 5,
      mode: 'std',
      async: true,
    });

    expect(request).toHaveBeenCalledWith('POST', '/kling/talking-photo', {
      json: {
        image_url: 'https://example.com/photo.jpg',
        audio_url: 'https://example.com/audio.mp3',
        model: 'kling-v1-6',
        duration: 5,
        mode: 'std',
        async: true,
      },
    });
  });

  it('rejects invalid talkingPhoto duration before transport', async () => {
    const request = jest.fn();
    const kling = new Kling({ request } as any);

    await expect(
      kling.talkingPhoto({
        imageUrl: 'https://example.com/photo.jpg',
        audioUrl: 'https://example.com/audio.mp3',
        duration: 3 as any,
      })
    ).rejects.toThrow('duration must be 5 or 10');
    expect(request).not.toHaveBeenCalled();
  });
});
