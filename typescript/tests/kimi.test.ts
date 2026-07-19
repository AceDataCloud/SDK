import { AceDataCloud } from '../src/client';
import { Kimi } from '../src/resources/kimi';

describe('Kimi resource', () => {
  it('posts chat completions to the kimi endpoint', async () => {
    const request = jest.fn().mockResolvedValue({ choices: [{ message: { content: 'Hello!' } }] });
    const kimi = new Kimi({ request } as any);

    const result = await kimi.chat.completions.create({
      model: 'kimi-k3',
      messages: [{ role: 'user', content: 'Hi' }],
      temperature: 0.5,
    });

    expect(result).toEqual({ choices: [{ message: { content: 'Hello!' } }] });
    expect(request).toHaveBeenCalledWith('POST', '/kimi/chat/completions', {
      json: {
        model: 'kimi-k3',
        messages: [{ role: 'user', content: 'Hi' }],
        temperature: 0.5,
      },
    });
  });

  it('streams chat completions from the kimi endpoint', async () => {
    const requestStream = jest.fn().mockImplementation(async function* () {
      yield JSON.stringify({ choices: [{ delta: { content: 'Hi' } }] });
      yield JSON.stringify({ choices: [{ delta: { content: ' there' } }] });
    });
    const kimi = new Kimi({ requestStream } as any);

    const stream = await kimi.chat.completions.create({
      model: 'kimi-k3',
      messages: [{ role: 'user', content: 'Hi' }],
      stream: true,
    });

    await expect((async () => {
      const chunks = [];
      for await (const chunk of stream) chunks.push(chunk);
      return chunks;
    })()).resolves.toEqual([
      { choices: [{ delta: { content: 'Hi' } }] },
      { choices: [{ delta: { content: ' there' } }] },
    ]);
    expect(requestStream).toHaveBeenCalledWith('POST', '/kimi/chat/completions', {
      json: {
        model: 'kimi-k3',
        messages: [{ role: 'user', content: 'Hi' }],
        stream: true,
      },
    });
  });

  it('wires the kimi resource onto the top-level client', () => {
    const client = new AceDataCloud({ apiToken: 'test-token' });

    expect(client.kimi).toBeDefined();
    expect(client.kimi).toBeInstanceOf(Kimi);
  });
});
