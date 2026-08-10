import { Gemini } from '../src/resources/providers/gemini';
import { Kimi } from '../src/resources/kimi';
import { TaskHandle } from '../src/runtime/tasks';

describe('Gemini and Kimi resources', () => {
  it('submits Gemini video generation as a task', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'gemini-1' });
    const task = await new Gemini({ request } as any).videos({ prompt: 'A kitten' });

    expect(task).toBeInstanceOf(TaskHandle);
    expect(request).toHaveBeenCalledWith('POST', '/gemini/videos', {
      json: { prompt: 'A kitten', model: 'omni-flash', aspect_ratio: '16:9', resolution: '720p', async: true },
    });
  });

  it('uses the documented Kimi chat endpoint', async () => {
    const request = jest.fn().mockResolvedValue({ id: 'kimi-1' });
    await new Kimi({ request } as any).chat.completions.create({
      model: 'kimi-k3',
      messages: [{ role: 'user', content: 'Hi' }],
    });

    expect(request).toHaveBeenCalledWith('POST', '/kimi/chat/completions', {
      json: { model: 'kimi-k3', messages: [{ role: 'user', content: 'Hi' }] },
    });
  });
});
