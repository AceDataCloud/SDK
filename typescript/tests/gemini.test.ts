import { Gemini } from '../src/resources/providers/gemini';
import { TaskHandle } from '../src/runtime/tasks';

describe('Gemini provider', () => {
  it('serializes video generation as a task request', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'gemini-video-1' });
    const gemini = new Gemini({ request } as any);

    const task = await gemini.generate({ prompt: 'A cinematic ocean sunrise' });

    expect(task).toBeInstanceOf(TaskHandle);
    expect(request).toHaveBeenCalledWith('POST', '/gemini/videos', {
      json: {
        prompt: 'A cinematic ocean sunrise',
        model: 'omni-flash',
        aspect_ratio: '16:9',
        resolution: '720p',
        async: true,
      },
    });
  });

  it('serializes generateContent model as a path parameter', async () => {
    const request = jest.fn().mockResolvedValue({ ok: true });
    const gemini = new Gemini({ request } as any);

    await gemini.model_generatecontent({
      model: 'gemini-2.5-flash',
      contents: [{ parts: [{ text: 'hi' }] }],
    });

    expect(request).toHaveBeenCalledWith('POST', '/v1beta/models/gemini-2.5-flash:generateContent', {
      json: {
        contents: [{ parts: [{ text: 'hi' }] }],
      },
    });
  });

  it('serializes streamGenerateContent query parameters separately from the body', async () => {
    const request = jest.fn().mockResolvedValue({ ok: true });
    const gemini = new Gemini({ request } as any);

    await gemini.model_streamgeneratecontent({
      model: 'gemini-2.5-flash',
      contents: [{ parts: [{ text: 'hi' }] }],
      alt: 'sse',
    });

    expect(request).toHaveBeenCalledWith('POST', '/v1beta/models/gemini-2.5-flash:streamGenerateContent', {
      json: {
        contents: [{ parts: [{ text: 'hi' }] }],
      },
      params: { alt: 'sse' },
    });
  });
});
