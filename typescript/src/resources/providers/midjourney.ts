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

export type MidjourneyMode = 'fast' | 'relax' | 'turbo';
export type MidjourneyVideoResolution = '480p' | '720p';
export type MidjourneyVideoAction = 'generate' | 'extend';

export class Midjourney {
  constructor(private transport: Transport) {}

  async imagine(opts: {
    prompt?: string;
    imageId?: string;
    mask?: string;
    mode?: MidjourneyMode;
    action?: string;
    timeout?: number;
    translation?: boolean;
    splitImages?: boolean;
    version?: string;
    hd?: boolean;
    quality?: string;
    styleReference?: boolean;
    moodboard?: boolean;
    callbackUrl?: string;
    async?: boolean;
    wait?: boolean;
  } = {}): Promise<TaskHandle> {
    const body: Record<string, unknown> = {};
    if (opts.prompt !== undefined) body.prompt = opts.prompt;
    if (opts.imageId !== undefined) body.image_id = opts.imageId;
    if (opts.mask !== undefined) body.mask = opts.mask;
    if (opts.mode !== undefined) body.mode = opts.mode;
    if (opts.action !== undefined) body.action = opts.action;
    if (opts.timeout !== undefined) body.timeout = opts.timeout;
    if (opts.translation !== undefined) body.translation = opts.translation;
    if (opts.splitImages !== undefined) body.split_images = opts.splitImages;
    if (opts.version !== undefined) body.version = opts.version;
    if (opts.hd !== undefined) body.hd = opts.hd;
    if (opts.quality !== undefined) body.quality = opts.quality;
    if (opts.styleReference !== undefined) body.style_reference = opts.styleReference;
    if (opts.moodboard !== undefined) body.moodboard = opts.moodboard;
    if (opts.callbackUrl !== undefined) body.callback_url = opts.callbackUrl;
    if (opts.async !== undefined) body.async = opts.async;
    const result = (await this.transport.request('POST', '/midjourney/imagine', { json: body })) as Record<string, unknown>;
    return new TaskHandle(taskId(result), '/midjourney/tasks', this.transport, result);
  }

  async edits(opts: {
    prompt?: string;
    imageUrl?: string;
    mask?: string;
    mode?: MidjourneyMode;
    action?: string;
    splitImages?: boolean;
    callbackUrl?: string;
    async?: boolean;
  } = {}): Promise<TaskHandle> {
    const body: Record<string, unknown> = {};
    if (opts.prompt !== undefined) body.prompt = opts.prompt;
    if (opts.imageUrl !== undefined) body.image_url = opts.imageUrl;
    if (opts.mask !== undefined) body.mask = opts.mask;
    if (opts.mode !== undefined) body.mode = opts.mode;
    if (opts.action !== undefined) body.action = opts.action;
    if (opts.splitImages !== undefined) body.split_images = opts.splitImages;
    if (opts.callbackUrl !== undefined) body.callback_url = opts.callbackUrl;
    if (opts.async !== undefined) body.async = opts.async;
    const result = (await this.transport.request('POST', '/midjourney/edits', { json: body })) as Record<string, unknown>;
    return new TaskHandle(taskId(result), '/midjourney/tasks', this.transport, result);
  }

  async videos(opts: {
    action?: MidjourneyVideoAction;
    mode?: 'fast' | 'turbo';
    resolution?: MidjourneyVideoResolution;
    prompt?: string;
    videoId?: string;
    videoIndex?: number;
    loop?: boolean;
    imageUrl?: string;
    endImageUrl?: string;
    callbackUrl?: string;
    async?: boolean;
  } = {}): Promise<TaskHandle> {
    const body: Record<string, unknown> = {};
    if (opts.action !== undefined) body.action = opts.action;
    if (opts.mode !== undefined) body.mode = opts.mode;
    if (opts.resolution !== undefined) body.resolution = opts.resolution;
    if (opts.prompt !== undefined) body.prompt = opts.prompt;
    if (opts.videoId !== undefined) body.video_id = opts.videoId;
    if (opts.videoIndex !== undefined) body.video_index = opts.videoIndex;
    if (opts.loop !== undefined) body.loop = opts.loop;
    if (opts.imageUrl !== undefined) body.image_url = opts.imageUrl;
    if (opts.endImageUrl !== undefined) body.end_image_url = opts.endImageUrl;
    if (opts.callbackUrl !== undefined) body.callback_url = opts.callbackUrl;
    if (opts.async !== undefined) body.async = opts.async;
    const result = (await this.transport.request('POST', '/midjourney/videos', { json: body })) as Record<string, unknown>;
    return new TaskHandle(taskId(result), '/midjourney/tasks', this.transport, result);
  }

  async seed(opts: { imageId: string }): Promise<Record<string, unknown>> {
    return (await this.transport.request('POST', '/midjourney/seed', { json: { image_id: opts.imageId } })) as Record<string, unknown>;
  }

  async describe(opts: { imageUrl: string }): Promise<Record<string, unknown>> {
    return (await this.transport.request('POST', '/midjourney/describe', { json: { image_url: opts.imageUrl } })) as Record<string, unknown>;
  }

  async shorten(opts: { prompt: string }): Promise<Record<string, unknown>> {
    return (await this.transport.request('POST', '/midjourney/shorten', { json: { prompt: opts.prompt } })) as Record<string, unknown>;
  }

  async translate(opts: { content: string }): Promise<Record<string, unknown>> {
    return (await this.transport.request('POST', '/midjourney/translate', { json: { content: opts.content } })) as Record<string, unknown>;
  }
}
