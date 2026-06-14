/** Dreamina video generation resources. */

import { Transport } from '../runtime/transport';
import { TaskHandle } from '../runtime/tasks';

export class Dreamina {
  constructor(private transport: Transport) {}

  async generate(opts: {
    imageUrl: string;
    audioUrl: string;
    model?: 'omnihuman-1.5' | (string & {});
    prompt?: string;
    maskUrls?: string[];
    callbackUrl?: string;
    async?: boolean;
    wait?: boolean;
    pollInterval?: number;
    maxWait?: number;
    [key: string]: unknown;
  }): Promise<Record<string, unknown> | TaskHandle> {
    const { imageUrl, audioUrl, model, prompt, maskUrls, callbackUrl, wait: shouldWait, pollInterval, maxWait, ...rest } = opts;
    const body: Record<string, unknown> = { image_url: imageUrl, audio_url: audioUrl, ...rest };
    if (model !== undefined) body.model = model;
    if (prompt !== undefined) body.prompt = prompt;
    if (maskUrls !== undefined) body.mask_url = maskUrls;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;

    const result = await this.transport.request('POST', '/dreamina/videos', { json: body });
    const taskId = result.task_id as string | undefined;

    if (!taskId || (result.data && !shouldWait)) return result;

    const handle = new TaskHandle(taskId, '/dreamina/tasks', this.transport);
    if (shouldWait) return handle.wait({ pollInterval, maxWait });
    return handle;
  }
}
