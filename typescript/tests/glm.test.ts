import { AceDataCloud } from '../src';

describe('GLM resource', () => {
  afterEach(() => {
    jest.restoreAllMocks();
  });

  it('posts chat completions to the GLM endpoint with the latest model enum', async () => {
    const fetchMock = jest.spyOn(global, 'fetch').mockResolvedValue(
      new Response(JSON.stringify({ id: 'glm-1' }), {
        status: 200,
        headers: { 'content-type': 'application/json' },
      })
    );
    const client = new AceDataCloud({ apiToken: 'test-token', baseURL: 'https://api.acedata.cloud', maxRetries: 0 });

    const result = await client.glm.chat.completions.create({
      model: 'glm-5.2',
      messages: [{ role: 'user', content: 'hi' }],
    });

    expect(result.id).toBe('glm-1');
    expect(fetchMock).toHaveBeenCalledWith(
      'https://api.acedata.cloud/glm/chat/completions',
      expect.objectContaining({
        body: JSON.stringify({
          model: 'glm-5.2',
          messages: [{ role: 'user', content: 'hi' }],
        }),
      })
    );
  });
});
