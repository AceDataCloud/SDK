import { Glm } from '../src/resources/glm';
import type { AiChatModel, GlmModel } from '../src';

describe('GLM provider', () => {
  it('sends current Docs model names to chat completions', async () => {
    const request = jest.fn().mockResolvedValue({ choices: [] });
    const glm = new Glm({ request } as any);

    await glm.chat.completions.create({
      model: 'glm-5.3',
      messages: [{ role: 'user', content: 'Hi' }],
    });

    expect(request).toHaveBeenCalledWith('POST', '/glm/chat/completions', {
      json: {
        model: 'glm-5.3',
        messages: [{ role: 'user', content: 'Hi' }],
      },
    });
  });

  it('types new GLM models on both chat surfaces', () => {
    const glmModel: GlmModel = 'glm-5.3';
    const aiChatModel: AiChatModel = 'glm-5.2';

    expect(glmModel).toBe('glm-5.3');
    expect(aiChatModel).toBe('glm-5.2');
  });
});
