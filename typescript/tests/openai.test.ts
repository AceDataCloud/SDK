import { OpenAI } from '../src/resources/openai';

describe('OpenAI resource', () => {
  afterEach(() => {
    jest.restoreAllMocks();
  });

  it('calls model, audio, transcription, and realtime endpoints', async () => {
    const request = jest.fn().mockResolvedValue({ data: [{ id: 'gpt-4o-mini' }] });
    const openai = new OpenAI({
      request,
      baseURL: 'https://api.acedata.cloud',
      headers: { authorization: '******', 'content-type': 'application/json' },
      timeout: 1000,
    } as any);

    const fetchMock = jest.spyOn(global, 'fetch').mockResolvedValueOnce(
      new Response(new Uint8Array([1, 2, 3]), { status: 200, headers: { 'content-type': 'audio/mpeg' } })
    ).mockResolvedValueOnce(
      new Response(JSON.stringify({ text: 'hello' }), { status: 200, headers: { 'content-type': 'application/json' } })
    );

    await expect(openai.models.list()).resolves.toEqual({ data: [{ id: 'gpt-4o-mini' }] });
    const speech = await openai.audio.speech({ input: 'hello', voice: 'nova', responseFormat: 'mp3' });
    await expect(openai.audio.transcriptions({ file: Buffer.from('abc'), filename: 'sample.wav' })).resolves.toEqual({
      text: 'hello',
    });

    expect(request).toHaveBeenCalledWith('GET', '/openai/models');
    expect(Array.from(new Uint8Array(speech))).toEqual([1, 2, 3]);
    expect(fetchMock.mock.calls[0][0]).toBe('https://api.acedata.cloud/v1/audio/speech');
    expect(JSON.parse(fetchMock.mock.calls[0][1]?.body as string)).toMatchObject({
      input: 'hello',
      voice: 'nova',
      response_format: 'mp3',
    });
    expect(fetchMock.mock.calls[1][0]).toBe('https://api.acedata.cloud/v1/audio/transcriptions');
    expect(openai.realtime.url()).toBe('wss://api.acedata.cloud/v1/realtime?model=gpt-realtime-2.1');
  });
});
