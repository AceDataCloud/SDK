import { Video } from '../src/resources/video';

describe('Video resource', () => {
  it('supports dreamina payload fields', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'task-dreamina' });
    const video = new Video({ request } as any);

    await video.generate({
      provider: 'dreamina',
      imageUrl: 'https://cdn.acedata.cloud/i.jpg',
      audioUrl: 'https://cdn.acedata.cloud/a.wav',
      maskUrl: ['https://cdn.acedata.cloud/m.png'],
      model: 'omnihuman-1.5',
    });

    expect(request).toHaveBeenCalledWith('POST', '/dreamina/videos', {
      json: {
        image_url: 'https://cdn.acedata.cloud/i.jpg',
        audio_url: 'https://cdn.acedata.cloud/a.wav',
        mask_url: ['https://cdn.acedata.cloud/m.png'],
        model: 'omnihuman-1.5',
      },
    });
  });
});
