import { Suno, SunoLyricsOptions } from '../src/resources/providers/suno';
import { TaskHandle } from '../src/runtime/tasks';

describe('Suno provider', () => {
  it('serializes replace section result mode and string prompts', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'suno-1' });
    const suno = new Suno({ request } as any);

    await suno.generate({
      prompt: 'lofi beat',
      lyricPrompt: 'winter lyrics',
      replaceSectionResultMode: 'candidates',
    });

    expect(request.mock.calls[0][2].json).toMatchObject({
      prompt: 'lofi beat',
      lyric_prompt: 'winter lyrics',
      replace_section_result_mode: 'candidates',
      async: true,
    });
  });

  it('exposes mp3 as a task endpoint', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'suno-mp3' });
    const suno = new Suno({ request } as any);

    const task = await suno.mp3({ audioId: 'audio-1' });

    expect(task).toBeInstanceOf(TaskHandle);
    expect(request).toHaveBeenCalledWith('POST', '/suno/mp3', {
      json: { audio_id: 'audio-1', async: true },
    });
  });

  it('keeps lyrics model separate from generation models', () => {
    type LyricsModel = SunoLyricsOptions['model'];
    type ChirpIsSupported = 'chirp-v5' extends LyricsModel ? true : false;
    const chirpIsSupported: ChirpIsSupported = false;
    expect(chirpIsSupported).toBe(false);
  });
});
