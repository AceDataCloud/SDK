import { AiChat } from '../src/resources/aichat';
import { Deepseek } from '../src/resources/deepseek';

describe('AiChat resource', () => {
  it('sends latest model names and v2 conversation parameters', async () => {
    const request = jest.fn().mockResolvedValue({ id: 'conversation-1' });
    const aichat = new AiChat({ request } as any);

    await aichat.create({ model: 'deepseek-v4-pro', question: 'hi' });
    expect(request).toHaveBeenCalledWith('POST', '/aichat/conversations', {
      json: { model: 'deepseek-v4-pro', question: 'hi' },
    });

    await aichat.createV2({
      model: 'deepseek-v3.2-exp',
      action: 'chat',
      question: 'hi',
      allowed_skills: ['web_search'],
      async: true,
      limit: 10,
    });
    expect(request).toHaveBeenLastCalledWith('POST', '/aichat2/conversations', {
      json: {
        model: 'deepseek-v3.2-exp',
        action: 'chat',
        question: 'hi',
        allowed_skills: ['web_search'],
        async: true,
        limit: 10,
      },
    });
  });
});

describe('Deepseek resource', () => {
  it('uses the DeepSeek chat completions path', async () => {
    const request = jest.fn().mockResolvedValue({ choices: [] });
    const deepseek = new Deepseek({ request } as any);

    await deepseek.chat.completions.create({
      model: 'deepseek-v3.2-exp',
      messages: [{ role: 'user', content: 'hi' }],
      reasoning_effort: 'high',
      service_tier: 'priority',
      max_completion_tokens: 20,
    });

    expect(request).toHaveBeenCalledWith('POST', '/deepseek/chat/completions', {
      json: {
        model: 'deepseek-v3.2-exp',
        messages: [{ role: 'user', content: 'hi' }],
        reasoning_effort: 'high',
        service_tier: 'priority',
        max_completion_tokens: 20,
      },
    });
  });
});
