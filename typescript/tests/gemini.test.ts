import { Gemini } from '../src/resources/gemini';

describe('Gemini resource', () => {
  it('posts chat completions to the gemini path', async () => {
    const request = jest.fn().mockResolvedValue({ id: 'chat-1' });
    const gemini = new Gemini({ request } as any);

    await gemini.chat.completions.create({
      model: 'gemini-3.0-pro',
      messages: [{ role: 'user', content: 'hi' }],
      temperature: 0.5,
    });

    expect(request).toHaveBeenCalledWith('POST', '/gemini/chat/completions', {
      json: {
        model: 'gemini-3.0-pro',
        messages: [{ role: 'user', content: 'hi' }],
        temperature: 0.5,
      },
    });
  });

  it('applies spec defaults for video generation and returns a handle', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'task-gemini' });
    const gemini = new Gemini({ request } as any);

    const handle = await gemini.videos.generate({ prompt: 'a kitten in a garden' });

    expect(request).toHaveBeenCalledWith('POST', '/gemini/videos', {
      json: {
        prompt: 'a kitten in a garden',
        model: 'omni-flash',
        aspect_ratio: '16:9',
        resolution: '720p',
        async: true,
      },
    });
    expect(handle.id).toBe('task-gemini');
  });

  it('rejects more than one reference video', async () => {
    const request = jest.fn();
    const gemini = new Gemini({ request } as any);

    await expect(
      gemini.videos.generate({
        prompt: 'x',
        videoUrls: ['https://example.com/a.mp4', 'https://example.com/b.mp4'],
      }),
    ).rejects.toThrow(/at most 1/);
    expect(request).not.toHaveBeenCalled();
  });

  it('puts the model in the path for native generateContent', async () => {
    const request = jest.fn().mockResolvedValue({});
    const gemini = new Gemini({ request } as any);

    await gemini.generateContent({
      model: 'gemini-2.5-flash',
      contents: [{ role: 'user', parts: [{ text: 'hi' }] }],
      generationConfig: { temperature: 0.2 },
    });

    expect(request).toHaveBeenCalledWith('POST', '/v1beta/models/gemini-2.5-flash:generateContent', {
      json: {
        contents: [{ role: 'user', parts: [{ text: 'hi' }] }],
        generationConfig: { temperature: 0.2 },
      },
    });
  });
});
