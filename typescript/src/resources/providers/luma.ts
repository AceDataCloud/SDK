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
  /** Luma Videos Loop */
  loop?: boolean;
  /** Luma Videos Action */
  action?: "generate" | "extend";
  /** Luma Videos Prompt */
  prompt?: string;
  /** Luma Videos Timeout */
  timeout?: number;
  /** Luma Videos Video Id */
  videoId?: string;
  /** Luma Videos Aspect Ratio */
  aspectRatio?: string;
  /** Luma Videos Video Url */
  videoUrl?: string;
  /** Luma Videos Enhancement */
  enhancement?: boolean;
  /** Luma Videos End Image Url */
  endImageUrl?: string;
  /** Luma Videos Start Image Url */
  startImageUrl?: string;
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
    if (options.aspectRatio !== undefined) body["aspect_ratio"] = options.aspectRatio;
    if (options.videoUrl !== undefined) body["video_url"] = options.videoUrl;
    body["enhancement"] = options.enhancement ?? true;
    if (options.endImageUrl !== undefined) body["end_image_url"] = options.endImageUrl;
    if (options.startImageUrl !== undefined) body["start_image_url"] = options.startImageUrl;
    for (const [key, value] of Object.entries(options)) {
      if (!["action", "aspectRatio", "async", "callbackUrl", "endImageUrl", "enhancement", "loop", "maxWait", "pollInterval", "prompt", "startImageUrl", "timeout", "videoId", "videoUrl", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    body.async = options.async ?? true;
    const result = (await this.transport.request('POST', "/luma/videos", { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), "/luma/tasks", this.transport, result);
    if (options.wait) {
      await handle.wait({ pollInterval: options.pollInterval, maxWait: options.maxWait });
    }
    return handle;
  }

}
