import { OpenAI } from '../src/resources/openai';

describe('OpenAI audio and models', () => {
  it('lists models', async () => {
    const request = jest.fn().mockResolvedValue({ data: [{ id: 'gpt-4o' }] });
    const openai = new OpenAI({ request } as any);

    await openai.models.list();

    expect(request).toHaveBeenCalledWith('GET', '/openai/models');
  });

  it('posts speech requests and returns the raw audio', async () => {
    const requestRaw = jest.fn().mockResolvedValue(new Uint8Array([1, 2, 3]));
    const openai = new OpenAI({ requestRaw } as any);

    const result = await openai.audio.speech.create({
      input: 'Hello from AceData Cloud.',
      model: 'tts-1-hd',
      voice: 'nova',
      responseFormat: 'mp3',
      speed: 1.25,
    });

    expect(result).toEqual(new Uint8Array([1, 2, 3]));
    expect(requestRaw).toHaveBeenCalledWith('POST', '/v1/audio/speech', {
      json: {
        input: 'Hello from AceData Cloud.',
        model: 'tts-1-hd',
        voice: 'nova',
        response_format: 'mp3',
        speed: 1.25,
      },
    });
  });

  it('uploads transcriptions as multipart form data', async () => {
    const requestRaw = jest.fn().mockResolvedValue(new TextEncoder().encode(JSON.stringify({ text: 'Hello.' })));
    const openai = new OpenAI({ requestRaw } as any);

    const result = await openai.audio.transcriptions.create({
      file: new Uint8Array([1, 2, 3]),
      filename: 'sample.mp3',
      model: 'gpt-transcribe',
      language: 'en',
      timestampGranularities: ['word'],
    });

    expect(result).toEqual({ text: 'Hello.' });
    const [method, path, opts] = requestRaw.mock.calls[0];
    expect(method).toBe('POST');
    expect(path).toBe('/v1/audio/transcriptions');
    const form = opts.form as FormData;
    expect(form.get('model')).toBe('gpt-transcribe');
    expect(form.get('language')).toBe('en');
    expect(form.get('timestamp_granularities[]')).toBe('word');
    expect((form.get('file') as File).name).toBe('sample.mp3');
  });

  it('wraps plain-text transcriptions', async () => {
    const requestRaw = jest.fn().mockResolvedValue(new TextEncoder().encode('Hello there.'));
    const openai = new OpenAI({ requestRaw } as any);

    const result = await openai.audio.transcriptions.create({
      file: new Uint8Array([1]),
      responseFormat: 'text',
    });

    expect(result).toEqual({ text: 'Hello there.' });
  });
});
