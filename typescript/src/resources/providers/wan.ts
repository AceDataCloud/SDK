/**
 * Wan (wan) — generated from the platform OpenAPI spec.
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

export interface WanGenerateOptions {
  /** Models for generating videos include optional values such as `wan2.6-t2v` (text-to-video), `wan2.6-i2v` (image-to-video), `wan2.6-i2v-flash` (fast version of image-to-video), and `wan2.6-r2v` (reference video generation). */
  model: "wan2.6-i2v" | "wan2.6-r2v" | "wan2.6-i2v-flash" | "wan2.6-t2v";
  /** Operation types. `text2video` indicates text-to-video, and `image2video` indicates image-to-video. */
  action: "text2video" | "image2video";
  /** Prompts for generating videos. */
  prompt: string;
  /** Video size specifications. */
  size?: string;
  /** Specify whether the generated video contains sound. */
  audio?: boolean;
  /** Specify the duration of the video to be generated (in seconds), with optional values of `5`, `10`, or `15`. */
  duration?: number;
  /** The URL of the audio file, the model will generate the corresponding video based on that audio. */
  audioUrl?: string;
  /** The URL of the starting frame image, which will serve as the first frame of the generated video. */
  imageUrl?: string;
  /** Specify the type of shots for the video, that is, whether the video consists of a single continuous shot (`single`) or multiple switching shots (`multi`). */
  shotType?: "single" | "multi";
  /** Specify the resolution level for generating the video, used to adjust the video clarity (total pixel count). The model will automatically scale to a similar total pixel count based on the selected resolution level, and the aspect ratio of the generated video will strive to remain consistent with the aspect ratio of the input image `image_url`. */
  resolution?: "480P" | "720P" | "1080P";
  /** Whether to enable intelligent rewriting of prompts. Once enabled, a large model will be used to intelligently expand the input prompts, which can significantly improve the generation effect of shorter prompts, but will increase processing time. */
  promptExtend?: boolean;
  /** Reverse prompt words, used to describe content that is not desired to appear in the video footage, can be used to limit the video visuals. Supports both Chinese and English, with a length not exceeding 500 characters; any excess will be automatically truncated. */
  negativePrompt?: string;
  /** An array of URLs for reference video files, used to extract the character images (and vocal tones, if any) from the reference videos to generate videos that match the reference features. */
  referenceVideoUrls?: string[];
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

/** wan client. */
export class Wan {
  constructor(private transport: Transport) {}

  /** Generate videos based on prompt and image frames */
  async generate(options: WanGenerateOptions): Promise<TaskHandle> {
    const body: Record<string, unknown> = {};
    body["model"] = options.model;
    body["action"] = options.action;
    body["prompt"] = options.prompt;
    if (options.size !== undefined) body["size"] = options.size;
    body["audio"] = options.audio ?? false;
    if (options.duration !== undefined) body["duration"] = options.duration;
    if (options.audioUrl !== undefined) body["audio_url"] = options.audioUrl;
    if (options.imageUrl !== undefined) body["image_url"] = options.imageUrl;
    if (options.shotType !== undefined) body["shot_type"] = options.shotType;
    if (options.resolution !== undefined) body["resolution"] = options.resolution;
    body["prompt_extend"] = options.promptExtend ?? false;
    if (options.negativePrompt !== undefined) body["negative_prompt"] = options.negativePrompt;
    if (options.referenceVideoUrls !== undefined) body["reference_video_urls"] = options.referenceVideoUrls;
    for (const [key, value] of Object.entries(options)) {
      if (!["action", "async", "audio", "audioUrl", "callbackUrl", "duration", "imageUrl", "maxWait", "model", "negativePrompt", "pollInterval", "prompt", "promptExtend", "referenceVideoUrls", "resolution", "shotType", "size", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    body.async = options.async ?? true;
    const result = (await this.transport.request('POST', "/wan/videos", { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), "/wan/tasks", this.transport, result);
    if (options.wait) {
      await handle.wait({ pollInterval: options.pollInterval, maxWait: options.maxWait });
    }
    return handle;
  }

}
