/**
 * Midjourney (midjourney) — generated from the platform OpenAPI spec.
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

export interface MidjourneyImagineOptions {
  /** Midjourney Imagine Mask */
  mask?: string;
  /** Midjourney Imagine Mode */
  mode?: "fast" | "relax" | "turbo";
  /** Midjourney Imagine Action */
  action?: string;
  /** Midjourney Imagine Prompt */
  prompt?: string;
  /** Midjourney Imagine Timeout */
  timeout?: number;
  /** Midjourney Imagine Image Id */
  imageId?: string;
  /** Midjourney Imagine Translation */
  translation?: boolean;
  /** Midjourney Imagine Split Images */
  splitImages?: boolean;
  /** Midjourney Imagine Version */
  version?: "8.2" | "8.1" | "8" | "7" | "6.1" | "6" | "5.2";
  /** Midjourney Imagine Hd */
  hd?: boolean;
  /** Midjourney Imagine Quality */
  quality?: string;
  /** Midjourney Imagine Style Reference */
  styleReference?: boolean;
  /** Midjourney Imagine Moodboard */
  moodboard?: boolean;
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

export interface MidjourneySeedOptions {
  /** Midjourney Seed Image Id */
  imageId: string;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

export interface MidjourneyEditsOptions {
  /** Midjourney Edits Mask */
  mask?: string;
  /** Midjourney Edits Mode */
  mode?: "fast" | "relax" | "turbo";
  /** Midjourney Edits Action */
  action?: string;
  /** Midjourney Edits Prompt */
  prompt?: string;
  /** Midjourney Edits Image Url */
  imageUrl?: string;
  /** Midjourney Edits Split Images */
  splitImages?: boolean;
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

export interface MidjourneyGenerateOptions {
  /** Midjourney Videos Action */
  action?: "generate" | "extend";
  /** Midjourney Videos Mode */
  mode?: "fast" | "turbo";
  /** Midjourney Videos Resolution */
  resolution?: "480p" | "720p";
  /** Midjourney Videos Prompt */
  prompt?: string;
  /** Midjourney Videos Video Id */
  videoId?: string;
  /** Midjourney Videos Video Index */
  videoIndex?: number;
  /** Midjourney Videos Loop */
  loop?: boolean;
  /** Midjourney Videos Image Url */
  imageUrl?: string;
  /** Midjourney Videos End Image Url */
  endImageUrl?: string;
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

export interface MidjourneyDescribeOptions {
  /** Midjourney Describe Image Url */
  imageUrl: string;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

export interface MidjourneyShortenOptions {
  /** Midjourney Shorten Prompt */
  prompt: string;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

export interface MidjourneyTranslateOptions {
  /** Midjourney Translate 2 */
  content: string;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

/** midjourney client. */
export class Midjourney {
  constructor(private transport: Transport) {}

