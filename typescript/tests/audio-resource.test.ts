import { Audio } from '../src/resources/audio';

describe('Audio resource fish routing', () => {
  test('uses /fish/tts with text body and model header', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 't1' });
    const audio = new Audio({ request } as any);

    await audio.generate({
      provider: 'fish',
      prompt: 'fallback prompt',
      text: 'hello fish',
      model: 's2-pro',
    });

    expect(request).toHaveBeenCalledWith('POST', '/fish/tts', {
      json: { text: 'hello fish' },
      headers: { model: 's2-pro' },
    });
  });

  test('keeps non-fish providers on /{provider}/audios', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 't2' });
    const audio = new Audio({ request } as any);

    await audio.generate({
      provider: 'suno',
      prompt: 'a happy song',
      model: 'v4',
    });

    expect(request).toHaveBeenCalledWith('POST', '/suno/audios', {
      json: { prompt: 'a happy song', model: 'v4' },
      headers: {},
    });
  });
});
