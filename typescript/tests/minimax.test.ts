import { Minimax } from '../src/resources/providers/minimax';
import { TaskHandle } from '../src/runtime/tasks';

describe('Minimax provider', () => {
  it('wraps the default synchronous response in a completed task handle', async () => {
    const request = jest.fn().mockResolvedValue({
      task: {
        id: 'minimax-1',
        status: 'succeeded',
        content: { url: 'https://cdn.example.com/minimax.mp4' },
      },
    });
    const minimax = new Minimax({ request } as any);

    const task = await minimax.generate({
      model: 'MiniMax-H3',
      content: [{ type: 'text', text: 'A cat' }],
      resolution: '2K',
      duration: 5,
      ratio: '16:9',
    });

    expect(task).toBeInstanceOf(TaskHandle);
    expect(task.id).toBe('minimax-1');
    expect(task.done).toBe(true);
    expect(task.urls()).toEqual(['https://cdn.example.com/minimax.mp4']);
    expect(request).toHaveBeenCalledWith('POST', '/minimax/videos', {
      json: {
        model: 'MiniMax-H3',
        content: [{ type: 'text', text: 'A cat' }],
        resolution: '2K',
        duration: 5,
        ratio: '16:9',
        async: false,
      },
    });
  });

  it('does not poll a synchronous failure without an artifact', async () => {
    const request = jest.fn().mockResolvedValue({
      task: {
        id: 'minimax-failed',
        status: 'failed',
        error: { code: 'generation_failed', message: 'Generation failed.' },
      },
    });
    const minimax = new Minimax({ request } as any);

    const task = await minimax.generate({
      model: 'MiniMax-H3',
      content: [{ type: 'text', text: 'A cat' }],
      resolution: '2K',
      duration: 5,
    });

    expect(task.id).toBe('minimax-failed');
    expect(task.done).toBe(true);
    await task.wait();
    expect(request).toHaveBeenCalledTimes(1);
  });
});
