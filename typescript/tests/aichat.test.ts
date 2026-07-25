import { AiChat } from '../src/resources/aichat';

describe('AiChat resource', () => {
  it('posts conversations with synced models', async () => {
    const request = jest.fn().mockResolvedValue({ id: 'conv-123' });
    const aichat = new AiChat({ request } as any);

    await aichat.create({
      model: 'gpt-5.6-sol',
      question: 'Hello',
      references: ['doc-1'],
    });

    expect(request).toHaveBeenCalledWith('POST', '/aichat/conversations', {
      json: {
        model: 'gpt-5.6-sol',
        question: 'Hello',
        references: ['doc-1'],
      },
    });
  });
});
