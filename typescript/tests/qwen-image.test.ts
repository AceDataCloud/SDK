import { QwenImage } from '../src/resources/providers/qwen-image';

describe('QwenImage provider', () => {
  it('defaults async to false and keeps spec defaults for booleans', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'qwen-1' });
    const qwen = new QwenImage({ request } as any);

    await qwen.generate({
      model: 'qwen-image-3.0',
      prompt: 'a cat',
    });

    expect(request).toHaveBeenCalledWith('POST', '/qwen-image/images', {
      json: expect.objectContaining({
        async: false,
        prompt_extend: true,
        enable_thinking: true,
      }),
    });
  });
});
