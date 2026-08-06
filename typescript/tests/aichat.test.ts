import { AceDataCloud } from '../src';
import { AiChat, AiChat2 } from '../src/resources/aichat';

describe('AI Chat resources', () => {
  it('accepts latest aichat models', async () => {
    const request = jest.fn().mockResolvedValue({ answer: 'ok' });
    const aichat = new AiChat({ request } as any);

    await aichat.create({ model: 'gpt-5.6-sol', question: 'Hi' });

    expect(request).toHaveBeenCalledWith('POST', '/aichat/conversations', {
      json: { model: 'gpt-5.6-sol', question: 'Hi' },
    });
  });

  it('serializes aichat2 conversation options', async () => {
    const request = jest.fn().mockResolvedValue({ id: 'conversation-1' });
    const aichat2 = new AiChat2({ request } as any);

    await aichat2.create({
      model: 'claude-sonnet-5',
      action: 'chat',
      message: [{ type: 'text', text: 'Hi' }],
      async: true,
      allowed_mcp_servers: ['server-1'],
      unattended_policy: { expires_at: 123 },
      model_group: 'claude',
    });

    expect(request).toHaveBeenCalledWith('POST', '/aichat2/conversations', {
      json: {
        model: 'claude-sonnet-5',
        action: 'chat',
        message: [{ type: 'text', text: 'Hi' }],
        async: true,
        allowed_mcp_servers: ['server-1'],
        unattended_policy: { expires_at: 123 },
        model_group: 'claude',
      },
    });
  });

  it('attaches aichat2 to the top-level client', () => {
    const client = new AceDataCloud({ apiToken: 'test-token' });

    expect(client.aichat2).toBeInstanceOf(AiChat2);
  });
});
