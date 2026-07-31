import { OpenAI } from '../src/resources/openai';

describe('OpenAI resource', () => {
  describe('models.list', () => {
    it('calls GET /openai/models', async () => {
      const mockResponse = {
        object: 'list',
        data: [{ id: 'gpt-4o', object: 'model', created: 1714500000, owned_by: 'system' }],
      };
      const request = jest.fn().mockResolvedValue(mockResponse);
      const openai = new OpenAI({ request, getBaseURL: () => 'https://x402.acedata.cloud' } as any);

      const result = await openai.models.list();

      expect(request).toHaveBeenCalledWith('GET', '/openai/models');
      expect(result).toEqual(mockResponse);
    });
  });

  describe('realtime.url', () => {
    it('builds a wss:// URL with the given model', () => {
      const openai = new OpenAI({
        request: jest.fn(),
        getBaseURL: () => 'https://x402.acedata.cloud',
      } as any);

      const url = openai.realtime.url('gpt-realtime');
      expect(url).toBe('wss://x402.acedata.cloud/v1/realtime?model=gpt-realtime');
    });

    it('defaults to gpt-realtime model', () => {
      const openai = new OpenAI({
        request: jest.fn(),
        getBaseURL: () => 'https://x402.acedata.cloud',
      } as any);

      const url = openai.realtime.url();
      expect(url).toContain('model=gpt-realtime');
      expect(url).toMatch(/^wss:\/\//);
    });
  });

  describe('audio.speech.create', () => {
    it('calls POST /v1/audio/speech and returns Uint8Array', async () => {
      const fakeAudio = new Uint8Array([1, 2, 3]);
      const requestBytes = jest.fn().mockResolvedValue(fakeAudio);
      const openai = new OpenAI({
        request: jest.fn(),
        requestBytes,
        getBaseURL: () => 'https://x402.acedata.cloud',
      } as any);

      const result = await openai.audio.speech.create({
        input: 'Hello world',
        model: 'tts-1-hd',
        voice: 'nova',
      });

      expect(requestBytes).toHaveBeenCalledWith('POST', '/v1/audio/speech', {
        json: { input: 'Hello world', model: 'tts-1-hd', voice: 'nova', response_format: 'mp3' },
      });
      expect(result).toBe(fakeAudio);
    });
  });

  describe('audio.transcriptions.create', () => {
    it('calls uploadForm on /v1/audio/transcriptions', async () => {
      const mockResponse = { text: 'Hello from transcript.' };
      const uploadForm = jest.fn().mockResolvedValue(mockResponse);
      const openai = new OpenAI({
        request: jest.fn(),
        uploadForm,
        getBaseURL: () => 'https://x402.acedata.cloud',
      } as any);

      const fakeFile = new Uint8Array([1, 2, 3]);
      const result = await openai.audio.transcriptions.create({
        file: fakeFile,
        filename: 'test.mp3',
        model: 'whisper-1',
      });

      expect(uploadForm).toHaveBeenCalledWith(
        '/v1/audio/transcriptions',
        fakeFile,
        'test.mp3',
        { model: 'whisper-1', response_format: 'json' }
      );
      expect(result).toEqual(mockResponse);
    });

    it('includes optional fields when provided', async () => {
      const uploadForm = jest.fn().mockResolvedValue({ text: 'ok' });
      const openai = new OpenAI({
        request: jest.fn(),
        uploadForm,
        getBaseURL: () => 'https://x402.acedata.cloud',
      } as any);

      await openai.audio.transcriptions.create({
        file: Buffer.from('audio'),
        filename: 'audio.wav',
        model: 'whisper-1',
        language: 'en',
        prompt: 'test',
        responseFormat: 'text',
        temperature: 0.5,
      });

      expect(uploadForm).toHaveBeenCalledWith(
        '/v1/audio/transcriptions',
        Buffer.from('audio'),
        'audio.wav',
        { model: 'whisper-1', response_format: 'text', language: 'en', prompt: 'test', temperature: '0.5' }
      );
    });
  });
});
