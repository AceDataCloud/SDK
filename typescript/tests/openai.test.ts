import { AceDataCloud } from '../src';

describe('OpenAI resource', () => {
  afterEach(() => {
    jest.restoreAllMocks();
  });

  it('maps new responses options to the OpenAI wire format', async () => {
    const fetchMock = jest.spyOn(global, 'fetch').mockResolvedValue(
      new Response(JSON.stringify({ id: 'resp-123' }), {
        status: 200,
        headers: { 'content-type': 'application/json' },
      })
    );
    const client = new AceDataCloud({ apiToken: 'test-token', baseURL: 'https://api.acedata.cloud', maxRetries: 0 });

    await client.openai.responses.create({
      model: 'gpt-5.6-luna',
      input: 'Hello',
      maxOutputTokens: 128,
      parallelToolCalls: false,
      reasoning: { effort: 'low' },
      store: true,
      streamOptions: { include_usage: true },
      text: { format: { type: 'text' } },
      toolChoice: 'auto',
    });

    expect(fetchMock).toHaveBeenCalledWith(
      'https://api.acedata.cloud/openai/responses',
      expect.objectContaining({
        body: JSON.stringify({
          model: 'gpt-5.6-luna',
          input: 'Hello',
          reasoning: { effort: 'low' },
          store: true,
          text: { format: { type: 'text' } },
          max_output_tokens: 128,
          parallel_tool_calls: false,
          stream_options: { include_usage: true },
          tool_choice: 'auto',
        }),
      })
    );
  });

  it('lists OpenAI-compatible models', async () => {
    const fetchMock = jest.spyOn(global, 'fetch').mockResolvedValue(
      new Response(JSON.stringify({ data: [{ id: 'gpt-5.6-luna' }] }), {
        status: 200,
        headers: { 'content-type': 'application/json' },
      })
    );
    const client = new AceDataCloud({ apiToken: 'test-token', baseURL: 'https://api.acedata.cloud', maxRetries: 0 });

    const result = await client.openai.models.list();

    expect(fetchMock).toHaveBeenCalledWith('https://api.acedata.cloud/openai/models', expect.any(Object));
    expect(result.data).toEqual([{ id: 'gpt-5.6-luna' }]);
  });
});
