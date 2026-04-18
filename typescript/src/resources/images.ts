/** Image generation resources. */

import { Transport } from '../runtime/transport';
import { TaskHandle } from '../runtime/tasks';

export type ImageProvider = 'nano-banana' | 'midjourney' | 'flux' | 'seedream' | (string & {});

export class Images {
  constructor(private transport: Transport) {}

  async generate(opts: {
    prompt: string;
    provider?: ImageProvider;
    model?: string;
    negativePrompt?: string;
    imageUrl?: string;
    callbackUrl?: string;
    wait?: boolean;
    pollInterval?: number;
    maxWait?: number;
    [key: string]: unknown;
  }): Promise<Record<string, unknown> | TaskHandle> {
    const { prompt, provider = 'nano-banana', model, negativePrompt, imageUrl, callbackUrl, wait: shouldWait, pollInterval, maxWait, ...rest } = opts;
    const body: Record<string, unknown> = { prompt, ...rest };
    if (model !== undefined) body.model = model;
    if (negativePrompt !== undefined) body.negative_prompt = negativePrompt;
    if (imageUrl !== undefined) body.image_url = imageUrl;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;

    const endpoint = provider === 'midjourney' ? '/midjourney/imagine' : `/${provider}/images`;
    const result = await this.transport.request('POST', endpoint, { json: body });
    const taskId = result.task_id as string | undefined;

    if (!taskId || (result.data && !shouldWait)) return result;

    const handle = new TaskHandle(taskId, `/${provider}/tasks`, this.transport);
    if (shouldWait) return handle.wait({ pollInterval, maxWait });
    return handle;
  }
}
