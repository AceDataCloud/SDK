import { Captcha } from '../src/resources/captcha';

describe('Captcha resource', () => {
  describe('recognition.hcaptcha', () => {
    it('posts to /captcha/recognition/hcaptcha with all params', async () => {
      const request = jest.fn().mockResolvedValue({ token: 'abc' });
      const captcha = new Captcha({ request } as any);

      await captcha.recognition.hcaptcha({
        queries: ['q1', 'q2'],
        question: 'Select all cars',
        async: false,
      });

      expect(request).toHaveBeenCalledWith('POST', '/captcha/recognition/hcaptcha', {
        json: { queries: ['q1', 'q2'], question: 'Select all cars', async: false },
      });
    });

    it('omits undefined optional params', async () => {
      const request = jest.fn().mockResolvedValue({});
      const captcha = new Captcha({ request } as any);

      await captcha.recognition.hcaptcha();

      expect(request).toHaveBeenCalledWith('POST', '/captcha/recognition/hcaptcha', { json: {} });
    });
  });

  describe('recognition.image2text', () => {
    it('posts to /captcha/recognition/image2text with image', async () => {
      const request = jest.fn().mockResolvedValue({ text: 'hello' });
      const captcha = new Captcha({ request } as any);

      await captcha.recognition.image2text({ image: 'https://example.com/img.png' });

      expect(request).toHaveBeenCalledWith('POST', '/captcha/recognition/image2text', {
        json: { image: 'https://example.com/img.png' },
      });
    });
  });

  describe('recognition.recaptcha2', () => {
    it('posts to /captcha/recognition/recaptcha2 with image and question', async () => {
      const request = jest.fn().mockResolvedValue({ token: 'tok' });
      const captcha = new Captcha({ request } as any);

      await captcha.recognition.recaptcha2({ image: 'data:image/png;base64,...', question: 'Select cars' });

      expect(request).toHaveBeenCalledWith('POST', '/captcha/recognition/recaptcha2', {
        json: { image: 'data:image/png;base64,...', question: 'Select cars' },
      });
    });
  });

  describe('token.hcaptcha', () => {
    it('posts to /captcha/token/hcaptcha with required params', async () => {
      const request = jest.fn().mockResolvedValue({ token: 'tok-hcap' });
      const captcha = new Captcha({ request } as any);

      await captcha.token.hcaptcha({ websiteKey: 'key-123', websiteUrl: 'https://example.com' });

      expect(request).toHaveBeenCalledWith('POST', '/captcha/token/hcaptcha', {
        json: { website_key: 'key-123', website_url: 'https://example.com' },
      });
    });

    it('includes proxy when provided', async () => {
      const request = jest.fn().mockResolvedValue({});
      const captcha = new Captcha({ request } as any);

      await captcha.token.hcaptcha({
        websiteKey: 'key',
        websiteUrl: 'https://example.com',
        proxy: 'http://proxy:8080',
      });

      expect(request).toHaveBeenCalledWith('POST', '/captcha/token/hcaptcha', {
        json: { website_key: 'key', website_url: 'https://example.com', proxy: 'http://proxy:8080' },
      });
    });
  });

  describe('token.recaptcha2', () => {
    it('posts to /captcha/token/recaptcha2', async () => {
      const request = jest.fn().mockResolvedValue({ token: 'rc2-tok' });
      const captcha = new Captcha({ request } as any);

      await captcha.token.recaptcha2({ websiteKey: 'rc2-key', websiteUrl: 'https://example.com' });

      expect(request).toHaveBeenCalledWith('POST', '/captcha/token/recaptcha2', {
        json: { website_key: 'rc2-key', website_url: 'https://example.com' },
      });
    });
  });

  describe('token.recaptcha3', () => {
    it('posts to /captcha/token/recaptcha3 with page_action', async () => {
      const request = jest.fn().mockResolvedValue({ token: 'rc3-tok' });
      const captcha = new Captcha({ request } as any);

      await captcha.token.recaptcha3({
        websiteKey: 'rc3-key',
        websiteUrl: 'https://example.com',
        pageAction: 'login',
      });

      expect(request).toHaveBeenCalledWith('POST', '/captcha/token/recaptcha3', {
        json: { website_key: 'rc3-key', website_url: 'https://example.com', page_action: 'login' },
      });
    });
  });

  describe('token.turnstile', () => {
    it('posts to /captcha/token/turnstile with required params', async () => {
      const request = jest.fn().mockResolvedValue({ token: 'ts-tok' });
      const captcha = new Captcha({ request } as any);

      await captcha.token.turnstile({ websiteKey: 'ts-key', websiteUrl: 'https://example.com' });

      expect(request).toHaveBeenCalledWith('POST', '/captcha/token/turnstile', {
        json: { website_key: 'ts-key', website_url: 'https://example.com' },
      });
    });

    it('includes optional action and cdata', async () => {
      const request = jest.fn().mockResolvedValue({});
      const captcha = new Captcha({ request } as any);

      await captcha.token.turnstile({
        websiteKey: 'ts-key',
        websiteUrl: 'https://example.com',
        action: 'login',
        cdata: 'extra',
      });

      expect(request).toHaveBeenCalledWith('POST', '/captcha/token/turnstile', {
        json: { website_key: 'ts-key', website_url: 'https://example.com', action: 'login', cdata: 'extra' },
      });
    });
  });
});
