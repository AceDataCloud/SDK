import { Audio } from '../src/resources/audio';
import { Fish } from '../src/resources/providers/fish';
import { Suno, SunoGenerateOptions } from '../src/resources/providers/suno';
import { Producer, ProducerGenerateOptions } from '../src/resources/providers/producer';
import { Maestro } from '../src/resources/providers/maestro';
import { WebExtrator } from '../src/resources/webextrator';
import { Transport } from '../src/runtime/transport';

describe('Recent provider contracts', () => {
  it.each<ProducerGenerateOptions>([
    { action: 'generate', prompt: 'A jazz song' },
    { action: 'generate', custom: true, instrumental: true },
    { action: 'extend', audioId: 'source-audio', continueAt: 12.5, lyric: 'New verse' },
    { action: 'cover', audioId: 'source-audio' },
  ])('does not require lyrics and a prompt for every Producer action (%p)', async (options) => {
    const request = jest.fn().mockResolvedValue({});
    await new Producer({ request } as any).generate(options);
    expect(request).toHaveBeenCalledTimes(1);
    const body = request.mock.calls[0][2].json;
    expect(request.mock.calls[0].slice(0, 2)).toEqual(['POST', '/producer/audios']);
    expect(body.action).toBe(options.action);
    if (options.prompt === undefined) expect(body).not.toHaveProperty('prompt');
    else expect(body.prompt).toBe(options.prompt);
    if (options.lyric === undefined) expect(body).not.toHaveProperty('lyric');
    else expect(body.lyric).toBe(options.lyric);
  });

  it('accepts a freeform Maestro style and a reference voice', async () => {
    const request = jest.fn().mockResolvedValue({});
    await new Maestro({ request } as any).generate({
      prompt: 'Launch video', style: 'watercolor storyboard', voice: '0123456789abcdef0123456789abcdef',
    });
    expect(request.mock.calls[0][2].json).toMatchObject({
      style: 'watercolor storyboard', voice: '0123456789abcdef0123456789abcdef',
    });
  });

  it.each(['extract', 'render'] as const)('maps WebExtrator %s cookie and cache options', async (operation) => {
    const request = jest.fn().mockResolvedValue({});
    const client = new WebExtrator({ request } as any);
    const cookies = [{ name: 'session', value: 'test', domain: 'example.com', httpOnly: true, sameSite: 'Lax' as const }];
    await client[operation]({ url: 'https://example.com', cookies, bypassCache: false, cacheTtlSeconds: 0, delay: 0 });
    expect(request).toHaveBeenCalledWith('POST', `/webextrator/${operation}`, {
      json: { url: 'https://example.com', cookies, bypass_cache: false, cache_ttl_seconds: 0, delay: 0 },
    });
    request.mockClear();
    await client[operation]({ url: 'https://example.com' });
    expect(request).toHaveBeenCalledWith('POST', `/webextrator/${operation}`, { json: { url: 'https://example.com' } });
  });
});

describe('Audio resource', () => {
  const availability = {
    success: true,
    task_id: '11111111-1111-4111-8111-111111111111',
    trace_id: '22222222-2222-4222-8222-222222222222',
    data: { id: '33333333-3333-4333-8333-333333333333', available: true },
  };

  it('returns Suno availability directly without polling', async () => {
    const fetchMock = jest.spyOn(global, 'fetch').mockResolvedValue(
      new Response(JSON.stringify(availability), { status: 200 })
    );
    try {
      const suno = new Suno(new Transport({ apiToken: 'test-token', maxRetries: 0 }));

      expect(await suno.availability({ audioId: availability.data.id })).toEqual(availability);
      expect(fetchMock).toHaveBeenCalledTimes(1);
      expect(fetchMock.mock.calls[0][0]).toBe('https://x402.acedata.cloud/suno/availability');
      expect(JSON.parse(fetchMock.mock.calls[0][1]!.body as string)).toEqual({ audio_id: availability.data.id });
      expect(new Headers(fetchMock.mock.calls[0][1]!.headers).get('Authorization')).toBe('Bearer test-token');
    } finally {
      fetchMock.mockRestore();
    }
  });

  it.each([500, 503])('throws on inconclusive Suno availability (HTTP %s), not false', async (status) => {
    const body = {
      error: { code: 'availability_unknown', message: 'Availability could not be confirmed.' },
      trace_id: 'test-trace',
    };
    const fetchMock = jest.spyOn(global, 'fetch').mockResolvedValue(
      new Response(JSON.stringify(body), { status })
    );
    try {
      const suno = new Suno(new Transport({ apiToken: 'test-token', maxRetries: 0 }));

      await expect(suno.availability({ audioId: availability.data.id })).rejects.toMatchObject({
        statusCode: status, code: 'availability_unknown', traceId: 'test-trace', body,
      });
      expect(fetchMock).toHaveBeenCalledTimes(1);
    } finally {
      fetchMock.mockRestore();
    }
  });

  it.each([undefined, 'voice-persona'])('serializes an optional Suno upload persona (%s)', async (personaId) => {
    const request = jest.fn().mockResolvedValue({});
    const suno = new Suno({ request } as any);

    await suno.upload({ audioUrl: 'https://example.com/song.mp3', personaId });

    expect(request).toHaveBeenCalledTimes(1);
    expect(request).toHaveBeenCalledWith('POST', '/suno/upload', {
      json: {
        audio_url: 'https://example.com/song.mp3',
        ...(personaId === undefined ? {} : { persona_id: personaId }),
      },
    });
  });

  it.each([undefined, 'full_song', 'candidates'] as const)(
    'maps Suno replacement lyrics and result mode (%s)', async (replaceSectionResultMode) => {
      const request = jest.fn().mockResolvedValue({});
      const options: SunoGenerateOptions = {
        action: 'replace_section', audioId: 'source-audio',
        lyric: 'Local new lyrics', prompt: 'Local new lyrics',
        replaceSectionStart: 0, replaceSectionEnd: 12.5, replaceSectionResultMode,
      };

      await new Suno({ request } as any).generate(options);

      expect(request).toHaveBeenCalledWith('POST', '/suno/audios', {
        json: {
          action: 'replace_section', audio_id: 'source-audio',
          lyric: 'Local new lyrics', prompt: 'Local new lyrics',
          replace_section_start: 0, replace_section_end: 12.5, async: true,
          ...(replaceSectionResultMode === undefined ? {} : { replace_section_result_mode: replaceSectionResultMode }),
        },
      });
    }
  );

  it.each([undefined, '', 'no distorted guitars; '.repeat(100)])(
    'preserves Suno negativeTags without truncation (%p)', async (negativeTags) => {
      const request = jest.fn().mockResolvedValue({});
      const suno = new Suno({ request } as any);

      await suno.generate({ custom: true, negativeTags });

      expect(request).toHaveBeenCalledWith('POST', '/suno/audios', {
        json: {
          custom: true,
          async: true,
          ...(negativeTags === undefined ? {} : { negative_tags: negativeTags }),
        },
      });
    }
  );

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
