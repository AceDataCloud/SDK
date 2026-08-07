/** Captcha resources (`/captcha/*`). */

import { Transport } from '../runtime/transport';
import { TaskHandle } from '../runtime/tasks';

function taskId(result: Record<string, unknown>): string {
  if (typeof result.task_id === 'string') return result.task_id;
  return typeof result.id === 'string' ? result.id : '';
}

export interface HCaptchaRecognitionOptions {
  queries?: string[];
  question?: string;
  async?: boolean;
  wait?: boolean;
  pollInterval?: number;
  maxWait?: number;
  [key: string]: unknown;
}

export interface HCaptchaTokenOptions {
  websiteKey: string;
  websiteUrl: string;
  rqdata?: string;
  proxy?: string;
  async?: boolean;
  wait?: boolean;
  pollInterval?: number;
  maxWait?: number;
  [key: string]: unknown;
}

export class CaptchaRecognition {
  constructor(private transport: Transport) {}

  async hcaptcha(options: HCaptchaRecognitionOptions = {}): Promise<Record<string, unknown> | TaskHandle> {
    const body: Record<string, unknown> = {};
    if (options.queries !== undefined) body.queries = options.queries;
    if (options.question !== undefined) body.question = options.question;
    for (const [key, value] of Object.entries(options)) {
      if (!['async', 'maxWait', 'pollInterval', 'queries', 'question', 'wait'].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    body.async = options.async ?? false;
    const result = (await this.transport.request('POST', '/captcha/recognition/hcaptcha', { json: body })) as Record<
      string,
      unknown
    >;
    if (!body.async) return result;
    const handle = new TaskHandle(taskId(result), '/captcha/tasks', this.transport, result, {
      pollIdField: 'task_id',
      pollAction: null,
    });
    if (options.wait) await handle.wait({ pollInterval: options.pollInterval, maxWait: options.maxWait });
    return handle;
  }
}

export class CaptchaToken {
  constructor(private transport: Transport) {}

  async hcaptcha(options: HCaptchaTokenOptions): Promise<Record<string, unknown> | TaskHandle> {
    const body: Record<string, unknown> = {
      website_key: options.websiteKey,
      website_url: options.websiteUrl,
    };
    if (options.rqdata !== undefined) body.rqdata = options.rqdata;
    if (options.proxy !== undefined) body.proxy = options.proxy;
    for (const [key, value] of Object.entries(options)) {
      if (
        !['async', 'maxWait', 'pollInterval', 'proxy', 'rqdata', 'wait', 'websiteKey', 'websiteUrl'].includes(key) &&
        value !== undefined
      ) {
        body[key] = value;
      }
    }
    body.async = options.async ?? false;
    const result = (await this.transport.request('POST', '/captcha/token/hcaptcha', { json: body })) as Record<
      string,
      unknown
    >;
    if (!body.async) return result;
    const handle = new TaskHandle(taskId(result), '/captcha/tasks', this.transport, result, {
      pollIdField: 'task_id',
      pollAction: null,
    });
    if (options.wait) await handle.wait({ pollInterval: options.pollInterval, maxWait: options.maxWait });
    return handle;
  }
}

export class Captcha {
  readonly recognition: CaptchaRecognition;
  readonly token: CaptchaToken;

  constructor(transport: Transport) {
    this.recognition = new CaptchaRecognition(transport);
    this.token = new CaptchaToken(transport);
  }
}
