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
  /** Image size specifications. */
  size: string;
  /** Types of operations for generating images. If it is `generate`, a new image will be created based on the prompt; if it is `edit`, the original image will be edited according to the prompt and `image_url`. */
  action: "generate" | "edit";
  /** Prompts for generating images. */
  prompt: string;
  /** Number of generated images. */
  count?: number;
  /** Model used for generating images. */
  model?: "flux-dev" | "flux-pro" | "flux-kontext-pro" | "flux-kontext-max" | "flux-2-flex" | "flux-2-pro" | "flux-2-max" | "flux-2-klein";
  /** Link to the original image that needs editing. */
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

export interface FluxVideosOptions {
  mode: "t2v" | "i2v" | "v2v" | "draft_enhance";
  action?: "generate";
  prompt?: string;
  aspectRatio?: "21:9" | "2:1" | "16:9" | "4:3" | "1:1" | "3:4" | "9:16" | "9:21" | "auto";
  duration?: number | "auto";
  resolution?: "hd" | "fhd" | "qhd" | "uhd";
  version?: "latest";
  generateAudio?: boolean;
  safetyTolerance?: number;
  draft?: boolean;
  model?: "flux-3";
  keyframes?: string | unknown[] | string[];
  startVideo?: string;
  draftTaskId?: string;
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

  /** Flux AI image generation API, generates 1 image per request. */
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

  /** Flux Generate Summary */
  async videos(options: FluxVideosOptions): Promise<TaskHandle> {
    const body: Record<string, unknown> = {};
    body["mode"] = options.mode;
    body["action"] = options.action ?? "generate";
    if (options.prompt !== undefined) body["prompt"] = options.prompt;
    body["aspect_ratio"] = options.aspectRatio ?? "auto";
    if (options.duration !== undefined) body["duration"] = options.duration;
    body["resolution"] = options.resolution ?? "hd";
    body["version"] = options.version ?? "latest";
    if (options.generateAudio !== undefined) body["generate_audio"] = options.generateAudio;
    body["safety_tolerance"] = options.safetyTolerance ?? 2;
    if (options.draft !== undefined) body["draft"] = options.draft;
    body["model"] = options.model ?? "flux-3";
    if (options.keyframes !== undefined) body["keyframes"] = options.keyframes;
    if (options.startVideo !== undefined) body["start_video"] = options.startVideo;
    if (options.draftTaskId !== undefined) body["draft_task_id"] = options.draftTaskId;
    for (const [key, value] of Object.entries(options)) {
      if (!["action", "aspectRatio", "async", "callbackUrl", "draft", "draftTaskId", "duration", "generateAudio", "keyframes", "maxWait", "mode", "model", "pollInterval", "prompt", "resolution", "safetyTolerance", "startVideo", "version", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    body.async = options.async ?? true;
    const result = (await this.transport.request('POST', "/flux/videos", { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), "/flux/tasks", this.transport, result);
    if (options.wait) {
      await handle.wait({ pollInterval: options.pollInterval, maxWait: options.maxWait });
    }
    return handle;
  }

}
