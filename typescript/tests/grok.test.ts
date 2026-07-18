import { Grok } from '../src/resources/grok';
import { Tasks } from '../src/resources/tasks';

describe('Grok resource', () => {
  it('calls /grok/chat/completions with mapped fields', async () => {
    const request = jest.fn().mockResolvedValue({ id: 'chat-1' });
    const grok = new Grok({ request } as any);

    await grok.chat.completions.create({
      model: 'grok-4.5',
      messages: [{ role: 'user', content: 'hello' }],
      maxTokens: 128,
      topP: 0.8,
    });

    expect(request).toHaveBeenCalledWith('POST', '/grok/chat/completions', {
      json: {
        model: 'grok-4.5',
        messages: [{ role: 'user', content: 'hello' }],
        max_tokens: 128,
        top_p: 0.8,
      },
    });
  });

  it('supports streaming grok chat completions', async () => {
    const requestStream = jest.fn().mockImplementation(async function* () {
      yield '{"choices":[{"delta":{"content":"hi"}}]}';
    });
    const grok = new Grok({ requestStream } as any);

    const stream = (await grok.chat.completions.create({
      model: 'grok-4',
      messages: [{ role: 'user', content: 'hello' }],
      stream: true,
    })) as AsyncGenerator<Record<string, unknown>>;

    const chunks: Record<string, unknown>[] = [];
    for await (const chunk of stream) chunks.push(chunk);

    expect(requestStream).toHaveBeenCalledWith('POST', '/grok/chat/completions', {
      json: {
        model: 'grok-4',
        messages: [{ role: 'user', content: 'hello' }],
        stream: true,
      },
    });
    expect(chunks).toEqual([{ choices: [{ delta: { content: 'hi' } }] }]);
  });

  it('calls /grok/videos with mapped fields', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'task-1' });
    const grok = new Grok({ request } as any);

    await grok.videos.generate({
      model: 'grok-imagine-video-1.5-fast',
      imageUrl: 'https://example.com/img.png',
      referenceImageUrls: ['https://example.com/ref.png'],
      aspectRatio: '16:9',
      callbackUrl: 'https://example.com/callback',
    });

    expect(request).toHaveBeenCalledWith('POST', '/grok/videos', {
      json: {
        model: 'grok-imagine-video-1.5-fast',
        image_url: 'https://example.com/img.png',
        reference_image_urls: ['https://example.com/ref.png'],
        aspect_ratio: '16:9',
        callback_url: 'https://example.com/callback',
      },
    });
  });
});

describe('Tasks resource', () => {
  it('maps grok service to /grok/tasks', async () => {
    const request = jest.fn().mockResolvedValue({ id: 'task-1' });
    const tasks = new Tasks({ request } as any);

    await tasks.get('task-1', { service: 'grok' });

    expect(request).toHaveBeenCalledWith('POST', '/grok/tasks', {
      json: { id: 'task-1', action: 'retrieve' },
    });
  });
});
