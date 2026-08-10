import { Gemini } from '../src/resources/gemini';
import { TaskHandle } from '../src/runtime/tasks';

describe('Gemini', () => {
  it('submits videos to the Gemini endpoint', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'gemini-1' });
    const gemini = new Gemini({ request } as any);
    const task = await gemini.generate({ prompt: 'a cat', imageUrls: ['https://example.com/cat.png'] });
    expect(task).toBeInstanceOf(TaskHandle);
    expect(request).toHaveBeenCalledWith('POST', '/gemini/videos', expect.objectContaining({
      json: expect.objectContaining({ image_urls: ['https://example.com/cat.png'], async: true }),
    }));
  });
});
