import { Suno } from '../src/resources/providers/suno';

describe('Suno provider', () => {
  it('serializes the latest Suno request fields', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'suno-task' });
    const suno = new Suno({ request } as any);

    await suno.generate({
      prompt: 'A song about winter',
      lyricPrompt: 'Write lyrics about snow',
      replaceSectionResultMode: 'candidates',
    });
    expect(request).toHaveBeenLastCalledWith('POST', '/suno/audios', {
      json: expect.objectContaining({
        prompt: 'A song about winter',
        lyric_prompt: 'Write lyrics about snow',
        replace_section_result_mode: 'candidates',
      }),
    });

    await suno.vox({ audioId: 'audio-1', vocalStart: 1.5, vocalEnd: 8 });
    expect(request).toHaveBeenLastCalledWith('POST', '/suno/vox', {
      json: expect.objectContaining({
        audio_id: 'audio-1',
        vocal_start: 1.5,
        vocal_end: 8,
      }),
    });

    await suno.upload({
      audioUrl: 'https://cdn.example.com/song.mp3',
      mode: 'enhanced',
      name: 'Reference',
    });
    expect(request).toHaveBeenLastCalledWith('POST', '/suno/upload', {
      json: expect.objectContaining({
        audio_url: 'https://cdn.example.com/song.mp3',
        mode: 'enhanced',
        name: 'Reference',
      }),
    });
  });
});
