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
  /** Public URL of the source face video (preferred). One of video_url/image_url required. */
  videoUrl: string;
  /** Spoken text -> TTS (requires voice_id). */
  text?: string;
  /** Audio tempo multiplier. */
  speed?: number;
  /** Diffusion steps (LatentSync). */
  steps?: number;
  /** latentsync = quality (default); heygem = fast tier. */
  engine?: "latentsync" | "heygem";
  /** Lip-sync strength (LatentSync). Lower loosens sync. */
  guidance?: number;
  /** Apply the mouth-seam reduction blend. */
  seamFix?: boolean;
  /** A cloned voice from POST /digital-human/voices. */
  voiceId?: string;
  /** Public URL of the driving audio (.wav/.mp3/.m4a). OR supply text(+voice_id). */
  audioUrl?: string;
  /** Public URL of a source face photo (photo-driven path). */
  imageUrl?: string;
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

  /** Digital Human video generation API — turn a portrait plus audio or text into a talking-head video. */
  async generate(options: DigitalhumanGenerateOptions): Promise<TaskHandle> {
    const body: Record<string, unknown> = {};
    body["video_url"] = options.videoUrl;
    body["text"] = options.text ?? "\u5927\u5bb6\u597d\uff0c\u8fd9\u662f\u79bb\u7ebf\u751f\u6210\u7684\u6570\u5b57\u4eba\u3002";
    body["speed"] = options.speed ?? 1.0;
    body["steps"] = options.steps ?? 40;
    body["engine"] = options.engine ?? "latentsync";
    body["guidance"] = options.guidance ?? 2.0;
    body["seam_fix"] = options.seamFix ?? true;
    if (options.voiceId !== undefined) body["voice_id"] = options.voiceId;
    if (options.audioUrl !== undefined) body["audio_url"] = options.audioUrl;
    if (options.imageUrl !== undefined) body["image_url"] = options.imageUrl;
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

  /** Digital Human voice-clone API — upload an audio sample to clone a custom voice for speech synthesis. */
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
