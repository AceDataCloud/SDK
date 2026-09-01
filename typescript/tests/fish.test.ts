import { Fish } from '../src/resources/providers/fish';

describe('Fish provider', () => {
  it('serializes the current TTS contract', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'task-fish' });

    await new Fish({ request } as any).generate({
      text: 'Hello',
      format: 'pcm',
      mp3Bitrate: 192,
    });

    expect(request).toHaveBeenCalledWith('POST', '/fish/tts', {
      json: { text: 'Hello', format: 'pcm', mp3_bitrate: 192, async: true },
      headers: {},
    });
  });
});
