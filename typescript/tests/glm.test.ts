import { AceDataCloud } from '../src';

describe('GLM chat completions', () => {
  afterEach(() => {
    jest.restoreAllMocks();
  });

  it('supports the latest documented models and request parameters', async () => {
    const fetchMock = jest.spyOn(global, 'fetch').mockResolvedValue(
      new Response(JSON.stringify({ id: 'glm-1' }), {
        status: 200,
        headers: { 'content-type': 'application/json' },
      })
    );
    const client = new AceDataCloud({
      apiToken: 'test-token',
      baseURL: 'https://api.acedata.cloud',
      maxRetries: 0,
    });

    const result = await client.glm.chat.completions.create({
      model: 'glm-5.2',
      messages: [{ role: 'user', content: 'Hi' }],
      reasoning_effort: 'high',
    });

    expect(result).toEqual({ id: 'glm-1' });
    expect(fetchMock).toHaveBeenCalledWith(
      'https://api.acedata.cloud/glm/chat/completions',
      expect.objectContaining({
        body: JSON.stringify({
          model: 'glm-5.2',
          messages: [{ role: 'user', content: 'Hi' }],
          reasoning_effort: 'high',
        }),
      })
    );
  });
});
