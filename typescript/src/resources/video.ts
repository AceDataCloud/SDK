/** Video generation resources. */

import { Transport } from '../runtime/transport';
import { TaskHandle } from '../runtime/tasks';

export type VideoProvider = 'sora' | 'luma' | 'veo' | 'kling' | 'hailuo' | 'seedance' | 'wan' | 'pika' | 'pixverse' | 'midjourney' | (string & {});

export class Video {
  constructor(private transport: Transport) {}

  async generate(opts: {
    prompt?: string;
    provider?: VideoProvider;
    model?: string;
    content?: Array<Record<string, unknown>>;
    imageUrl?: string;
    resolution?: '480p' | '720p' | '1080p';
    ratio?: '16:9' | '4:3' | '1:1' | '3:4' | '9:16' | '21:9' | 'adaptive';
    duration?: number;
    frames?: number;
    seed?: number;
    cameraFixed?: boolean;
    watermark?: boolean;
    generateAudio?: boolean;
    callbackUrl?: string;
    returnLastFrame?: boolean;
    serviceTier?: 'default' | 'flex';
    executionExpiresAfter?: number;
    wait?: boolean;
    pollInterval?: number;
    maxWait?: number;
    [key: string]: unknown;
  }): Promise<Record<string, unknown> | TaskHandle> {
    const {
      prompt,
      provider = 'sora',
      model,
      content,
      imageUrl,
      resolution,
      ratio,
      duration,
      frames,
      seed,
      cameraFixed,
      watermark,
      generateAudio,
      callbackUrl,
      returnLastFrame,
      serviceTier,
      executionExpiresAfter,
      wait: shouldWait,
      pollInterval,
      maxWait,
      ...rest
    } = opts;
    const body: Record<string, unknown> = { ...rest };
    if (prompt !== undefined) body.prompt = prompt;
    if (model !== undefined) body.model = model;
    if (content !== undefined) body.content = content;
    if (imageUrl !== undefined) body.image_url = imageUrl;
    if (resolution !== undefined) body.resolution = resolution;
    if (ratio !== undefined) body.ratio = ratio;
    if (duration !== undefined) body.duration = duration;
    if (frames !== undefined) body.frames = frames;
    if (seed !== undefined) body.seed = seed;
    if (cameraFixed !== undefined) body.camerafixed = cameraFixed;
    if (watermark !== undefined) body.watermark = watermark;
    if (generateAudio !== undefined) body.generate_audio = generateAudio;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    if (returnLastFrame !== undefined) body.return_last_frame = returnLastFrame;
    if (serviceTier !== undefined) body.service_tier = serviceTier;
    if (executionExpiresAfter !== undefined) body.execution_expires_after = executionExpiresAfter;

    const result = await this.transport.request('POST', `/${provider}/videos`, { json: body });
    const taskId = result.task_id as string | undefined;

    if (!taskId || (result.data && !shouldWait)) return result;

    const handle = new TaskHandle(taskId, `/${provider}/tasks`, this.transport);
    if (shouldWait) return handle.wait({ pollInterval, maxWait });
    return handle;
  }
}
