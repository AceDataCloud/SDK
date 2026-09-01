import { Midjourney } from '../src/resources/providers/midjourney';
import { TaskHandle } from '../src/runtime/tasks';

describe('Midjourney provider', () => {
  it('submits a video request and returns a task handle', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'midjourney-1' });
    const midjourney = new Midjourney({ request } as any);

    const task = await midjourney.generate({
      action: 'generate',
      mode: 'fast',
      resolution: '720p',
      prompt: 'a cat',
      imageUrl: 'https://example.com/cat.png',
    });

    expect(task).toBeInstanceOf(TaskHandle);
    expect(request).toHaveBeenCalledWith('POST', '/midjourney/videos', {
      json: {
        action: 'generate',
        mode: 'fast',
        resolution: '720p',
        prompt: 'a cat',
        image_url: 'https://example.com/cat.png',
        async: true,
      },
    });
  });
});
