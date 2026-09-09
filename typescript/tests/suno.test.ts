import { Suno } from '../src/resources/providers/suno';

describe('Suno provider', () => {
  it('sends latest generate parameters', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'task-suno' });
    const suno = new Suno({ request } as any);

    await suno.generate({
      model: 'chirp-v6',
      prompt: 'lofi track',
      lyricPrompt: 'write warm lyrics',
      replaceSectionResultMode: 'candidates',
    });

    expect(request).toHaveBeenCalledWith('POST', '/suno/audios', {
      json: expect.objectContaining({
        model: 'chirp-v6',
        prompt: 'lofi track',
        lyric_prompt: 'write warm lyrics',
        replace_section_result_mode: 'candidates',
      }),
    });
  });

  it('exposes mp3 as a task endpoint', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'task-mp3' });
    const suno = new Suno({ request } as any);

    const result = await suno.mp3({ audioId: 'audio-1' });

    expect(result.id).toBe('task-mp3');
    expect(request).toHaveBeenCalledWith('POST', '/suno/mp3', {
      json: {
        audio_id: 'audio-1',
        async: true,
      },
    });
  });
});
