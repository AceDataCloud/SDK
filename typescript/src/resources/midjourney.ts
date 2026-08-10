/** Midjourney resources (`/midjourney/*`). */

import { Transport } from '../runtime/transport';
import { TaskHandle } from '../runtime/tasks';

function taskId(result: Record<string, unknown>): string {
  if (typeof result.task_id === 'string') return result.task_id;
  const data = result.data as Record<string, unknown> | undefined;
  if (data && typeof data.task_id === 'string') return data.task_id;
  return typeof result.id === 'string' ? result.id : '';
}

type TaskOpts = {
  callbackUrl?: string;
  async?: boolean;
  wait?: boolean;
  pollInterval?: number;
  maxWait?: number;
  [key: string]: unknown;
};

export class Midjourney {
  constructor(private transport: Transport) {}

  private async submit(path: string, opts: TaskOpts): Promise<TaskHandle> {
    const { callbackUrl, wait, pollInterval, maxWait, ...rest } = opts;
    const body: Record<string, unknown> = { ...rest, async: opts.async ?? true };
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    const result = (await this.transport.request('POST', path, { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), '/midjourney/tasks', this.transport, result);
    if (wait) await handle.wait({ pollInterval, maxWait });
    return handle;
  }

  imagine(opts: TaskOpts = {}): Promise<TaskHandle> {
    return this.submit('/midjourney/imagine', opts);
  }

  edits(opts: TaskOpts = {}): Promise<TaskHandle> {
    return this.submit('/midjourney/edits', opts);
  }

  videos(opts: TaskOpts = {}): Promise<TaskHandle> {
    return this.submit('/midjourney/videos', opts);
  }

  seed(opts: { imageId: string; [key: string]: unknown }): Promise<Record<string, unknown>> {
    const { imageId, ...rest } = opts;
    return this.transport.request('POST', '/midjourney/seed', { json: { image_id: imageId, ...rest } });
  }

  describe(opts: { imageUrl: string; [key: string]: unknown }): Promise<Record<string, unknown>> {
    const { imageUrl, ...rest } = opts;
    return this.transport.request('POST', '/midjourney/describe', { json: { image_url: imageUrl, ...rest } });
  }

  shorten(opts: { prompt: string; [key: string]: unknown }): Promise<Record<string, unknown>> {
    return this.transport.request('POST', '/midjourney/shorten', { json: opts });
  }

  translate(opts: { content: string; [key: string]: unknown }): Promise<Record<string, unknown>> {
    return this.transport.request('POST', '/midjourney/translate', { json: opts });
  }

  tasks(opts: Record<string, unknown> = {}): Promise<Record<string, unknown>> {
    return this.transport.request('POST', '/midjourney/tasks', { json: opts });
  }
}
