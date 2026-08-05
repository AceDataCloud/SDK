import { Audio } from '../src/resources/audio';
import { Suno } from '../src/resources/providers/suno';

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

  it('lists and deletes Suno personas with documented query parameters', async () => {
    const request = jest.fn().mockResolvedValue({ success: true });
    const suno = new Suno({ request } as any);

    await suno.listPersonas({ userId: 'user-1', limit: 25, offset: 5 });
    await suno.deletePersona({ personaId: 'persona-1', userId: 'user-1' });

    expect(request).toHaveBeenNthCalledWith(1, 'GET', '/suno/persona', {
      params: { user_id: 'user-1', limit: '25', offset: '5' },
    });
    expect(request).toHaveBeenNthCalledWith(2, 'DELETE', '/suno/persona', {
      params: { persona_id: 'persona-1', user_id: 'user-1' },
    });
  });
});
