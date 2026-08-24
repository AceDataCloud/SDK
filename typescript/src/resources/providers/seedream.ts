/**
 * Seedream (seedream) — generated from the platform OpenAPI spec.
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

export interface SeedreamGenerateOptions {
  /** Seedream Images Model */
  model: "doubao-seedream-5-0-pro-260628" | "doubao-seedream-5-0-260128" | "doubao-seedream-4-0-250828" | "doubao-seedream-4-5-251128";
  /** Seedream Images Prompt */
  prompt: string;
  /** Seedream Images Image */
  image?: string[];
  /** Seedream Images Size */
  size?: "1K" | "2K" | "3K" | "4K";
  /** Seedream Images Sequential Image Generation */
  sequentialImageGeneration?: "auto" | "disabled";
  /** Seedream Images Sequential Image Generation Options */
  sequentialImageGenerationOptions?: Record<string, unknown>;
  /** Seedream Images Stream */
  stream?: boolean;
  /** Seedream Images Response Format */
  responseFormat?: string;
  /** Seedream Images Watermark */
  watermark?: boolean;
  /** Seedream Images Output Format */
  outputFormat?: "jpeg" | "png";
  /** Seedream Images Tools */
  tools?: Array<Record<string, unknown>>;
  /** Seedream Images Optimize Prompt Options */
  optimizePromptOptions?: Record<string, unknown>;
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

/** seedream client. */
export class Seedream {
  constructor(private transport: Transport) {}

  /** Seedream Images */
  async generate(options: SeedreamGenerateOptions): Promise<TaskHandle> {
    const body: Record<string, unknown> = {};
    body["model"] = options.model;
    body["prompt"] = options.prompt;
    if (options.image !== undefined) body["image"] = options.image;
    if (options.size !== undefined) body["size"] = options.size;
    if (options.sequentialImageGeneration !== undefined) body["sequential_image_generation"] = options.sequentialImageGeneration;
    if (options.sequentialImageGenerationOptions !== undefined) body["sequential_image_generation_options"] = options.sequentialImageGenerationOptions;
    if (options.stream !== undefined) body["stream"] = options.stream;
    if (options.responseFormat !== undefined) body["response_format"] = options.responseFormat;
    if (options.watermark !== undefined) body["watermark"] = options.watermark;
    if (options.outputFormat !== undefined) body["output_format"] = options.outputFormat;
    if (options.tools !== undefined) body["tools"] = options.tools;
    if (options.optimizePromptOptions !== undefined) body["optimize_prompt_options"] = options.optimizePromptOptions;
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "callbackUrl", "image", "maxWait", "model", "optimizePromptOptions", "outputFormat", "pollInterval", "prompt", "responseFormat", "sequentialImageGeneration", "sequentialImageGenerationOptions", "size", "stream", "tools", "wait", "watermark"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    body.async = options.async ?? true;
    const result = (await this.transport.request('POST', "/seedream/images", { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), "/seedream/tasks", this.transport, result);
    if (options.wait) {
      await handle.wait({ pollInterval: options.pollInterval, maxWait: options.maxWait });
    }
    return handle;
  }

}
