import { AceDataCloud } from '../src/client';

const cases = [
  ['completions', '/v1/chat/completions', 'gemini-4-argon'],
  ['completions', '/v1/chat/completions', 'gpt-4o-image'],
  ['responses', '/v1/responses', 'gpt-5-pro'],
  ['messages', '/v1/messages', 'claude-sonnet-5-5'],
  ['messages', '/v1/messages', 'claude-opus-5-5'],
] as const;

describe('Unified protocol entrypoints', () => {
  const originalFetch = global.fetch;
  afterEach(() => { global.fetch = originalFetch; });

  it.each(cases)('%s routes %s for %s without changing its model', async (protocol, path, model) => {
    for (const stream of [false, true]) {
      const data = { model, type: 'fixture' };
      const fetchMock = jest.fn().mockResolvedValue(new Response(
        stream ? `data: ${JSON.stringify(data)}\n\n` : JSON.stringify(data),
        { headers: { 'content-type': stream ? 'text/event-stream' : 'application/json' } },
      ));
      global.fetch = fetchMock;
      const client = new AceDataCloud({ apiToken: 'test-token', baseURL: 'https://api.acedata.cloud', maxRetries: 0 });
      const messages = [{ role: 'user', content: 'Fixture' }];
      const execute = () => {
        if (protocol === 'responses') {
          const options = { model, input: 'Fixture', max_output_tokens: 12 };
          return stream ? client.responses.create({ ...options, stream: true }) : client.responses.create(options);
        }
        if (protocol === 'messages') {
          const options = { model, messages, maxTokens: 12 };
          return stream ? client.chat.messages.create({ ...options, stream: true }) : client.chat.messages.create(options);
        }
        const options = { model, messages, max_tokens: 12 };
        return stream ? client.chat.completions.create({ ...options, stream: true }) : client.chat.completions.create(options);
      };
      const result = await execute();
      if (stream) {
        const events = [];
        for await (const event of result as AsyncGenerator<Record<string, unknown>>) events.push(event);
        expect(events).toEqual([data]);
      } else expect(result).toEqual(data);
      expect(fetchMock).toHaveBeenCalledTimes(1);
      const [url, options] = fetchMock.mock.calls[0];
      expect(url).toBe(`https://api.acedata.cloud${path}`);
      const headers = new Headers(options.headers);
      expect(headers.get('authorization')).toBe('Bearer test-token');
      expect(headers.has('x-api-key')).toBe(false);
      expect(JSON.parse(options.body)).toEqual({
        model,
        ...(protocol === 'responses' ? { input: 'Fixture', max_output_tokens: 12 } : { messages, max_tokens: 12 }),
        ...(stream ? { stream: true } : {}),
      });
    }
  });

  it('keeps existing OpenAI-compatible facade paths', async () => {
    const fetchMock = jest.fn().mockImplementation(() => Promise.resolve(new Response('{}', { headers: { 'content-type': 'application/json' } })));
    global.fetch = fetchMock;
    const client = new AceDataCloud({ apiToken: 'test-token', baseURL: 'https://api.acedata.cloud', maxRetries: 0 });
    await client.openai.chat.completions.create({ model: 'gpt-4.1', messages: [] });
    await client.openai.responses.create({ model: 'gpt-4.1', input: 'Fixture' });
    expect(fetchMock.mock.calls.map(([url]) => url)).toEqual([
      'https://api.acedata.cloud/openai/chat/completions', 'https://api.acedata.cloud/openai/responses',
    ]);
  });
});
