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

  it('removes retired models and parameters from the public contract', () => {
    type Model = SeedreamGenerateOptions['model'];
    type RetiredModelIsSupported = 'doubao-seedream-3-0-t2i-250415' extends Model ? true : false;
    type SeedIsSupported = 'seed' extends keyof SeedreamGenerateOptions ? true : false;
    type GuidanceScaleIsSupported = 'guidanceScale' extends keyof SeedreamGenerateOptions ? true : false;

    const retiredModelIsSupported: RetiredModelIsSupported = false;
    const seedIsSupported: SeedIsSupported = false;
    const guidanceScaleIsSupported: GuidanceScaleIsSupported = false;
    expect({ retiredModelIsSupported, seedIsSupported, guidanceScaleIsSupported }).toEqual({
      retiredModelIsSupported: false,
      seedIsSupported: false,
      guidanceScaleIsSupported: false,
    });
  });
});
