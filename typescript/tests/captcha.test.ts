import { Captcha } from '../src/resources/captcha';

describe('Captcha resource', () => {
  it('calls recognition hcaptcha endpoint', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'captcha-1' });
    const captcha = new Captcha({ request } as any);

    await captcha.recognition.hcaptcha({
      queries: ['cat'],
      question: 'Pick cats',
      async: true,
    });

    expect(request).toHaveBeenCalledWith('POST', '/captcha/recognition/hcaptcha', {
      json: { queries: ['cat'], question: 'Pick cats', async: true },
    });
  });

  it('calls token hcaptcha endpoint and maps website keys', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'captcha-2' });
    const captcha = new Captcha({ request } as any);

    await captcha.token.hcaptcha({
      websiteKey: 'site-key',
      websiteUrl: 'https://accounts.hcaptcha.com/demo',
      rqdata: 'rq',
      proxy: '1.2.3.4:8080',
      async: true,
    });

    expect(request).toHaveBeenCalledWith('POST', '/captcha/token/hcaptcha', {
      json: {
        website_key: 'site-key',
        website_url: 'https://accounts.hcaptcha.com/demo',
        rqdata: 'rq',
        proxy: '1.2.3.4:8080',
        async: true,
      },
    });
  });

  it('calls captcha tasks endpoint with task_id', async () => {
    const request = jest.fn().mockResolvedValue({ status: 'succeeded' });
    const captcha = new Captcha({ request } as any);

    await captcha.tasks.retrieve({ taskId: 'task-1' });

    expect(request).toHaveBeenCalledWith('POST', '/captcha/tasks', {
      json: { task_id: 'task-1' },
    });
  });
});
