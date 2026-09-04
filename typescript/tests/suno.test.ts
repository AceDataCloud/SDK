import { Suno } from '../src/resources/providers/suno';
import { TaskHandle } from '../src/runtime/tasks';

describe('Suno provider', () => {
  it('supports the new mp3 endpoint as an async task', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'suno-mp3-1' });
    const suno = new Suno({ request } as any);

    const task = await suno.mp3({ audioId: 'audio-1' });

    expect(task).toBeInstanceOf(TaskHandle);
    expect(request).toHaveBeenCalledWith('POST', '/suno/mp3', {
      json: { audio_id: 'audio-1', async: true },
    });
  });

  it('uses standard as the upload mode default', async () => {
    const request = jest.fn().mockResolvedValue({ success: true });
    const suno = new Suno({ request } as any);

    await suno.upload({ audioUrl: 'https://cdn.example.com/audio.mp3' });

    expect(request).toHaveBeenCalledWith('POST', '/suno/upload', {
      json: { audio_url: 'https://cdn.example.com/audio.mp3', mode: 'standard' },
    });
  });
});
