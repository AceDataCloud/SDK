import { Suno } from '../src/resources/providers/suno';

describe('Suno provider', () => {
  it('syncs recent Docs fields and mp3 endpoint', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'suno-1' });
    const suno = new Suno({ request } as any);

    await suno.generate({
      prompt: 'A song for the release',
      lyricPrompt: 'Write upbeat launch lyrics',
      replaceSectionResultMode: 'candidates',
    });
    expect(request).toHaveBeenLastCalledWith('POST', '/suno/audios', {
      json: expect.objectContaining({
        prompt: 'A song for the release',
        lyric_prompt: 'Write upbeat launch lyrics',
        replace_section_result_mode: 'candidates',
      }),
    });

    await suno.mp3({ audioId: 'audio-1', async: false });
    expect(request).toHaveBeenLastCalledWith('POST', '/suno/mp3', {
      json: { audio_id: 'audio-1', async: false },
    });

    await suno.upload({ audioUrl: 'https://example.com/audio.mp3', mode: 'enhanced', name: 'demo' });
    expect(request).toHaveBeenLastCalledWith('POST', '/suno/upload', {
      json: {
        audio_url: 'https://example.com/audio.mp3',
        mode: 'enhanced',
        name: 'demo',
      },
    });
  });
});
