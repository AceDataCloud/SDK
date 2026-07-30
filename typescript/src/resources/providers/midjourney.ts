/** Midjourney (midjourney) — synced from the platform OpenAPI spec. */

import { Transport } from '../../runtime/transport';
import { TaskHandle } from '../../runtime/tasks';

function taskId(result: Record<string, unknown>): string {
  if (typeof result?.task_id === 'string') return result.task_id;
  const data = result?.data as Record<string, unknown> | undefined;
  if (data && typeof data.task_id === 'string') return data.task_id;
  return typeof result?.id === 'string' ? result.id : '';
}

export interface MidjourneyImagineOptions {
  mask?: string;
  mode?: 'fast' | 'relax' | 'turbo';
  action?: string;
  prompt?: string;
  timeout?: number;
  imageId?: string;
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
  mask?: string;
  mode?: 'fast' | 'relax' | 'turbo';
  action?: string;
  prompt?: string;
  imageUrl?: string;
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
  mode?: 'fast' | 'turbo';
  resolution?: '480p' | '720p';
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

  async imagine(options: MidjourneyImagineOptions = {}): Promise<TaskHandle> {
    const { imageId, splitImages, styleReference, callbackUrl, ...rest } = options;
    const body: Record<string, unknown> = { ...rest };
    if (imageId !== undefined) body.image_id = imageId;
    if (splitImages !== undefined) body.split_images = splitImages;
    if (styleReference !== undefined) body.style_reference = styleReference;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    body.async = options.async ?? true;
    const result = (await this.transport.request('POST', '/midjourney/imagine', { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), '/midjourney/tasks', this.transport, result);
    if (options.wait) await handle.wait({ pollInterval: options.pollInterval, maxWait: options.maxWait });
    return handle;
  }

  async seed(imageId: string, options: { callbackUrl?: string; [key: string]: unknown } = {}): Promise<Record<string, unknown>> {
    const { callbackUrl, ...rest } = options;
    const body: Record<string, unknown> = { image_id: imageId, ...rest };
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    return this.transport.request('POST', '/midjourney/seed', { json: body });
  }

  async edits(options: MidjourneyEditsOptions = {}): Promise<TaskHandle> {
    const { imageUrl, splitImages, callbackUrl, ...rest } = options;
    const body: Record<string, unknown> = { ...rest };
    if (imageUrl !== undefined) body.image_url = imageUrl;
    if (splitImages !== undefined) body.split_images = splitImages;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    body.async = options.async ?? true;
    const result = (await this.transport.request('POST', '/midjourney/edits', { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), '/midjourney/tasks', this.transport, result);
    if (options.wait) await handle.wait({ pollInterval: options.pollInterval, maxWait: options.maxWait });
    return handle;
  }

  async videos(options: MidjourneyVideosOptions = {}): Promise<TaskHandle> {
    const { videoId, videoIndex, imageUrl, endImageUrl, callbackUrl, ...rest } = options;
    const body: Record<string, unknown> = { ...rest };
    if (videoId !== undefined) body.video_id = videoId;
    if (videoIndex !== undefined) body.video_index = videoIndex;
    if (imageUrl !== undefined) body.image_url = imageUrl;
    if (endImageUrl !== undefined) body.end_image_url = endImageUrl;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    body.async = options.async ?? true;
    const result = (await this.transport.request('POST', '/midjourney/videos', { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), '/midjourney/tasks', this.transport, result);
    if (options.wait) await handle.wait({ pollInterval: options.pollInterval, maxWait: options.maxWait });
    return handle;
  }

  async describe(imageUrl: string, options: { callbackUrl?: string; [key: string]: unknown } = {}): Promise<Record<string, unknown>> {
    const { callbackUrl, ...rest } = options;
    const body: Record<string, unknown> = { image_url: imageUrl, ...rest };
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    return this.transport.request('POST', '/midjourney/describe', { json: body });
  }

  async shorten(prompt: string, options: { callbackUrl?: string; [key: string]: unknown } = {}): Promise<Record<string, unknown>> {
    const { callbackUrl, ...rest } = options;
    const body: Record<string, unknown> = { prompt, ...rest };
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    return this.transport.request('POST', '/midjourney/shorten', { json: body });
  }

  async translate(content: string, options: { callbackUrl?: string; [key: string]: unknown } = {}): Promise<Record<string, unknown>> {
    const { callbackUrl, ...rest } = options;
    const body: Record<string, unknown> = { content, ...rest };
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    return this.transport.request('POST', '/midjourney/translate', { json: body });
  }
}
