import { Captcha } from '../src/resources/captcha';

describe('Captcha resource', () => {
  it('calls recognition endpoints with docs-aligned payloads', async () => {
    const request = jest.fn().mockResolvedValue({ text: '7364' });
    const captcha = new Captcha({ request } as any);

    await captcha.recognition.hcaptcha({
      question: 'Please click the center of the seahorses head',
      queries: 'seahorse',
      async: true,
    });
    await captcha.recognition.image2text({ image: 'base64-image' });
    await captcha.recognition.recaptcha2({ image: 'base64-image', question: 'Select all buses' });

    expect(request).toHaveBeenNthCalledWith(1, 'POST', '/captcha/recognition/hcaptcha', {
      json: {
        question: 'Please click the center of the seahorses head',
        queries: 'seahorse',
        async: true,
      },
    });
    expect(request).toHaveBeenNthCalledWith(2, 'POST', '/captcha/recognition/image2text', {
      json: { image: 'base64-image' },
    });
    expect(request).toHaveBeenNthCalledWith(3, 'POST', '/captcha/recognition/recaptcha2', {
      json: { image: 'base64-image', question: 'Select all buses' },
    });
  });

  it('maps token options to required snake_case fields', async () => {
    const request = jest.fn().mockResolvedValue({ token: 'abc' });
    const captcha = new Captcha({ request } as any);

    await captcha.token.hcaptcha({ websiteKey: 'k1', websiteUrl: 'https://example.com' });
    await captcha.token.recaptcha2({ websiteKey: 'k2', websiteUrl: 'https://example.com' });
    await captcha.token.recaptcha3({
      websiteKey: 'k3',
      websiteUrl: 'https://example.com',
      pageAction: 'submit',
      async: true,
    });

    expect(request).toHaveBeenNthCalledWith(1, 'POST', '/captcha/token/hcaptcha', {
      json: {
        website_key: 'k1',
        website_url: 'https://example.com',
      },
    });
    expect(request).toHaveBeenNthCalledWith(2, 'POST', '/captcha/token/recaptcha2', {
      json: {
        website_key: 'k2',
        website_url: 'https://example.com',
      },
    });
    expect(request).toHaveBeenNthCalledWith(3, 'POST', '/captcha/token/recaptcha3', {
      json: {
        website_key: 'k3',
        website_url: 'https://example.com',
        page_action: 'submit',
        async: true,
      },
    });
  });
});
