import { OpenAI } from '../src/resources/openai';

describe('OpenAI chat completions endpoints', () => {
  it('uses /v1/chat/completions for non-stream requests', async () => {
    const transport = {
      request: jest.fn().mockResolvedValue({ id: 'ok' }),
      requestStream: jest.fn()
    };
    const openai = new OpenAI(transport as any);

    await openai.chat.completions.create({
      model: 'claude-sonnet-4-20250514',
      messages: [{ role: 'user', content: 'hi' }]
    });

    expect(transport.request).toHaveBeenCalledWith('POST', '/v1/chat/completions', {
      json: { model: 'claude-sonnet-4-20250514', messages: [{ role: 'user', content: 'hi' }] }
    });
  });

  it('uses /v1/chat/completions for stream requests', async () => {
    const transport = {
      request: jest.fn(),
      requestStream: jest.fn(async function* () {
        yield JSON.stringify({ id: 'chunk-1' });
        yield JSON.stringify({ id: 'chunk-2' });
      })
    };
    const openai = new OpenAI(transport as any);

    const stream = await openai.chat.completions.create({
      model: 'claude-sonnet-4-20250514',
      messages: [{ role: 'user', content: 'hi' }],
      stream: true
    });
    const chunks: Record<string, unknown>[] = [];
    for await (const chunk of stream as AsyncGenerator<Record<string, unknown>>) {
      chunks.push(chunk);
    }
    expect(chunks).toEqual([{ id: 'chunk-1' }, { id: 'chunk-2' }]);

    expect(transport.requestStream).toHaveBeenCalledWith('POST', '/v1/chat/completions', {
      json: { model: 'claude-sonnet-4-20250514', messages: [{ role: 'user', content: 'hi' }], stream: true }
    });
  });
});
