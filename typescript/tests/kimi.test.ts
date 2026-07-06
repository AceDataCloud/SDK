import { Kimi } from '../src/resources/kimi';

describe('Kimi resource', () => {
  it('uses /kimi/chat/completions for non-stream requests', async () => {
    const request = jest.fn().mockResolvedValue({ id: 'kimi-1' });
    const kimi = new Kimi({ request } as any);

    await kimi.chat.completions.create({
      model: 'kimi-k2.6',
      messages: [{ role: 'user', content: 'Hello' }],
      temperature: 0.2,
    });

    expect(request).toHaveBeenCalledWith('POST', '/kimi/chat/completions', {
      json: {
        model: 'kimi-k2.6',
        messages: [{ role: 'user', content: 'Hello' }],
        temperature: 0.2,
      },
    });
  });

  it('streams from /kimi/chat/completions when stream=true', async () => {
    const requestStream = jest.fn().mockImplementation(async function* () {
      yield JSON.stringify({ choices: [{ delta: { content: 'Hi' } }] });
    });
    const kimi = new Kimi({ requestStream } as any);

    const stream = (await kimi.chat.completions.create({
      model: 'kimi-k2.6',
      messages: [{ role: 'user', content: 'Say hi' }],
      stream: true,
    })) as AsyncGenerator<Record<string, unknown>>;

    const chunks: Record<string, unknown>[] = [];
    for await (const chunk of stream) chunks.push(chunk);

    expect(requestStream).toHaveBeenCalledWith('POST', '/kimi/chat/completions', {
      json: {
        model: 'kimi-k2.6',
        messages: [{ role: 'user', content: 'Say hi' }],
        stream: true,
      },
    });
    expect(chunks).toEqual([{ choices: [{ delta: { content: 'Hi' } }] }]);
  });
});
