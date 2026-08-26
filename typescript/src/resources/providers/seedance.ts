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
  /** $t(seedance_videos_model) */
  model: "doubao-seedance-1-0-pro-250528" | "doubao-seedance-1-0-pro-fast-251015" | "doubao-seedance-1-5-pro-251215" | "doubao-seedance-1-0-lite-t2v-250428" | "doubao-seedance-1-0-lite-i2v-250428" | "doubao-seedance-2-0-260128" | "doubao-seedance-2-0-fast-260128" | "doubao-seedance-2-0-mini-260615" | "doubao-seedance-2-5-260628";
  /** $t(seedance_videos) */
  content: Array<Record<string, unknown>>;
  /** $t(seedance_videos_resolution) */
  resolution?: "480p" | "720p" | "1080p" | "4k";
  /** $t(seedance_videos_ratio) */
  ratio?: "16:9" | "4:3" | "1:1" | "3:4" | "9:16" | "21:9" | "adaptive";
  /** $t(seedance_videos_duration) */
  duration?: number;
  /** $t(seedance_videos_frames) */
  frames?: number;
  /** $t(seedance_videos_seed) */
  seed?: number;
  /** $t(seedance_videos_camerafixed) */
  camerafixed?: boolean;
  /** $t(seedance_videos_watermark) */
  watermark?: boolean;
  /** $t(seedance_videos_generate_audio) */
  generateAudio?: boolean;
  /** $t(seedance_videos_return_last_frame) */
  returnLastFrame?: boolean;
  /** $t(seedance_videos_execution_expires_after) */
  executionExpiresAfter?: number;
  /** $t(seedance_videos_omni_reference_task_type) */
  omniReferenceTaskType?: "auto" | "edit" | "extend";
  /** $t(seedance_videos_output_format) */
  outputFormat?: "mp4" | "mov";
  /** $t(seedance_videos_tools) */
  tools?: Array<Record<string, unknown>>;
  /** Submit asynchronously and poll. */
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

  /** Call /seedance/videos. */
  async generate(options: SeedanceGenerateOptions): Promise<TaskHandle> {
    const body: Record<string, unknown> = {};
    body["model"] = options.model;
    body["content"] = options.content;
    if (options.resolution !== undefined) body["resolution"] = options.resolution;
    body["ratio"] = options.ratio ?? "16:9";
    if (options.duration !== undefined) body["duration"] = options.duration;
    if (options.frames !== undefined) body["frames"] = options.frames;
    if (options.seed !== undefined) body["seed"] = options.seed;
    if (options.camerafixed !== undefined) body["camerafixed"] = options.camerafixed;
    if (options.watermark !== undefined) body["watermark"] = options.watermark;
    body["generate_audio"] = options.generateAudio ?? false;
    body["return_last_frame"] = options.returnLastFrame ?? false;
    body["execution_expires_after"] = options.executionExpiresAfter ?? 172800;
    if (options.omniReferenceTaskType !== undefined) body["omni_reference_task_type"] = options.omniReferenceTaskType;
    if (options.outputFormat !== undefined) body["output_format"] = options.outputFormat;
    if (options.tools !== undefined) body["tools"] = options.tools;
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "callbackUrl", "camerafixed", "content", "duration", "executionExpiresAfter", "frames", "generateAudio", "maxWait", "model", "omniReferenceTaskType", "outputFormat", "pollInterval", "ratio", "resolution", "returnLastFrame", "seed", "tools", "wait", "watermark"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    if (options.async !== undefined) body.async = options.async;
    const result = (await this.transport.request('POST', "/seedance/videos", { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), "/seedance/tasks", this.transport, result);
    if (options.wait) {
      await handle.wait({ pollInterval: options.pollInterval, maxWait: options.maxWait });
    }
    return handle;
  }

}
