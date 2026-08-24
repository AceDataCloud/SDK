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
  /** Seedance Videos Model */
  model: "doubao-seedance-1-0-pro-250528" | "doubao-seedance-1-0-pro-fast-251015" | "doubao-seedance-1-5-pro-251215" | "doubao-seedance-1-0-lite-t2v-250428" | "doubao-seedance-1-0-lite-i2v-250428" | "doubao-seedance-2-0-260128" | "doubao-seedance-2-0-fast-260128" | "doubao-seedance-2-0-mini-260615" | "doubao-seedance-2-5-260628";
  /** Seedance Videos */
  content: Array<Record<string, unknown>>;
  /** Seedance Videos Resolution */
  resolution?: "480p" | "720p" | "1080p" | "4k";
  /** Seedance Videos Ratio */
  ratio?: "16:9" | "4:3" | "1:1" | "3:4" | "9:16" | "21:9" | "adaptive";
  /** Seedance Videos Duration */
  duration?: number;
  /** Seedance Videos Frames */
  frames?: number;
  /** Seedance Videos Seed */
  seed?: number;
  /** Seedance Videos Camerafixed */
  camerafixed?: boolean;
  /** Seedance Videos Watermark */
  watermark?: boolean;
  /** Seedance Videos Generate Audio */
  generateAudio?: boolean;
  /** Seedance Videos Return Last Frame */
  returnLastFrame?: boolean;
  /** Seedance Videos Execution Expires After */
  executionExpiresAfter?: number;
  /** Seedance Videos Omni Reference Task Type */
  omniReferenceTaskType?: "auto" | "edit" | "extend";
  /** Seedance Videos Output Format */
  outputFormat?: "mp4" | "mov";
  /** Seedance Videos Tools */
  tools?: Array<Record<string, unknown>>;
  /** Seedance Videos Priority */
  priority?: number;
  /** Seedance Videos Safety Identifier */
  safetyIdentifier?: string;
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

  /** Seedance Videos */
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
    body["priority"] = options.priority ?? 0;
    if (options.safetyIdentifier !== undefined) body["safety_identifier"] = options.safetyIdentifier;
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "callbackUrl", "camerafixed", "content", "duration", "executionExpiresAfter", "frames", "generateAudio", "maxWait", "model", "omniReferenceTaskType", "outputFormat", "pollInterval", "priority", "ratio", "resolution", "returnLastFrame", "safetyIdentifier", "seed", "tools", "wait", "watermark"].includes(key) && value !== undefined) {
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
