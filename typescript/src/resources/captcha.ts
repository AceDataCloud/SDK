/** Captcha solving resources (`/captcha/*`). */

import { Transport } from '../runtime/transport';
import { TaskHandle } from '../runtime/tasks';

type CaptchaResult = Promise<Record<string, unknown> | TaskHandle>;

class CaptchaBase {
  constructor(protected transport: Transport) {}

  protected async request(
    endpoint: string,
    body: Record<string, unknown>,
    opts: { wait?: boolean; pollInterval?: number; maxWait?: number } = {}
  ): CaptchaResult {
    const result = await this.transport.request('POST', endpoint, { json: body });
    const taskId = result.task_id as string | undefined;

    if (!taskId || (result.data && !opts.wait)) return result;

    const handle = new TaskHandle(taskId, '/captcha/tasks', this.transport);
    if (opts.wait) return handle.wait({ pollInterval: opts.pollInterval, maxWait: opts.maxWait });
    return handle;
  }
}

class Recognition extends CaptchaBase {
  hcaptcha(opts: {
    queries?: string[];
    question?: string;
    async?: boolean;
    wait?: boolean;
    pollInterval?: number;
    maxWait?: number;
    [key: string]: unknown;
  }): CaptchaResult {
    const { wait, pollInterval, maxWait, ...body } = opts;
    return this.request('/captcha/recognition/hcaptcha', body, { wait, pollInterval, maxWait });
  }

  image2text(opts: {
    image: string;
    async?: boolean;
    wait?: boolean;
    pollInterval?: number;
    maxWait?: number;
    [key: string]: unknown;
  }): CaptchaResult {
    const { wait, pollInterval, maxWait, ...body } = opts;
    return this.request('/captcha/recognition/image2text', body, { wait, pollInterval, maxWait });
  }

  recaptcha2(opts: {
    image: string;
    question: string;
    async?: boolean;
    wait?: boolean;
    pollInterval?: number;
    maxWait?: number;
    [key: string]: unknown;
  }): CaptchaResult {
    const { wait, pollInterval, maxWait, ...body } = opts;
    return this.request('/captcha/recognition/recaptcha2', body, { wait, pollInterval, maxWait });
  }
}

class Token extends CaptchaBase {
  hcaptcha(opts: {
    websiteKey: string;
    websiteUrl: string;
    proxy?: string;
    async?: boolean;
    wait?: boolean;
    pollInterval?: number;
    maxWait?: number;
    [key: string]: unknown;
  }): CaptchaResult {
    const { websiteKey, websiteUrl, wait, pollInterval, maxWait, ...rest } = opts;
    return this.request(
      '/captcha/token/hcaptcha',
      { website_key: websiteKey, website_url: websiteUrl, ...rest },
      { wait, pollInterval, maxWait }
    );
  }

  recaptcha2(opts: {
    websiteKey: string;
    websiteUrl: string;
    proxy?: string;
    async?: boolean;
    wait?: boolean;
    pollInterval?: number;
    maxWait?: number;
    [key: string]: unknown;
  }): CaptchaResult {
    const { websiteKey, websiteUrl, wait, pollInterval, maxWait, ...rest } = opts;
    return this.request(
      '/captcha/token/recaptcha2',
      { website_key: websiteKey, website_url: websiteUrl, ...rest },
      { wait, pollInterval, maxWait }
    );
  }

  recaptcha3(opts: {
    pageAction: string;
    websiteKey: string;
    websiteUrl: string;
    async?: boolean;
    wait?: boolean;
    pollInterval?: number;
    maxWait?: number;
    [key: string]: unknown;
  }): CaptchaResult {
    const { pageAction, websiteKey, websiteUrl, wait, pollInterval, maxWait, ...rest } = opts;
    return this.request(
      '/captcha/token/recaptcha3',
      { page_action: pageAction, website_key: websiteKey, website_url: websiteUrl, ...rest },
      { wait, pollInterval, maxWait }
    );
  }
}

export class Captcha {
  readonly recognition: Recognition;
  readonly token: Token;

  constructor(transport: Transport) {
    this.recognition = new Recognition(transport);
    this.token = new Token(transport);
  }
}
