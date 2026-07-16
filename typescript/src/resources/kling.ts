/** Kling-specific video generation resources. */

import { Transport } from '../runtime/transport';

export const KLING_MODELS = [
  'kling-v1',
  'kling-v1-6',
  'kling-v2-master',
  'kling-v2-1-master',
  'kling-v2-5-turbo',
  'kling-v2-6',
  'kling-v3',
  'kling-v3-omni',
  'kling-o1',
] as const;

export type KlingModel = (typeof KLING_MODELS)[number];

export interface KlingCameraControl {
  type: 'simple' | 'down_back' | 'forward_up' | 'left_turn_forward' | 'right_turn_forward';
  config?: {
    horizontal?: number;
    vertical?: number;
    pan?: number;
    tilt?: number;
    roll?: number;
    zoom?: number;
  };
}

export interface KlingReferenceImage {
  imageUrl: string;
  type?: 'first_frame' | 'end_frame';
}

export interface KlingReferenceVideo {
  videoUrl: string;
  referType?: 'base' | 'feature';
  keepOriginalSound?: 'yes' | 'no';
}

export interface KlingGenerateOptions {
  action: 'text2video' | 'image2video' | 'extend';
  mode?: 'std' | 'pro' | '4k';
  model: KlingModel;
  prompt?: string;
  duration?: number;
  generateAudio?: boolean;
  videoId?: string;
  cfgScale?: number;
  aspectRatio?: '16:9' | '9:16' | '1:1';
  callbackUrl?: string;
  async?: boolean;
  timeout?: number;
  endImageUrl?: string;
  cameraControl?: KlingCameraControl;
  imageList?: KlingReferenceImage[];
  videoList?: KlingReferenceVideo[];
  negativePrompt?: string;
  startImageUrl?: string;
}

function isHttpUrl(value: string): boolean {
  try {
    const url = new URL(value);
    return url.protocol === 'http:' || url.protocol === 'https:';
  } catch {
    return false;
  }
}

