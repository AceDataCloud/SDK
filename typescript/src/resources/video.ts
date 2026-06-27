/** Video generation resources. */

import { Transport } from '../runtime/transport';
import { TaskHandle } from '../runtime/tasks';

export type VideoProvider = 'sora' | 'luma' | 'veo' | 'kling' | 'hailuo' | 'seedance' | 'wan' | 'pika' | 'pixverse' | 'midjourney' | (string & {});
export type SeedanceContentItem =
  | { type: 'text'; text: string }
  | { type: 'image_url'; image_url: { url: string }; role?: 'first_frame' | 'last_frame' | 'reference_image' }
  | { type: 'audio_url'; audio_url: { url: string }; role?: 'reference_audio' }
  | { type: 'video_url'; video_url: { url: string }; role?: 'reference_video' };

export class Video {
  constructor(private transport: Transport) {}

  async generate(opts: {
    prompt?: string;
    content?: SeedanceContentItem[];
    provider?: VideoProvider;
    model?: string;
    imageUrl?: string;
    callbackUrl?: string;
    resolution?: '480p' | '720p' | '1080p' | '4k';
    ratio?: '16:9' | '4:3' | '1:1' | '3:4' | '9:16' | '21:9' | 'adaptive';
    duration?: number;
    frames?: number;
    seed?: number;
    cameraFixed?: boolean;
    watermark?: boolean;
    generateAudio?: boolean;
    async?: boolean;
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
      content,
      provider = 'sora',
      model,
      imageUrl,
      callbackUrl,
      resolution,
      ratio,
      duration,
      frames,
      seed,
      cameraFixed,
      watermark,
      generateAudio,
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
    if (content !== undefined) body.content = content;
    if (model !== undefined) body.model = model;
    if (imageUrl !== undefined) body.image_url = imageUrl;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    if (resolution !== undefined) body.resolution = resolution;
    if (ratio !== undefined) body.ratio = ratio;
    if (duration !== undefined) body.duration = duration;
    if (frames !== undefined) body.frames = frames;
    if (seed !== undefined) body.seed = seed;
    if (cameraFixed !== undefined) body.camerafixed = cameraFixed;
    if (watermark !== undefined) body.watermark = watermark;
    if (generateAudio !== undefined) body.generate_audio = generateAudio;
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
