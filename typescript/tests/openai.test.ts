import { OpenAI } from '../src/resources/openai';

describe('OpenAI resource', () => {
  it('maps audio transcription fields to the API payload', async () => {
    const request = jest.fn().mockResolvedValue({ text: 'hello world' });
    const openai = new OpenAI({ request } as any);

    await openai.audio.transcriptions.create({
      file: 'https://example.com/audio.mp3',
      model: 'gpt-transcribe',
      responseFormat: 'json',
      timestampGranularities: ['segment'],
      stream: false,
      languages: ['en'],
      keywords: ['Acme'],
    });

    expect(request).toHaveBeenCalledWith('POST', '/v1/audio/transcriptions', {
      json: {
        file: 'https://example.com/audio.mp3',
        model: 'gpt-transcribe',
        response_format: 'json',
        'timestamp_granularities[]': ['segment'],
        stream: false,
        'languages[]': ['en'],
        'keywords[]': ['Acme'],
      },
    });
  });
});
