import { Midjourney } from '../src/resources/midjourney';
import { Qrart } from '../src/resources/qrart';
import { Tiktok } from '../src/resources/tiktok';
import { Tw } from '../src/resources/tw';
import { TaskHandle } from '../src/runtime/tasks';

describe('Docs sync resources', () => {
  it('exposes Midjourney, QRArt, TikTok, and X endpoints', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'task-1' });
    const midjourney = new Midjourney({ request } as any);
    const qrart = new Qrart({ request } as any);
    const tiktok = new Tiktok({ request } as any);
    const tw = new Tw({ request } as any);

    expect(await midjourney.imagine({ prompt: 'a cat' })).toBeInstanceOf(TaskHandle);
    expect(request).toHaveBeenLastCalledWith('POST', '/midjourney/imagine', {
      json: { prompt: 'a cat', async: true },
    });

    expect(await qrart.generate({ type: 'link', prompt: 'floral' })).toBeInstanceOf(TaskHandle);
    expect(request).toHaveBeenLastCalledWith('POST', '/qrart/generate', {
      json: { type: 'link', prompt: 'floral', async: true },
    });

    await tiktok.video({ videoUrl: 'https://www.tiktok.com/@u/video/1' });
    expect(request).toHaveBeenLastCalledWith('POST', '/tiktok/video', {
      json: { video_url: 'https://www.tiktok.com/@u/video/1' },
    });

    await tw.posts({ userId: '123' });
    expect(request).toHaveBeenLastCalledWith('POST', '/x/posts', { json: { user_id: '123' } });
  });
});
