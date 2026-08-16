import { AceDataCloud } from '../src';

describe('OpenAI-compatible resources', () => {
  afterEach(() => {
    jest.restoreAllMocks();
  });

  it('lists models and supports audio endpoints', async () => {
    const fetchMock = jest
      .spyOn(global, 'fetch')
      .mockResolvedValueOnce(new Response(JSON.stringify({ object: 'list', data: [] }), { status: 200 }))
      .mockResolvedValueOnce(new Response(new TextEncoder().encode('mp3-bytes'), { status: 200 }))
      .mockResolvedValueOnce(new Response(JSON.stringify({ text: 'hello' }), { status: 200 }));
    const client = new AceDataCloud({ apiToken: 'test-token', baseURL: 'https://api.acedata.cloud' });

    await expect(client.openai.models.list()).resolves.toMatchObject({ object: 'list' });
    const audio = await client.openai.audio.speech.create({ input: 'hello', voice: 'nova' });
    expect(new TextDecoder().decode(audio)).toBe('mp3-bytes');
    await expect(
      client.openai.audio.transcriptions.create({
        file: new Uint8Array([1, 2, 3]),
        filename: 'audio.wav',
        model: 'whisper-1',
      })
    ).resolves.toMatchObject({ text: 'hello' });

    expect(fetchMock.mock.calls[0][0]).toBe('https://api.acedata.cloud/openai/models');
    expect(fetchMock.mock.calls[1][0]).toBe('https://api.acedata.cloud/v1/audio/speech');
    expect(fetchMock.mock.calls[2][0]).toBe('https://api.acedata.cloud/v1/audio/transcriptions');
    expect(fetchMock.mock.calls[2][1]?.body).toBeInstanceOf(FormData);
  });
});
