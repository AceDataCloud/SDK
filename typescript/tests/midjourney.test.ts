import { Midjourney } from '../src/resources/providers/midjourney';
import { TaskHandle } from '../src/runtime/tasks';

describe('Midjourney provider', () => {
  it('submits the latest imagine contract and returns a task handle', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'midjourney-1' });
    const midjourney = new Midjourney({ request } as any);

    const task = await midjourney.imagine({ prompt: 'a cat', version: '8.2' });

    expect(task).toBeInstanceOf(TaskHandle);
    expect(task.id).toBe('midjourney-1');
    expect(request).toHaveBeenCalledWith('POST', '/midjourney/imagine', {
      json: expect.objectContaining({
        prompt: 'a cat',
        version: '8.2',
        async: true,
      }),
    });
  });
});
