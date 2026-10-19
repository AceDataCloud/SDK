import { Audio } from '../src/resources/audio';
import { Fish } from '../src/resources/providers/fish';
import { Transport } from '../src/runtime/transport';

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

  it.each([undefined, 'private'] as const)('accepts HTTP 201 when creating a Fish model (visibility=%s)', async (visibility) => {
    const response = { _id: 'd7900c21663f485ab63ebdb7e5905036', visibility: 'public' };
    const fetchMock = jest.spyOn(global, 'fetch').mockResolvedValue(
      new Response(JSON.stringify(response), {
        status: 201,
        headers: { 'content-type': 'application/json' },
      })
    );
    try {
      const fish = new Fish(new Transport({ apiToken: 'test-token', maxRetries: 0 }));
      const result = await fish.model({
        title: 'My Custom Voice',
        voices: 'https://example.com/sample-voice.mp3',
        ...(visibility === undefined ? {} : { visibility }),
      });

      expect(result).toEqual(response);
      expect(fetchMock).toHaveBeenCalledTimes(1);
      expect(fetchMock.mock.calls[0][0]).toBe('https://x402.acedata.cloud/fish/model');
      expect(JSON.parse(fetchMock.mock.calls[0][1]!.body as string)).toEqual({
        title: 'My Custom Voice',
        voices: 'https://example.com/sample-voice.mp3',
        ...(visibility === undefined ? {} : { visibility }),
      });
    } finally {
      fetchMock.mockRestore();
    }
  });

  it.each([[true, false], [true, true], [false, null]] as const)(
    'preserves Fish pagination for selfOnly=%s and has_more=%s', async (selfOnly, hasMore) => {
      const response = { total: 0, items: [], has_more: hasMore };
      const request = jest.fn().mockResolvedValue(response);
      const audio = new Audio({ request } as any);

      expect(await audio.listFishModels({ selfOnly, sortBy: 'created_at' })).toEqual(response);
      expect(request).toHaveBeenCalledWith('GET', '/fish/model', {
        params: { self: String(selfOnly), sort_by: 'created_at' },
      });
    }
  );

  it('calls fish model endpoints', async () => {
    const request = jest.fn().mockResolvedValue({ total: 0, items: [], has_more: false });
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
