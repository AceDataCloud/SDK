/** Image generation resources. */

import { Transport } from '../runtime/transport';
import { TaskHandle } from '../runtime/tasks';

export type ImageProvider = 'nano-banana' | 'midjourney' | 'flux' | 'seedream' | 'headshots' | 'qrart' | (string & {});

const IMAGE_ENDPOINTS: Record<string, string> = {
  midjourney: '/midjourney/imagine',
  headshots: '/headshots/generate',
  qrart: '/qrart/generate',
};

export class Images {
  constructor(private transport: Transport) {}

  async generate(opts: {
    prompt: string;
    provider?: ImageProvider;
    action?: 'generate' | 'edit';
    model?: string;
    negativePrompt?: string;
    imageUrl?: string;
    imageUrls?: string[];
    aspectRatio?: string;
    resolution?: string;
    callbackUrl?: string;
    wait?: boolean;
    pollInterval?: number;
    maxWait?: number;
    [key: string]: unknown;
  }): Promise<Record<string, unknown> | TaskHandle> {
    const { prompt, provider = 'nano-banana', action, model, negativePrompt, imageUrl, imageUrls, aspectRatio, resolution, callbackUrl, wait: shouldWait, pollInterval, maxWait, ...rest } = opts;
    const body: Record<string, unknown> = { prompt, ...rest };
    if (action !== undefined) body.action = action;
    if (model !== undefined) body.model = model;
    if (negativePrompt !== undefined) body.negative_prompt = negativePrompt;
    if (imageUrl !== undefined) body.image_url = imageUrl;
    if (imageUrls !== undefined) body.image_urls = imageUrls;
    if (aspectRatio !== undefined) body.aspect_ratio = aspectRatio;
    if (resolution !== undefined) body.resolution = resolution;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;

    const endpoint = IMAGE_ENDPOINTS[provider] ?? `/${provider}/images`;
    const result = await this.transport.request('POST', endpoint, { json: body });
    const taskId = result.task_id as string | undefined;

    if (!taskId || (result.data && !shouldWait)) return result;

    const handle = new TaskHandle(taskId, `/${provider}/tasks`, this.transport);
    if (shouldWait) return handle.wait({ pollInterval, maxWait });
    return handle;
  }
}
