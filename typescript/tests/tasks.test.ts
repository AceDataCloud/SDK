import { TaskHandle } from '../src/runtime/tasks';

describe('TaskHandle', () => {
  it('waits through accepted responses and completes on success data without status', async () => {
    const request = jest
      .fn()
      .mockResolvedValueOnce({ response: { success: true, task_id: 'task-1' } })
      .mockResolvedValueOnce({
        finished_at: '2026-07-18T08:16:11Z',
        response: {
          success: true,
          task_id: 'task-1',
          data: [{ image_url: 'https://cdn.example/image.png' }],
        },
      });
    const handle = new TaskHandle('task-1', '/nano-banana/tasks', { request } as any);

    const result = await handle.wait({ pollInterval: 0, maxWait: 1000 });

    expect(result).toEqual(expect.objectContaining({ response: expect.objectContaining({ success: true }) }));
    expect(request).toHaveBeenCalledTimes(2);
  });

  it('recognizes explicit terminal status', async () => {
    const request = jest.fn().mockResolvedValue({ response: { status: 'succeeded' } });
    const handle = new TaskHandle('task-1', '/tasks', { request } as any);

    await expect(handle.isCompleted()).resolves.toBe(true);
  });

  it.each([
    { response: { success: true, data: [] } },
    { response: { success: true, data: null } },
    { response: { success: false, error: 'temporary' } },
    { response: { success: false, error: null } },
    { response: null },
    { finished_at: '2026-07-18T08:16:11Z', response: { status: 'processing', success: true } },
  ])('waits without terminal status or finished_at: %p', async (state) => {
    const request = jest.fn().mockResolvedValue(state);
    const handle = new TaskHandle('task-1', '/tasks', { request } as any);

    await expect(handle.isCompleted()).resolves.toBe(false);
  });

  it.each([
    [{ finished_at: '2026-07-18T08:16:11Z', response: { success: true, data: null } }, true],
    [{ response: { finished_at: '2026-07-18T08:16:11Z', success: false } }, true],
    [{ finished_at: '2026-07-18T08:16:11Z', response: { success: null } }, false],
    [{ finished_at: '2026-07-18T08:16:11Z', response: { status: 'succeeded', success: false } }, true],
    [{ response: null, status: 'succeeded' }, true],
  ])('handles terminal shape %p', async (state, expected) => {
    const request = jest.fn().mockResolvedValue(state);
    const handle = new TaskHandle('task-1', '/tasks', { request } as any);

    await expect(handle.isCompleted()).resolves.toBe(expected);
  });
});