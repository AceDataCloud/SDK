import { Gemini } from '../src/resources/providers/gemini';
import { TaskHandle } from '../src/runtime/tasks';

describe('Gemini provider', () => {
  it('submits the documented video request and returns a task handle', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'gemini-1' });
    const gemini = new Gemini({ request } as any);

    const task = await gemini.generate({
      prompt: 'A cat running on the beach',
    });

    expect(task).toBeInstanceOf(TaskHandle);
    expect(task.id).toBe('gemini-1');
    expect(request).toHaveBeenCalledWith('POST', '/gemini/videos', {
      json: {
        prompt: 'A cat running on the beach',
        model: 'omni-flash',
        aspect_ratio: '16:9',
        resolution: '720p',
        async: true,
      },
    });
  });
});
