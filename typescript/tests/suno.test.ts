import { Suno } from '../src/resources/providers/suno';

describe('Suno provider', () => {
  it('serializes string text prompts from the current spec', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'suno-1' });
    const suno = new Suno({ request } as any);

    await suno.generate({
      prompt: 'A bright pop song',
      lyricPrompt: 'Write lyrics about summer',
    });

    expect(request.mock.calls[0][2].json).toEqual(
      expect.objectContaining({
        prompt: 'A bright pop song',
        lyric_prompt: 'Write lyrics about summer',
      }),
    );
  });

  it('always sends the required vox vocal range', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'vox-1' });
    const suno = new Suno({ request } as any);

    await suno.vox({ audioId: 'song-1', vocalStart: 0, vocalEnd: 12.5 });

    expect(request.mock.calls[0][2].json).toEqual(
      expect.objectContaining({
        audio_id: 'song-1',
        vocal_start: 0,
        vocal_end: 12.5,
      }),
    );
  });
});
