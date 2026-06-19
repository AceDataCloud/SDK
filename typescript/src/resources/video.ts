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
  | 'midjourney'
  | 'dreamina'
  | 'grok'
  | (string & {});

export class Video {
  constructor(private transport: Transport) {}

  async generate(opts: {
    prompt: string;
    provider?: VideoProvider;
    model?: string;
    imageUrl?: string;
    audioUrl?: string;
    maskUrl?: string[];
    referenceImageUrls?: string[];
    aspectRatio?: string;
    resolution?: string;
    callbackUrl?: string;
    duration?: number;
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
      audioUrl,
      maskUrl,
      referenceImageUrls,
      aspectRatio,
      resolution,
      callbackUrl,
      duration,
      wait: shouldWait,
      pollInterval,
      maxWait,
      ...rest
    } = opts;
    const body: Record<string, unknown> = { prompt, ...rest };
    if (model !== undefined) body.model = model;
    if (imageUrl !== undefined) body.image_url = imageUrl;
    if (audioUrl !== undefined) body.audio_url = audioUrl;
    if (maskUrl !== undefined) body.mask_url = maskUrl;
    if (referenceImageUrls !== undefined) body.reference_image_urls = referenceImageUrls;
    if (aspectRatio !== undefined) body.aspect_ratio = aspectRatio;
    if (resolution !== undefined) body.resolution = resolution;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    if (duration !== undefined) body.duration = duration;

    const result = await this.transport.request('POST', `/${provider}/videos`, { json: body });
    const taskId = result.task_id as string | undefined;

    if (!taskId || (result.data && !shouldWait)) return result;

    const handle = new TaskHandle(taskId, `/${provider}/tasks`, this.transport);
    if (shouldWait) return handle.wait({ pollInterval, maxWait });
    return handle;
  }
}
