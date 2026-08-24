/**
 * Flux (flux) — generated from the platform OpenAPI spec.
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

export interface FluxGenerateOptions {
  /** Flux Images Size */
  size: string;
  /** Flux Images Action */
  action: "generate" | "edit";
  /** Flux Images Prompt */
  prompt: string;
  /** Flux Images Count */
  count?: number;
  /** Flux Images Model */
  model?: "flux-dev" | "flux-pro" | "flux-kontext-pro" | "flux-kontext-max" | "flux-2-flex" | "flux-2-pro" | "flux-2-max" | "flux-2-klein";
  /** Flux Images Image Url */
  imageUrl?: string;
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

/** flux client. */
export class Flux {
  constructor(private transport: Transport) {}

  /** Flux Images */
  async generate(options: FluxGenerateOptions): Promise<TaskHandle> {
    const body: Record<string, unknown> = {};
    body["size"] = options.size;
    body["action"] = options.action;
    body["prompt"] = options.prompt;
    if (options.count !== undefined) body["count"] = options.count;
    if (options.model !== undefined) body["model"] = options.model;
    if (options.imageUrl !== undefined) body["image_url"] = options.imageUrl;
    for (const [key, value] of Object.entries(options)) {
      if (!["action", "async", "callbackUrl", "count", "imageUrl", "maxWait", "model", "pollInterval", "prompt", "size", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    body.async = options.async ?? true;
    const result = (await this.transport.request('POST', "/flux/images", { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), "/flux/tasks", this.transport, result);
    if (options.wait) {
      await handle.wait({ pollInterval: options.pollInterval, maxWait: options.maxWait });
    }
    return handle;
  }

}
