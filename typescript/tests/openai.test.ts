import { OpenAI } from '../src/resources/openai';

describe('OpenAI facade', () => {
  it('serializes newly documented Responses options', async () => {
    const request = jest.fn().mockResolvedValue({ id: 'resp-123' });
    const openai = new OpenAI({ request } as any);

    await openai.responses.create({
      model: 'gpt-5.6-sol',
      input: 'Hello',
      include: ['file_search_call.results'],
      maxOutputTokens: 128,
      parallelToolCalls: false,
      reasoning: { effort: 'low' },
      streamOptions: { include_usage: true },
      toolChoice: 'auto',
    });

    expect(request).toHaveBeenCalledWith('POST', '/openai/responses', {
      json: expect.objectContaining({
        include: ['file_search_call.results'],
        max_output_tokens: 128,
        parallel_tool_calls: false,
        reasoning: { effort: 'low' },
        stream_options: { include_usage: true },
        tool_choice: 'auto',
      }),
    });
  });

  it('lists OpenAI-compatible models', async () => {
    const request = jest.fn().mockResolvedValue({ object: 'list', data: [] });
    const openai = new OpenAI({ request } as any);

    await expect(openai.models.list()).resolves.toEqual({ object: 'list', data: [] });
    expect(request).toHaveBeenCalledWith('GET', '/openai/models');
  });
});
