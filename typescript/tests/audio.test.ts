import { Audio } from '../src/resources/audio';

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

  it('maps fish camelCase options to API snake_case fields', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'task-fish' });
    const audio = new Audio({ request } as any);

    await audio.generate({
      provider: 'fish',
      prompt: 'hello',
      referenceId: 'voice-1',
      sampleRate: 32000,
      mp3Bitrate: 128,
      chunkLength: 200,
      minChunkLength: 100,
      topP: 0.8,
      repetitionPenalty: 1.1,
      maxNewTokens: 512,
      normalize: true,
    });

    expect(request).toHaveBeenCalledWith('POST', '/fish/tts', {
      json: {
        text: 'hello',
        reference_id: 'voice-1',
        sample_rate: 32000,
        mp3_bitrate: 128,
        chunk_length: 200,
        min_chunk_length: 100,
        top_p: 0.8,
        repetition_penalty: 1.1,
        max_new_tokens: 512,
        normalize: true,
      },
      headers: undefined,
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
});
