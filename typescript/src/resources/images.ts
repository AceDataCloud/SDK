/** Image generation resources. */

import { Transport } from '../runtime/transport';
import { TaskHandle } from '../runtime/tasks';

export type ImageProvider = 'nano-banana' | 'flux' | 'seedream' | (string & {});

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
    count?: number;
    aspectRatio?: string;
    resolution?: string;
    callbackUrl?: string;
    async?: boolean;
    wait?: boolean;
    pollInterval?: number;
    maxWait?: number;
    [key: string]: unknown;
  }): Promise<Record<string, unknown> | TaskHandle> {
    const { prompt, provider = 'nano-banana', action, model, negativePrompt, imageUrl, imageUrls, count, aspectRatio, resolution, callbackUrl, wait: shouldWait, pollInterval, maxWait, ...rest } = opts;
    const body: Record<string, unknown> = { prompt, ...rest };
    const isNanoBanana = provider === 'nano-banana';
    const normalizedAction = action ?? (isNanoBanana ? 'generate' : undefined);
    const normalizedImageUrls = imageUrls ?? (isNanoBanana && imageUrl !== undefined ? [imageUrl] : undefined);

    if (normalizedAction !== undefined) body.action = normalizedAction;
    if (model !== undefined) body.model = model;
    if (negativePrompt !== undefined) body.negative_prompt = negativePrompt;
    if (imageUrl !== undefined && !isNanoBanana) body.image_url = imageUrl;
    if (normalizedImageUrls !== undefined) body.image_urls = normalizedImageUrls;
    if (count !== undefined) body.count = count;
    if (aspectRatio !== undefined) body.aspect_ratio = aspectRatio;
    if (resolution !== undefined) body.resolution = resolution;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;

    const endpoint = `/${provider}/images`;
    const result = await this.transport.request('POST', endpoint, { json: body });
    const taskId = result.task_id as string | undefined;

    if (!taskId || (result.data && !shouldWait)) return result;

    const handle = new TaskHandle(taskId, `/${provider}/tasks`, this.transport);
    if (shouldWait) return handle.wait({ pollInterval, maxWait });
    return handle;
  }
}
