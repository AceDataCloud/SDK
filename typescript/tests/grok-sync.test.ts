import { Tasks } from '../src/resources/tasks';
import { Video } from '../src/resources/video';

describe('grok sync', () => {
  it('uses grok video and task endpoints for video generation', async () => {
    const request = jest
      .fn()
      .mockResolvedValueOnce({ task_id: 'task-grok' })
      .mockResolvedValueOnce({ response: { status: 'succeeded' } });
    const video = new Video({ request } as any);

    const handle = (await video.generate({
      prompt: 'A cinematic sunrise',
      provider: 'grok',
    })) as any;

    expect(request).toHaveBeenNthCalledWith(1, 'POST', '/grok/videos', {
      json: { prompt: 'A cinematic sunrise' },
    });

    await handle.get();

    expect(request).toHaveBeenNthCalledWith(2, 'POST', '/grok/tasks', {
      json: { id: 'task-grok', action: 'retrieve' },
    });
  });

  it('uses grok task endpoint in tasks.get', async () => {
    const request = jest.fn().mockResolvedValue({ response: { status: 'processing' } });
    const tasks = new Tasks({ request } as any);

    await tasks.get('task-grok', { service: 'grok' });

    expect(request).toHaveBeenCalledWith('POST', '/grok/tasks', {
      json: { id: 'task-grok', action: 'retrieve' },
    });
  });
});
