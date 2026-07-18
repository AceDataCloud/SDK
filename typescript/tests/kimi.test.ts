import { Kimi } from '../src/resources/kimi';

describe('Kimi resource', () => {
  it('sends chat completions to /kimi/chat/completions', async () => {
    const request = jest.fn().mockResolvedValue({ id: 'chatcmpl-kimi' });
    const kimi = new Kimi({ request } as any);

    await kimi.chat.completions.create({
      model: 'kimi-k3',
      messages: [{ role: 'user', content: 'hello' }],
      temperature: 0.5,
    });

    expect(request).toHaveBeenCalledWith('POST', '/kimi/chat/completions', {
      json: {
        model: 'kimi-k3',
        messages: [{ role: 'user', content: 'hello' }],
        temperature: 0.5,
      },
    });
  });

  it('streams chat completions from /kimi/chat/completions', async () => {
    async function* stream() {
      yield '{"id":"chunk-1"}';
    }
    const requestStream = jest.fn().mockReturnValue(stream());
    const kimi = new Kimi({ requestStream } as any);

    const iterator = (await kimi.chat.completions.create({
      model: 'kimi-k3',
      messages: [{ role: 'user', content: 'stream please' }],
      stream: true,
    })) as AsyncGenerator<Record<string, unknown>>;
    const chunks: Record<string, unknown>[] = [];
    for await (const chunk of iterator) chunks.push(chunk);

    expect(requestStream).toHaveBeenCalledWith('POST', '/kimi/chat/completions', {
      json: {
        model: 'kimi-k3',
        messages: [{ role: 'user', content: 'stream please' }],
        stream: true,
      },
    });
    expect(chunks).toEqual([{ id: 'chunk-1' }]);
  });
});
