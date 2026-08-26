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

  it('calls recognition image2text endpoint', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'captcha-1b' });
    const captcha = new Captcha({ request } as any);

    await captcha.recognition.image2text({
      image: 'base64-image',
      async: false,
    });

    expect(request).toHaveBeenCalledWith('POST', '/captcha/recognition/image2text', {
      json: { image: 'base64-image', async: false },
    });
  });

  it('calls recognition recaptcha2 endpoint', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'captcha-1c' });
    const captcha = new Captcha({ request } as any);

    await captcha.recognition.recaptcha2({
      image: 'base64-grid',
      question: 'Pick buses',
      async: true,
    });

    expect(request).toHaveBeenCalledWith('POST', '/captcha/recognition/recaptcha2', {
      json: { image: 'base64-grid', question: 'Pick buses', async: true },
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

  it('calls token recaptcha2 endpoint and maps website keys', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'captcha-3' });
    const captcha = new Captcha({ request } as any);

    await captcha.token.recaptcha2({
      websiteKey: 'site-key',
      websiteUrl: 'https://www.google.com/recaptcha/api2/demo',
      proxy: '1.2.3.4:8080',
      async: true,
    });

    expect(request).toHaveBeenCalledWith('POST', '/captcha/token/recaptcha2', {
      json: {
        website_key: 'site-key',
        website_url: 'https://www.google.com/recaptcha/api2/demo',
        proxy: '1.2.3.4:8080',
        async: true,
      },
    });
  });

  it('calls token recaptcha3 endpoint and maps page_action', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'captcha-4' });
    const captcha = new Captcha({ request } as any);

    await captcha.token.recaptcha3({
      pageAction: 'submit',
      websiteKey: 'site-key',
      websiteUrl: 'https://www.google.com/recaptcha/api3/demo',
      async: false,
    });

    expect(request).toHaveBeenCalledWith('POST', '/captcha/token/recaptcha3', {
      json: {
        page_action: 'submit',
        website_key: 'site-key',
        website_url: 'https://www.google.com/recaptcha/api3/demo',
        async: false,
      },
    });
  });

  it('calls token turnstile endpoint', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'captcha-5' });
    const captcha = new Captcha({ request } as any);

    await captcha.token.turnstile({
      websiteKey: 'ts-site-key',
      websiteUrl: 'https://challenges.cloudflare.com/turnstile-demo',
      action: 'managed',
      cdata: 'abc123',
      async: false,
    });

    expect(request).toHaveBeenCalledWith('POST', '/captcha/token/turnstile', {
      json: {
        website_key: 'ts-site-key',
        website_url: 'https://challenges.cloudflare.com/turnstile-demo',
        action: 'managed',
        cdata: 'abc123',
        async: false,
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
