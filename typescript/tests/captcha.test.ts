import { TaskHandle } from '../src/runtime/tasks';
import { Captcha } from '../src/resources/captcha';
import { Tasks } from '../src/resources/tasks';

describe('Captcha resource', () => {
  it('maps recaptcha3 token options to the documented endpoint', async () => {
    const request = jest.fn().mockResolvedValue({ token: 'captcha-token' });
    const captcha = new Captcha({ request } as any);

    await captcha.token.recaptcha3({
      pageAction: 'examples/v3scores',
      websiteKey: 'site-key',
      websiteUrl: 'https://example.com',
    });

    expect(request).toHaveBeenCalledWith('POST', '/captcha/token/recaptcha3', {
      json: {
        page_action: 'examples/v3scores',
        website_key: 'site-key',
        website_url: 'https://example.com',
      },
    });
  });

  it('returns a task handle for async captcha requests', async () => {
    const request = jest.fn().mockResolvedValue({ task_id: 'captcha-task' });
    const captcha = new Captcha({ request } as any);

    const result = await captcha.recognition.image2text({
      image: 'data:image/png;base64,abc',
      async: true,
    });

    expect(result).toBeInstanceOf(TaskHandle);
  });

  it('returns solved captcha responses immediately even when task_id is present', async () => {
    const solved = { task_id: 'captcha-task', token: 'captcha-token' };
    const request = jest.fn().mockResolvedValue(solved);
    const captcha = new Captcha({ request } as any);

    const result = await captcha.token.hcaptcha({
      websiteKey: 'site-key',
      websiteUrl: 'https://example.com',
      async: true,
    });

    expect(result).toEqual(solved);
  });

  it('polls captcha tasks through the shared captcha task endpoint', async () => {
    const request = jest.fn().mockResolvedValue({ response: { status: 'succeeded', data: { text: '1234' } } });
    const tasks = new Tasks({ request } as any);

    await tasks.get('captcha-task', { service: 'captcha' });

    expect(request).toHaveBeenCalledWith('POST', '/captcha/tasks', {
      json: { id: 'captcha-task', action: 'retrieve' },
    });
  });
});
