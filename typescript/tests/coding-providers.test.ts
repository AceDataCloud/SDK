import { Claude } from '../src/resources/providers/claude';
import { Coding } from '../src/resources/providers/coding';
import { Deepseek } from '../src/resources/providers/deepseek';

describe('coding-related providers', () => {
  it('routes DeepSeek chat completions with the current model enum', async () => {
    const request = jest.fn().mockResolvedValue({ id: 'chatcmpl-1' });
    const deepseek = new Deepseek({ request } as any);

    await deepseek.completions({
      model: 'deepseek-v4-pro',
      messages: [{ role: 'user', content: 'hi' }],
    });

    expect(request).toHaveBeenCalledWith('POST', '/deepseek/chat/completions', {
      json: expect.objectContaining({ model: 'deepseek-v4-pro' }),
    });
  });

  it('routes Codex-compatible responses through the coding provider', async () => {
    const request = jest.fn().mockResolvedValue({ id: 'resp-1' });
    const coding = new Coding({ request } as any);

    await coding.responses({
      model: 'gpt-6-astra',
      input: 'Fix the failing test',
    });

    expect(request).toHaveBeenCalledWith('POST', '/openai/responses', {
      json: expect.objectContaining({ model: 'gpt-6-astra' }),
    });
  });

  it('resolves Claude Messages request schemas', async () => {
    const request = jest.fn().mockResolvedValue({ id: 'msg-1' });
    const claude = new Claude({ request } as any);

    await claude.messages({
      model: 'claude-sonnet-5',
      messages: [{ role: 'user', content: 'hi' }],
      maxTokens: 32,
    });

    expect(request).toHaveBeenCalledWith('POST', '/v1/messages', {
      json: expect.objectContaining({ max_tokens: 32 }),
    });
  });
});
