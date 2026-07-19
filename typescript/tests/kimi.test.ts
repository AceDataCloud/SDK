import { Kimi } from '../src/resources/kimi';

describe('Kimi resource', () => {
  it('posts chat completions to the kimi endpoint', async () => {
    const request = jest.fn().mockResolvedValue({ id: 'chatcmpl-kimi' });
    const kimi = new Kimi({ request } as any);

    await kimi.chat.completions.create({
      model: 'kimi-k3',
      messages: [{ role: 'user', content: 'hello' }],
      temperature: 0.2,
    });

    expect(request).toHaveBeenCalledWith('POST', '/kimi/chat/completions', {
      json: {
        model: 'kimi-k3',
        messages: [{ role: 'user', content: 'hello' }],
        temperature: 0.2,
      },
    });
  });

  it('streams chat completions from the kimi endpoint', async () => {
    const requestStream = jest.fn().mockImplementation(async function* () {
      yield '{"delta":"hello"}';
    });
    const kimi = new Kimi({ requestStream } as any);

    const stream = await kimi.chat.completions.create({
      model: 'kimi-k3',
      messages: [{ role: 'user', content: 'hello' }],
      stream: true,
    });

    const chunks: Array<Record<string, unknown>> = [];
    for await (const chunk of stream) chunks.push(chunk);

    expect(chunks).toEqual([{ delta: 'hello' }]);
    expect(requestStream).toHaveBeenCalledWith('POST', '/kimi/chat/completions', {
      json: {
        model: 'kimi-k3',
        messages: [{ role: 'user', content: 'hello' }],
        stream: true,
      },
    });
  });
});
