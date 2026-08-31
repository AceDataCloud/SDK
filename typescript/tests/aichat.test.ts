import { AiChat } from '../src/resources/aichat';

describe('AIChat v2', () => {
  it('serializes current Gemini models and v2 fields', async () => {
    const transport = {
      request: jest.fn().mockResolvedValue({ id: 'conversation-1', answer: 'Hello' }),
    };
    const aichat = new AiChat(transport as never);

    await aichat.createV2({
      model: 'gemini-3.7-flash',
      action: 'chat',
      message: { role: 'user', content: 'Hello' },
      allowedMcpServers: ['server-1'],
      async: false,
      limit: 25,
    });

    expect(transport.request).toHaveBeenCalledWith('POST', '/aichat2/conversations', {
      json: {
        model: 'gemini-3.7-flash',
        action: 'chat',
        message: { role: 'user', content: 'Hello' },
        async: false,
        limit: 25,
        allowed_mcp_servers: ['server-1'],
      },
    });
  });
});
