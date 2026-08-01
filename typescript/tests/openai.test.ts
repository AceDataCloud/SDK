import { OpenAI } from '../src/resources/openai';
import { Transport } from '../src/runtime/transport';

describe('OpenAI resource', () => {
  afterEach(() => {
    jest.restoreAllMocks();
  });

  it('lists models from /openai/models', async () => {
    const request = jest.fn().mockResolvedValue({
      object: 'list',
      data: [{ id: 'gpt-4o-mini', object: 'model', created: 1, owned_by: 'openai' }],
    });
    const openai = new OpenAI({ request } as any);

    const result = await openai.models.list();

    expect(request).toHaveBeenCalledWith('GET', '/openai/models');
    expect((result as any).data[0].id).toBe('gpt-4o-mini');
  });

  it('returns audio bytes from /v1/audio/speech', async () => {
    jest.spyOn(global, 'fetch').mockResolvedValue(
      new Response('audio-bytes', { status: 200, headers: { 'content-type': 'audio/mpeg' } })
    );
    const openai = new OpenAI(new Transport({ apiToken: 'test-token', baseURL: 'https://api.acedata.cloud', maxRetries: 0 }));

    const result = await openai.audio.speech({
      input: 'Hello there',
      model: 'tts-1',
      voice: 'alloy',
    });

    expect(new TextDecoder().decode(result)).toBe('audio-bytes');
    expect(fetch).toHaveBeenCalledWith(
      'https://api.acedata.cloud/v1/audio/speech',
      expect.objectContaining({
        method: 'POST',
        headers: expect.objectContaining({ accept: 'audio/mpeg' }),
        body: JSON.stringify({ input: 'Hello there', model: 'tts-1', voice: 'alloy' }),
      })
    );
  });

  it('requests text transcriptions with bracketed array keys', async () => {
    jest.spyOn(global, 'fetch').mockResolvedValue(
      new Response('hello world', { status: 200, headers: { 'content-type': 'text/plain' } })
    );
    const openai = new OpenAI(new Transport({ apiToken: 'test-token', baseURL: 'https://api.acedata.cloud', maxRetries: 0 }));

    const result = await openai.audio.transcriptions({
      file: 'https://cdn.acedata.cloud/test.mp3',
      responseFormat: 'text',
      timestampGranularities: ['word'],
      languages: ['en'],
      keywords: ['sdk'],
    });

    expect(result).toBe('hello world');
    expect(fetch).toHaveBeenCalledWith(
      'https://api.acedata.cloud/v1/audio/transcriptions',
      expect.objectContaining({
        method: 'POST',
        headers: expect.objectContaining({ accept: 'text/plain' }),
        body: JSON.stringify({
          file: 'https://cdn.acedata.cloud/test.mp3',
          response_format: 'text',
          'timestamp_granularities[]': ['word'],
          'languages[]': ['en'],
          'keywords[]': ['sdk'],
        }),
      })
    );
  });

  it('builds websocket realtime URLs', () => {
    const openai = new OpenAI(new Transport({ apiToken: 'test-token', baseURL: 'https://api.acedata.cloud', maxRetries: 0 }));

    expect(openai.realtime.url({ model: 'gpt-realtime', voice: 'alloy' })).toBe(
      'wss://api.acedata.cloud/v1/realtime?model=gpt-realtime&voice=alloy'
    );
  });
});
