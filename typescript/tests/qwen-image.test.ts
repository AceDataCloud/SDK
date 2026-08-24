import { QwenImage } from '../src/resources/providers/qwen-image';
import { TaskHandle } from '../src/runtime/tasks';

describe('QwenImage provider', () => {
  it('serializes spec defaults', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'qwen-1' });
    const qwenImage = new QwenImage({ request } as any);

    const task = await qwenImage.generate({
      model: 'qwen-image-3.0-pro',
      prompt: 'a cat',
    });

    expect(task).toBeInstanceOf(TaskHandle);
    expect(request).toHaveBeenCalledWith('POST', '/qwen-image/images', {
      json: {
        model: 'qwen-image-3.0-pro',
        prompt: 'a cat',
        n: 1,
        prompt_extend: true,
        prompt_extend_mode: 'direct',
        enable_thinking: true,
        watermark: false,
        async: true,
      },
    });
  });
});
