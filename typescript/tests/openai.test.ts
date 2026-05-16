import { OpenAI } from '../src/resources/openai';

describe('OpenAI resource', () => {
  test('chat completions uses the docs endpoint', async () => {
    const request = jest.fn().mockResolvedValue({ id: 'chatcmpl-123' });
    const openai = new OpenAI({ request, requestStream: jest.fn() } as any);

    await openai.chat.completions.create({
      model: 'gpt-4o-mini',
      messages: [{ role: 'user', content: 'Hi' }],
    });

    expect(request).toHaveBeenCalledWith('POST', '/openai/chat/completions', {
      json: {
        model: 'gpt-4o-mini',
        messages: [{ role: 'user', content: 'Hi' }],
      },
    });
  });

  test('responses forwards the background option', async () => {
    const request = jest.fn().mockResolvedValue({ id: 'resp-123' });
    const openai = new OpenAI({ request, requestStream: jest.fn() } as any);

    await openai.responses.create({
      model: 'gpt-4o',
      input: [{ role: 'user', content: 'Hello' }],
      background: true,
    });

    expect(request).toHaveBeenCalledWith('POST', '/openai/responses', {
      json: {
        model: 'gpt-4o',
        input: [{ role: 'user', content: 'Hello' }],
        background: true,
      },
    });
  });
});
