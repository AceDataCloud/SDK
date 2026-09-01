import { Gemini } from '../src/resources/gemini';
import { TaskHandle } from '../src/runtime/tasks';

describe('Gemini resource', () => {
  it('submits documented video defaults and returns a task handle', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'gemini-task' });
    const task = await new Gemini({ request } as any).generateVideo({ prompt: 'A cat' });

    expect(task).toBeInstanceOf(TaskHandle);
    expect(request).toHaveBeenCalledWith('POST', '/gemini/videos', {
      json: {
        prompt: 'A cat',
        model: 'omni-flash',
        aspect_ratio: '16:9',
        resolution: '720p',
        async: true,
      },
    });
  });
});
