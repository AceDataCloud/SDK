import { AceDataCloud } from '../src';

describe('Kimi resource', () => {
  afterEach(() => {
    jest.restoreAllMocks();
  });

  it('posts chat completions to the Kimi endpoint', async () => {
    const fetchMock = jest.spyOn(global, 'fetch').mockResolvedValue(
      new Response(JSON.stringify({ choices: [{ message: { content: 'Hello from Kimi' } }] }), {
        status: 200,
        headers: { 'content-type': 'application/json' },
      })
    );
    const client = new AceDataCloud({ apiToken: 'test-token', baseURL: 'https://api.acedata.cloud', maxRetries: 0 });

    const result = await client.kimi.chat.completions.create({
      model: 'kimi-k3',
      messages: [{ role: 'user', content: 'Hi' }],
      reasoning_effort: 'max',
    });

    expect(result).toEqual({ choices: [{ message: { content: 'Hello from Kimi' } }] });
    expect(fetchMock).toHaveBeenCalledWith(
      'https://api.acedata.cloud/kimi/chat/completions',
      expect.objectContaining({
        method: 'POST',
        body: JSON.stringify({
          model: 'kimi-k3',
          messages: [{ role: 'user', content: 'Hi' }],
          reasoning_effort: 'max',
        }),
      })
    );
  });
});
