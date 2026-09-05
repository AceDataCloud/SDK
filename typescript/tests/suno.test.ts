import { Suno } from '../src/resources/providers/suno';
import { TaskHandle } from '../src/runtime/tasks';

describe('Suno provider', () => {
  it('serializes the latest Docs contract', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'suno-1' });
    const suno = new Suno({ request } as any);

    const task = await suno.mp3({
      audioId: 'audio-1',
      async: false,
      callbackUrl: 'https://example.com/hook',
    });
    expect(task).toBeInstanceOf(TaskHandle);
    expect(request).toHaveBeenLastCalledWith('POST', '/suno/mp3', {
      json: {
        audio_id: 'audio-1',
        callback_url: 'https://example.com/hook',
        async: false,
      },
    });

    await suno.generate({
      prompt: 'a short prompt',
      lyricPrompt: 'write a chorus',
      replaceSectionResultMode: 'candidates',
    });
    expect(request.mock.calls[request.mock.calls.length - 1][2].json).toEqual(
      expect.objectContaining({
        prompt: 'a short prompt',
        lyric_prompt: 'write a chorus',
        replace_section_result_mode: 'candidates',
      }),
    );

    await suno.upload({
      audioUrl: 'https://cdn.example.com/ref.mp3',
      mode: 'enhanced',
      name: 'Reference',
    });
    expect(request.mock.calls[request.mock.calls.length - 1][2].json).toEqual(
      expect.objectContaining({
        audio_url: 'https://cdn.example.com/ref.mp3',
        mode: 'enhanced',
        name: 'Reference',
      }),
    );
  });
});
