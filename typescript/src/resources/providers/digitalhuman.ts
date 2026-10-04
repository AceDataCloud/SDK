/**
 * Digitalhuman (digitalhuman) — generated from the platform OpenAPI spec.
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

export interface DigitalhumanGenerateOptions {
  /** Public URL of the source face video (preferred). Supply either video_url or image_url. */
  videoUrl?: string;
  /** Public URL of a source face photo (photo-driven path). Supply either video_url or image_url. */
  imageUrl?: string;
  /** Public URL of the driving audio (.wav/.mp3/.m4a). OR supply text(+voice_id). */
  audioUrl?: string;
  /** Spoken text -> TTS (requires voice_id). */
  text?: string;
  /** A cloned voice from POST /digital-human/voices. */
  voiceId?: string;
  /** [Deprecated] Accepted for backward compatibility but no longer changes the output or the price — every request is billed at the unified rate. */
  engine?: "latentsync" | "heygem";
  /** Lip-sync strength (LatentSync). Lower loosens sync. */
  guidance?: number;
  /** Diffusion steps (LatentSync). */
  steps?: number;
  /** Apply the mouth-seam reduction blend. */
  seamFix?: boolean;
  /** Audio tempo multiplier. */
  speed?: number;
  /** [Deprecated] Output is always rendered at 720p. */
  resolution?: "720p" | "540p";
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

export interface DigitalhumanVoicesOptions {
  /** Public URL of a clean 10-20s voice sample. */
  audioUrl: string;
  lang?: "zh" | "en";
  /** Optional label. */
  name?: string;
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

/** digitalhuman client. */
export class Digitalhuman {
  constructor(private transport: Transport) {}

  /** Digital Human Videos */
  async generate(options: DigitalhumanGenerateOptions = {}): Promise<TaskHandle> {
    const body: Record<string, unknown> = {};
    if (options.videoUrl !== undefined) body["video_url"] = options.videoUrl;
    if (options.imageUrl !== undefined) body["image_url"] = options.imageUrl;
    if (options.audioUrl !== undefined) body["audio_url"] = options.audioUrl;
    if (options.text !== undefined) body["text"] = options.text;
    if (options.voiceId !== undefined) body["voice_id"] = options.voiceId;
    body["engine"] = options.engine ?? "latentsync";
    body["guidance"] = options.guidance ?? 2.0;
    body["steps"] = options.steps ?? 40;
    body["seam_fix"] = options.seamFix ?? true;
    body["speed"] = options.speed ?? 1.0;
    body["resolution"] = options.resolution ?? "720p";
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "audioUrl", "callbackUrl", "engine", "guidance", "imageUrl", "maxWait", "pollInterval", "resolution", "seamFix", "speed", "steps", "text", "videoUrl", "voiceId", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    body.async = options.async ?? true;
    const result = (await this.transport.request('POST', "/digital-human/videos", { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), "/digital-human/tasks", this.transport, result);
    if (options.wait) {
      await handle.wait({ pollInterval: options.pollInterval, maxWait: options.maxWait });
    }
    return handle;
  }

  /** Digital Human Voices */
  async voices(options: DigitalhumanVoicesOptions): Promise<TaskHandle> {
    const body: Record<string, unknown> = {};
    body["audio_url"] = options.audioUrl;
    body["lang"] = options.lang ?? "zh";
    if (options.name !== undefined) body["name"] = options.name;
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "audioUrl", "callbackUrl", "lang", "maxWait", "name", "pollInterval", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    body.async = options.async ?? true;
    const result = (await this.transport.request('POST', "/digital-human/voices", { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), "/digital-human/tasks", this.transport, result);
    if (options.wait) {
      await handle.wait({ pollInterval: options.pollInterval, maxWait: options.maxWait });
    }
    return handle;
  }

}
