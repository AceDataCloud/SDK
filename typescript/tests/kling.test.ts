import { Kling } from '../src/resources/kling';

describe('Kling resource', () => {
  it('calls lip-sync endpoint', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'task-lip-sync' });
    const kling = new Kling({ request } as any);

    await kling.lipSync({
      mode: 'std',
      videoUrl: 'https://cdn.acedata.cloud/v.mp4',
      audioUrl: 'https://cdn.acedata.cloud/a.wav',
      voiceLanguage: 'en',
    });

    expect(request).toHaveBeenCalledWith('POST', '/kling/lip-sync', {
      json: {
        mode: 'std',
        video_url: 'https://cdn.acedata.cloud/v.mp4',
        audio_url: 'https://cdn.acedata.cloud/a.wav',
        voice_language: 'en',
      },
    });
  });
});
