/**
 * Happyhorse (happyhorse) — generated from the platform OpenAPI spec.
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

export interface HappyhorseGenerateOptions {
  /** Happyhorse Videos Action */
  action?: "generate" | "image_to_video" | "reference_to_video" | "video_edit";
  /** Happyhorse Videos Model */
  model?: "happyhorse-1.0-t2v" | "happyhorse-1.1-t2v" | "happyhorse-1.0-i2v" | "happyhorse-1.1-i2v" | "happyhorse-1.0-r2v" | "happyhorse-1.1-r2v" | "happyhorse-1.0-video-edit";
  /** Happyhorse Videos Prompt */
  prompt?: string;
  /** Happyhorse Videos Image Url */
  imageUrl?: string;
  /** Happyhorse Videos Image Urls */
  imageUrls?: string[];
  /** Happyhorse Videos Video Url */
  videoUrl?: string;
  /** Happyhorse Videos Resolution */
  resolution?: "720P" | "1080P";
  /** Happyhorse Videos Ratio */
  ratio?: "16:9" | "9:16" | "1:1" | "4:3" | "3:4";
  /** Happyhorse Videos Duration */
  duration?: number;
  /** Happyhorse Videos Watermark */
  watermark?: boolean;
  /** Happyhorse Videos Audio Setting */
  audioSetting?: "auto" | "origin";
  /** Happyhorse Videos Seed */
  seed?: number;
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

/** happyhorse client. */
export class Happyhorse {
  constructor(private transport: Transport) {}

  /** Happyhorse Videos */
  async generate(options: HappyhorseGenerateOptions = {}): Promise<TaskHandle> {
    const body: Record<string, unknown> = {};
    body["action"] = options.action ?? "generate";
    body["model"] = options.model ?? "happyhorse-1.1-t2v";
    if (options.prompt !== undefined) body["prompt"] = options.prompt;
    if (options.imageUrl !== undefined) body["image_url"] = options.imageUrl;
    if (options.imageUrls !== undefined) body["image_urls"] = options.imageUrls;
    if (options.videoUrl !== undefined) body["video_url"] = options.videoUrl;
    body["resolution"] = options.resolution ?? "1080P";
    body["ratio"] = options.ratio ?? "16:9";
    body["duration"] = options.duration ?? 5;
    body["watermark"] = options.watermark ?? false;
    body["audio_setting"] = options.audioSetting ?? "auto";
    if (options.seed !== undefined) body["seed"] = options.seed;
    for (const [key, value] of Object.entries(options)) {
      if (!["action", "async", "audioSetting", "callbackUrl", "duration", "imageUrl", "imageUrls", "maxWait", "model", "pollInterval", "prompt", "ratio", "resolution", "seed", "videoUrl", "wait", "watermark"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    body.async = options.async ?? true;
    const result = (await this.transport.request('POST', "/happyhorse/videos", { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), "/happyhorse/tasks", this.transport, result);
    if (options.wait) {
      await handle.wait({ pollInterval: options.pollInterval, maxWait: options.maxWait });
    }
    return handle;
  }

}
