/** Video generation resources. */

import { Transport } from '../runtime/transport';
import { TaskHandle } from '../runtime/tasks';

export type VideoProvider =
  | 'sora'
  | 'luma'
  | 'veo'
  | 'kling'
  | 'hailuo'
  | 'seedance'
  | 'wan'
  | 'pika'
  | 'pixverse'
  | 'gemini'
  | 'grok'
  | 'dreamina'
  | (string & {});

export class Video {
  constructor(private transport: Transport) {}

  async generate(opts: {
    prompt?: string;
    provider?: VideoProvider;
    model?: string;
    imageUrl?: string;
    imageUrls?: string[];
    referenceImageUrls?: string[];
    audioUrl?: string;
    maskUrl?: string[];
    aspectRatio?: string;
    duration?: string | number;
    resolution?: string;
    callbackUrl?: string;
    async?: boolean;
    wait?: boolean;
    pollInterval?: number;
    maxWait?: number;
    [key: string]: unknown;
  }): Promise<Record<string, unknown> | TaskHandle> {
    const {
      prompt,
      provider = 'sora',
      model,
      imageUrl,
      imageUrls,
      referenceImageUrls,
      audioUrl,
      maskUrl,
      aspectRatio,
      duration,
      resolution,
      callbackUrl,
      wait: shouldWait,
      pollInterval,
      maxWait,
      ...rest
    } = opts;
    const body: Record<string, unknown> = { ...rest };
    if (prompt !== undefined) body.prompt = prompt;
    if (model !== undefined) body.model = model;
    if (imageUrl !== undefined) body.image_url = imageUrl;
    if (imageUrls !== undefined) body.image_urls = imageUrls;
    if (referenceImageUrls !== undefined) body.reference_image_urls = referenceImageUrls;
    if (audioUrl !== undefined) body.audio_url = audioUrl;
    if (maskUrl !== undefined) body.mask_url = maskUrl;
    if (aspectRatio !== undefined) body.aspect_ratio = aspectRatio;
    if (duration !== undefined) body.duration = duration;
    if (resolution !== undefined) body.resolution = resolution;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;

    const result = await this.transport.request('POST', `/${provider}/videos`, { json: body });
    const taskId = result.task_id as string | undefined;

    if (!taskId || (result.data && !shouldWait)) return result;

    const handle = new TaskHandle(taskId, `/${provider}/tasks`, this.transport);
    if (shouldWait) return handle.wait({ pollInterval, maxWait });
    return handle;
  }
}
