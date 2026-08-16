import { Suno } from '../src/resources/providers/suno';

describe('Suno provider', () => {
  it('sends string prompt fields for audios generation', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'suno-1' });
    const suno = new Suno({ request } as any);

    await suno.generate({ prompt: 'A song for Christmas', lyricPrompt: 'A lyric idea' });

    expect(request).toHaveBeenCalledWith('POST', '/suno/audios', {
      json: expect.objectContaining({
        prompt: 'A song for Christmas',
        lyric_prompt: 'A lyric idea',
      }),
    });
  });

  it('always sends vocal window fields for vox', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'suno-vox-1' });
    const suno = new Suno({ request } as any);

    await suno.vox({ audioId: 'audio-1', vocalStart: 0, vocalEnd: 12.5 });

    expect(request).toHaveBeenCalledWith('POST', '/suno/vox', {
      json: expect.objectContaining({
        audio_id: 'audio-1',
        vocal_start: 0,
        vocal_end: 12.5,
      }),
    });
  });

  it('sends lyrics prompt as string', async () => {
    const request = jest.fn().mockResolvedValue({ data: [] });
    const suno = new Suno({ request } as any);

    await suno.lyrics({ model: 'default', prompt: 'A song about winter' });

    expect(request).toHaveBeenCalledWith('POST', '/suno/lyrics', {
      json: expect.objectContaining({
        model: 'default',
        prompt: 'A song about winter',
      }),
    });
  });
});
