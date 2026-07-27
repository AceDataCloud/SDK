/**
 * Seedance (seedance) — generated from the platform OpenAPI spec.
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

export interface SeedanceGenerateOptions {
  /** Model ID for video generation */
  model: "doubao-seedance-1-0-pro-250528" | "doubao-seedance-1-0-pro-fast-251015" | "doubao-seedance-1-5-pro-251215" | "doubao-seedance-1-0-lite-t2v-250428" | "doubao-seedance-1-0-lite-i2v-250428" | "doubao-seedance-2-0-260128" | "doubao-seedance-2-0-fast-260128" | "doubao-seedance-2-0-mini-260615";
  /** Input content for video generation. Each entry must include one of `text`, `image_url`, `audio_url`, or `video_url` corresponding to the `type`. The meaning of other fields and whether they are required depends on the value of `type`. */
  content: unknown[];
  /** The random seed used for reproducible generation has a value range from -1 to 4294967295; -1 indicates randomness. */
  seed?: number;
  /** Aspect ratio of the generated video */
  ratio?: "16:9" | "4:3" | "1:1" | "3:4" | "9:16" | "21:9" | "adaptive";
  /** The frame count for generating a video must meet 25 + 4n (such as 29, 33, 37... 361). Either duration or frames can be specified; if both are specified, frames take priority over duration. */
  frames?: number;
  /** The duration of the generated video, in seconds. Either duration or frames can be specified; if both are specified, frames take priority over duration. The duration range varies for each model: Seedance 2.0 series is 4 to 15 seconds or -1, Seedance 1.5 Pro is 4 to 12 seconds or -1, and Seedance 1.0 series is 2 to 12 seconds. -1 indicates automatic duration. */
  duration?: number;
  /** Whether to add a watermark to the generated video. */
  watermark?: boolean;
  /** Video resolution. The default value depends on the model used: most models default to 720p, while the lite model defaults to 480p. Note that the supported resolutions vary by model: `4k` is only supported by doubao-seedance-2-0 (standard version); doubao-seedance-2-0-fast and doubao-seedance-2-0-mini do not support 1080p and 4k. */
  resolution?: "480p" | "720p" | "1080p" | "4k";
  /** Is the camera position fixed during the generation process? */
  camerafixed?: boolean;
  /** Whether to generate audio from video. The `doubao-seedance-1-5-pro-251215` and `doubao-seedance-2-0` series models support this parameter, while other models will ignore this parameter. */
  generateAudio?: boolean;
  /** Whether to return the last frame of the generated video. */
  returnLastFrame?: boolean;
  /** Task timeout threshold, unit in seconds */
  executionExpiresAfter?: number;
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

/** seedance client. */
export class Seedance {
  constructor(private transport: Transport) {}

  /** ByteDance Seedance video generation API. Supports doubao-seedance-1-0-pro-250528, doubao-seedance-1-0-pro-fast-251015, doubao-seedance-1-5-pro-251215, doubao-seedance-1-0-lite-t2v-250428, and doubao-s */
  async generate(options: SeedanceGenerateOptions): Promise<TaskHandle> {
    const body: Record<string, unknown> = {};
    body["model"] = options.model;
    body["content"] = options.content;
    if (options.seed !== undefined) body["seed"] = options.seed;
    body["ratio"] = options.ratio ?? "16:9";
    if (options.frames !== undefined) body["frames"] = options.frames;
    if (options.duration !== undefined) body["duration"] = options.duration;
    if (options.watermark !== undefined) body["watermark"] = options.watermark;
    if (options.resolution !== undefined) body["resolution"] = options.resolution;
    if (options.camerafixed !== undefined) body["camerafixed"] = options.camerafixed;
    body["generate_audio"] = options.generateAudio ?? false;
    body["return_last_frame"] = options.returnLastFrame ?? false;
    body["execution_expires_after"] = options.executionExpiresAfter ?? 172800;
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "callbackUrl", "camerafixed", "content", "duration", "executionExpiresAfter", "frames", "generateAudio", "maxWait", "model", "pollInterval", "ratio", "resolution", "returnLastFrame", "seed", "wait", "watermark"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    body.async = options.async ?? true;
    const result = (await this.transport.request('POST', "/seedance/videos", { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), "/seedance/tasks", this.transport, result);
    if (options.wait) {
      await handle.wait({ pollInterval: options.pollInterval, maxWait: options.maxWait });
    }
    return handle;
  }

}