function validateGenerateOptions(opts: KlingGenerateOptions): void {
  if (!KLING_MODELS.includes(opts.model)) {
    throw new Error(`model must be one of: ${KLING_MODELS.join(', ')}`);
  }
  const isV3 = opts.model === 'kling-v3' || opts.model === 'kling-v3-omni';
  const hasReferences = Boolean(opts.imageList?.length || opts.videoList?.length);

  if (opts.imageList !== undefined && opts.imageList.length === 0) {
    throw new Error('imageList must be non-empty or omitted');
  }
  if (opts.videoList !== undefined && opts.videoList.length === 0) {
    throw new Error('videoList must be non-empty or omitted');
  }

  if ((opts.action === 'text2video' || opts.action === 'image2video') && !opts.prompt) {
    throw new Error('prompt is required for text2video and image2video');
  }
  if (opts.action === 'image2video' && !opts.startImageUrl) {
    throw new Error('startImageUrl is required for image2video');
  }
  if (opts.action === 'extend' && !opts.videoId) {
    throw new Error('videoId is required for extend');
  }
  if (opts.endImageUrl && !opts.startImageUrl) {
    throw new Error('startImageUrl is required with endImageUrl');
  }
  if (opts.startImageUrl && !isHttpUrl(opts.startImageUrl)) {
    throw new Error('startImageUrl must be an HTTP URL');
  }
  if (opts.endImageUrl && !isHttpUrl(opts.endImageUrl)) {
    throw new Error('endImageUrl must be an HTTP URL');
  }
  if (opts.callbackUrl && !isHttpUrl(opts.callbackUrl)) {
    throw new Error('callbackUrl must be an HTTP URL');
  }
  if (opts.cfgScale !== undefined && (opts.cfgScale < 0 || opts.cfgScale > 1)) {
    throw new Error('cfgScale must be between 0 and 1');
  }
  if (opts.duration !== undefined && !Number.isInteger(opts.duration)) {
    throw new Error('duration must be an integer');
  }
  if (isV3 && opts.duration !== undefined && (opts.duration < 3 || opts.duration > 15)) {
    throw new Error('Kling V3 duration must be between 3 and 15 seconds');
  }
  if (!isV3 && opts.model !== 'kling-o1' && opts.duration !== undefined && ![5, 10].includes(opts.duration)) {
    throw new Error('This Kling model supports only 5- or 10-second generation');
  }
  if (opts.model === 'kling-o1' && opts.duration !== undefined && opts.duration !== 5) {
    throw new Error('kling-o1 supports only 5-second generation');
  }
  if (opts.model === 'kling-o1' && opts.mode !== undefined && !['std', 'pro'].includes(opts.mode)) {
    throw new Error('kling-o1 supports only std and pro modes');
  }
  if (opts.mode === '4k' && !isV3) {
    throw new Error('4k mode requires kling-v3 or kling-v3-omni');
  }
  if (opts.action === 'extend' && !['kling-v1', 'kling-v1-6', 'kling-v2-5-turbo'].includes(opts.model)) {
    throw new Error('extend requires kling-v1, kling-v1-6, or kling-v2-5-turbo');
  }
  if (opts.action === 'extend' && hasReferences) {
    throw new Error('imageList and videoList are not supported with extend');
  }
  if (hasReferences && opts.model !== 'kling-o1' && opts.model !== 'kling-v3-omni') {
    throw new Error('Omni references require kling-o1 or kling-v3-omni');
  }
  if (hasReferences && opts.mode === '4k') {
    throw new Error('4k cannot be combined with Omni references');
  }
  if ((opts.model === 'kling-o1' || hasReferences) && (opts.negativePrompt !== undefined || opts.cameraControl !== undefined || opts.cfgScale !== undefined)) {
    throw new Error('Kling O1 and Omni references do not support negativePrompt, cameraControl, or cfgScale');
  }
  if (opts.model === 'kling-o1' && opts.generateAudio) {
    throw new Error('kling-o1 does not support generateAudio');
  }
  if (opts.generateAudio && !isV3 && opts.model !== 'kling-v2-6') {
    throw new Error('generateAudio requires a V3 model or kling-v2-6 pro mode');
  }
  if (opts.generateAudio && opts.model === 'kling-v2-6' && opts.mode !== 'pro') {
    throw new Error('kling-v2-6 supports generateAudio only in pro mode');
  }
  if (opts.generateAudio && opts.videoList?.length) {
    throw new Error('generateAudio cannot be used with videoList');
  }
  if (opts.videoList && (opts.videoList.length === 0 || opts.videoList.length > 1)) {
    throw new Error('videoList must contain exactly one reference video');
  }

  for (const image of opts.imageList ?? []) {
    if (!isHttpUrl(image.imageUrl)) throw new Error('Every reference image requires an HTTP imageUrl');
    if (image.type !== undefined && !['first_frame', 'end_frame'].includes(image.type)) {
      throw new Error('Reference image type must be first_frame or end_frame');
    }
  }
  for (const video of opts.videoList ?? []) {
    if (!isHttpUrl(video.videoUrl)) throw new Error('Every reference video requires an HTTP videoUrl');
    if (video.referType !== undefined && !['base', 'feature'].includes(video.referType)) {
      throw new Error('Reference video referType must be base or feature');
    }
    if (video.keepOriginalSound !== undefined && !['yes', 'no'].includes(video.keepOriginalSound)) {
      throw new Error('Reference video keepOriginalSound must be yes or no');
    }
  }

  const firstFrames = Number(Boolean(opts.startImageUrl)) + (opts.imageList ?? []).filter((item) => item.type === 'first_frame').length;
  const endFrames = Number(Boolean(opts.endImageUrl)) + (opts.imageList ?? []).filter((item) => item.type === 'end_frame').length;
  if (firstFrames > 1 || endFrames > 1) {
    throw new Error('Only one first frame and one end frame are allowed');
  }
  if (endFrames > 0 && firstFrames === 0) {
    throw new Error('A first frame is required with an end frame');
  }
  if ((opts.videoList?.[0]?.referType ?? 'base') === 'base' && opts.videoList?.length && (firstFrames > 0 || endFrames > 0)) {
    throw new Error('A base reference video cannot be combined with first or end frames');
  }

  const imageCount = (opts.imageList?.length ?? 0) + Number(Boolean(opts.startImageUrl)) + Number(Boolean(opts.endImageUrl));
  const imageLimit = opts.videoList?.length ? 4 : 7;
  if (imageCount > imageLimit) {
    throw new Error(`Reference images cannot exceed ${imageLimit} for this request`);
  }
}

