/** Captcha recognition and solving resources. */

import { Transport } from '../runtime/transport';
import { TaskHandle } from '../runtime/tasks';

export class Captcha {
  constructor(private transport: Transport) {}

  async recognize(opts: {
    queries?: string[];
    question?: string;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { queries, question, ...rest } = opts;
    const body: Record<string, unknown> = { ...rest };
    if (queries !== undefined) body.queries = queries;
    if (question !== undefined) body.question = question;
    return this.transport.request('POST', '/captcha/recognition/hcaptcha', { json: body });
  }

  async token(opts: {
    websiteKey: string;
    websiteUrl: string;
    async?: boolean;
    wait?: boolean;
    pollInterval?: number;
    maxWait?: number;
    [key: string]: unknown;
  }): Promise<Record<string, unknown> | TaskHandle> {
    const { websiteKey, websiteUrl, wait: shouldWait, pollInterval, maxWait, ...rest } = opts;
    const body: Record<string, unknown> = {
      website_key: websiteKey,
      website_url: websiteUrl,
      ...rest,
    };
    const result = await this.transport.request('POST', '/captcha/token/hcaptcha', { json: body });
    const taskId = result.task_id as string | undefined;

    if (!taskId || (result.data && !shouldWait)) return result;

    const handle = new TaskHandle(taskId, '/captcha/tasks', this.transport);
    if (shouldWait) return handle.wait({ pollInterval, maxWait });
    return handle;
  }
}
