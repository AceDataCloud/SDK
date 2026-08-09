import { Veo } from '../src/resources/veo';
import { TaskHandle } from '../src/runtime/tasks';

describe('Veo resource', () => {
  it('submits the latest video request shape and returns a task handle', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'veo-1' });
    const veo = new Veo({ request } as any);

    const task = await veo.generate({
      action: 'ingredients2video',
      model: 'veo31-fast-ingredients',
      prompt: 'A rotating mug',
      resolution: '1080p',
      aspectRatio: '16:9',
      imageUrls: ['https://example.com/mug.png'],
    });

    expect(task).toBeInstanceOf(TaskHandle);
    expect(task.id).toBe('veo-1');
    expect(request).toHaveBeenCalledWith('POST', '/veo/videos', {
      json: {
        action: 'ingredients2video',
        prompt: 'A rotating mug',
        model: 'veo31-fast-ingredients',
        resolution: '1080p',
        aspect_ratio: '16:9',
        image_urls: ['https://example.com/mug.png'],
        async: true,
      },
    });
  });
});
