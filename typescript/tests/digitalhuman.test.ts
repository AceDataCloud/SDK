import { Digitalhuman } from '../src/resources/providers/digitalhuman';

describe('Digitalhuman provider', () => {
  it('allows imageUrl without videoUrl', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'task-digitalhuman' });
    const digitalhuman = new Digitalhuman({ request } as any);

    await digitalhuman.generate({ imageUrl: 'https://cdn.example.com/avatar.jpg' });

    const body = request.mock.calls[0][2].json;
    expect(body.image_url).toBe('https://cdn.example.com/avatar.jpg');
    expect(body).not.toHaveProperty('video_url');
  });

  it('rejects requests without videoUrl or imageUrl before transport', async () => {
    const request = jest.fn();
    const digitalhuman = new Digitalhuman({ request } as any);

    await expect(digitalhuman.generate({} as any)).rejects.toThrow('videoUrl or imageUrl is required');
    expect(request).not.toHaveBeenCalled();
  });
});
