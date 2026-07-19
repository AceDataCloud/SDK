import { Kimi } from '../src/resources/kimi';

describe('Kimi resource', () => {
  it('calls chat completions endpoint', async () => {
    const request = jest.fn().mockResolvedValue({ id: 'cmpl-kimi' });
    const kimi = new Kimi({ request } as any);

    const result = await kimi.chat.completions.create({
      model: 'kimi-k3',
      messages: [{ role: 'user', content: 'Hi' }],
      temperature: 0.7,
    });

    expect(result).toEqual({ id: 'cmpl-kimi' });
    expect(request).toHaveBeenCalledWith('POST', '/kimi/chat/completions', {
      json: {
        model: 'kimi-k3',
        messages: [{ role: 'user', content: 'Hi' }],
        temperature: 0.7,
      },
    });
  });

  it('streams chat completion chunks', async () => {
    const requestStream = jest.fn(async function* () {
      yield '{"delta":"a"}';
      yield '{"delta":"b"}';
    });
    const kimi = new Kimi({ requestStream } as any);

    const stream = await kimi.chat.completions.create({
      model: 'kimi-k3',
      messages: [{ role: 'user', content: 'Hi' }],
      stream: true,
    });
    const chunks = [];
    for await (const chunk of stream) chunks.push(chunk);

    expect(chunks).toEqual([{ delta: 'a' }, { delta: 'b' }]);
    expect(requestStream).toHaveBeenCalledWith('POST', '/kimi/chat/completions', {
      json: {
        model: 'kimi-k3',
        messages: [{ role: 'user', content: 'Hi' }],
        stream: true,
      },
    });
  });
});
