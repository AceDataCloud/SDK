/** QRArt resources (`/qrart/*`). */

import { Transport } from '../runtime/transport';
import { TaskHandle } from '../runtime/tasks';

function taskId(result: Record<string, unknown>): string {
  if (typeof result.task_id === 'string') return result.task_id;
  const data = result.data as Record<string, unknown> | undefined;
  if (data && typeof data.task_id === 'string') return data.task_id;
  return typeof result.id === 'string' ? result.id : '';
}

export class Qrart {
  constructor(private transport: Transport) {}

  async generate(opts: {
    type: 'link' | 'text' | 'email' | 'phone' | 'sms';
    prompt: string;
    callbackUrl?: string;
    async?: boolean;
    wait?: boolean;
    pollInterval?: number;
    maxWait?: number;
    [key: string]: unknown;
  }): Promise<TaskHandle> {
    const { callbackUrl, wait, pollInterval, maxWait, ...rest } = opts;
    const body: Record<string, unknown> = { ...rest, async: opts.async ?? true };
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    const result = (await this.transport.request('POST', '/qrart/generate', { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), '/qrart/tasks', this.transport, result);
    if (wait) await handle.wait({ pollInterval, maxWait });
    return handle;
  }

  tasks(opts: Record<string, unknown> = {}): Promise<Record<string, unknown>> {
    return this.transport.request('POST', '/qrart/tasks', { json: opts });
  }
}
