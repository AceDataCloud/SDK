import { Audio } from '../src/resources/audio';

describe('Audio resource', () => {
  test('uses fish tts endpoint and model header for fish provider', async () => {
    const request = jest.fn().mockResolvedValue({ audio_url: 'https://example.com/audio.mp3' });
    const audio = new Audio({ request } as any);

    await audio.generate({
      provider: 'fish',
      prompt: 'Hello world',
      model: 's2-pro',
      referenceId: 'voice-id',
      format: 'mp3',
      sampleRate: 44100,
    });

    expect(request).toHaveBeenCalledWith('POST', '/fish/tts', {
      json: {
        text: 'Hello world',
        reference_id: 'voice-id',
        format: 'mp3',
        sample_rate: 44100,
      },
      headers: { model: 's2-pro' },
    });
  });

  test('lists fish models with query params', async () => {
    const request = jest.fn().mockResolvedValue({ total: 1 });
    const audio = new Audio({ request } as any);

    await audio.listFishModels({ page_size: '20' });

    expect(request).toHaveBeenCalledWith('GET', '/fish/model', { params: { page_size: '20' } });
  });
});
