import { OpenAI } from '../src/resources/openai';

describe('OpenAI resource — new endpoints', () => {
  describe('models.list()', () => {
    it('calls GET /openai/models', async () => {
      const mockResponse = {
        object: 'list',
        data: [
          { id: 'gpt-4o', object: 'model', created: 1714500000, owned_by: 'system' },
        ],
      };
      const request = jest.fn().mockResolvedValue(mockResponse);
      const openai = new OpenAI({ request } as any);

      const result = await openai.models.list();

      expect(request).toHaveBeenCalledWith('GET', '/openai/models');
      expect(result).toEqual(mockResponse);
    });
  });

  describe('audio.speech.create()', () => {
    it('calls POST /v1/audio/speech with requestBytes', async () => {
      const audioBytes = new Uint8Array([0xff, 0xfb, 0x90, 0x00]);
      const requestBytes = jest.fn().mockResolvedValue(audioBytes);
      const openai = new OpenAI({ request: jest.fn(), requestBytes } as any);

      const result = await openai.audio.speech.create({
        input: 'Hello from AceData Cloud.',
        model: 'tts-1-hd',
        voice: 'nova',
        responseFormat: 'mp3',
      });

      expect(requestBytes).toHaveBeenCalledWith('POST', '/v1/audio/speech', {
        json: {
          input: 'Hello from AceData Cloud.',
          model: 'tts-1-hd',
          voice: 'nova',
          response_format: 'mp3',
        },
      });
      expect(result).toEqual(audioBytes);
    });

    it('only includes provided params', async () => {
      const audioBytes = new Uint8Array([0]);
      const requestBytes = jest.fn().mockResolvedValue(audioBytes);
      const openai = new OpenAI({ request: jest.fn(), requestBytes } as any);

      await openai.audio.speech.create({ input: 'Hi' });

      expect(requestBytes).toHaveBeenCalledWith('POST', '/v1/audio/speech', {
        json: { input: 'Hi' },
      });
    });
  });

  describe('audio.transcriptions.create()', () => {
    it('calls POST /v1/audio/transcriptions with multipartRequest', async () => {
      const mockResponse = { text: 'Hello world' };
      const multipartRequest = jest.fn().mockResolvedValue(mockResponse);
      const openai = new OpenAI({ request: jest.fn(), multipartRequest } as any);

      const fileData = new Uint8Array([82, 73, 70, 70]);
      const result = await openai.audio.transcriptions.create({
        file: fileData,
        filename: 'test.wav',
        model: 'whisper-1',
        language: 'en',
      });

      expect(multipartRequest).toHaveBeenCalledWith('POST', '/v1/audio/transcriptions', {
        fileField: 'file',
        fileData,
        filename: 'test.wav',
        data: { model: 'whisper-1', language: 'en' },
      });
      expect(result).toEqual(mockResponse);
    });

    it('uses default filename when not provided', async () => {
      const mockResponse = { text: 'test' };
      const multipartRequest = jest.fn().mockResolvedValue(mockResponse);
      const openai = new OpenAI({ request: jest.fn(), multipartRequest } as any);

      await openai.audio.transcriptions.create({
        file: new Uint8Array([0]),
      });

      const call = multipartRequest.mock.calls[0];
      expect(call[2].filename).toBe('audio.mp3');
    });
  });

  describe('realtime.url()', () => {
    it('builds wss URL with default model', () => {
      const openai = new OpenAI({ baseURL: 'https://api.acedata.cloud', request: jest.fn() } as any);
      const url = openai.realtime.url();
      expect(url).toBe('wss://api.acedata.cloud/v1/realtime?model=gpt-realtime');
    });

    it('builds wss URL with custom model', () => {
      const openai = new OpenAI({ baseURL: 'https://api.acedata.cloud', request: jest.fn() } as any);
      const url = openai.realtime.url({ model: 'gpt-realtime-2' });
      expect(url).toBe('wss://api.acedata.cloud/v1/realtime?model=gpt-realtime-2');
    });
  });
});
