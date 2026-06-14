import { Kling } from '../src/resources/kling';

describe('Kling resource', () => {
  it('calls lip-sync endpoint with expected payload fields', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'task-kling-lipsync' });
    const kling = new Kling({ request } as any);

    await kling.lipSync({
      mode: 'text2video',
      videoUrl: 'https://cdn.acedata.cloud/video.mp4',
      text: 'Hello world',
      voiceLanguage: 'en',
      voiceSpeed: 1.1,
      callbackUrl: 'https://example.com/callback',
    });

    expect(request).toHaveBeenCalledWith('POST', '/kling/lip-sync', {
      json: {
        mode: 'text2video',
        video_url: 'https://cdn.acedata.cloud/video.mp4',
        text: 'Hello world',
        voice_language: 'en',
        voice_speed: 1.1,
        callback_url: 'https://example.com/callback',
      },
    });
  });
});
