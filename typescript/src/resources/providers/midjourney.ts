/**
 * Midjourney (midjourney) — provider client for Midjourney image and video generation.
 */

import { Transport } from '../../runtime/transport';
import { TaskHandle } from '../../runtime/tasks';

export type MidjourneyMode = 'fast' | 'relax' | 'turbo';
export type MidjourneyVideoMode = 'fast' | 'turbo';
export type MidjourneyVideoResolution = '480p' | '720p';

function taskId(result: Record<string, unknown>): string {
  if (typeof result?.task_id === 'string') return result.task_id;
  const data = result?.data as Record<string, unknown> | undefined;
  if (data && typeof data.task_id === 'string') return data.task_id;
  return typeof result?.id === 'string' ? result.id : '';
}

export interface MidjourneyImagineOptions {
  prompt?: string;
  action?: string;
  imageId?: string;
  mask?: string;
  mode?: MidjourneyMode;
  timeout?: number;
  translation?: boolean;
  splitImages?: boolean;
  version?: string;
  hd?: boolean;
  quality?: string;
  styleReference?: boolean;
  moodboard?: boolean;
  async?: boolean;
  wait?: boolean;
  pollInterval?: number;
  maxWait?: number;
  callbackUrl?: string;
  [key: string]: unknown;
}

export interface MidjourneyEditsOptions {
  prompt?: string;
  action?: string;
  imageUrl?: string;
  mask?: string;
  mode?: MidjourneyMode;
  splitImages?: boolean;
  async?: boolean;
  wait?: boolean;
  pollInterval?: number;
  maxWait?: number;
  callbackUrl?: string;
  [key: string]: unknown;
}

export interface MidjourneyVideosOptions {
  action?: 'generate' | 'extend';
  mode?: MidjourneyVideoMode;
  resolution?: MidjourneyVideoResolution;
  prompt?: string;
  videoId?: string;
  videoIndex?: number;
  loop?: boolean;
  imageUrl?: string;
  endImageUrl?: string;
  async?: boolean;
  wait?: boolean;
  pollInterval?: number;
  maxWait?: number;
  callbackUrl?: string;
  [key: string]: unknown;
}

export class Midjourney {
  constructor(private transport: Transport) {}

  /** Midjourney imagine API — generate images from text prompts. */
  async imagine(opts: MidjourneyImagineOptions = {}): Promise<TaskHandle> {
    const { prompt, action, imageId, mask, mode, timeout, translation, splitImages, version, hd, quality, styleReference, moodboard, callbackUrl, ...rest } = opts;
    const body: Record<string, unknown> = {};
    if (prompt !== undefined) body.prompt = prompt;
    if (action !== undefined) body.action = action;
    if (imageId !== undefined) body.image_id = imageId;
    if (mask !== undefined) body.mask = mask;
    if (mode !== undefined) body.mode = mode;
    if (timeout !== undefined) body.timeout = timeout;
    if (translation !== undefined) body.translation = translation;
    if (splitImages !== undefined) body.split_images = splitImages;
    if (version !== undefined) body.version = version;
    if (hd !== undefined) body.hd = hd;
    if (quality !== undefined) body.quality = quality;
    if (styleReference !== undefined) body.style_reference = styleReference;
    if (moodboard !== undefined) body.moodboard = moodboard;
    for (const [key, value] of Object.entries(rest)) {
      if (!['async', 'maxWait', 'pollInterval', 'wait'].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    if (opts.async !== undefined) body.async = opts.async;
    const result = (await this.transport.request('POST', '/midjourney/imagine', { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), '/midjourney/tasks', this.transport, result);
    if (opts.wait) {
      await handle.wait({ pollInterval: opts.pollInterval, maxWait: opts.maxWait });
    }
    return handle;
  }

  /** Midjourney edits API — edit and remix existing images. */
  async edits(opts: MidjourneyEditsOptions = {}): Promise<TaskHandle> {
    const { prompt, action, imageUrl, mask, mode, splitImages, callbackUrl, ...rest } = opts;
    const body: Record<string, unknown> = {};
    if (prompt !== undefined) body.prompt = prompt;
    if (action !== undefined) body.action = action;
    if (imageUrl !== undefined) body.image_url = imageUrl;
    if (mask !== undefined) body.mask = mask;
    if (mode !== undefined) body.mode = mode;
    if (splitImages !== undefined) body.split_images = splitImages;
    for (const [key, value] of Object.entries(rest)) {
      if (!['async', 'maxWait', 'pollInterval', 'wait'].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    if (opts.async !== undefined) body.async = opts.async;
    const result = (await this.transport.request('POST', '/midjourney/edits', { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), '/midjourney/tasks', this.transport, result);
    if (opts.wait) {
      await handle.wait({ pollInterval: opts.pollInterval, maxWait: opts.maxWait });
    }
    return handle;
  }

  /** Midjourney video generation API. */
  async videos(opts: MidjourneyVideosOptions = {}): Promise<TaskHandle> {
    const { action, mode, resolution, prompt, videoId, videoIndex, loop, imageUrl, endImageUrl, callbackUrl, ...rest } = opts;
    const body: Record<string, unknown> = {};
    if (action !== undefined) body.action = action;
    if (mode !== undefined) body.mode = mode;
    if (resolution !== undefined) body.resolution = resolution;
    if (prompt !== undefined) body.prompt = prompt;
    if (videoId !== undefined) body.video_id = videoId;
    if (videoIndex !== undefined) body.video_index = videoIndex;
    if (loop !== undefined) body.loop = loop;
    if (imageUrl !== undefined) body.image_url = imageUrl;
    if (endImageUrl !== undefined) body.end_image_url = endImageUrl;
    for (const [key, value] of Object.entries(rest)) {
      if (!['async', 'maxWait', 'pollInterval', 'wait'].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    if (opts.async !== undefined) body.async = opts.async;
    const result = (await this.transport.request('POST', '/midjourney/videos', { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), '/midjourney/tasks', this.transport, result);
    if (opts.wait) {
      await handle.wait({ pollInterval: opts.pollInterval, maxWait: opts.maxWait });
    }
    return handle;
  }

  /** Get the seed of a Midjourney image. */
  async seed(opts: { imageId: string; [key: string]: unknown }): Promise<Record<string, unknown>> {
    const { imageId, ...rest } = opts;
    return this.transport.request('POST', '/midjourney/seed', { json: { image_id: imageId, ...rest } });
  }

  /** Describe a Midjourney image URL. */
  async describe(opts: { imageUrl: string; [key: string]: unknown }): Promise<Record<string, unknown>> {
    const { imageUrl, ...rest } = opts;
    return this.transport.request('POST', '/midjourney/describe', { json: { image_url: imageUrl, ...rest } });
  }

  /** Shorten a Midjourney prompt. */
  async shorten(opts: { prompt: string; [key: string]: unknown }): Promise<Record<string, unknown>> {
    const { prompt, ...rest } = opts;
    return this.transport.request('POST', '/midjourney/shorten', { json: { prompt, ...rest } });
  }

  /** Translate content for Midjourney. */
  async translate(opts: { content: string; [key: string]: unknown }): Promise<Record<string, unknown>> {
    const { content, ...rest } = opts;
    return this.transport.request('POST', '/midjourney/translate', { json: { content, ...rest } });
  }
}
