import { Veo } from '../src/resources/veo';

describe('Veo resource', () => {
  it('sends boolean translation flag to /veo/videos', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'task-veo' });
    const veo = new Veo({ request } as any);

    await veo.generate({
      action: 'text2video',
      prompt: 'A quick demo',
      translation: true,
    });

    expect(request).toHaveBeenCalledWith('POST', '/veo/videos', {
      json: {
        action: 'text2video',
        prompt: 'A quick demo',
        translation: true,
      },
    });
  });
});
