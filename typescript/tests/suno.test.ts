import { Suno } from '../src/resources/providers/suno';
import { TaskHandle } from '../src/runtime/tasks';

describe('Suno provider', () => {
  it('serializes Docs-synced generate parameters', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'suno-1' });
    const suno = new Suno({ request } as any);

    await suno.generate({
      prompt: 'lofi beat',
      lyricPrompt: 'write a short hook',
      replaceSectionResultMode: 'candidates',
    });

    expect(request.mock.calls[0][2].json).toMatchObject({
      prompt: 'lofi beat',
      lyric_prompt: 'write a short hook',
      replace_section_result_mode: 'candidates',
      async: true,
    });
  });

  it('supports the mp3 task endpoint', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'mp3-1' });
    const suno = new Suno({ request } as any);

    const handle = await suno.mp3({ audioId: 'audio-1' });

    expect(handle).toBeInstanceOf(TaskHandle);
    expect(request).toHaveBeenCalledWith('POST', '/suno/mp3', {
      json: {
        audio_id: 'audio-1',
        async: true,
      },
    });
  });

  it('supports upload mode and name', async () => {
    const request = jest.fn().mockResolvedValue({ data: { audio_id: 'uploaded-1' } });
    const suno = new Suno({ request } as any);

    await suno.upload({
      audioUrl: 'https://cdn.example.com/in.mp3',
      mode: 'enhanced',
      name: 'Reference',
    });

    expect(request.mock.calls[0][2].json).toEqual({
      audio_url: 'https://cdn.example.com/in.mp3',
      mode: 'enhanced',
      name: 'Reference',
    });
  });
});
