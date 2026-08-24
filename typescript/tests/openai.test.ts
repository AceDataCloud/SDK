import { AceDataCloud } from '../src';

describe('OpenAI facade', () => {
  afterEach(() => {
    jest.restoreAllMocks();
  });

  it('lists models', async () => {
    const fetchMock = jest.spyOn(global, 'fetch').mockResolvedValue(
      new Response(JSON.stringify({ object: 'list', data: [] }), {
        status: 200,
        headers: { 'content-type': 'application/json' },
      })
    );
    const client = new AceDataCloud({ apiToken: 'test-token', baseURL: 'https://api.acedata.cloud' });

    const result = await client.openai.models.list();

    expect(result.object).toBe('list');
    expect(fetchMock).toHaveBeenCalledWith('https://api.acedata.cloud/openai/models', expect.any(Object));
  });

  it('creates speech audio', async () => {
    const fetchMock = jest.spyOn(global, 'fetch').mockResolvedValue(
      new Response(new Uint8Array([1, 2, 3]), {
        status: 200,
        headers: { 'content-type': 'audio/mpeg' },
      })
    );
    const client = new AceDataCloud({ apiToken: 'test-token', baseURL: 'https://api.acedata.cloud' });

    const result = await client.openai.audio.speech.create({
      input: 'hello',
      model: 'tts-1',
      voice: 'alloy',
      responseFormat: 'mp3',
    });

    expect(Array.from(new Uint8Array(result))).toEqual([1, 2, 3]);
    expect(fetchMock).toHaveBeenCalledWith(
      'https://api.acedata.cloud/v1/audio/speech',
      expect.objectContaining({
        method: 'POST',
        body: JSON.stringify({ input: 'hello', model: 'tts-1', voice: 'alloy', response_format: 'mp3' }),
      })
    );
  });

  it('creates audio transcriptions with multipart form data', async () => {
    const fetchMock = jest.spyOn(global, 'fetch').mockResolvedValue(
      new Response(JSON.stringify({ text: 'hello' }), {
        status: 200,
        headers: { 'content-type': 'application/json' },
      })
    );
    const client = new AceDataCloud({ apiToken: 'test-token', baseURL: 'https://api.acedata.cloud' });

    const result = await client.openai.audio.transcriptions.create({
      file: new Uint8Array([1, 2, 3]),
      filename: 'sample.wav',
      model: 'whisper-1',
      responseFormat: 'json',
      timestampGranularities: ['word'],
    });

    expect(result).toEqual({ text: 'hello' });
    expect(fetchMock).toHaveBeenCalledWith(
      'https://api.acedata.cloud/v1/audio/transcriptions',
      expect.objectContaining({
        method: 'POST',
        body: expect.any(FormData),
      })
    );
  });
});
