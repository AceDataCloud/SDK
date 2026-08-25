import { AceDataCloud, AiChat2Model, AiChatModel, GlmModel } from '../src';

const aichatModel: AiChatModel = 'gpt-5.6-luna';
const aichat2Model: AiChat2Model = 'claude-opus-4-6';
const glmModel: GlmModel = 'glm-5.3';
void [aichatModel, aichat2Model, glmModel];

describe('Docs sync resources', () => {
  afterEach(() => {
    jest.restoreAllMocks();
  });

  it('serializes AIChat v2 parameters', async () => {
    const fetchMock = jest.spyOn(global, 'fetch').mockResolvedValue(
      new Response(JSON.stringify({ id: 'conversation-1' }), {
        status: 200,
        headers: { 'content-type': 'application/json' },
      })
    );
    const client = new AceDataCloud({ apiToken: 'test-token', maxRetries: 0 });

    await client.aichat.createV2({
      model: 'claude-opus-4-6',
      action: 'chat',
      message: { role: 'user', content: 'hi' },
      allowedSkills: ['web_search'],
      allowedMcpServers: ['docs'],
      modelGroup: 'claude',
      async: true,
    });

    expect(fetchMock).toHaveBeenCalledWith(
      'https://x402.acedata.cloud/aichat2/conversations',
      expect.objectContaining({
        method: 'POST',
        body: JSON.stringify({
          model: 'claude-opus-4-6',
          action: 'chat',
          message: { role: 'user', content: 'hi' },
          async: true,
          allowed_skills: ['web_search'],
          allowed_mcp_servers: ['docs'],
          model_group: 'claude',
        }),
      })
    );
  });

  it('serializes latest OpenAI responses parameters', async () => {
    const fetchMock = jest.spyOn(global, 'fetch').mockResolvedValue(
      new Response(JSON.stringify({ id: 'resp-1' }), {
        status: 200,
        headers: { 'content-type': 'application/json' },
      })
    );
    const client = new AceDataCloud({ apiToken: 'test-token', maxRetries: 0 });

    await client.openai.responses.create({
      model: 'gpt-5.6-luna',
      input: 'hi',
      parallelToolCalls: false,
      include: ['file_search_call.results'],
      reasoning: { effort: 'medium' },
      text: { format: { type: 'text' } },
      maxOutputTokens: 128,
      streamOptions: { include_usage: true },
    });

    expect(fetchMock).toHaveBeenCalledWith(
      'https://x402.acedata.cloud/openai/responses',
      expect.objectContaining({
        method: 'POST',
        body: JSON.stringify({
          model: 'gpt-5.6-luna',
          input: 'hi',
          include: ['file_search_call.results'],
          reasoning: { effort: 'medium' },
          text: { format: { type: 'text' } },
          parallel_tool_calls: false,
          max_output_tokens: 128,
          stream_options: { include_usage: true },
        }),
      })
    );
  });

  it('lists OpenAI models', async () => {
    const fetchMock = jest.spyOn(global, 'fetch').mockResolvedValue(
      new Response(JSON.stringify({ object: 'list', data: [] }), {
        status: 200,
        headers: { 'content-type': 'application/json' },
      })
    );
    const client = new AceDataCloud({ apiToken: 'test-token', maxRetries: 0 });

    await expect(client.openai.models.list()).resolves.toEqual({ object: 'list', data: [] });
    expect(fetchMock).toHaveBeenCalledWith('https://x402.acedata.cloud/openai/models', expect.any(Object));
  });
});
