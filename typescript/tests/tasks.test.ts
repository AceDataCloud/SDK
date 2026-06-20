import { Tasks } from '../src/resources/tasks';

describe('Tasks resource', () => {
  it('uses mapped endpoint for gemini service', async () => {
    const request = jest.fn().mockResolvedValue({ id: 'task-gemini' });
    const tasks = new Tasks({ request } as any);

    await tasks.get('task-gemini', { service: 'gemini' });

    expect(request).toHaveBeenCalledWith('POST', '/gemini/tasks', {
      json: { id: 'task-gemini', action: 'retrieve' },
    });
  });
});
