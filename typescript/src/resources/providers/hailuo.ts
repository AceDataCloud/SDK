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
  /** Hailuo Videos Action */
  action: "generate";
  /** Hailuo Videos Model */
  model?: "minimax-i2v" | "minimax-t2v" | "minimax-i2v-director";
  /** Hailuo Videos Prompt */
  prompt?: string;
  /** Hailuo Videos First Image Url */
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

  /** Hailuo Videos */
  async generate(options: HailuoGenerateOptions): Promise<TaskHandle> {
    const body: Record<string, unknown> = {};
    body["action"] = options.action;
    if (options.model !== undefined) body["model"] = options.model;
    if (options.prompt !== undefined) body["prompt"] = options.prompt;
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
