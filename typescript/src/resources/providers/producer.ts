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
  /** The CDN address for the custom audio files to be uploaded. */
  audioUrl: string;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

export interface ProducerGenerateOptions {
  /** Reference audio ID. */
  audioId: string;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

export interface ProducerWavOptions {
  /** Reference audio ID. */
  audioId: string;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

export interface ProducerProducerAudiosOptions {
  /** Lyrics content for generating audio. */
  lyric: string;
  /** Types of audio generation operations. Supported values include `generate` (generate based on prompts), `cover` (cover song), `extend` (continue writing), `variation` (variant), `swap_vocals` (replace vocals), `swap_instrumentals` (replace instrumentals), `replace_section` (replace section), `stems` (separate tracks). */
  action: "generate" | "cover" | "extend" | "variation" | "swap_vocals" | "swap_instrumentals" | "replace_section" | "stems";
  /** Prompts for generating audio should not exceed 200 characters in length. */
  prompt: string;
  /** Random seed used for audio generation. */
  seed?: string;
  /** The model used for generating music is `FUZZ-2.0` by default. */
  model?: "FUZZ-2.0 Pro" | "FUZZ-2.0" | "FUZZ-2.0 Raw" | "FUZZ-1.1 Pro" | "FUZZ-1.0 Pro" | "FUZZ-1.0" | "FUZZ-1.1" | "FUZZ-0.8";
  /** Title used for generating songs. */
  title?: string;
  /** Is it a custom mode? If `true`, the audio will be generated based on the `lyric`; otherwise, it will be generated based on the `prompt`. */
  custom?: boolean;
  /** The unique ID of the reference song. */
  audioId?: string;
  /** The degree of uniqueness of style can be selected between 0 and 1, with a default value of 0.5. */
  weirdness?: number;
  /** Specify the time point (in seconds) from which to continue writing the song. */
  continueAt?: number;
  /** If `true`, the generated audio will only contain the accompaniment, without vocal lyrics. */
  instrumental?: boolean;
  /** The impact intensity of the audio prompt words can be selected between 0.2 and 1, with a default value of 0.5. */
  soundStrength?: number;
  /** The degree of influence of lyrics on audio generation can be selected between 0 and 1, with a default value of 0.5. */
  lyricsStrength?: number;
  /** Replace the end time point of the segment (seconds). */
  replaceSectionEnd?: number;
  /** Replace the starting time point of the segment (seconds). */
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
  /** Prompts for generating lyrics. */
  prompt: Record<string, unknown>;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

/** producer client. */
export class Producer {
  constructor(private transport: Transport) {}

  /** Producer reference audio upload API, upload audio to get an audio_id for generation. */
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

  /** AceData Producer MP4 retrieval API. Pass an audio_id to receive an MP4 video download link with cover art. */
  async generate(options: ProducerGenerateOptions): Promise<Record<string, unknown>> {
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

  /** AceData Producer WAV (lossless) retrieval API. Pass an audio_id to receive a WAV-format download link. */
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

  /** Producer AI music generation API, generates 1 song per request. */
  async producer_audios(options: ProducerProducerAudiosOptions): Promise<TaskHandle> {
    const body: Record<string, unknown> = {};
    body["lyric"] = options.lyric;
    body["action"] = options.action;
    body["prompt"] = options.prompt;
    if (options.seed !== undefined) body["seed"] = options.seed;
    if (options.model !== undefined) body["model"] = options.model;
    if (options.title !== undefined) body["title"] = options.title;
    if (options.custom !== undefined) body["custom"] = options.custom;
    if (options.audioId !== undefined) body["audio_id"] = options.audioId;
    body["weirdness"] = options.weirdness ?? false;
    body["continue_at"] = options.continueAt ?? false;
    body["instrumental"] = options.instrumental ?? false;
    body["sound_strength"] = options.soundStrength ?? false;
    body["lyrics_strength"] = options.lyricsStrength ?? false;
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

  /** Producer AI lyrics generation API, input a prompt to generate lyrics. */
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
