import { Wan } from '../src/resources/providers/wan';

describe('Wan provider', () => {
  it('serializes new video fields', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'wan-1' });
    const wan = new Wan({ request } as any);

    await wan.generate({
      model: 'wan3.0-video',
      media: [{ type: 'image', url: 'https://cdn.example.com/frame.png' }],
      ratio: '16:9',
      seed: 42,
      watermark: true,
    });

    expect(request).toHaveBeenCalledWith('POST', '/wan/videos', {
      json: expect.objectContaining({
        model: 'wan3.0-video',
        action: 'text2video',
        media: [{ type: 'image', url: 'https://cdn.example.com/frame.png' }],
        ratio: '16:9',
        seed: 42,
        watermark: true,
        async: true,
      }),
    });
    expect(request.mock.calls[0][2].json.prompt).toBeUndefined();
  });
});
