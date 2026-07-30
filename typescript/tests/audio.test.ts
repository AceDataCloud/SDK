import { Audio } from '../src/resources/audio';
import { Fish } from '../src/resources/providers/fish';

describe('Audio resource', () => {
  it('uses fish tts endpoint with text body and model header', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'task-fish' });
    const audio = new Audio({ request } as any);

    await audio.generate({
      provider: 'fish',
      prompt: 'hello',
      model: 'speech-1',
      callbackUrl: 'https://example.com/callback',
    });

    expect(request).toHaveBeenCalledWith('POST', '/fish/tts', {
      json: {
        text: 'hello',
        callback_url: 'https://example.com/callback',
      },
      headers: { model: 'speech-1' },
    });
  });

  it('keeps non-fish providers on /{provider}/audios', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'task-suno' });
    const audio = new Audio({ request } as any);

    await audio.generate({
      provider: 'suno',
      prompt: 'hello',
      model: 'chirp-v4',
    });

    expect(request).toHaveBeenCalledWith('POST', '/suno/audios', {
      json: {
        prompt: 'hello',
        model: 'chirp-v4',
      },
    });
  });

  it('calls fish model endpoints', async () => {
    const request = jest.fn().mockResolvedValue({ data: [] });
    const audio = new Audio({ request } as any);

    await audio.listFishModels({ pageSize: 10, pageNumber: 2, selfOnly: true });
    await audio.getFishModel('voice-1');

    expect(request).toHaveBeenNthCalledWith(1, 'GET', '/fish/model', {
      params: {
        page_size: '10',
        page_number: '2',
        self: 'true',
      },
    });
    expect(request).toHaveBeenNthCalledWith(2, 'GET', '/fish/model/voice-1');
  });

  it('ignores removed fish opus bitrate fields', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'task-fish' });
    const fish = new Fish({ request } as any);

    await fish.generate({ text: 'hello', format: 'pcm', opusBitrate: 64, opus_bitrate: 64 } as any);

    const body = request.mock.calls[0][2].json;
    expect(body).toMatchObject({
      text: 'hello',
      format: 'pcm',
      reference_id: 'd7900c21663f485ab63ebdb7e5905036',
      async: true,
    });
    expect(body).not.toHaveProperty('opus_bitrate');
    expect(body).not.toHaveProperty('opusBitrate');
  });
});
