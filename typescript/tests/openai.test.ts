import { OpenAI } from '../src/resources/openai';

describe('OpenAI resource', () => {
  describe('models.list()', () => {
    it('calls GET /openai/models', async () => {
      const mockResponse = { object: 'list', data: [{ id: 'gpt-4o', object: 'model' }] };
      const request = jest.fn().mockResolvedValue(mockResponse);
      const openai = new OpenAI({ request } as any);

      const result = await openai.models.list();

      expect(request).toHaveBeenCalledWith('GET', '/openai/models');
      expect(result).toEqual(mockResponse);
    });
  });

  describe('audio.speech()', () => {
    it('calls POST /v1/audio/speech with required input', async () => {
      const mockResponse = { url: 'https://example.com/audio.mp3' };
      const request = jest.fn().mockResolvedValue(mockResponse);
      const openai = new OpenAI({ request } as any);

      const result = await openai.audio.speech({ input: 'Hello world' });

      expect(request).toHaveBeenCalledWith('POST', '/v1/audio/speech', {
        json: { input: 'Hello world' },
      });
      expect(result).toEqual(mockResponse);
    });

    it('sends all optional parameters snake_cased', async () => {
      const request = jest.fn().mockResolvedValue({});
      const openai = new OpenAI({ request } as any);

      await openai.audio.speech({
        input: 'Test',
        model: 'tts-1-hd',
        voice: 'nova',
        responseFormat: 'opus',
        speed: 1.5,
      });

      expect(request).toHaveBeenCalledWith('POST', '/v1/audio/speech', {
        json: {
          input: 'Test',
          model: 'tts-1-hd',
          voice: 'nova',
          response_format: 'opus',
          speed: 1.5,
        },
      });
    });
  });

  describe('realtime.url()', () => {
    it('returns wss URL with default model', () => {
      const openai = new OpenAI({} as any, 'https://x402.acedata.cloud');
      expect(openai.realtime.url()).toBe('wss://x402.acedata.cloud/v1/realtime?model=gpt-realtime');
    });

    it('returns wss URL with specified model', () => {
      const openai = new OpenAI({} as any, 'https://x402.acedata.cloud');
      expect(openai.realtime.url({ model: 'gpt-realtime-2' })).toBe(
        'wss://x402.acedata.cloud/v1/realtime?model=gpt-realtime-2'
      );
    });

    it('converts https base URL to wss', () => {
      const openai = new OpenAI({} as any, 'https://api.acedata.cloud');
      expect(openai.realtime.url()).toBe('wss://api.acedata.cloud/v1/realtime?model=gpt-realtime');
    });
  });
});
