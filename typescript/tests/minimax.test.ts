import { Minimax } from '../src/resources/providers/minimax';
import { TaskHandle } from '../src/runtime/tasks';

describe('Minimax provider', () => {
  it('calls /minimax/videos and applies spec defaults', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'task-1' });
    const minimax = new Minimax({ request } as any);

    const handle = await minimax.generate({ prompt: 'a cat running' });

    expect(handle).toBeInstanceOf(TaskHandle);
    expect(request).toHaveBeenCalledWith('POST', '/minimax/videos', {
      json: expect.objectContaining({
        prompt: 'a cat running',
        model: 'minimax-h3',
        resolution: '2K',
        ratio: '16:9',
        duration: 4,
        aigc_watermark: false,
        async: true,
      }),
    });
  });
});
