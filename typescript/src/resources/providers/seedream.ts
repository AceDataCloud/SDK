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
  /** Models used for generating images. If not specified, the default is `doubao-seedream-5.0-lite`. `doubao-seedream-5.0-pro` is the latest flagship single image model (only generates single images, does not support group images, streaming, or online search). */
  model: "doubao-seedream-5-0-pro-260628" | "doubao-seedream-5-0-260128" | "doubao-seedream-4-0-250828" | "doubao-seedream-4-5-251128" | "doubao-seedream-3-0-t2i-250415" | "doubao-seededit-3-0-i2i-250628";
  /** Prompts for generating images. */
  prompt: string;
  /** Generate a random seed for image generation. The supported range is [-1, 2147483647], with a default value of `-1`. **Only `doubao-seedream-3.0-t2i` supports this parameter** (according to the official Volcengine documentation), other models do not accept this parameter. */
  seed?: number;
  /** Generate image dimensions or aspect ratios. Supports preset options (`1K`/`2K`/`3K`/`4K`), `adaptive` (adaptive reference image size), or explicit `<width>x<height>` format (e.g., `1024x1024`). **Different models support different preset options**: `doubao-seedream-5.0-pro` supports `1K`/`2K`; `doubao-seedream-5.0-lite` supports `2K`/`3K`/`4K`; `doubao-seedream-4.5` only supports `2K`/`4K`; `doubao-seedream-4.0` supports `1K`/`2K`/`4K`; `doubao-seedream-3.0-t2i` and `doubao-seedream-3.0-i2i` **do not support** any preset options and must receive explicit `<width>x<height>` values. */
  size?: "1K" | "2K" | "3K" | "4K" | "adaptive";
  /** Reference image links for image editing are required, supporting accessible http/https URLs, or base64 encoded image strings in the format `data:image/png;base64,iVBORw0KG...`. Each image must not exceed 10MB in size. This parameter is mandatory when using image-to-image models (such as `doubao-seededit-3.0-i2i`). */
  image?: string[];
  /** List of tools that can be called by the model. Currently, only `web_search` is supported. Applicable only to `doubao-seedream-5.0-lite`. */
  tools?: unknown[];
  /** Whether to return all images in a streaming manner, default is `false`. Only supports `doubao-seedream-5.0-lite`, `doubao-seedream-4.5`, and `doubao-seedream-4.0`. */
  stream?: boolean;
  /** Whether to add AI-generated watermark, default is `true`. */
  watermark?: boolean;
  /** The output image file format is `jpeg` by default. Only `doubao-seedream-5.0-pro` and `doubao-seedream-5.0-lite` are supported. */
  outputFormat?: "jpeg" | "png";
  /** Prompt word weight, the larger the value, the more relevant the generated result is to the prompt word. Only supports `doubao-seedream-3.0-t2i` (default value 2.5) and `doubao-seededit-3.0-i2i` (default value 5.5), both ranges are [1, 10]. */
  guidanceScale?: unknown;
  /** The response format defaults to `url`, and also supports `b64_json`. */
  responseFormat?: string;
  /** Optional prompt word optimization configuration. Only supports `doubao-seedream-5.0-lite`, `doubao-seedream-4.5` (only in `standard` mode), and `doubao-seedream-4.0`. */
  optimizePromptOptions?: Record<string, unknown>;
  /** The default value is `disabled`. Setting it to `auto` allows the model to generate a set of stylistically coherent related images (multi-image consistency, sharing characters, styles, and details across frames). Only `doubao-seedream-5.0-lite`, `doubao-seedream-4.5`, and `doubao-seedream-4.0` are supported. */
  sequentialImageGeneration?: "auto" | "disabled";
  /** Adjustable parameters for batch image generation. Effective only when `sequential_image_generation=auto`. Only supports `doubao-seedream-5.0-lite`, `doubao-seedream-4.5`, and `doubao-seedream-4.0`. */
  sequentialImageGenerationOptions?: Record<string, unknown>;
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

  /** ByteDance Seedream high-quality image generation and editing API. Supports text-to-image models doubao-seedream-3-0-t2i-250415, doubao-seedream-4-0-250828, doubao-seedream-4-5-251128, doubao-seedream- */
  async generate(options: SeedreamGenerateOptions): Promise<TaskHandle> {
    const body: Record<string, unknown> = {};
    body["model"] = options.model;
    body["prompt"] = options.prompt;
    if (options.seed !== undefined) body["seed"] = options.seed;
    body["size"] = options.size ?? "2K";
    if (options.image !== undefined) body["image"] = options.image;
    if (options.tools !== undefined) body["tools"] = options.tools;
    if (options.stream !== undefined) body["stream"] = options.stream;
    if (options.watermark !== undefined) body["watermark"] = options.watermark;
    if (options.outputFormat !== undefined) body["output_format"] = options.outputFormat;
    if (options.guidanceScale !== undefined) body["guidance_scale"] = options.guidanceScale;
    if (options.responseFormat !== undefined) body["response_format"] = options.responseFormat;
    if (options.optimizePromptOptions !== undefined) body["optimize_prompt_options"] = options.optimizePromptOptions;
    if (options.sequentialImageGeneration !== undefined) body["sequential_image_generation"] = options.sequentialImageGeneration;
    if (options.sequentialImageGenerationOptions !== undefined) body["sequential_image_generation_options"] = options.sequentialImageGenerationOptions;
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "callbackUrl", "guidanceScale", "image", "maxWait", "model", "optimizePromptOptions", "outputFormat", "pollInterval", "prompt", "responseFormat", "seed", "sequentialImageGeneration", "sequentialImageGenerationOptions", "size", "stream", "tools", "wait", "watermark"].includes(key) && value !== undefined) {
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
