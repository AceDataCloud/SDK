import { Fish } from '../src/resources/providers/fish';
import { OpenAI } from '../src/resources/openai';
import { Midjourney } from '../src/resources/providers/midjourney';

describe('OpenAI compatibility and Midjourney provider', () => {
  it('exposes models, audio speech, and realtime url', async () => {
    const request = jest.fn().mockResolvedValue({ data: [] });
    const openai = new OpenAI({ request } as any, 'https://x402.acedata.cloud');

    await openai.models.list();
    await openai.audio.speech({ input: 'hello', model: 'tts-1', voice: 'alloy', responseFormat: 'mp3', speed: 1.25 });

    expect(request).toHaveBeenNthCalledWith(1, 'GET', '/openai/models');
    expect(request).toHaveBeenNthCalledWith(2, 'POST', '/v1/audio/speech', {
      json: {
        input: 'hello',
        model: 'tts-1',
        voice: 'alloy',
        response_format: 'mp3',
        speed: 1.25,
      },
    });
    expect(openai.realtime.url({ model: 'gpt-realtime' })).toBe(
      'wss://x402.acedata.cloud/v1/realtime?model=gpt-realtime'
    );
  });

  it('serializes midjourney pollable and non-pollable endpoints', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'task-midjourney', data: [] });
    const midjourney = new Midjourney({ request } as any);

    const handle = await midjourney.imagine({ prompt: 'A cat', async: false });
    const describe = await midjourney.describe('https://example.com/cat.png');

    expect(handle.id).toBe('task-midjourney');
    expect(describe).toEqual({ task_id: 'task-midjourney', data: [] });
    expect(request).toHaveBeenNthCalledWith(1, 'POST', '/midjourney/imagine', {
      json: { prompt: 'A cat', async: false },
    });
    expect(request).toHaveBeenNthCalledWith(2, 'POST', '/midjourney/describe', {
      json: { image_url: 'https://example.com/cat.png' },
    });
  });

  it('exposes fish model read endpoints on the provider axis', async () => {
    const request = jest.fn().mockResolvedValue({ data: [] });
    const fish = new Fish({ request } as any);

    await fish.listModels({ pageSize: 10, pageNumber: 2, selfOnly: true });
    await fish.getModel('voice-1');

    expect(request).toHaveBeenNthCalledWith(1, 'GET', '/fish/model', {
      params: { page_size: '10', page_number: '2', self: 'true' },
    });
    expect(request).toHaveBeenNthCalledWith(2, 'GET', '/fish/model/voice-1');
  });
});
