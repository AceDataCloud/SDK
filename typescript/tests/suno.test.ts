import { Suno } from '../src/resources/providers/suno';

describe('Suno provider', () => {
  it('uses current prompt shapes and persona endpoints', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'suno-1' });
    const suno = new Suno({ request } as any);

    await suno.generate({ prompt: 'a synthwave carol', lyricPrompt: 'winter lights' });
    expect(request).toHaveBeenCalledWith('POST', '/suno/audios', {
      json: expect.objectContaining({
        prompt: 'a synthwave carol',
        lyric_prompt: 'winter lights',
      }),
    });

    await suno.lyrics({ model: 'remi-v1', prompt: 'write about winter' });
    expect(request).toHaveBeenLastCalledWith('POST', '/suno/lyrics', {
      json: {
        model: 'remi-v1',
        prompt: 'write about winter',
      },
    });

    await suno.listPersona({ userId: 'user-1', limit: 10, offset: 5 });
    expect(request).toHaveBeenLastCalledWith('GET', '/suno/persona', {
      params: {
        user_id: 'user-1',
        limit: '10',
        offset: '5',
      },
    });

    await suno.deletePersona({ personaId: 'persona-1', userId: 'user-1' });
    expect(request).toHaveBeenLastCalledWith('DELETE', '/suno/persona', {
      params: {
        persona_id: 'persona-1',
        user_id: 'user-1',
      },
    });
  });
});
