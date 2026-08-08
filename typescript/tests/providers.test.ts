import { Claude, Gemini } from '../src/resources/providers';

describe('Claude provider', () => {
  it('calls the Claude chat completions endpoint with current models', async () => {
    const request = jest.fn().mockResolvedValue({ id: 'chat-1' });
    const claude = new Claude({ request } as any);

    const result = await claude.chat.completions.create({
      model: 'claude-opus-4-8',
      messages: [{ role: 'user', content: 'Hi' }],
      maxTokens: 10,
    });

    expect(result).toEqual({ id: 'chat-1' });
    expect(request).toHaveBeenCalledWith('POST', '/v1/chat/completions', {
      json: expect.objectContaining({
        model: 'claude-opus-4-8',
        max_tokens: 10,
        reasoning_effort: 'medium',
      }),
    });
  });
});

describe('Gemini provider', () => {
  it('returns a task handle from video generation and sends documented defaults', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'gemini-task' });
    const gemini = new Gemini({ request } as any);

    const handle = await gemini.videos.generate({ prompt: 'A kitten in a garden' });

    expect(handle.id).toBe('gemini-task');
    expect(request).toHaveBeenCalledWith('POST', '/gemini/videos', {
      json: {
        prompt: 'A kitten in a garden',
        model: 'omni-flash',
        aspect_ratio: '16:9',
        resolution: '720p',
        async: true,
      },
    });
  });
});
