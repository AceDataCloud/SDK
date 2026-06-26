import { Audio } from '../src/resources/audio';

describe('Audio resource', () => {
  it('uses fish tts endpoint with text body and model header', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'task-fish' });
    const audio = new Audio({ request } as any);

    await audio.generate({
      provider: 'fish',
      prompt: 'hello',
      model: 'speech-1',
      callbackUrl: 'https://example.com/callback',
    });

    expect(request).toHaveBeenCalledWith('POST', '/fish/tts', {
      json: {
        text: 'hello',
        callback_url: 'https://example.com/callback',
      },
      headers: { model: 'speech-1' },
    });
  });

  it('keeps non-fish providers on /{provider}/audios', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'task-suno' });
    const audio = new Audio({ request } as any);

    await audio.generate({
      provider: 'suno',
      prompt: 'hello',
      model: 'chirp-v4',
    });

    expect(request).toHaveBeenCalledWith('POST', '/suno/audios', {
      json: {
        prompt: 'hello',
        model: 'chirp-v4',
      },
    });
  });

  it('maps documented Suno audio options to API field names', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'task-suno' });
    const audio = new Audio({ request } as any);

    await audio.generate({
      provider: 'suno',
      prompt: 'hello',
      lyric: 'verse',
      style: 'pop',
      variationCategory: 'remix',
      title: 'Song',
      action: 'extend',
      custom: true,
      lyricPrompt: { text: 'extra lyrics' },
      audioId: 'audio-1',
      mashupAudioIds: ['audio-1', 'audio-2'],
      audioUrls: ['https://cdn.example/song.mp3'],
      weirdness: 0.5,
      personaId: 'persona-1',
      overpaintingStart: 1,
      overpaintingEnd: 2,
      samplesStart: 3,
      samplesEnd: 4,
      underpaintingStart: 5,
      underpaintingEnd: 6,
      continueAt: 7,
      callbackUrl: 'https://example.com/callback',
      instrumental: true,
      vocalGender: 'female',
      styleNegative: 'noise',
      styleInfluence: 0.2,
      audioWeight: 0.8,
      replaceSectionEnd: 8,
      replaceSectionStart: 9,
    });

    expect(request).toHaveBeenCalledWith('POST', '/suno/audios', {
      json: {
        prompt: 'hello',
        lyric: 'verse',
        style: 'pop',
        variation_category: 'remix',
        title: 'Song',
        action: 'extend',
        custom: true,
        lyric_prompt: { text: 'extra lyrics' },
        audio_id: 'audio-1',
        mashup_audio_ids: ['audio-1', 'audio-2'],
        audio_urls: ['https://cdn.example/song.mp3'],
        weirdness: 0.5,
        persona_id: 'persona-1',
        overpainting_start: 1,
        overpainting_end: 2,
        samples_start: 3,
        samples_end: 4,
        underpainting_start: 5,
        underpainting_end: 6,
        continue_at: 7,
        callback_url: 'https://example.com/callback',
        instrumental: true,
        vocal_gender: 'female',
        style_negative: 'noise',
        style_influence: 0.2,
        audio_weight: 0.8,
        replace_section_end: 8,
        replace_section_start: 9,
      },
    });
  });

  it('calls fish model endpoints', async () => {
    const request = jest.fn().mockResolvedValue({ data: [] });
    const audio = new Audio({ request } as any);

    await audio.listFishModels({ pageSize: 10, pageNumber: 2, selfOnly: true });
    await audio.getFishModel('voice-1');

    expect(request).toHaveBeenNthCalledWith(1, 'GET', '/fish/model', {
      params: {
        page_size: '10',
        page_number: '2',
        self: 'true',
      },
    });
    expect(request).toHaveBeenNthCalledWith(2, 'GET', '/fish/model/voice-1');
  });
});
