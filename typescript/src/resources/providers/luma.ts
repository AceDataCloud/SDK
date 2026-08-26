/**
 * Luma (luma) — generated from the platform OpenAPI spec.
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

export interface LumaGenerateOptions {
  /** Whether to enable loop playback for the generated video. */
  loop?: boolean;
  /** Operation type. Use `generate` when creating a video for the first time, and use `extend` when continuing an existing video. */
  action?: "generate" | "extend";
  /** Text prompts for generating videos. */
  prompt?: string;
  /** The timeout for the API return data (unit: seconds). */
  timeout?: number;
  /** The unique identifier of the generated video used for the continuation operation (`extend`). If both are specified, `video_id` takes precedence over `video_url`. */
  videoId?: string;
  /** The original video URL used for the extend operation (`extend`). If `video_id` is specified at the same time, then `video_id` shall prevail. */
  videoUrl?: string;
  /** Whether to enable automatic optimization enhancement for the input prompt text, suitable for use when unsure how to write prompt words. */
  enhancement?: boolean;
  /** Generate the aspect ratio of the video, for example `16:9`. */
  aspectRatio?: string;
  /** The URL of the ending frame image, which will be used as the last frame of the generated video. */
  endImageUrl?: string;
  /** The URL of the starting frame image, which will be used as the first frame of the generated video. */
  startImageUrl?: string;
  /** Submit asynchronously and poll. */
  async?: boolean;
  /** Wait for completion before returning the handle. */
  wait?: boolean;
  pollInterval?: number;
  maxWait?: number;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

/** luma client. */
export class Luma {
  constructor(private transport: Transport) {}

  /** Generate videos based on prompt and image frames */
  async generate(options: LumaGenerateOptions = {}): Promise<TaskHandle> {
    const body: Record<string, unknown> = {};
    body["loop"] = options.loop ?? false;
    body["action"] = options.action ?? "generate";
    if (options.prompt !== undefined) body["prompt"] = options.prompt;
    body["timeout"] = options.timeout ?? 300;
    if (options.videoId !== undefined) body["video_id"] = options.videoId;
    if (options.videoUrl !== undefined) body["video_url"] = options.videoUrl;
    body["enhancement"] = options.enhancement ?? true;
    if (options.aspectRatio !== undefined) body["aspect_ratio"] = options.aspectRatio;
    if (options.endImageUrl !== undefined) body["end_image_url"] = options.endImageUrl;
    if (options.startImageUrl !== undefined) body["start_image_url"] = options.startImageUrl;
    for (const [key, value] of Object.entries(options)) {
      if (!["action", "aspectRatio", "async", "callbackUrl", "endImageUrl", "enhancement", "loop", "maxWait", "pollInterval", "prompt", "startImageUrl", "timeout", "videoId", "videoUrl", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    if (options.async !== undefined) body.async = options.async;
    const result = (await this.transport.request('POST', "/luma/videos", { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), "/luma/tasks", this.transport, result);
    if (options.wait) {
      await handle.wait({ pollInterval: options.pollInterval, maxWait: options.maxWait });
    }
    return handle;
  }

}
