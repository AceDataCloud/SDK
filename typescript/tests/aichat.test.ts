import { AiChat } from '../src/resources/aichat';

describe('AiChat resource', () => {
  it('preserves the legacy aichat endpoint', async () => {
    const request = jest.fn().mockResolvedValue({ ok: true });
    const aichat = new AiChat({ request } as any);

    await aichat.create({
      model: 'gpt-5.6-sol',
      question: 'Hello',
      id: 'conv-1',
      preset: 'default',
      stateful: true,
      references: ['doc-1'],
    });

    expect(request).toHaveBeenCalledWith('POST', '/aichat/conversations', {
      json: {
        model: 'gpt-5.6-sol',
        question: 'Hello',
        id: 'conv-1',
        preset: 'default',
        stateful: true,
        references: ['doc-1'],
      },
    });
  });

  it('serializes the aichat2 contract with snake_case request fields', async () => {
    const request = jest.fn().mockResolvedValue({ ok: true });
    const aichat = new AiChat({ request } as any);

    await aichat.createV2({
      model: 'claude-sonnet-5',
      action: 'chat',
      id: 'conv-2',
      question: 'Summarize this',
      message: { role: 'user', content: 'Hello' },
      stateful: false,
      references: ['doc-1', 'doc-2'],
      preset: 'agent',
      maxTurns: 8,
      async: true,
      callbackUrl: 'https://example.com/callback',
      allowedSkills: ['browser'],
      allowedMcpServers: ['github'],
      unattendedPolicy: { mode: 'auto' },
      toolResults: [{ tool: 'search', result: 'done' }],
      messages: [{ role: 'user', content: 'Hello again' }],
      title: 'Research thread',
      userId: 'user-1',
      applicationId: 'app-1',
      modelGroup: 'claude',
      offset: 10,
      limit: 5,
    });

    expect(request).toHaveBeenCalledWith('POST', '/aichat2/conversations', {
      json: {
        model: 'claude-sonnet-5',
        action: 'chat',
        id: 'conv-2',
        question: 'Summarize this',
        message: { role: 'user', content: 'Hello' },
        stateful: false,
        references: ['doc-1', 'doc-2'],
        preset: 'agent',
        max_turns: 8,
        async: true,
        callback_url: 'https://example.com/callback',
        allowed_skills: ['browser'],
        allowed_mcp_servers: ['github'],
        unattended_policy: { mode: 'auto' },
        tool_results: [{ tool: 'search', result: 'done' }],
        messages: [{ role: 'user', content: 'Hello again' }],
        title: 'Research thread',
        user_id: 'user-1',
        application_id: 'app-1',
        model_group: 'claude',
        offset: 10,
        limit: 5,
      },
    });
  });
});
