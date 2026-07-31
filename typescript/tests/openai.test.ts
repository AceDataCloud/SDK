import { OpenAI } from '../src/resources/openai';

describe('OpenAI models.list()', () => {
  it('calls GET /openai/models', async () => {
    const mockResponse = {
      object: 'list',
      data: [
        { id: 'gpt-4o', object: 'model', created: 1714500000, owned_by: 'system' },
        { id: 'gpt-4o-mini', object: 'model', created: 1714500000, owned_by: 'system' },
      ],
    };
    const request = jest.fn().mockResolvedValue(mockResponse);
    const openai = new OpenAI({ request } as any);

    const result = await openai.models.list();

    expect(request).toHaveBeenCalledWith('GET', '/openai/models');
    expect((result as any).object).toBe('list');
    expect((result as any).data).toHaveLength(2);
  });
});

describe('OpenAI audio.speech.create()', () => {
  it('calls POST /v1/audio/speech with required input', async () => {
    const audioBytes = Buffer.from('fake-audio');
    const request = jest.fn().mockResolvedValue(audioBytes);
    const openai = new OpenAI({ request } as any);

    await openai.audio.speech.create({
      input: 'Hello from AceData Cloud.',
      model: 'tts-1-hd',
      voice: 'nova',
      responseFormat: 'mp3',
    });

    expect(request).toHaveBeenCalledWith('POST', '/v1/audio/speech', {
      json: {
        input: 'Hello from AceData Cloud.',
        model: 'tts-1-hd',
        voice: 'nova',
        response_format: 'mp3',
      },
    });
  });

  it('omits optional fields when not provided', async () => {
    const request = jest.fn().mockResolvedValue(Buffer.from(''));
    const openai = new OpenAI({ request } as any);

    await openai.audio.speech.create({ input: 'Hello.' });

    expect(request).toHaveBeenCalledWith('POST', '/v1/audio/speech', {
      json: { input: 'Hello.' },
    });
  });
});

describe('OpenAI realtime.url()', () => {
  it('converts https base URL to wss and appends model query param', () => {
    const openai = new OpenAI({ baseURL: 'https://x402.acedata.cloud' } as any);

    const url = openai.realtime.url({ model: 'gpt-realtime' });

    expect(url).toBe('wss://x402.acedata.cloud/v1/realtime?model=gpt-realtime');
  });

  it('uses gpt-realtime as the default model', () => {
    const openai = new OpenAI({ baseURL: 'https://x402.acedata.cloud' } as any);

    const url = openai.realtime.url();

    expect(url).toContain('model=gpt-realtime');
  });

  it('supports gpt-realtime-2 model', () => {
    const openai = new OpenAI({ baseURL: 'https://x402.acedata.cloud' } as any);

    const url = openai.realtime.url({ model: 'gpt-realtime-2' });

    expect(url).toContain('model=gpt-realtime-2');
  });
});
