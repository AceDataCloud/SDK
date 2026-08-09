import { TaskHandle } from '../src/runtime/tasks';
import { Minimax } from '../src/resources/providers/minimax';

describe('Minimax provider', () => {
  it('creates a task handle and sends minimax defaults', async () => {
    const request = jest
      .fn()
      .mockResolvedValueOnce({ task_id: 'mx-1' })
      .mockResolvedValueOnce({ response: { status: 'processing' } });
    const minimax = new Minimax({ request } as any);

    const handle = await minimax.generate({
      model: 'MiniMax-H3',
      content: [{ type: 'text', text: 'A cat is running' }],
      resolution: '768P',
      duration: 6,
    });

    expect(handle).toBeInstanceOf(TaskHandle);
    expect(handle.id).toBe('mx-1');
    expect(request).toHaveBeenNthCalledWith(1, 'POST', '/minimax/videos', {
      json: expect.objectContaining({
        model: 'MiniMax-H3',
        resolution: '768P',
        duration: 6,
        aigc_watermark: false,
        async: true,
      }),
    });

    await handle.get();
    expect(request).toHaveBeenNthCalledWith(2, 'POST', '/minimax/tasks', {
      json: { id: 'mx-1', action: 'retrieve' },
    });
  });
});
