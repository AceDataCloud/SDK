/** Kling-specific video generation resources. */

import { Transport } from '../runtime/transport';

export type KlingModel =
  | 'kling-v1'
  | 'kling-v1-6'
  | 'kling-v2-master'
  | 'kling-v2-1-master'
  | 'kling-v2-5-turbo'
  | 'kling-v2-6'
  | 'kling-v3'
  | 'kling-v3-omni'
  | 'kling-video-o1'
  | (string & {});

export class Kling {
  constructor(private transport: Transport) {}

  async generate(opts: {
    action: 'text2video' | 'image2video' | 'extend';
    mode?: 'std' | 'pro' | '4k';
    model?: KlingModel;
    prompt?: string;
    duration?: 5 | 10;
    generateAudio?: boolean;
    videoId?: string;
    cfgScale?: number;
    aspectRatio?: '16:9' | '9:16' | '1:1';
    callbackUrl?: string;
    endImageUrl?: string;
    cameraControl?: string;
    elementList?: unknown[];
    videoList?: unknown[];
    negativePrompt?: string;
    startImageUrl?: string;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const {
      action,
      mode,
      model,
      prompt,
      duration,
      generateAudio,
      videoId,
      cfgScale,
      aspectRatio,
      callbackUrl,
      endImageUrl,
      cameraControl,
      elementList,
      videoList,
      negativePrompt,
      startImageUrl,
      ...rest
    } = opts;
    const body: Record<string, unknown> = { action, ...rest };
    if (mode !== undefined) body.mode = mode;
    if (model !== undefined) body.model = model;
    if (prompt !== undefined) body.prompt = prompt;
    if (duration !== undefined) body.duration = duration;
    if (generateAudio !== undefined) body.generate_audio = generateAudio;
    if (videoId !== undefined) body.video_id = videoId;
    if (cfgScale !== undefined) body.cfg_scale = cfgScale;
    if (aspectRatio !== undefined) body.aspect_ratio = aspectRatio;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    if (endImageUrl !== undefined) body.end_image_url = endImageUrl;
    if (cameraControl !== undefined) body.camera_control = cameraControl;
    if (elementList !== undefined) body.element_list = elementList;
    if (videoList !== undefined) body.video_list = videoList;
    if (negativePrompt !== undefined) body.negative_prompt = negativePrompt;
    if (startImageUrl !== undefined) body.start_image_url = startImageUrl;
    return this.transport.request('POST', '/kling/videos', { json: body });
  }

  async motion(opts: {
    mode: 'std' | 'pro';
    imageUrl: string;
    videoUrl: string;
    characterOrientation: 'image' | 'video';
    keepOriginalSound?: 'yes' | 'no';
    prompt?: string;
    callbackUrl?: string;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { mode, imageUrl, videoUrl, characterOrientation, keepOriginalSound, prompt, callbackUrl, ...rest } = opts;
    const body: Record<string, unknown> = {
      mode,
      image_url: imageUrl,
      video_url: videoUrl,
      character_orientation: characterOrientation,
      ...rest,
    };
    if (keepOriginalSound !== undefined) body.keep_original_sound = keepOriginalSound;
    if (prompt !== undefined) body.prompt = prompt;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    return this.transport.request('POST', '/kling/motion', { json: body });
  }
}
