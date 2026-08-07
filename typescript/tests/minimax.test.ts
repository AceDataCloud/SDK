import { Minimax } from '../src/resources/providers/minimax';
import { TaskHandle } from '../src/runtime/tasks';

describe('Minimax provider', () => {
  it('targets minimax endpoints and sends defaults', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'task-1' });
    const client = new Minimax({ request } as any);

    const handle = await client.generate();

    expect(handle).toBeInstanceOf(TaskHandle);
    expect(handle.id).toBe('task-1');
    expect(request).toHaveBeenCalledWith('POST', '/minimax/videos', {
      json: expect.objectContaining({
        model: 'minimax-h3',
        ratio: '16:9',
        duration: 4,
        async: true,
      }),
    });
  });
});
