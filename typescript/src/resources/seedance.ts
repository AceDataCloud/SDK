/** Seedance-specific video generation resources. */

import { Transport } from '../runtime/transport';
import { TaskHandle } from '../runtime/tasks';

export type SeedanceModel =
  | 'doubao-seedance-1-0-pro-250528'
  | 'doubao-seedance-1-0-pro-fast-251015'
  | 'doubao-seedance-1-5-pro-251215'
  | 'doubao-seedance-1-0-lite-t2v-250428'
  | 'doubao-seedance-1-0-lite-i2v-250428'
  | 'doubao-seedance-2-0-260128'
  | 'doubao-seedance-2-0-fast-260128'
  | 'doubao-seedance-2-0-mini-260615'
  | (string & {});

export type SeedanceContentItem =
  | { type: 'text'; text: string }
  | { type: 'image_url'; image_url: { url: string }; role?: 'first_frame' | 'last_frame' | 'reference_image' }
  | { type: 'audio_url'; audio_url: { url: string }; role?: 'reference_audio' }
  | { type: 'video_url'; video_url: { url: string }; role?: 'reference_video' };

export class Seedance {
  constructor(private transport: Transport) {}

  async generate(opts: {
    model: SeedanceModel;
    content: SeedanceContentItem[];
    resolution?: '480p' | '720p' | '1080p' | '4k';
    ratio?: '16:9' | '4:3' | '1:1' | '3:4' | '9:16' | '21:9' | 'adaptive';
    duration?: number;
    frames?: number;
    seed?: number;
    camerafixed?: boolean;
    watermark?: boolean;
    generateAudio?: boolean;
    callbackUrl?: string;
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
      model,
      content,
      resolution,
      ratio,
      duration,
      frames,
      seed,
      camerafixed,
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
    const body: Record<string, unknown> = { model, content, ...rest };
    if (resolution !== undefined) body.resolution = resolution;
    if (ratio !== undefined) body.ratio = ratio;
    if (duration !== undefined) body.duration = duration;
    if (frames !== undefined) body.frames = frames;
    if (seed !== undefined) body.seed = seed;
    if (camerafixed !== undefined) body.camerafixed = camerafixed;
    if (watermark !== undefined) body.watermark = watermark;
    if (generateAudio !== undefined) body.generate_audio = generateAudio;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    if (opts.async !== undefined) body.async = opts.async;
    if (returnLastFrame !== undefined) body.return_last_frame = returnLastFrame;
    if (serviceTier !== undefined) body.service_tier = serviceTier;
    if (executionExpiresAfter !== undefined) body.execution_expires_after = executionExpiresAfter;

    const result = await this.transport.request('POST', '/seedance/videos', { json: body });
    const taskId = result.task_id as string | undefined;

    if (!taskId || (result.data && !shouldWait)) return result;

    const handle = new TaskHandle(taskId, '/seedance/tasks', this.transport);
    if (shouldWait) return handle.wait({ pollInterval, maxWait });
    return handle;
  }
}
