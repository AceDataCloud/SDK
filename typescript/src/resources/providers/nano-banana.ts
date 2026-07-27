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
  /** Image operation type. If it is `generate`, then generate an image based on the prompt; if it is `edit`, then edit the image based on the prompt and `image_urls`. */
  action: "generate" | "edit";
  /** Prompts for generating images. */
  prompt: string;
  /** The number of images to be generated or edited supports 1 to 4, with a default of 1. If some images fail to generate, the corresponding `data` only contains the successfully generated images and charges based on the number of successful ones. */
  count?: number;
  /** Models used for generating images. If not specified, the default is `nano-banana`. `nano-banana-2-lite` is an alias for `gemini-3.1-flash-lite-image` (only 1K, fast generation speed), `nano-banana-2` is an alias for `gemini-3.1-flash-image` (provides professional-level quality at flash speed), `nano-banana-pro` is an alias for `gemini-3-pro-image`, and `nano-banana` is an alias for `gemini-2.5-flash-image`. Models with the `:official` suffix (`nano-banana:official`, `nano-banana-2-lite:official`, `nano-banana-2:official`, `nano-banana-pro:official`) are provided through official channels, offering better image quality and stability, with different billing. */
  model?: "nano-banana" | "nano-banana-2-lite" | "nano-banana-2" | "nano-banana-pro" | "nano-banana:official" | "nano-banana-2-lite:official" | "nano-banana-2:official" | "nano-banana-pro:official";
  /** Link to the image that needs to be edited. It can be an accessible http or https URL, or a Base64 encoded image string in the format `data:image/png;base64,iVBORw0KG...`. Each image must not exceed 10MB in size. This parameter is required when `action` is `edit`. */
  imageUrls?: string[];
  /** Resolution of generated images. Supported values are `1K`, `2K`, `4K`, with a default of `1K`. If this parameter is specified, images will be generated at the specified resolution regardless of whether the `action` is `generate` or `edit` (smaller reference images can be redrawn at a higher resolution); if not specified, the default value of `1K` will be used. `nano-banana` and `nano-banana-2-lite` only support `1K`; `2K` / `4K` are only applicable to models that support high resolution. */
  resolution?: "1K" | "2K" | "4K";
  /** Aspect ratio for generating images. Supported values are `1:1`, `3:2`, `2:3`, `16:9`, `9:16`, `4:3`, `3:4`. If this parameter is specified, the specified aspect ratio will be used for generation regardless of whether `action` is `generate` or `edit`; if not specified, the default for `action` as `generate` is `1:1`, and for `action` as `edit`, it will automatically adopt the aspect ratio of the first image in `image_urls` to preserve the original composition. Note: In `edit` mode, specifying an aspect ratio that differs significantly from the original image will cause the model to redraw according to the new ratio, which may deviate from the reference image. */
  aspectRatio?: "1:1" | "3:2" | "2:3" | "16:9" | "9:16" | "4:3" | "3:4";
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

  /** Google Nano Banana image generation and editing API. Supports nano-banana, nano-banana-2, and nano-banana-pro for text-to-image generation and reference-image editing. */
  async generate(options: NanoBananaGenerateOptions): Promise<TaskHandle> {
    const body: Record<string, unknown> = {};
    body["action"] = options.action;
    body["prompt"] = options.prompt;
    body["count"] = options.count ?? 1;
    if (options.model !== undefined) body["model"] = options.model;
    if (options.imageUrls !== undefined) body["image_urls"] = options.imageUrls;
    if (options.resolution !== undefined) body["resolution"] = options.resolution;
    body["aspect_ratio"] = options.aspectRatio ?? "1:1";
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
