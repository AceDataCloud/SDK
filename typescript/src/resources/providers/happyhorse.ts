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
  /** Random seed, range 0–2147483647. */
  seed?: number;
  /** HappyHorse model name. Different actions only support the corresponding model family. */
  model?: "happyhorse-1.0-t2v" | "happyhorse-1.1-t2v" | "happyhorse-1.0-i2v" | "happyhorse-1.1-i2v" | "happyhorse-1.0-r2v" | "happyhorse-1.1-r2v" | "happyhorse-1.0-video-edit";
  /** Output video aspect ratio. Text-to-video and reference image-to-video support this parameter; the first frame image-to-video will follow the aspect ratio of the first frame image. */
  ratio?: "16:9" | "9:16" | "1:1" | "4:3" | "3:4";
  /** Operation types. `generate` is for generating video from text, `image_to_video` is for generating video from the first frame image, `reference_to_video` is for generating video from reference images, and `video_edit` is for video editing based on video and reference images. */
  action?: "generate" | "image_to_video" | "reference_to_video" | "video_edit";
  /** Text prompt words. Text-to-video, reference image to video, and video editing scenarios are required. */
  prompt?: string;
  /** Output video duration (seconds), value range 3–15. The output duration of `video_edit` is determined by the input video. */
  duration?: number;
  /** The input image URL for the first frame of the video. Only used by `image_to_video`. */
  imageUrl?: string;
  /** URL of the video to be edited. For `video_edit` use only. */
  videoUrl?: string;
  /** Whether to add the HappyHorse watermark. Default is off. */
  watermark?: boolean;
  /** Reference image URL array. `reference_to_video` supports 1–9 images, `video_edit` supports 0–5 images. */
  imageUrls?: string[];
  /** Output video resolution, optional 720P or 1080P. */
  resolution?: "720P" | "1080P";
  /** Audio strategy for video editing. `auto` is determined by the model, `origin` retains the original audio of the input video. */
  audioSetting?: "auto" | "origin";
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

  /** Call /happyhorse/videos. */
  async generate(options: HappyhorseGenerateOptions = {}): Promise<TaskHandle> {
    const body: Record<string, unknown> = {};
    if (options.seed !== undefined) body["seed"] = options.seed;
    body["model"] = options.model ?? "happyhorse-1.1-t2v";
    body["ratio"] = options.ratio ?? "16:9";
    body["action"] = options.action ?? "generate";
    body["prompt"] = options.prompt ?? "A cinematic white horse lifts its head, the mane moves gently in the sunrise wind, slow camera push in, warm film lighting";
    body["duration"] = options.duration ?? 5;
    body["image_url"] = options.imageUrl ?? "https://cdn.acedata.cloud/b1c82e4937.png";
    body["video_url"] = options.videoUrl ?? "https://platform2.cdn.acedata.cloud/happyhorse/27837f92-d1c1-4db4-ad9a-4e6e81d9f6c1.mp4";
    body["watermark"] = options.watermark ?? false;
    if (options.imageUrls !== undefined) body["image_urls"] = options.imageUrls;
    body["resolution"] = options.resolution ?? "1080P";
    body["audio_setting"] = options.audioSetting ?? "auto";
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
