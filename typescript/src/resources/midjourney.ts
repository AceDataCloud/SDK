/** Midjourney image/video generation resources. */

import { Transport } from '../runtime/transport';

export class Midjourney {
  constructor(private transport: Transport) {}

  async imagine(opts: {
    prompt?: string;
    action?: string;
    mode?: string;
    mask?: string;
    imageId?: string;
    translation?: boolean;
    callbackUrl?: string;
    async?: boolean;
    splitImages?: boolean;
    version?: string;
    hd?: boolean;
    quality?: string;
    styleReference?: boolean;
    moodboard?: boolean;
    timeout?: number;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { prompt, action, mode, mask, imageId, translation, callbackUrl, splitImages, version, hd, quality, styleReference, moodboard, timeout, ...rest } = opts;
    const body: Record<string, unknown> = { ...rest };
    if (prompt !== undefined) body.prompt = prompt;
    if (action !== undefined) body.action = action;
    if (mode !== undefined) body.mode = mode;
    if (mask !== undefined) body.mask = mask;
    if (imageId !== undefined) body.image_id = imageId;
    if (translation !== undefined) body.translation = translation;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    if (opts.async !== undefined) body.async = opts.async;
    if (splitImages !== undefined) body.split_images = splitImages;
    if (version !== undefined) body.version = version;
    if (hd !== undefined) body.hd = hd;
    if (quality !== undefined) body.quality = quality;
    if (styleReference !== undefined) body.style_reference = styleReference;
    if (moodboard !== undefined) body.moodboard = moodboard;
    if (timeout !== undefined) body.timeout = timeout;
    return this.transport.request('POST', '/midjourney/imagine', { json: body });
  }

  async seed(opts: {
    imageId: string;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { imageId, ...rest } = opts;
    const body: Record<string, unknown> = { image_id: imageId, ...rest };
    return this.transport.request('POST', '/midjourney/seed', { json: body });
  }

  async edits(opts: {
    prompt?: string;
    action?: string;
    mode?: string;
    mask?: string;
    imageUrl?: string;
    callbackUrl?: string;
    async?: boolean;
    splitImages?: boolean;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { prompt, action, mode, mask, imageUrl, callbackUrl, splitImages, ...rest } = opts;
    const body: Record<string, unknown> = { ...rest };
    if (prompt !== undefined) body.prompt = prompt;
    if (action !== undefined) body.action = action;
    if (mode !== undefined) body.mode = mode;
    if (mask !== undefined) body.mask = mask;
    if (imageUrl !== undefined) body.image_url = imageUrl;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    if (opts.async !== undefined) body.async = opts.async;
    if (splitImages !== undefined) body.split_images = splitImages;
    return this.transport.request('POST', '/midjourney/edits', { json: body });
  }

  async videos(opts: {
    prompt?: string;
    action?: string;
    mode?: string;
    resolution?: string;
    videoId?: string;
    videoIndex?: number;
    loop?: boolean;
    imageUrl?: string;
    endImageUrl?: string;
    callbackUrl?: string;
    async?: boolean;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { prompt, action, mode, resolution, videoId, videoIndex, loop, imageUrl, endImageUrl, callbackUrl, ...rest } = opts;
    const body: Record<string, unknown> = { ...rest };
    if (prompt !== undefined) body.prompt = prompt;
    if (action !== undefined) body.action = action;
    if (mode !== undefined) body.mode = mode;
    if (resolution !== undefined) body.resolution = resolution;
    if (videoId !== undefined) body.video_id = videoId;
    if (videoIndex !== undefined) body.video_index = videoIndex;
    if (loop !== undefined) body.loop = loop;
    if (imageUrl !== undefined) body.image_url = imageUrl;
    if (endImageUrl !== undefined) body.end_image_url = endImageUrl;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    if (opts.async !== undefined) body.async = opts.async;
    return this.transport.request('POST', '/midjourney/videos', { json: body });
  }

  async describe(opts: {
    imageUrl: string;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { imageUrl, ...rest } = opts;
    const body: Record<string, unknown> = { image_url: imageUrl, ...rest };
    return this.transport.request('POST', '/midjourney/describe', { json: body });
  }

  async shorten(opts: {
    prompt: string;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { prompt, ...rest } = opts;
    const body: Record<string, unknown> = { prompt, ...rest };
    return this.transport.request('POST', '/midjourney/shorten', { json: body });
  }

  async translate(opts: {
    content: string;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { content, ...rest } = opts;
    const body: Record<string, unknown> = { content, ...rest };
    return this.transport.request('POST', '/midjourney/translate', { json: body });
  }
}
