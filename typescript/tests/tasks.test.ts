import { Tasks } from '../src/resources/tasks';

describe('Tasks resource', () => {
  it('uses explicit gemini tasks endpoint', async () => {
    const request = jest.fn().mockResolvedValue({ id: 'task-gemini' });
    const tasks = new Tasks({ request } as any);

    await tasks.get('task-gemini', { service: 'gemini' });

    expect(request).toHaveBeenCalledWith('POST', '/gemini/tasks', {
      json: { id: 'task-gemini', action: 'retrieve' },
    });
  });
});
