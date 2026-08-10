import { AiChat } from '../src/resources/aichat';
import { Fish } from '../src/resources/providers/fish';

describe('Docs sync endpoints', () => {
  it('builds the aichat2 conversation body', async () => {
    const request = jest.fn().mockResolvedValue({ id: 'conversation-1' });
    const aichat = new AiChat({ request } as any);

    await aichat.createV2({
      model: 'glm-5.2',
      action: 'chat',
      question: 'hello',
      modelGroup: 'glm',
      allowedSkills: ['web'],
      async: false,
    });

    expect(request).toHaveBeenCalledWith('POST', '/aichat2/conversations', {
      json: {
        model: 'glm-5.2',
        action: 'chat',
        question: 'hello',
        model_group: 'glm',
        allowed_skills: ['web'],
        async: false,
      },
    });
  });

  it('sends the Fish model header and query endpoints', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'fish-1' });
    const fish = new Fish({ request } as any);

    await fish.generate({ text: 'hello', model: 's2.1-pro', mp3Bitrate: 128 });
    await fish.models({ pageSize: 20, self: true, title: 'voice' });
    await fish.getModel('voice-1');

    expect(request).toHaveBeenNthCalledWith(
      1,
      'POST',
      '/fish/tts',
      expect.objectContaining({
        json: expect.objectContaining({ text: 'hello', mp3_bitrate: 128 }),
        headers: { model: 's2.1-pro' },
      })
    );
    expect(request).toHaveBeenNthCalledWith(2, 'GET', '/fish/model', {
      params: { page_size: '20', self: 'true', title: 'voice' },
    });
    expect(request).toHaveBeenNthCalledWith(3, 'GET', '/fish/model/voice-1');
  });
});
