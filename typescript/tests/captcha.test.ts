import { AceDataCloud } from '../src';
import { TaskHandle, taskStatus } from '../src/runtime/tasks';

describe('Captcha', () => {
  it('sends hcaptcha token parameters with API field names', async () => {
    const client = new AceDataCloud({ apiToken: 't' });
    const transport = {
      request: jest.fn().mockResolvedValue({ token: 'solved' }),
    };
    (client.captcha.token as any).transport = transport;

    const result = await client.captcha.token.hcaptcha({
      websiteKey: 'site-key',
      websiteUrl: 'https://example.com',
      rqdata: 'rq',
      proxy: 'http://proxy',
    });

    expect(result).toEqual({ token: 'solved' });
    expect(transport.request).toHaveBeenCalledWith('POST', '/captcha/token/hcaptcha', {
      json: {
        website_key: 'site-key',
        website_url: 'https://example.com',
        rqdata: 'rq',
        proxy: 'http://proxy',
        async: false,
      },
    });
  });

  it('returns an async handle that polls captcha tasks by task_id', async () => {
    const client = new AceDataCloud({ apiToken: 't' });
    const transport = {
      request: jest
        .fn()
        .mockResolvedValueOnce({ task_id: 'task-1', status: 'processing' })
        .mockResolvedValueOnce({ status: 'ready', token: 'ok' }),
    };
    (client.captcha.token as any).transport = transport;

    const handle = await client.captcha.token.hcaptcha({
      websiteKey: 'site-key',
      websiteUrl: 'https://example.com',
      async: true,
    });

    expect(handle).toBeInstanceOf(TaskHandle);
    await (handle as TaskHandle).get();
    expect(transport.request).toHaveBeenLastCalledWith('POST', '/captcha/tasks', {
      json: { task_id: 'task-1' },
    });
    expect((handle as TaskHandle).done).toBe(true);
  });

  it('sends hcaptcha recognition parameters', async () => {
    const client = new AceDataCloud({ apiToken: 't' });
    const transport = {
      request: jest.fn().mockResolvedValue({ solution: { label: 'cat' } }),
    };
    (client.captcha.recognition as any).transport = transport;

    await client.captcha.recognition.hcaptcha({
      queries: ['image'],
      question: 'Click cats',
    });

    expect(transport.request).toHaveBeenCalledWith('POST', '/captcha/recognition/hcaptcha', {
      json: {
        queries: ['image'],
        question: 'Click cats',
        async: false,
      },
    });
  });

  it('treats ready captcha tasks as successful terminal states', () => {
    expect(taskStatus({ status: 'ready', token: 'ok' })).toBe('succeeded');
  });
});
