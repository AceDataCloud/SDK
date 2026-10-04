/**
 * Wan (wan) — generated from the platform OpenAPI spec.
 *
 * Do not edit by hand: run `python scripts/generate_providers.py`. Parameter
 * names, types, enums and required-ness all come from the live spec.
 */

import { Transport } from '../../runtime/transport';
import { TaskHandle } from '../../runtime/tasks';


function taskId(result: Record<string, unknown>): string {
  if (typeof result?.task_id === 'string') return result.task_id;
  const data = result?.data as Record<string, unknown> | undefined;
  if (data && typeof data.task_id === 'string') return data.task_id;
  return typeof result?.id === 'string' ? result.id : '';
}

export interface WanGenerateOptions {
  /** $t(wan_videos_model) */
  model: "wan2.6-i2v" | "wan2.6-r2v" | "wan2.6-i2v-flash" | "wan2.6-t2v" | "wan3.0-video";
  /** $t(wan_videos_audio) */
  audio?: boolean;
  /** $t(wan_videos_prompt_extend) */
  promptExtend?: boolean;
  /** $t(wan_videos_action) */
  action?: "text2video" | "image2video";
  /** $t(wan_videos_resolution) */
  resolution?: "480P" | "720P" | "1080P";
  /** $t(wan_videos_shot_type) */
  shotType?: "single" | "multi";
  /** $t(wan_videos_duration) */
  duration?: number;
  /** $t(wan_videos_prompt) */
  prompt?: string;
  /** $t(wan_videos_negative_prompt) */
  negativePrompt?: string;
  /** $t(wan_videos_size) */
  size?: string;
  /** $t(wan_videos_audio_url) */
  audioUrl?: string;
  /** $t(wan_videos_reference_video_urls) */
  referenceVideoUrls?: string[];
  /** $t(wan_videos_image_url) */
  imageUrl?: string;
  /** $t(wan_videos_media) */
  media?: Array<Record<string, unknown>>;
  /** $t(wan_videos_ratio) */
  ratio?: "adaptive" | "16:9" | "4:3" | "1:1" | "3:4" | "9:16";
  /** $t(wan_videos_seed) */
  seed?: number;
  /** $t(wan_videos_watermark) */
  watermark?: boolean;
  /** Submit asynchronously and poll. Defaults to true. */
  async?: boolean;
  /** Wait for completion before returning the handle. */
  wait?: boolean;
  pollInterval?: number;
  maxWait?: number;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

/** wan client. */
export class Wan {
  constructor(private transport: Transport) {}

  /** Generate videos based on prompt and image frames */
  async generate(options: WanGenerateOptions): Promise<TaskHandle> {
    const body: Record<string, unknown> = {};
    body["model"] = options.model;
    body["audio"] = options.audio ?? false;
    body["prompt_extend"] = options.promptExtend ?? false;
    body["action"] = options.action ?? "text2video";
    if (options.resolution !== undefined) body["resolution"] = options.resolution;
    if (options.shotType !== undefined) body["shot_type"] = options.shotType;
    if (options.duration !== undefined) body["duration"] = options.duration;
    if (options.prompt !== undefined) body["prompt"] = options.prompt;
    if (options.negativePrompt !== undefined) body["negative_prompt"] = options.negativePrompt;
    if (options.size !== undefined) body["size"] = options.size;
    if (options.audioUrl !== undefined) body["audio_url"] = options.audioUrl;
    if (options.referenceVideoUrls !== undefined) body["reference_video_urls"] = options.referenceVideoUrls;
    if (options.imageUrl !== undefined) body["image_url"] = options.imageUrl;
    if (options.media !== undefined) body["media"] = options.media;
    if (options.ratio !== undefined) body["ratio"] = options.ratio;
    if (options.seed !== undefined) body["seed"] = options.seed;
    body["watermark"] = options.watermark ?? false;
    for (const [key, value] of Object.entries(options)) {
      if (!["action", "async", "audio", "audioUrl", "callbackUrl", "duration", "imageUrl", "maxWait", "media", "model", "negativePrompt", "pollInterval", "prompt", "promptExtend", "ratio", "referenceVideoUrls", "resolution", "seed", "shotType", "size", "wait", "watermark"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    body.async = options.async ?? true;
    const result = (await this.transport.request('POST', "/wan/videos", { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), "/wan/tasks", this.transport, result);
    if (options.wait) {
      await handle.wait({ pollInterval: options.pollInterval, maxWait: options.maxWait });
    }
    return handle;
  }

}
