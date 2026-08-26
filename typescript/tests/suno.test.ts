import { Suno } from '../src/resources/providers/suno';

describe('Suno provider', () => {
  it('requires and serializes the vocal range for vox', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'suno-vox' });
    const suno = new Suno({ request } as any);

    await suno.vox({ audioId: 'audio-1', vocalStart: 1.5, vocalEnd: 30 });

    expect(request).toHaveBeenCalledWith('POST', '/suno/vox', {
      json: { audio_id: 'audio-1', vocal_start: 1.5, vocal_end: 30 },
    });
  });
});
