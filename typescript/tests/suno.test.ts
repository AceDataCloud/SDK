import { Suno } from '../src/resources/providers/suno';
import { TaskHandle } from '../src/runtime/tasks';

describe('Suno provider', () => {
  it('serializes new generation defaults and exposes MP3 tasks', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'suno-1' });
    const suno = new Suno({ request } as any);

    await suno.generate({ prompt: 'a song', lyricPrompt: 'write lyrics' });
    expect(request).toHaveBeenCalledWith('POST', '/suno/audios', {
      json: expect.objectContaining({
        prompt: 'a song',
        lyric_prompt: 'write lyrics',
        replace_section_result_mode: 'full_song',
        async: true,
      }),
    });

    expect(await suno.mp3({ audioId: 'audio-1' })).toBeInstanceOf(TaskHandle);
    expect(request).toHaveBeenLastCalledWith('POST', '/suno/mp3', {
      json: { audio_id: 'audio-1', async: true },
    });
  });

  it('uses the documented upload defaults', async () => {
    const request = jest.fn().mockResolvedValue({});
    const suno = new Suno({ request } as any);

    await suno.upload({ audioUrl: 'https://example.com/audio.mp3', name: 'reference' });
    expect(request).toHaveBeenCalledWith('POST', '/suno/upload', {
      json: { audio_url: 'https://example.com/audio.mp3', mode: 'standard', name: 'reference' },
    });
  });
});
