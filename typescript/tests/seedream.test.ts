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

  it('sends an explicit supported size', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'seedream-1' });
    const seedream = new Seedream({ request } as any);

    await seedream.generate({
      model: 'doubao-seedream-5-0-260128',
      prompt: 'a cat',
      size: '4K',
    });

    expect(request.mock.calls[0][2].json.size).toBe('4K');
  });

  it('does not expose adaptive in the public size type', () => {
    type Size = SeedreamGenerateOptions['size'];
    type AdaptiveIsSupported = 'adaptive' extends Size ? true : false;
    const adaptiveIsSupported: AdaptiveIsSupported = false;
    expect(adaptiveIsSupported).toBe(false);
  });
});

describe('Seedream 5.0 official parity', () => {
  it('sends Pro layer decomposition without a prompt', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'layer-task' });
    const seedream = new Seedream({ request } as any);

    await seedream.generate({
      model: 'doubao-seedream-5-0-pro-260628',
      image: 'https://cdn.example.com/poster.png',
      size: '1.5K',
      layerDecomposition: true,
    });

    expect(request.mock.calls[0][2].json).toMatchObject({
      model: 'doubao-seedream-5-0-pro-260628',
      image: 'https://cdn.example.com/poster.png',
      size: '1.5K',
      layer_decomposition: true,
      async: true,
    });
    expect(request.mock.calls[0][2].json).not.toHaveProperty('prompt');
  });

  it('sends transparent-background editing and allows synchronous streaming', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'edit-task' });
    const seedream = new Seedream({ request } as any);

    await seedream.generate({
      model: 'doubao-seedream-5-0-pro-260628',
      prompt: 'Replace the object',
      image: ['data:image/png;base64,AA=='],
      outputFormat: 'png',
      background: 'transparent',
      async: false,
    });

    expect(request.mock.calls[0][2].json).toMatchObject({
      output_format: 'png',
      background: 'transparent',
      async: false,
    });
  });
});
