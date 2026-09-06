import { Glm, type GlmModel } from '../src/resources/glm';

describe('GLM resource', () => {
  it('accepts latest docs model ids in GlmModel and sends them unchanged', async () => {
    const request = jest.fn().mockResolvedValue({ id: 'ok' });
    const glm = new Glm({ request, requestStream: jest.fn() } as any);
    const model: GlmModel = 'glm-5.3';

    await glm.chat.completions.create({
      model,
      messages: [{ role: 'user', content: 'Hello' }],
    });

    expect(request).toHaveBeenCalledWith('POST', '/glm/chat/completions', {
      json: { model: 'glm-5.3', messages: [{ role: 'user', content: 'Hello' }] },
    });
  });
});
