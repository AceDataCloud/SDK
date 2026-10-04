/**
 * NanoBanana (nano-banana) — generated from the platform OpenAPI spec.
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

export interface NanoBananaGenerateOptions {
  /** Nano Banana Images Action */
  action: "generate" | "edit";
  /** Nano Banana Images Prompt */
  prompt: string;
  /** Nano Banana Images Model */
  model?: "nano-banana" | "nano-banana-2-lite" | "nano-banana-2" | "nano-banana-pro" | "nano-banana:official" | "nano-banana-2-lite:official" | "nano-banana-2:official" | "nano-banana-pro:official";
  /** Nano Banana Images Image Urls */
  imageUrls?: string[];
  /** Nano Banana Images Count */
  count?: number;
  /** Nano Banana Images Aspect Ratio */
  aspectRatio?: "1:1" | "3:2" | "2:3" | "16:9" | "9:16" | "4:3" | "3:4";
  /** Nano Banana Images Resolution */
  resolution?: "1K" | "2K" | "4K";
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

/** nano-banana client. */
export class NanoBanana {
  constructor(private transport: Transport) {}

  /** Nano Banana Images */
  async generate(options: NanoBananaGenerateOptions): Promise<TaskHandle> {
    const body: Record<string, unknown> = {};
    body["action"] = options.action;
    body["prompt"] = options.prompt;
    if (options.model !== undefined) body["model"] = options.model;
    if (options.imageUrls !== undefined) body["image_urls"] = options.imageUrls;
    body["count"] = options.count ?? 1;
    if (options.aspectRatio !== undefined) body["aspect_ratio"] = options.aspectRatio;
    if (options.resolution !== undefined) body["resolution"] = options.resolution;
    for (const [key, value] of Object.entries(options)) {
      if (!["action", "aspectRatio", "async", "callbackUrl", "count", "imageUrls", "maxWait", "model", "pollInterval", "prompt", "resolution", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    body.async = options.async ?? true;
    const result = (await this.transport.request('POST', "/nano-banana/images", { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), "/nano-banana/tasks", this.transport, result);
    if (options.wait) {
      await handle.wait({ pollInterval: options.pollInterval, maxWait: options.maxWait });
    }
    return handle;
  }

}
