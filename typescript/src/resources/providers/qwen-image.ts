/**
 * QwenImage (qwen-image) — generated from the platform OpenAPI spec.
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

export interface QwenImageGenerateOptions {
  /** Qwen Image Images Model */
  model: "qwen-image-3.0" | "qwen-image-3.0-pro";
  /** Qwen Image Images Prompt */
  prompt: string;
  /** Qwen Image Images Image Urls */
  imageUrls?: string[];
  /** Qwen Image Images N */
  n?: number;
  /** Qwen Image Images Size */
  size?: string;
  /** Qwen Image Images Prompt Extend */
  promptExtend?: boolean;
  /** Qwen Image Images Prompt Extend Mode */
  promptExtendMode?: "direct" | "agent";
  /** Qwen Image Images Enable Thinking */
  enableThinking?: boolean;
  /** Qwen Image Images Negative Prompt */
  negativePrompt?: string;
  /** Qwen Image Images Seed */
  seed?: number;
  /** Qwen Image Images Watermark */
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

/** qwen-image client. */
export class QwenImage {
  constructor(private transport: Transport) {}

  /** Qwen Image Images */
  async generate(options: QwenImageGenerateOptions): Promise<TaskHandle> {
    const body: Record<string, unknown> = {};
    body["model"] = options.model;
    body["prompt"] = options.prompt;
    if (options.imageUrls !== undefined) body["image_urls"] = options.imageUrls;
    body["n"] = options.n ?? 1;
    if (options.size !== undefined) body["size"] = options.size;
    body["prompt_extend"] = options.promptExtend ?? true;
    body["prompt_extend_mode"] = options.promptExtendMode ?? "direct";
    body["enable_thinking"] = options.enableThinking ?? true;
    if (options.negativePrompt !== undefined) body["negative_prompt"] = options.negativePrompt;
    if (options.seed !== undefined) body["seed"] = options.seed;
    body["watermark"] = options.watermark ?? false;
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "callbackUrl", "enableThinking", "imageUrls", "maxWait", "model", "n", "negativePrompt", "pollInterval", "prompt", "promptExtend", "promptExtendMode", "seed", "size", "wait", "watermark"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    body.async = options.async ?? true;
    const result = (await this.transport.request('POST', "/qwen-image/images", { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), "/qwen-image/tasks", this.transport, result);
    if (options.wait) {
      await handle.wait({ pollInterval: options.pollInterval, maxWait: options.maxWait });
    }
    return handle;
  }

}
