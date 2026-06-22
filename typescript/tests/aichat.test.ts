import { AiChat } from '../src/resources/aichat';

describe('AiChat resource', () => {
  it('posts conversations to /aichat/conversations', async () => {
    const request = jest.fn().mockResolvedValue({ id: 'conv-1' });
    const aichat = new AiChat({ request } as any);

    await aichat.create({
      model: 'glm-5.2',
      question: 'Hello',
      preset: 'general',
      stateful: true,
      references: ['doc-1'],
    });

    expect(request).toHaveBeenCalledWith('POST', '/aichat/conversations', {
      json: {
        model: 'glm-5.2',
        question: 'Hello',
        preset: 'general',
        stateful: true,
        references: ['doc-1'],
      },
    });
  });
});
