import { Wan } from '../src/resources/providers/wan';
import { TaskHandle } from '../src/runtime/tasks';

describe('Wan provider', () => {
  it('supports Wan 3.0 fields without requiring action or prompt', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'wan-3' });
    const wan = new Wan({ request } as any);

    const task = await wan.generate({
      model: 'wan3.0-video',
      media: [{ type: 'image', url: 'https://cdn.example.com/frame.png' }],
      ratio: '9:16',
      seed: 42,
      watermark: true,
    });

    expect(task).toBeInstanceOf(TaskHandle);
    expect(request).toHaveBeenCalledWith('POST', '/wan/videos', {
      json: {
        model: 'wan3.0-video',
        audio: false,
        prompt_extend: false,
        action: 'text2video',
        media: [{ type: 'image', url: 'https://cdn.example.com/frame.png' }],
        ratio: '9:16',
        seed: 42,
        watermark: true,
        async: true,
      },
    });
  });
});
