import { Captcha } from '../src/resources/captcha';

describe('Captcha resource', () => {
  it('calls recognition endpoints with expected payloads', async () => {
    const request = jest.fn().mockResolvedValue({ success: true });
    const captcha = new Captcha({ request } as any);

    await captcha.recognition.hcaptcha({ queries: ['a', 'b'], question: 'pick bus', async: true });
    await captcha.recognition.image2text({ image: 'data:image/png;base64,abc' });
    await captcha.recognition.recaptcha2({ image: 'data:image/png;base64,def', question: 'cars' });

    expect(request).toHaveBeenNthCalledWith(1, 'POST', '/captcha/recognition/hcaptcha', {
      json: { queries: ['a', 'b'], question: 'pick bus', async: true },
    });
    expect(request).toHaveBeenNthCalledWith(2, 'POST', '/captcha/recognition/image2text', {
      json: { image: 'data:image/png;base64,abc' },
    });
    expect(request).toHaveBeenNthCalledWith(3, 'POST', '/captcha/recognition/recaptcha2', {
      json: { image: 'data:image/png;base64,def', question: 'cars' },
    });
  });

  it('maps token request fields to snake_case', async () => {
    const request = jest.fn().mockResolvedValue({ success: true });
    const captcha = new Captcha({ request } as any);

    await captcha.token.hcaptcha({ websiteKey: 'site-key', websiteUrl: 'https://example.com' });
    await captcha.token.recaptcha3({
      pageAction: 'submit',
      websiteKey: 'site-key',
      websiteUrl: 'https://example.com',
      async: true,
    });

    expect(request).toHaveBeenNthCalledWith(1, 'POST', '/captcha/token/hcaptcha', {
      json: {
        website_key: 'site-key',
        website_url: 'https://example.com',
      },
    });
    expect(request).toHaveBeenNthCalledWith(2, 'POST', '/captcha/token/recaptcha3', {
      json: {
        page_action: 'submit',
        website_key: 'site-key',
        website_url: 'https://example.com',
        async: true,
      },
    });
  });
});
