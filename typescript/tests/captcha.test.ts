import { Captcha } from '../src/resources/captcha';

describe('Captcha resource', () => {
  it('calls hcaptcha recognition endpoint', async () => {
    const request = jest.fn().mockResolvedValue({ solution: {} });
    const captcha = new Captcha({ request } as any);

    await captcha.recognition.hcaptcha({
      queries: ['seahorse'],
      question: 'Click the seahorse',
      async: true,
    });

    expect(request).toHaveBeenCalledWith('POST', '/captcha/recognition/hcaptcha', {
      json: {
        queries: ['seahorse'],
        question: 'Click the seahorse',
        async: true,
      },
    });
  });

  it('maps recaptcha3 token parameters to the documented endpoint', async () => {
    const request = jest.fn().mockResolvedValue({ token: 'abc' });
    const captcha = new Captcha({ request } as any);

    await captcha.token.recaptcha3({
      pageAction: 'submit',
      websiteKey: 'site-key',
      websiteUrl: 'https://example.com/form',
      async: true,
    });

    expect(request).toHaveBeenCalledWith('POST', '/captcha/token/recaptcha3', {
      json: {
        page_action: 'submit',
        website_key: 'site-key',
        website_url: 'https://example.com/form',
        async: true,
      },
    });
  });
});
