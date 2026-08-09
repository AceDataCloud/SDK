import { Minimax } from '../src/resources/providers/minimax';
import { TaskHandle } from '../src/runtime/tasks';

describe('Minimax provider', () => {
  it('submits the documented video request and returns a task handle', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'minimax-1' });
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
    expect(request).toHaveBeenCalledWith('POST', '/minimax/videos', {
      json: {
        model: 'MiniMax-H3',
        content: [{ type: 'text', text: 'A cat' }],
        resolution: '2K',
        duration: 5,
        ratio: '16:9',
        async: true,
      },
    });
  });

  it('rejects invalid content entries before sending request', async () => {
    const request = jest.fn();
    const minimax = new Minimax({ request } as any);

    await expect(
      minimax.generate({
        model: 'MiniMax-H3',
        content: [{ type: 'video_url', video_url: { url: 'https://example.com/ref.mp4' } } as any],
        resolution: '2K',
        duration: 5,
      }),
    ).rejects.toThrow("role='reference_video'");
    expect(request).not.toHaveBeenCalled();
  });
});
