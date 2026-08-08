import { Minimax } from '../src/resources/providers/minimax';
import { TaskHandle } from '../src/runtime/tasks';

describe('Minimax', () => {
  it('submits the H3 request shape and returns a task handle', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'minimax-task' });
    const minimax = new Minimax({ request } as never);

    const handle = await minimax.generate({
      model: 'MiniMax-H3',
      content: [{ type: 'text', text: 'A cat running' }],
      resolution: '2K',
      duration: 5,
    });

    expect(handle).toBeInstanceOf(TaskHandle);
    expect(request).toHaveBeenCalledWith('POST', '/minimax/videos', {
      json: {
        model: 'MiniMax-H3',
        content: [{ type: 'text', text: 'A cat running' }],
        resolution: '2K',
        duration: 5,
        aigc_watermark: false,
      },
    });
  });
});
