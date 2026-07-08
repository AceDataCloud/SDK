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

export type KlingMotionModel = 'kling-v2-6' | 'kling-v3' | (string & {});

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
    cfgScale?: string | number;
    aspectRatio?: '16:9' | '9:16' | '1:1';
    callbackUrl?: string;
    async?: boolean;
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
    modelName?: KlingMotionModel;
    mode: 'std' | 'pro';
    watermarkInfo?: { enabled?: boolean; [key: string]: unknown };
    imageUrl: string;
    videoUrl: string;
    characterOrientation: 'image' | 'video';
    keepOriginalSound?: 'yes' | 'no';
    prompt?: string;
    callbackUrl?: string;
    async?: boolean;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { modelName, mode, watermarkInfo, imageUrl, videoUrl, characterOrientation, keepOriginalSound, prompt, callbackUrl, ...rest } = opts;
    const body: Record<string, unknown> = {
      mode,
      image_url: imageUrl,
      video_url: videoUrl,
      character_orientation: characterOrientation,
      ...rest,
    };
    if (modelName !== undefined) body.model_name = modelName;
    if (watermarkInfo !== undefined) body.watermark_info = watermarkInfo;
    if (keepOriginalSound !== undefined) body.keep_original_sound = keepOriginalSound;
    if (prompt !== undefined) body.prompt = prompt;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    return this.transport.request('POST', '/kling/motion', { json: body });
  }

  async lipSync(opts: {
    videoId?: string;
    videoUrl?: string;
    mode: 'audio2video' | 'text2video';
    audioUrl?: string;
    audioType?: 'url' | 'file';
    audioFile?: string;
    text?: string;
    voiceId?: string;
    voiceLanguage?: 'zh' | 'en';
    voiceSpeed?: number;
    callbackUrl?: string;
    async?: boolean;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { videoId, videoUrl, mode, audioUrl, audioType, audioFile, text, voiceId, voiceLanguage, voiceSpeed, callbackUrl, ...rest } = opts;
    const body: Record<string, unknown> = { mode, ...rest };
    if (videoId !== undefined) body.video_id = videoId;
    if (videoUrl !== undefined) body.video_url = videoUrl;
    if (audioUrl !== undefined) body.audio_url = audioUrl;
    if (audioType !== undefined) body.audio_type = audioType;
    if (audioFile !== undefined) body.audio_file = audioFile;
    if (text !== undefined) body.text = text;
    if (voiceId !== undefined) body.voice_id = voiceId;
    if (voiceLanguage !== undefined) body.voice_language = voiceLanguage;
    if (voiceSpeed !== undefined) body.voice_speed = voiceSpeed;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    return this.transport.request('POST', '/kling/lip-sync', { json: body });
  }

  async talkingPhoto(opts: {
    imageUrl: string;
    audioUrl: string;
    prompt?: string;
    model?: KlingModel;
    duration?: 5 | 10;
    mode?: 'std' | 'pro';
    callbackUrl?: string;
    async?: boolean;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { imageUrl, audioUrl, prompt, model, duration, mode, callbackUrl, ...rest } = opts;
    const body: Record<string, unknown> = {
      image_url: imageUrl,
      audio_url: audioUrl,
      ...rest,
    };
    if (prompt !== undefined) body.prompt = prompt;
    if (model !== undefined) body.model = model;
    if (duration !== undefined) body.duration = duration;
    if (mode !== undefined) body.mode = mode;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    return this.transport.request('POST', '/kling/talking-photo', { json: body });
  }
}
