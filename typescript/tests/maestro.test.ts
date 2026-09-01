import { Maestro } from '../src/resources/providers/maestro';

describe('Maestro provider', () => {
  it('does not send the removed quality parameter', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'task-maestro' });

    await new Maestro({ request } as any).generate({
      prompt: 'Launch video',
      duration: 300,
      scenario: 'drama',
    });

    expect(request).toHaveBeenCalledWith('POST', '/maestro/videos', {
      json: {
        prompt: 'Launch video',
        action: 'generate',
        langs: ['zh-cn'],
        aspect: '9:16',
        duration: 300,
        scenario: 'drama',
        style: 'auto',
        voice: 'auto',
        async: true,
      },
    });
  });
});
