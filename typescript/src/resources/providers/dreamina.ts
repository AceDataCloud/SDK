/**
 * Dreamina (dreamina) — generated from the platform OpenAPI spec.
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

export interface DreaminaGenerateOptions {
  /** Public URL for audio (mp3/wav). The character will lip-sync to it, and it is recommended that the duration be controlled within 60 seconds. */
  audioUrl: string;
  /** Public URL of portrait images. Clear frontal face effects are best. */
  imageUrl: string;
  /** The model being used is OmniHuman 1.5. */
  model?: "omnihuman-1.5";
  /** Optional text prompts for guiding expressions, emotions, stability, and style. */
  prompt?: string;
  /** Optional subject mask URL (from object detection) to specify and drive a particular person in a multi-person image. */
  maskUrl?: string[];
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

/** dreamina client. */
export class Dreamina {
  constructor(private transport: Transport) {}

  /** Audio-driven talking-photo digital human video generation (OmniHuman 1.5) */
  async generate(options: DreaminaGenerateOptions): Promise<TaskHandle> {
    const body: Record<string, unknown> = {};
    body["audio_url"] = options.audioUrl;
    body["image_url"] = options.imageUrl;
    body["model"] = options.model ?? "omnihuman-1.5";
    if (options.prompt !== undefined) body["prompt"] = options.prompt;
    if (options.maskUrl !== undefined) body["mask_url"] = options.maskUrl;
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "audioUrl", "callbackUrl", "imageUrl", "maskUrl", "maxWait", "model", "pollInterval", "prompt", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    body.async = options.async ?? true;
    const result = (await this.transport.request('POST', "/dreamina/videos", { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), "/dreamina/tasks", this.transport, result);
    if (options.wait) {
      await handle.wait({ pollInterval: options.pollInterval, maxWait: options.maxWait });
    }
    return handle;
  }

}
