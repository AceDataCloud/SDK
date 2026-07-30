import { OpenAI } from '../src/resources/openai';

describe('OpenAI resource', () => {
  it('calls models list endpoint', async () => {
    const request = jest.fn().mockResolvedValue({ data: [] });
    const openai = new OpenAI({ request } as any);

    await openai.models.list();

    expect(request).toHaveBeenCalledWith('GET', '/openai/models');
  });

  it('calls audio speech endpoint with snake_case fields', async () => {
    const request = jest.fn().mockResolvedValue({ audio: 'base64' });
    const openai = new OpenAI({ request } as any);

    await openai.audio.speech({
      input: 'hello',
      model: 'tts-1',
      responseFormat: 'mp3',
      speed: 1.2,
    });

    expect(request).toHaveBeenCalledWith('POST', '/v1/audio/speech', {
      json: {
        input: 'hello',
        model: 'tts-1',
        response_format: 'mp3',
        speed: 1.2,
      },
    });
  });

  it('builds realtime websocket url from configured base url', () => {
    const openai = new OpenAI({ baseURL: 'https://x402.acedata.cloud/' } as any);

    expect(openai.realtime.url({ model: 'gpt-realtime-2' })).toBe(
      'wss://x402.acedata.cloud/v1/realtime?model=gpt-realtime-2'
    );
  });
});
