import { Gemini } from '../src/resources/providers/gemini';
import { TaskHandle } from '../src/runtime/tasks';

describe('Gemini provider', () => {
  it('calls chat completions at the docs path with defaults', async () => {
    const request = jest.fn().mockResolvedValue({ id: 'chat-1' });
    const gemini = new Gemini({ request } as any);

    await gemini.chat.completions.create({
      model: 'gemini-3.1-pro',
      messages: [{ role: 'user', content: 'hi' }],
    });

    expect(request).toHaveBeenCalledWith('POST', '/gemini/chat/completions', {
      json: expect.objectContaining({
        model: 'gemini-3.1-pro',
        messages: [{ role: 'user', content: 'hi' }],
        stream: false,
        reasoning_effort: 'medium',
      }),
    });
  });

  it('uses the native generateContent model path', async () => {
    const request = jest.fn().mockResolvedValue({ candidates: [] });
    const gemini = new Gemini({ request } as any);

    await gemini.generateContent({
      model: 'gemini-2.5-flash',
      contents: [{ parts: [{ text: 'hi' }] }],
      generationConfig: { temperature: 0 },
    });

    expect(request).toHaveBeenCalledWith('POST', '/v1beta/models/gemini-2.5-flash:generateContent', {
      json: {
        contents: [{ parts: [{ text: 'hi' }] }],
        generationConfig: { temperature: 0 },
      },
    });
  });

  it('streams native generateContent with alt=sse', async () => {
    async function* requestStream() {
      yield JSON.stringify({ candidates: [] });
    }
    const transport = { requestStream: jest.fn(requestStream) } as any;
    const gemini = new Gemini(transport);

    const chunks = [];
    for await (const chunk of gemini.streamGenerateContent({
      model: 'gemini-2.5-flash',
      contents: [{ parts: [{ text: 'hi' }] }],
    })) {
      chunks.push(chunk);
    }

    expect(chunks).toEqual([{ candidates: [] }]);
    expect(transport.requestStream).toHaveBeenCalledWith(
      'POST',
      '/v1beta/models/gemini-2.5-flash:streamGenerateContent?alt=sse',
      { json: { contents: [{ parts: [{ text: 'hi' }] }] } }
    );
  });

  it('returns a task handle for videos with spec defaults', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'gemini-video-task' });
    const gemini = new Gemini({ request } as any);

    const handle = await gemini.videos.generate({ prompt: 'a kitten' });

    expect(handle).toBeInstanceOf(TaskHandle);
    expect(handle.id).toBe('gemini-video-task');
    expect(request).toHaveBeenCalledWith('POST', '/gemini/videos', {
      json: {
        prompt: 'a kitten',
        model: 'omni-flash',
        aspect_ratio: '16:9',
        resolution: '720p',
        async: true,
      },
    });
  });
});
