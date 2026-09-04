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
  /** Full model ID. Seedream 5.0 Pro supports single-image generation, precise editing, transparent backgrounds, and layer decomposition; Seedream 5.0 Lite supports single or sequential images, streaming, and web search. */
  model: "doubao-seedream-5-0-pro-260628" | "doubao-seedream-5-0-260128" | "doubao-seedream-5-0-lite-260128" | "doubao-seedream-4-0-250828" | "doubao-seedream-4-5-251128";
  /** Generation or editing prompt. Optional only for Seedream 5.0 Pro layer decomposition, where omission automatically decomposes the main elements. */
  prompt?: string;
  /** One reference image URL/base64 string or an array. Pro accepts up to 10 images in regular mode and exactly one for decomposition; Lite/4.x accept up to 14. Each image must be at most 30 MB. */
  image?: string | string[];
  /** Output size. Pro supports 1K/1.5K/2K or valid dimensions; decomposition also supports auto. Lite supports 2K/3K/4K or valid dimensions. */
  size?: "1K" | "1.5K" | "2K" | "3K" | "4K" | "auto" | `${number}x${number}`;
  /** Sequential image mode. auto lets supported Lite/4.x models generate a related set; disabled returns one image. Not supported by Pro. */
  sequentialImageGeneration?: "auto" | "disabled";
  /** Sequential image options. max_images is 1-15 and input images plus outputs must not exceed 15. */
  sequentialImageGenerationOptions?: Record<string, unknown>;
  /** Stream normalized image events. Supported by Lite/4.x only and cannot be combined with async or callback_url. */
  stream?: boolean;
  /** Image response format: url or b64_json. */
  responseFormat?: "url" | "b64_json";
  /** Whether to add the AI-generated watermark. */
  watermark?: boolean;
  /** Output image format, jpeg or png. Supported by Seedream 5.0 Pro and Lite. */
  outputFormat?: "jpeg" | "png";
  /** Model tools. Seedream 5.0 Lite supports web_search. */
  tools?: Array<Record<string, unknown>>;
  /** Prompt optimization. Pro supports standard/fast; Lite and 4.5 support standard; 4.0 supports standard/fast. */
  optimizePromptOptions?: Record<string, unknown>;
  /** Seedream 5.0 Pro layer decomposition. Requires exactly one PNG/JPEG and returns one base image plus up to 16 transparent PNG layers. */
  layerDecomposition?: boolean;
  /** Seedream 5.0 Pro background mode. transparent requires one transparent PNG input and PNG output; opaque produces a regular background. */
  background?: "transparent" | "opaque";
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

  /** Call /seedream/images. */
  async generate(options: SeedreamGenerateOptions): Promise<TaskHandle> {
    const body: Record<string, unknown> = {};
    body["model"] = options.model;
    if (options.prompt !== undefined) body["prompt"] = options.prompt;
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
    if (options.layerDecomposition !== undefined) body["layer_decomposition"] = options.layerDecomposition;
    if (options.background !== undefined) body["background"] = options.background;
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "background", "callbackUrl", "image", "layerDecomposition", "maxWait", "model", "optimizePromptOptions", "outputFormat", "pollInterval", "prompt", "responseFormat", "sequentialImageGeneration", "sequentialImageGenerationOptions", "size", "stream", "tools", "wait", "watermark"].includes(key) && value !== undefined) {
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
