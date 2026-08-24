/**
 * Producer (producer) — generated from the platform OpenAPI spec.
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

export interface ProducerUploadOptions {
  /** Producer Upload Audio Url */
  audioUrl: string;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

export interface ProducerVideosOptions {
  /** Producer Videos Audio Id */
  audioId: string;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

export interface ProducerWavOptions {
  /** Producer Wav Audio Id */
  audioId: string;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

export interface ProducerGenerateOptions {
  /** Producer Audios Lyric */
  lyric: string;
  /** Producer Audios Action */
  action: "generate" | "cover" | "extend" | "variation" | "swap_vocals" | "swap_instrumentals" | "replace_section" | "stems";
  /** Producer Audios Prompt */
  prompt: string;
  /** Producer Audios Model */
  model?: "FUZZ-2.0 Pro" | "FUZZ-2.0" | "FUZZ-2.0 Raw" | "FUZZ-1.1 Pro" | "FUZZ-1.0 Pro" | "FUZZ-1.0" | "FUZZ-1.1" | "FUZZ-0.8";
  /** Producer Audios Title */
  title?: string;
  /** Producer Audios Custom */
  custom?: boolean;
  /** Producer Audios Audio Id */
  audioId?: string;
  /** Producer Audios Continue At */
  continueAt?: number;
  /** Producer Audios Seed */
  seed?: string;
  /** Producer Audios Instrumental */
  instrumental?: boolean;
  /** Producer Audios Sound Strength */
  soundStrength?: number;
  /** Producer Audios Lyrics Strength */
  lyricsStrength?: number;
  /** Producer Audios Weirdness */
  weirdness?: number;
  /** Producer Audios Replace Section End */
  replaceSectionEnd?: number;
  /** Producer Audios Replace Section Start */
  replaceSectionStart?: number;
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

export interface ProducerLyricsOptions {
  /** Producer Lyrics Prompt */
  prompt: string;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

/** producer client. */
export class Producer {
  constructor(private transport: Transport) {}

  /** Producer Upload */
  async upload(options: ProducerUploadOptions): Promise<Record<string, unknown>> {
    const body: Record<string, unknown> = {};
    body["audio_url"] = options.audioUrl;
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "audioUrl", "callbackUrl", "maxWait", "pollInterval", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    return (await this.transport.request('POST', "/producer/upload", { json: body })) as Record<string, unknown>;
  }

  /** Producer Videos */
  async videos(options: ProducerVideosOptions): Promise<Record<string, unknown>> {
    const body: Record<string, unknown> = {};
    body["audio_id"] = options.audioId;
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "audioId", "callbackUrl", "maxWait", "pollInterval", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    return (await this.transport.request('POST', "/producer/videos", { json: body })) as Record<string, unknown>;
  }

  /** Producer Wav */
  async wav(options: ProducerWavOptions): Promise<Record<string, unknown>> {
    const body: Record<string, unknown> = {};
    body["audio_id"] = options.audioId;
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "audioId", "callbackUrl", "maxWait", "pollInterval", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    return (await this.transport.request('POST', "/producer/wav", { json: body })) as Record<string, unknown>;
  }

  /** Producer Audios */
  async generate(options: ProducerGenerateOptions): Promise<TaskHandle> {
    const body: Record<string, unknown> = {};
    body["lyric"] = options.lyric;
    body["action"] = options.action;
    body["prompt"] = options.prompt;
    if (options.model !== undefined) body["model"] = options.model;
    if (options.title !== undefined) body["title"] = options.title;
    if (options.custom !== undefined) body["custom"] = options.custom;
    if (options.audioId !== undefined) body["audio_id"] = options.audioId;
    body["continue_at"] = options.continueAt ?? false;
    if (options.seed !== undefined) body["seed"] = options.seed;
    body["instrumental"] = options.instrumental ?? false;
    body["sound_strength"] = options.soundStrength ?? false;
    body["lyrics_strength"] = options.lyricsStrength ?? false;
    body["weirdness"] = options.weirdness ?? false;
    body["replace_section_end"] = options.replaceSectionEnd ?? false;
    body["replace_section_start"] = options.replaceSectionStart ?? false;
    for (const [key, value] of Object.entries(options)) {
      if (!["action", "async", "audioId", "callbackUrl", "continueAt", "custom", "instrumental", "lyric", "lyricsStrength", "maxWait", "model", "pollInterval", "prompt", "replaceSectionEnd", "replaceSectionStart", "seed", "soundStrength", "title", "wait", "weirdness"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    body.async = options.async ?? true;
    const result = (await this.transport.request('POST', "/producer/audios", { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), "/producer/tasks", this.transport, result);
    if (options.wait) {
      await handle.wait({ pollInterval: options.pollInterval, maxWait: options.maxWait });
    }
    return handle;
  }

  /** Producer Lyrics */
  async lyrics(options: ProducerLyricsOptions): Promise<Record<string, unknown>> {
    const body: Record<string, unknown> = {};
    body["prompt"] = options.prompt;
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "callbackUrl", "maxWait", "pollInterval", "prompt", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    return (await this.transport.request('POST', "/producer/lyrics", { json: body })) as Record<string, unknown>;
  }

}
