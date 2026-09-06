import { Glm } from '../src/resources/glm';

async function* streamChunks(chunks: string[]): AsyncGenerator<string> {
  for (const chunk of chunks) {
    yield chunk;
  }
}

describe('GLM resource', () => {
  it('posts non-stream requests to /glm/chat/completions', async () => {
    const request = jest.fn().mockResolvedValue({ id: 'glm-sync' });
    const glm = new Glm({ request } as any);

    const result = await glm.chat.completions.create({
      model: 'glm-5.3',
      messages: [{ role: 'user', content: 'Hi' }],
      temperature: 0.2,
    });

    expect(result).toEqual({ id: 'glm-sync' });
    expect(request).toHaveBeenCalledWith('POST', '/glm/chat/completions', {
      json: {
        model: 'glm-5.3',
        messages: [{ role: 'user', content: 'Hi' }],
        temperature: 0.2,
      },
    });
  });

  it('streams and parses chunked JSON responses', async () => {
    const requestStream = jest.fn().mockReturnValue(streamChunks(['{"delta":"hello"}']));
    const glm = new Glm({ request: jest.fn(), requestStream } as any);

    const stream = (await glm.chat.completions.create({
      model: 'glm-5.2',
      messages: [{ role: 'user', content: 'Hi' }],
      stream: true,
    })) as AsyncGenerator<Record<string, unknown>>;

    const chunks: Record<string, unknown>[] = [];
    for await (const chunk of stream) chunks.push(chunk);

    expect(chunks).toEqual([{ delta: 'hello' }]);
    expect(requestStream).toHaveBeenCalledWith('POST', '/glm/chat/completions', {
      json: {
        model: 'glm-5.2',
        messages: [{ role: 'user', content: 'Hi' }],
        stream: true,
      },
    });
  });
});
