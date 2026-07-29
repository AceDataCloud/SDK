import { AiChat } from '../src/resources/aichat';

describe('AiChat resource', () => {
  it('uses /aichat/conversations and accepts latest models', async () => {
    const request = jest.fn().mockResolvedValue({ id: 'chat-1', answer: 'Hello!' });
    const aichat = new AiChat({ request } as any);

    const result = await aichat.create({
      model: 'gpt-5.6-sol',
      question: 'Hi',
    });

    expect(request).toHaveBeenCalledWith('POST', '/aichat/conversations', {
      json: {
        model: 'gpt-5.6-sol',
        question: 'Hi',
      },
    });
    expect(result.id).toBe('chat-1');
  });
});
