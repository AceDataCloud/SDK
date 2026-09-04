import { Suno } from '../src/resources/providers/suno';
import { TaskHandle } from '../src/runtime/tasks';

describe('Suno provider', () => {
  it('supports the mp3 endpoint', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'suno-mp3-1' });
    const suno = new Suno({ request } as any);

    const task = await suno.mp3({ audioId: 'audio-1' });

    expect(task).toBeInstanceOf(TaskHandle);
    expect(request).toHaveBeenCalledWith('POST', '/suno/mp3', {
      json: {
        audio_id: 'audio-1',
        async: true,
      },
    });
  });

  it('requires and sends vocal window on vox', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'suno-vox-1' });
    const suno = new Suno({ request } as any);

    await suno.vox({ audioId: 'audio-2', vocalStart: 1.5, vocalEnd: 8.0 });

    expect(request).toHaveBeenCalledWith('POST', '/suno/vox', {
      json: {
        audio_id: 'audio-2',
        vocal_start: 1.5,
        vocal_end: 8.0,
        async: true,
      },
    });
  });

  it('defaults upload mode to standard', async () => {
    const request = jest.fn().mockResolvedValue({ id: 'ok' });
    const suno = new Suno({ request } as any);

    await suno.upload({ audioUrl: 'https://cdn.example.com/ref.mp3' });

    expect(request).toHaveBeenCalledWith('POST', '/suno/upload', {
      json: {
        audio_url: 'https://cdn.example.com/ref.mp3',
        mode: 'standard',
      },
    });
  });
});
