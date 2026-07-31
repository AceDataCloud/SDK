/** Midjourney provider resources. */

import { Transport } from '../../runtime/transport';
import { TaskHandle } from '../../runtime/tasks';

export type MidjourneyMode = 'fast' | 'relax' | 'turbo';
export type MidjourneyVideoMode = 'fast' | 'turbo';
export type MidjourneyVideoResolution = '480p' | '720p';
export type MidjourneyVideoAction = 'generate' | 'extend';

function taskId(result: Record<string, unknown>): string {
  if (typeof result?.task_id === 'string') return result.task_id;
  const data = result?.data as Record<string, unknown> | undefined;
  if (data && typeof data.task_id === 'string') return data.task_id;
  return typeof result?.id === 'string' ? result.id : '';
}

export class Midjourney {
  constructor(private transport: Transport) {}

  async imagine(opts: {
    prompt?: string;
    action?: string;
    mode?: MidjourneyMode;
    imageId?: string;
    mask?: string;
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
  }): Promise<TaskHandle> {
    const { prompt, action, mode, imageId, mask, timeout, translation, splitImages, version, hd, quality, styleReference, moodboard, callbackUrl, wait, pollInterval, maxWait, ...rest } = opts;
    const body: Record<string, unknown> = { ...rest };
    if (prompt !== undefined) body.prompt = prompt;
    if (action !== undefined) body.action = action;
    if (mode !== undefined) body.mode = mode;
    if (imageId !== undefined) body.image_id = imageId;
    if (mask !== undefined) body.mask = mask;
    if (timeout !== undefined) body.timeout = timeout;
    if (translation !== undefined) body.translation = translation;
    if (splitImages !== undefined) body.split_images = splitImages;
    if (version !== undefined) body.version = version;
    if (hd !== undefined) body.hd = hd;
    if (quality !== undefined) body.quality = quality;
    if (styleReference !== undefined) body.style_reference = styleReference;
    if (moodboard !== undefined) body.moodboard = moodboard;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    body.async = opts.async ?? true;
    const result = (await this.transport.request('POST', '/midjourney/imagine', { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), '/midjourney/tasks', this.transport, result);
    if (wait) {
      await handle.wait({ pollInterval, maxWait });
    }
    return handle;
  }

  async edits(opts: {
    prompt?: string;
    action?: string;
    mode?: MidjourneyMode;
    imageUrl?: string;
    mask?: string;
    splitImages?: boolean;
    async?: boolean;
    wait?: boolean;
    pollInterval?: number;
    maxWait?: number;
    callbackUrl?: string;
    [key: string]: unknown;
  }): Promise<TaskHandle> {
    const { prompt, action, mode, imageUrl, mask, splitImages, callbackUrl, wait, pollInterval, maxWait, ...rest } = opts;
    const body: Record<string, unknown> = { ...rest };
    if (prompt !== undefined) body.prompt = prompt;
    if (action !== undefined) body.action = action;
    if (mode !== undefined) body.mode = mode;
    if (imageUrl !== undefined) body.image_url = imageUrl;
    if (mask !== undefined) body.mask = mask;
    if (splitImages !== undefined) body.split_images = splitImages;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    body.async = opts.async ?? true;
    const result = (await this.transport.request('POST', '/midjourney/edits', { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), '/midjourney/tasks', this.transport, result);
    if (wait) {
      await handle.wait({ pollInterval, maxWait });
    }
    return handle;
  }

  async videos(opts: {
    action?: MidjourneyVideoAction;
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
  }): Promise<TaskHandle> {
    const { action, mode, resolution, prompt, videoId, videoIndex, loop, imageUrl, endImageUrl, callbackUrl, wait, pollInterval, maxWait, ...rest } = opts;
    const body: Record<string, unknown> = { ...rest };
    if (action !== undefined) body.action = action;
    if (mode !== undefined) body.mode = mode;
    if (resolution !== undefined) body.resolution = resolution;
    if (prompt !== undefined) body.prompt = prompt;
    if (videoId !== undefined) body.video_id = videoId;
    if (videoIndex !== undefined) body.video_index = videoIndex;
    if (loop !== undefined) body.loop = loop;
    if (imageUrl !== undefined) body.image_url = imageUrl;
    if (endImageUrl !== undefined) body.end_image_url = endImageUrl;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    body.async = opts.async ?? true;
    const result = (await this.transport.request('POST', '/midjourney/videos', { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), '/midjourney/tasks', this.transport, result);
    if (wait) {
      await handle.wait({ pollInterval, maxWait });
    }
    return handle;
  }

  async seed(opts: { imageId: string; [key: string]: unknown }): Promise<Record<string, unknown>> {
    const { imageId, ...rest } = opts;
    return this.transport.request('POST', '/midjourney/seed', { json: { image_id: imageId, ...rest } });
  }

  async describe(opts: { imageUrl: string; [key: string]: unknown }): Promise<Record<string, unknown>> {
    const { imageUrl, ...rest } = opts;
    return this.transport.request('POST', '/midjourney/describe', { json: { image_url: imageUrl, ...rest } });
  }

  async shorten(opts: { prompt: string; [key: string]: unknown }): Promise<Record<string, unknown>> {
    return this.transport.request('POST', '/midjourney/shorten', { json: opts });
  }

  async translate(opts: { content: string; [key: string]: unknown }): Promise<Record<string, unknown>> {
    return this.transport.request('POST', '/midjourney/translate', { json: opts });
  }
}