export class Kling {
  constructor(private transport: Transport) {}

  async generate(opts: KlingGenerateOptions): Promise<Record<string, unknown>> {
    validateGenerateOptions(opts);
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
      async: asyncMode,
      timeout,
      endImageUrl,
      cameraControl,
      imageList,
      videoList,
      negativePrompt,
      startImageUrl,
    } = opts;
    const body: Record<string, unknown> = { action };
    if (mode !== undefined) body.mode = mode;
    if (model !== undefined) body.model = model;
    if (prompt !== undefined) body.prompt = prompt;
    if (duration !== undefined) body.duration = duration;
    if (generateAudio !== undefined) body.generate_audio = generateAudio;
    if (videoId !== undefined) body.video_id = videoId;
    if (cfgScale !== undefined) body.cfg_scale = cfgScale;
    if (aspectRatio !== undefined) body.aspect_ratio = aspectRatio;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    if (asyncMode !== undefined) body.async = asyncMode;
    if (timeout !== undefined) body.timeout = timeout;
    if (endImageUrl !== undefined) body.end_image_url = endImageUrl;
    if (cameraControl !== undefined) body.camera_control = cameraControl;
    if (imageList !== undefined) {
      body.image_list = imageList.map(({ imageUrl, type }) => ({ image_url: imageUrl, ...(type ? { type } : {}) }));
    }
    if (videoList !== undefined) {
      body.video_list = videoList.map(({ videoUrl, referType, keepOriginalSound }) => ({
        video_url: videoUrl,
        ...(referType ? { refer_type: referType } : {}),
        ...(keepOriginalSound ? { keep_original_sound: keepOriginalSound } : {}),
      }));
    }
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
    async?: boolean;
  }): Promise<Record<string, unknown>> {
    const { mode, imageUrl, videoUrl, characterOrientation, keepOriginalSound, prompt, callbackUrl } = opts;
    if (!['std', 'pro'].includes(mode)) throw new Error('mode must be std or pro');
    if (!isHttpUrl(imageUrl)) throw new Error('imageUrl must be an HTTP URL');
    if (!isHttpUrl(videoUrl)) throw new Error('videoUrl must be an HTTP URL');
    if (!['image', 'video'].includes(characterOrientation)) {
      throw new Error('characterOrientation must be image or video');
    }
    if (keepOriginalSound !== undefined && !['yes', 'no'].includes(keepOriginalSound)) {
      throw new Error('keepOriginalSound must be yes or no');
    }
    if (callbackUrl && !isHttpUrl(callbackUrl)) throw new Error('callbackUrl must be an HTTP URL');
    const body: Record<string, unknown> = {
      mode,
      image_url: imageUrl,
      video_url: videoUrl,
      character_orientation: characterOrientation,
    };
    if (keepOriginalSound !== undefined) body.keep_original_sound = keepOriginalSound;
    if (prompt !== undefined) body.prompt = prompt;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    if (opts.async !== undefined) body.async = opts.async;
    return this.transport.request('POST', '/kling/motion', { json: body });
  }
}
