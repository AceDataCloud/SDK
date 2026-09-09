import { Suno } from '../src/resources/providers/suno';

describe('Suno provider', () => {
  it('serializes current upload options', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'upload-1' });
    const suno = new Suno({ request } as any);

    await suno.upload({
      audioUrl: 'https://cdn.example.com/reference.wav',
      mode: 'enhanced',
      name: 'Reference',
      callbackUrl: 'https://example.com/callback',
    });

    expect(request).toHaveBeenCalledWith('POST', '/suno/upload', {
      json: {
        audio_url: 'https://cdn.example.com/reference.wav',
        mode: 'enhanced',
        name: 'Reference',
        callback_url: 'https://example.com/callback',
      },
    });
  });
});