  /** Midjourney Imagine */
  async imagine(options: MidjourneyImagineOptions = {}): Promise<TaskHandle> {
    const body: Record<string, unknown> = {};
    if (options.mask !== undefined) body["mask"] = options.mask;
    body["mode"] = options.mode ?? "fast";
    body["action"] = options.action ?? "generate";
    if (options.prompt !== undefined) body["prompt"] = options.prompt;
    body["timeout"] = options.timeout ?? 480;
    if (options.imageId !== undefined) body["image_id"] = options.imageId;
    body["translation"] = options.translation ?? false;
    body["split_images"] = options.splitImages ?? false;
    if (options.version !== undefined) body["version"] = options.version;
    body["hd"] = options.hd ?? false;
    body["quality"] = options.quality ?? "1";
    body["style_reference"] = options.styleReference ?? false;
    body["moodboard"] = options.moodboard ?? false;
    for (const [key, value] of Object.entries(options)) {
      if (!["action", "async", "callbackUrl", "hd", "imageId", "mask", "maxWait", "mode", "moodboard", "pollInterval", "prompt", "quality", "splitImages", "styleReference", "timeout", "translation", "version", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    body.async = options.async ?? true;
    const result = (await this.transport.request('POST', "/midjourney/imagine", { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), "/midjourney/tasks", this.transport, result);
    if (options.wait) {
      await handle.wait({ pollInterval: options.pollInterval, maxWait: options.maxWait });
    }
    return handle;
  }

  /** Midjourney Seed */
  async seed(options: MidjourneySeedOptions): Promise<Record<string, unknown>> {
    const body: Record<string, unknown> = {};
    body["image_id"] = options.imageId;
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "callbackUrl", "imageId", "maxWait", "pollInterval", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    return (await this.transport.request('POST', "/midjourney/seed", { json: body })) as Record<string, unknown>;
  }

  /** Midjourney Edits */
  async edits(options: MidjourneyEditsOptions = {}): Promise<TaskHandle> {
    const body: Record<string, unknown> = {};
    if (options.mask !== undefined) body["mask"] = options.mask;
    if (options.mode !== undefined) body["mode"] = options.mode;
    body["action"] = options.action ?? "generate";
    if (options.prompt !== undefined) body["prompt"] = options.prompt;
    if (options.imageUrl !== undefined) body["image_url"] = options.imageUrl;
    body["split_images"] = options.splitImages ?? false;
    for (const [key, value] of Object.entries(options)) {
      if (!["action", "async", "callbackUrl", "imageUrl", "mask", "maxWait", "mode", "pollInterval", "prompt", "splitImages", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    body.async = options.async ?? true;
    const result = (await this.transport.request('POST', "/midjourney/edits", { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), "/midjourney/tasks", this.transport, result);
    if (options.wait) {
      await handle.wait({ pollInterval: options.pollInterval, maxWait: options.maxWait });
    }
    return handle;
  }

  /** Midjourney Videos */
  async generate(options: MidjourneyGenerateOptions = {}): Promise<TaskHandle> {
    const body: Record<string, unknown> = {};
    if (options.action !== undefined) body["action"] = options.action;
    if (options.mode !== undefined) body["mode"] = options.mode;
    if (options.resolution !== undefined) body["resolution"] = options.resolution;
    if (options.prompt !== undefined) body["prompt"] = options.prompt;
    if (options.videoId !== undefined) body["video_id"] = options.videoId;
    if (options.videoIndex !== undefined) body["video_index"] = options.videoIndex;
    if (options.loop !== undefined) body["loop"] = options.loop;
    if (options.imageUrl !== undefined) body["image_url"] = options.imageUrl;
    if (options.endImageUrl !== undefined) body["end_image_url"] = options.endImageUrl;
    for (const [key, value] of Object.entries(options)) {
      if (!["action", "async", "callbackUrl", "endImageUrl", "imageUrl", "loop", "maxWait", "mode", "pollInterval", "prompt", "resolution", "videoId", "videoIndex", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    body.async = options.async ?? true;
    const result = (await this.transport.request('POST', "/midjourney/videos", { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), "/midjourney/tasks", this.transport, result);
    if (options.wait) {
      await handle.wait({ pollInterval: options.pollInterval, maxWait: options.maxWait });
    }
    return handle;
  }

  /** Midjourney Describe */
  async describe(options: MidjourneyDescribeOptions): Promise<Record<string, unknown>> {
    const body: Record<string, unknown> = {};
    body["image_url"] = options.imageUrl;
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "callbackUrl", "imageUrl", "maxWait", "pollInterval", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    return (await this.transport.request('POST', "/midjourney/describe", { json: body })) as Record<string, unknown>;
  }

  /** Midjourney Shorten */
  async shorten(options: MidjourneyShortenOptions): Promise<Record<string, unknown>> {
    const body: Record<string, unknown> = {};
    body["prompt"] = options.prompt;
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "callbackUrl", "maxWait", "pollInterval", "prompt", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    return (await this.transport.request('POST', "/midjourney/shorten", { json: body })) as Record<string, unknown>;
  }

  /** Midjourney Translate */
  async translate(options: MidjourneyTranslateOptions): Promise<Record<string, unknown>> {
    const body: Record<string, unknown> = {};
    body["content"] = options.content;
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "callbackUrl", "content", "maxWait", "pollInterval", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    return (await this.transport.request('POST', "/midjourney/translate", { json: body })) as Record<string, unknown>;
  }

}
