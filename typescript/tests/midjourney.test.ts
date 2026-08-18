import { Midjourney } from '../src/resources/providers/midjourney';
import { TaskHandle } from '../src/runtime/tasks';

describe('Midjourney provider', () => {
  it('serializes documented imagine defaults', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'midjourney-1' });
    const midjourney = new Midjourney({ request } as any);

    const task = await midjourney.imagine({ prompt: 'a cat', version: '8.2' });

    expect(task).toBeInstanceOf(TaskHandle);
    expect(request).toHaveBeenCalledWith('POST', '/midjourney/imagine', {
      json: {
        mode: 'fast',
        action: 'generate',
        prompt: 'a cat',
        timeout: 480,
        translation: false,
        split_images: false,
        version: '8.2',
        hd: false,
        quality: '1',
        style_reference: false,
        moodboard: false,
        async: true,
      },
    });
  });
});
