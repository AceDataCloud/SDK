import { AiChat } from '../src/resources/aichat';
import { Glm } from '../src/resources/glm';

describe('AIChat and GLM resources', () => {
  it('calls aichat2 conversations endpoint and maps camel-case fields', async () => {
    const request = jest.fn().mockResolvedValue({ ok: true });
    const aichat = new AiChat({ request } as any);

    await aichat.createV2({
      model: 'gpt-5.4-mini',
      action: 'retrieve_batch',
      ids: ['extra-id'],
      async: false,
      offset: 0,
      limit: 25,
      allowedMcpServers: ['server-a'],
      toolResults: [{ tool_use_id: 'tool-1', output: 'ok', is_error: false }],
      modelGroup: 'chatgpt',
    });

    expect(request).toHaveBeenCalledWith('POST', '/aichat2/conversations', {
      json: {
        model: 'gpt-5.4-mini',
        ids: ['extra-id'],
        action: 'retrieve_batch',
        async: false,
        allowed_mcp_servers: ['server-a'],
        tool_results: [{ tool_use_id: 'tool-1', output: 'ok', is_error: false }],
        model_group: 'chatgpt',
        offset: 0,
        limit: 25,
      },
    });
  });

  it('passes current GLM completion fields through to the endpoint', async () => {
    const request = jest.fn().mockResolvedValue({ ok: true });
    const glm = new Glm({ request } as any);

    await glm.chat.completions.create({
      model: 'glm-5.3',
      messages: [{ role: 'user', content: 'hi' }],
      n: 1,
      temperature: 0,
      parallel_tool_calls: false,
      reasoning_effort: 'low',
      web_search_options: { search_context_size: 'medium' },
    });

    expect(request).toHaveBeenCalledWith('POST', '/glm/chat/completions', {
      json: {
        model: 'glm-5.3',
        messages: [{ role: 'user', content: 'hi' }],
        n: 1,
        temperature: 0,
        parallel_tool_calls: false,
        reasoning_effort: 'low',
        web_search_options: { search_context_size: 'medium' },
      },
    });
  });
});
