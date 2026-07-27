/**
 * Hailuo (hailuo) — generated from the platform OpenAPI spec.
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

export interface HailuoGenerateOptions {
  /** The operation type for video generation. When set to `generate`, it will generate a video based on the prompt. */
  action: "generate";
  /** The model used for generating videos has a default value of `minimax-t2v`. */
  model?: "minimax-i2v" | "minimax-t2v" | "minimax-i2v-director";
  /** Prompts for generating videos. */
  prompt?: string;
  /** You can specify the URL of the first frame image to generate a video from the image. */
  firstImageUrl?: string;
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

/** hailuo client. */
export class Hailuo {
  constructor(private transport: Transport) {}

  /** Minimax Hailuo AI video generation API. Supports minimax-t2v for text-to-video, minimax-i2v for image-to-video, and minimax-i2v-director for director mode with camera/movement instructions. */
  async generate(options: HailuoGenerateOptions): Promise<TaskHandle> {
    const body: Record<string, unknown> = {};
    body["action"] = options.action;
    if (options.model !== undefined) body["model"] = options.model;
    body["prompt"] = options.prompt ?? "\u706b\u6c14";
    if (options.firstImageUrl !== undefined) body["first_image_url"] = options.firstImageUrl;
    for (const [key, value] of Object.entries(options)) {
      if (!["action", "async", "callbackUrl", "firstImageUrl", "maxWait", "model", "pollInterval", "prompt", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    body.async = options.async ?? true;
    const result = (await this.transport.request('POST', "/hailuo/videos", { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), "/hailuo/tasks", this.transport, result);
    if (options.wait) {
      await handle.wait({ pollInterval: options.pollInterval, maxWait: options.maxWait });
    }
    return handle;
  }

}
