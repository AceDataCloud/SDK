import { Seedance } from '../src/resources/providers/seedance';
import { TaskHandle } from '../src/runtime/tasks';

describe('Seedance provider', () => {
  it('serializes the Seedance 2.5 public contract', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'seedance-25' });
    const seedance = new Seedance({ request } as any);
    const task = await seedance.generate({
      model: 'doubao-seedance-2-5-260628',
      content: [{ type: 'text', text: 'Extend the scene' }],
      duration: 30,
      camerafixed: true,
      omniReferenceTaskType: 'extend',
      outputFormat: 'mov',
      tools: [{ type: 'web_search' }],
    });
    expect(task).toBeInstanceOf(TaskHandle);
    expect(request).toHaveBeenCalledWith('POST', '/seedance/videos', {
      json: expect.objectContaining({
        model: 'doubao-seedance-2-5-260628',
        duration: 30,
        camerafixed: true,
        omni_reference_task_type: 'extend',
        output_format: 'mov',
        tools: [{ type: 'web_search' }],
        async: true,
      }),
    });
    expect((request.mock.calls[0][2].json as Record<string, unknown>).camera_fixed).toBeUndefined();
  });

  it('does not send Seedance 2.5 defaults to 2.0', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'seedance-20' });
    const seedance = new Seedance({ request } as any);
    await seedance.generate({
      model: 'doubao-seedance-2-0-260128',
      content: [{ type: 'text', text: 'A scene' }],
    });
    expect(request.mock.calls[0][2].json.output_format).toBeUndefined();
  });
});
