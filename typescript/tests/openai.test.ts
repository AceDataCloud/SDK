import { OpenAI } from '../src/resources/openai';

describe('OpenAI responses', () => {
  it('maps new responses fields to API payload names', async () => {
    const request = jest.fn().mockResolvedValue({ id: 'resp-1' });
    const openai = new OpenAI({ request } as any);

    await openai.responses.create({
      model: 'gpt-4o-mini',
      input: 'hello',
      maxOutputTokens: 128,
      parallelToolCalls: false,
      responseFormat: { type: 'json_object' },
      streamOptions: { include_usage: true },
      toolChoice: { type: 'auto' },
    });

    expect(request).toHaveBeenCalledWith('POST', '/openai/responses', {
      json: {
        model: 'gpt-4o-mini',
        input: 'hello',
        max_output_tokens: 128,
        parallel_tool_calls: false,
        response_format: { type: 'json_object' },
        stream_options: { include_usage: true },
        tool_choice: { type: 'auto' },
      },
    });
  });
});
