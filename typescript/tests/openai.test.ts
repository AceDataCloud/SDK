import { OpenAI } from '../src/resources/openai';

describe('OpenAI resource', () => {
  it('passes schema response options to /openai/responses', async () => {
    const request = jest.fn().mockResolvedValue({ id: 'resp-1' });
    const openai = new OpenAI({ request } as any);

    await openai.responses.create({
      model: 'gpt-4o-mini',
      input: 'hi',
      n: 2,
      background: 'auto',
      tools: [{ type: 'web_search_preview' }],
      max_tokens: 128,
      temperature: 0.2,
      response_format: { type: 'json_object' },
    });

    expect(request).toHaveBeenCalledWith('POST', '/openai/responses', {
      json: {
        model: 'gpt-4o-mini',
        input: 'hi',
        n: 2,
        background: 'auto',
        tools: [{ type: 'web_search_preview' }],
        max_tokens: 128,
        temperature: 0.2,
        response_format: { type: 'json_object' },
      },
    });
  });
});
