import { Seedream, SeedreamGenerateOptions } from '../src/resources/providers/seedream';
import { TaskHandle } from '../src/runtime/tasks';

describe('Seedream provider', () => {
  it('omits example-only size and consumes array response data', async () => {
    const request = jest.fn().mockResolvedValue({
      success: true,
      task_id: 'seedream-1',
      data: [{ image_url: 'https://cdn.example.com/seedream.png' }],
    });
    const seedream = new Seedream({ request } as any);

    const task = await seedream.generate({
      model: 'doubao-seedream-5-0-260128',
      prompt: 'a cat',
    });

    expect(task).toBeInstanceOf(TaskHandle);
    expect(task.done).toBe(true);
    expect(task.urls()).toEqual(['https://cdn.example.com/seedream.png']);
    expect(request).toHaveBeenCalledWith('POST', '/seedream/images', {
      json: {
        model: 'doubao-seedream-5-0-260128',
        prompt: 'a cat',
        async: true,
      },
    });
  });

  it('serializes the new request contract', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'seedream-1' });
    const seedream = new Seedream({ request } as any);

    await seedream.generate({
      model: 'doubao-seedream-5-0-pro-260628',
      image: 'https://example.com/source.png',
      size: '1.5K',
      layerDecomposition: true,
      responseFormat: 'b64_json',
      background: 'transparent',
    });

    expect(request.mock.calls[0][2].json).toMatchObject({
      image: 'https://example.com/source.png',
      size: '1.5K',
      layer_decomposition: true,
      response_format: 'b64_json',
      background: 'transparent',
    });
  });

  it('accepts either a string or array image', () => {
    const stringImage: SeedreamGenerateOptions['image'] = 'https://example.com/source.png';
    const arrayImage: SeedreamGenerateOptions['image'] = ['https://example.com/source.png'];
    expect([stringImage, arrayImage]).toHaveLength(2);
  });
});
