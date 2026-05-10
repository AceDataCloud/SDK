import { Video } from '../src/resources/video';

describe('Video.generate', () => {
  test('maps Seedance-specific params and supports content-only payloads', async () => {
    const request = jest.fn().mockResolvedValue({
      success: true,
      task_id: 'task-1',
    });
    const video = new Video({ request } as any);

    await video.generate({
      provider: 'seedance',
      model: 'doubao-seedance-1-0-pro-fast-251015',
      content: [{ type: 'text', text: 'A fox running in snow' }],
      resolution: '720p',
      ratio: '16:9',
      duration: 5,
      frames: 29,
      seed: 11,
      cameraFixed: true,
      watermark: false,
      generateAudio: true,
      callbackUrl: 'https://example.com/callback',
      returnLastFrame: true,
      serviceTier: 'default',
      executionExpiresAfter: 3600,
    });

    expect(request).toHaveBeenCalledWith('POST', '/seedance/videos', {
      json: {
        model: 'doubao-seedance-1-0-pro-fast-251015',
        content: [{ type: 'text', text: 'A fox running in snow' }],
        resolution: '720p',
        ratio: '16:9',
        duration: 5,
        frames: 29,
        seed: 11,
        camerafixed: true,
        watermark: false,
        generate_audio: true,
        callback_url: 'https://example.com/callback',
        return_last_frame: true,
        service_tier: 'default',
        execution_expires_after: 3600,
      },
    });
  });
});
