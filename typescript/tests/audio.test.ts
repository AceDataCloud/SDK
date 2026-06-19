import { Audio } from '../src/resources/audio';

describe('Audio resource', () => {
  it('uses fish tts endpoint with text body and model header', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'task-fish' });
    const audio = new Audio({ request } as any);

    await audio.generate({
      provider: 'fish',
      prompt: 'hello',
      model: 's1',
      callbackUrl: 'https://example.com/callback',
      referenceId: 'voice-ref',
      format: 'mp3',
      sampleRate: 44100,
      mp3Bitrate: 128,
      latency: 'balanced',
      chunkLength: 200,
      minChunkLength: 100,
      temperature: 0.7,
      topP: 0.9,
      repetitionPenalty: 1.1,
      maxNewTokens: 512,
      normalize: true,
      prosody: { speed: 1.2 },
      references: [{ audio: 'https://example.com/ref.mp3' }],
    });

    expect(request).toHaveBeenCalledWith('POST', '/fish/tts', {
      json: {
        text: 'hello',
        callback_url: 'https://example.com/callback',
        reference_id: 'voice-ref',
        format: 'mp3',
        sample_rate: 44100,
        mp3_bitrate: 128,
        latency: 'balanced',
        chunk_length: 200,
        min_chunk_length: 100,
        temperature: 0.7,
        top_p: 0.9,
        repetition_penalty: 1.1,
        max_new_tokens: 512,
        normalize: true,
        prosody: { speed: 1.2 },
        references: [{ audio: 'https://example.com/ref.mp3' }],
      },
      headers: { model: 's1' },
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
