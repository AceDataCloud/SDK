import { AiChat } from '../src/resources/aichat';

describe('AiChat resource', () => {
  it('accepts newly documented models and posts to /aichat/conversations', async () => {
    const request = jest.fn().mockResolvedValue({ id: 'conv-1', answer: 'ok' });
    const aichat = new AiChat({ request } as any);

    await aichat.create({
      model: 'gpt-5.6-sol',
      question: 'hello',
      references: ['https://example.com'],
    });

    expect(request).toHaveBeenCalledWith('POST', '/aichat/conversations', {
      json: {
        model: 'gpt-5.6-sol',
        question: 'hello',
        references: ['https://example.com'],
      },
    });
  });
});
