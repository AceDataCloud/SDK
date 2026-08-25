import { Suno } from '../src/resources/providers/suno';
import { TaskHandle } from '../src/runtime/tasks';

describe('Suno provider', () => {
  it('submits string prompt fields from the current API schema', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'suno-1' });
    const suno = new Suno({ request } as any);

    const task = await suno.generate({
      prompt: 'A song for Christmas',
      lyricPrompt: 'winter chorus',
    });

    expect(task).toBeInstanceOf(TaskHandle);
    expect(request).toHaveBeenCalledWith('POST', '/suno/audios', {
      json: expect.objectContaining({
        prompt: 'A song for Christmas',
        lyric_prompt: 'winter chorus',
        async: true,
      }),
    });
  });

  it('includes the required vox vocal range even when it starts at zero', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'suno-vox-1' });
    const suno = new Suno({ request } as any);

    await suno.vox({
      audioId: 'audio-1',
      vocalStart: 0,
      vocalEnd: 60,
    });

    expect(request).toHaveBeenCalledWith('POST', '/suno/vox', {
      json: expect.objectContaining({
        audio_id: 'audio-1',
        vocal_start: 0,
        vocal_end: 60,
        async: true,
      }),
    });
  });
});
