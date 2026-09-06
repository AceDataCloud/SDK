import { Suno } from '../src/resources/providers/suno';
import { TaskHandle } from '../src/runtime/tasks';

describe('Suno provider', () => {
  it('defaults replace_section_result_mode to full_song', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'suno-generate' });
    const suno = new Suno({ request } as any);

    await suno.generate({
      action: 'replace_section',
      replaceSectionStart: 1.25,
      replaceSectionEnd: 2.5,
    });

    expect(request).toHaveBeenCalledWith('POST', '/suno/audios', {
      json: expect.objectContaining({
        action: 'replace_section',
        replace_section_start: 1.25,
        replace_section_end: 2.5,
        replace_section_result_mode: 'full_song',
        async: true,
      }),
    });
  });

  it('submits mp3 export to /suno/mp3 and returns a task handle', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'suno-mp3' });
    const suno = new Suno({ request } as any);

    const task = await suno.mp3({ audioId: 'audio-123' });

    expect(task).toBeInstanceOf(TaskHandle);
    expect(task.id).toBe('suno-mp3');
    expect(request).toHaveBeenCalledWith('POST', '/suno/mp3', {
      json: {
        audio_id: 'audio-123',
        async: true,
      },
    });
  });
});
