/** Veo-specific video generation and editing resources. */

import { Transport } from '../runtime/transport';

export type VeoModel = 'veo2' | 'veo2-fast' | 'veo3' | 'veo3-fast' | 'veo31-fast' | 'veo31' | 'veo31-fast-ingredients' | (string & {});

export class Veo {
  constructor(private transport: Transport) {}

  async generate(opts: {
    action: 'text2video' | 'image2video' | 'ingredients2video' | 'get1080p';
    prompt?: string;
    model?: VeoModel;
    resolution?: '4k' | '1080p' | 'gif';
    videoId?: string;
    translation?: string;
    aspectRatio?: '9:16' | '1:1' | '3:4' | '4:3' | '16:9';
    imageUrls?: string[];
    callbackUrl?: string;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { action, prompt, model, resolution, videoId, translation, aspectRatio, imageUrls, callbackUrl, ...rest } = opts;
    const body: Record<string, unknown> = { action, ...rest };
    if (prompt !== undefined) body.prompt = prompt;
    if (model !== undefined) body.model = model;
    if (resolution !== undefined) body.resolution = resolution;
    if (videoId !== undefined) body.video_id = videoId;
    if (translation !== undefined) body.translation = translation;
    if (aspectRatio !== undefined) body.aspect_ratio = aspectRatio;
    if (imageUrls !== undefined) body.image_urls = imageUrls;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    return this.transport.request('POST', '/veo/videos', { json: body });
  }

  async upsample(opts: {
    videoId: string;
    action: '1080p' | '4k' | 'gif';
    callbackUrl?: string;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { videoId, action, callbackUrl, ...rest } = opts;
    const body: Record<string, unknown> = { video_id: videoId, action, ...rest };
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    return this.transport.request('POST', '/veo/upsample', { json: body });
  }

  async extend(opts: {
    videoId: string;
    model: 'veo31-fast' | 'veo31' | (string & {});
    prompt?: string;
    callbackUrl?: string;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { videoId, model, prompt, callbackUrl, ...rest } = opts;
    const body: Record<string, unknown> = { video_id: videoId, model, ...rest };
    if (prompt !== undefined) body.prompt = prompt;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    return this.transport.request('POST', '/veo/extend', { json: body });
  }

  async reshoot(opts: {
    videoId: string;
    motionType: 'STATIONARY' | 'STATIONARY_UP' | 'STATIONARY_DOWN' | 'STATIONARY_LEFT' | 'STATIONARY_RIGHT' | 'STATIONARY_DOLLY_IN_ZOOM_OUT' | 'STATIONARY_DOLLY_OUT_ZOOM_IN' | 'UP' | 'DOWN' | 'LEFT_TO_RIGHT' | 'RIGHT_TO_LEFT' | 'FORWARD' | 'BACKWARD' | 'DOLLY_IN_ZOOM_OUT' | 'DOLLY_OUT_ZOOM_IN' | (string & {});
    callbackUrl?: string;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { videoId, motionType, callbackUrl, ...rest } = opts;
    const body: Record<string, unknown> = { video_id: videoId, motion_type: motionType, ...rest };
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    return this.transport.request('POST', '/veo/reshoot', { json: body });
  }

  async objects(opts: {
    videoId: string;
    action: 'insert' | 'remove';
    prompt?: string;
    imageMask?: string;
    callbackUrl?: string;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { videoId, action, prompt, imageMask, callbackUrl, ...rest } = opts;
    const body: Record<string, unknown> = { video_id: videoId, action, ...rest };
    if (prompt !== undefined) body.prompt = prompt;
    if (imageMask !== undefined) body.image_mask = imageMask;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    return this.transport.request('POST', '/veo/objects', { json: body });
  }
}
