import { OpenAI } from '../src/resources/openai';

describe('OpenAI resource', () => {
  it('maps models, audio, and realtime endpoints', async () => {
    const request = jest.fn().mockResolvedValue({ data: [{ id: 'gpt-realtime' }] });
    const requestBytes = jest.fn().mockResolvedValue(new ArrayBuffer(3));
    const multipart = jest.fn().mockResolvedValue({ text: 'hello' });
    const buildURL = jest.fn().mockReturnValue('wss://api.acedata.cloud/v1/realtime?model=gpt-realtime-2');
    const openai = new OpenAI({ request, requestBytes, multipart, buildURL } as any);

    await expect(openai.models.list()).resolves.toEqual({ data: [{ id: 'gpt-realtime' }] });
    await openai.audio.speech.create({ input: 'hello', model: 'tts-1', responseFormat: 'mp3' });
    await expect(
      openai.audio.transcriptions.create({
        file: Buffer.from('wav'),
        filename: 'sample.wav',
        model: 'whisper-1',
        timestampGranularities: ['word'],
      })
    ).resolves.toEqual({ text: 'hello' });

    expect(request).toHaveBeenCalledWith('GET', '/openai/models');
    expect(requestBytes).toHaveBeenCalledWith('POST', '/v1/audio/speech', {
      json: { input: 'hello', model: 'tts-1', response_format: 'mp3' },
    });
    expect(multipart).toHaveBeenCalledWith('/v1/audio/transcriptions', expect.any(Buffer), 'sample.wav', {
      fields: { model: 'whisper-1', 'timestamp_granularities[]': ['word'] },
    });
    expect(openai.realtime.url({ model: 'gpt-realtime-2' })).toBe(
      'wss://api.acedata.cloud/v1/realtime?model=gpt-realtime-2'
    );
    expect(buildURL).toHaveBeenCalledWith('/v1/realtime', {
      params: { model: 'gpt-realtime-2' },
      websocket: true,
    });
  });
});
