import { Maestro } from '../src/resources/providers/maestro';
import { TaskHandle } from '../src/runtime/tasks';

describe('Maestro provider', () => {
  it('uses current defaults and returns a task handle', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'maestro-1' });
    const maestro = new Maestro({ request } as any);

    const task = await maestro.generate({ prompt: 'a video' });

    expect(task).toBeInstanceOf(TaskHandle);
    expect(task.id).toBe('maestro-1');
    expect(request).toHaveBeenCalledWith('POST', '/maestro/videos', {
      json: {
        prompt: 'a video', action: 'generate', langs: ['zh-cn'], aspect: '9:16',
        duration: 30, quality: 'standard', scenario: 'auto', style: 'auto', voice: 'auto', async: true,
      },
    });
  });

  it('requires a reference task for edits', async () => {
    const maestro = new Maestro({ request: jest.fn() } as any);
    await expect(maestro.generate({ prompt: 'a video', action: 'edit' })).rejects.toThrow('refTaskId');
  });
});
