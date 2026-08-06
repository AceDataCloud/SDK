import { Glm, GlmModel } from '../src/resources/glm';

describe('GLM resource', () => {
  it('supports the latest GLM model and completion endpoint', async () => {
    const request = jest.fn().mockResolvedValue({ id: 'glm-1', choices: [] });
    const glm = new Glm({ request } as any);
    const model: GlmModel = 'glm-5.2';

    await glm.chat.completions.create({
      model,
      messages: [{ role: 'user', content: 'Hi' }],
    });

    expect(request).toHaveBeenCalledWith('POST', '/glm/chat/completions', {
      json: {
        model: 'glm-5.2',
        messages: [{ role: 'user', content: 'Hi' }],
      },
    });
  });
});
