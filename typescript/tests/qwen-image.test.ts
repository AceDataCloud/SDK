import { QwenImage } from '../src/resources/providers/qwen-image';
import { TaskHandle } from '../src/runtime/tasks';

describe('Qwen Image provider', () => {
  it('serializes the current generation contract', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'qwen-image-1' });
    const qwenImage = new QwenImage({ request } as any);

    const task = await qwenImage.generate({
      model: 'qwen-image-3.0-pro',
      prompt: 'A watercolor city',
      imageUrls: ['https://cdn.example.com/reference.png'],
      n: 2,
      size: '1536x1024',
      promptExtend: false,
      promptExtendMode: 'agent',
      enableThinking: false,
      negativePrompt: 'text',
      seed: 42,
      watermark: true,
    });

    expect(task).toBeInstanceOf(TaskHandle);
    expect(task.id).toBe('qwen-image-1');
    expect(request).toHaveBeenCalledWith('POST', '/qwen-image/images', {
      json: {
        model: 'qwen-image-3.0-pro',
        prompt: 'A watercolor city',
        image_urls: ['https://cdn.example.com/reference.png'],
        n: 2,
        size: '1536x1024',
        prompt_extend: false,
        prompt_extend_mode: 'agent',
        enable_thinking: false,
        negative_prompt: 'text',
        seed: 42,
        watermark: true,
        async: true,
      },
    });
  });

  it('applies documented defaults', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'qwen-image-1' });
    const qwenImage = new QwenImage({ request } as any);

    await qwenImage.generate({ model: 'qwen-image-3.0', prompt: 'A lighthouse' });

    expect(request.mock.calls[0][2].json).toEqual({
      model: 'qwen-image-3.0',
      prompt: 'A lighthouse',
      n: 1,
      prompt_extend: true,
      prompt_extend_mode: 'direct',
      enable_thinking: true,
      watermark: false,
      async: true,
    });
  });
});
