/**
 * Suno (suno) — generated from the platform OpenAPI spec.
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

export interface SunoGenerateOptions {
  /** Suno Audios Lyric */
  lyric?: string;
  /** Suno Audios Model */
  model?: "chirp-v5-5" | "chirp-v5" | "chirp-v4-5-plus" | "chirp-v4-5" | "chirp-v4" | "chirp-v3-5" | "chirp-v3-0";
  /** Suno Audios Style */
  style?: string;
  /** Suno Audios Variation Category */
  variationCategory?: string;
  /** Suno Audios Title */
  title?: string;
  /** Suno Audios Action */
  action?: "generate" | "extend" | "upload_extend" | "upload_cover" | "concat" | "cover" | "artist_consistency" | "artist_consistency_vox" | "stems" | "all_stems" | "replace_section" | "underpainting" | "overpainting" | "remaster" | "mashup" | "samples" | "inspo";
  /** Suno Audios Custom */
  custom?: boolean;
  /** Suno Audios Prompt */
  prompt?: string;
  /** Suno Audios Lyric Prompt */
  lyricPrompt?: string;
  /** Suno Audios Audio Id */
  audioId?: string;
  /** Suno Audios Mashup Audio Ids */
  mashupAudioIds?: string[];
  /** Suno Audios Audio Urls */
  audioUrls?: string[];
  /** Suno Audios Weirdness */
  weirdness?: number;
  /** Suno Audios Persona Id */
  personaId?: string;
  /** Suno Audios Overpainting Start */
  overpaintingStart?: number;
  /** Suno Audios Overpainting End */
  overpaintingEnd?: number;
  /** Suno Audios Samples Start */
  samplesStart?: number;
  /** Suno Audios Samples End */
  samplesEnd?: number;
  /** Suno Audios Underpainting Start */
  underpaintingStart?: number;
  /** Suno Audios Underpainting End */
  underpaintingEnd?: number;
  /** Suno Audios Continue At */
  continueAt?: number;
  /** Suno Audios Instrumental */
  instrumental?: boolean;
  /** Suno Audios Vocal Gender */
  vocalGender?: string;
  /** Suno Audios Negative Tags */
  negativeTags?: string;
  /** Suno Audios Style Influence */
  styleInfluence?: number;
  /** Suno Audios Audio Weight */
  audioWeight?: number;
  /** Suno Audios Duration */
  duration?: number;
  /** Suno Audios Replace Section End */
  replaceSectionEnd?: number;
  /** Suno Audios Replace Section Start */
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

export interface SunoPersonaOptions {
  /** Suno Persona Name */
  name: string;
  /** Suno Persona Audio Id */
  audioId: string;
  /** Suno Persona Vox Audio Id */
  voxAudioId?: string;
  /** Suno Persona Vocal Start */
  vocalStart?: number;
  /** Suno Persona Vocal End */
  vocalEnd?: number;
  /** Suno Persona Description */
  description?: string;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

export interface SunoMp4Options {
  /** Suno Mp4 Audio Id */
  audioId: string;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

export interface SunoVoicesOptions {
  /** Suno Voices Audio Url */
  audioUrl: string;
  /** Suno Voices Name */
  name?: string;
  /** Suno Voices Description */
  description?: string;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

export interface SunoTimingOptions {
  /** Suno Timing Audio Id */
  audioId: string;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

export interface SunoVoxOptions {
  /** Suno Vox Audio Id */
  audioId: string;
  /** Suno Vox Vocal Start */
  vocalStart: number;
  /** Suno Vox Vocal End */
  vocalEnd: number;
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

export interface SunoWavOptions {
  /** Suno Wav Audio Id */
  audioId: string;
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

export interface SunoMidiOptions {
  /** Suno Midi Audio Id */
  audioId: string;
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

export interface SunoStyleOptions {
  /** Suno Style Prompt */
  prompt: string;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

export interface SunoLyricsOptions {
  /** Suno Lyrics Model */
  model: "default" | "remi-v1";
  /** Suno Lyrics Prompt */
  prompt: string;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

export interface SunoMashupLyricsOptions {
  /** Suno Mashup Lyrics Lyrics A */
  lyricsA: string;
  /** Suno Mashup Lyrics Lyrics B */
  lyricsB: string;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

export interface SunoUploadOptions {
  /** Suno Upload Audio Url */
  audioUrl: string;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

/** suno client. */
export class Suno {
  constructor(private transport: Transport) {}

  /** Suno Audios */
  async generate(options: SunoGenerateOptions = {}): Promise<TaskHandle> {
    const body: Record<string, unknown> = {};
    if (options.lyric !== undefined) body["lyric"] = options.lyric;
    if (options.model !== undefined) body["model"] = options.model;
    if (options.style !== undefined) body["style"] = options.style;
    if (options.variationCategory !== undefined) body["variation_category"] = options.variationCategory;
    if (options.title !== undefined) body["title"] = options.title;
    if (options.action !== undefined) body["action"] = options.action;
    if (options.custom !== undefined) body["custom"] = options.custom;
    if (options.prompt !== undefined) body["prompt"] = options.prompt;
    if (options.lyricPrompt !== undefined) body["lyric_prompt"] = options.lyricPrompt;
    if (options.audioId !== undefined) body["audio_id"] = options.audioId;
    if (options.mashupAudioIds !== undefined) body["mashup_audio_ids"] = options.mashupAudioIds;
    if (options.audioUrls !== undefined) body["audio_urls"] = options.audioUrls;
    if (options.weirdness !== undefined) body["weirdness"] = options.weirdness;
    if (options.personaId !== undefined) body["persona_id"] = options.personaId;
    if (options.overpaintingStart !== undefined) body["overpainting_start"] = options.overpaintingStart;
    if (options.overpaintingEnd !== undefined) body["overpainting_end"] = options.overpaintingEnd;
    if (options.samplesStart !== undefined) body["samples_start"] = options.samplesStart;
    if (options.samplesEnd !== undefined) body["samples_end"] = options.samplesEnd;
    if (options.underpaintingStart !== undefined) body["underpainting_start"] = options.underpaintingStart;
    if (options.underpaintingEnd !== undefined) body["underpainting_end"] = options.underpaintingEnd;
    if (options.continueAt !== undefined) body["continue_at"] = options.continueAt;
    if (options.instrumental !== undefined) body["instrumental"] = options.instrumental;
    if (options.vocalGender !== undefined) body["vocal_gender"] = options.vocalGender;
    if (options.negativeTags !== undefined) body["negative_tags"] = options.negativeTags;
    if (options.styleInfluence !== undefined) body["style_influence"] = options.styleInfluence;
    if (options.audioWeight !== undefined) body["audio_weight"] = options.audioWeight;
    if (options.duration !== undefined) body["duration"] = options.duration;
    if (options.replaceSectionEnd !== undefined) body["replace_section_end"] = options.replaceSectionEnd;
    if (options.replaceSectionStart !== undefined) body["replace_section_start"] = options.replaceSectionStart;
    for (const [key, value] of Object.entries(options)) {
      if (!["action", "async", "audioId", "audioUrls", "audioWeight", "callbackUrl", "continueAt", "custom", "duration", "instrumental", "lyric", "lyricPrompt", "mashupAudioIds", "maxWait", "model", "negativeTags", "overpaintingEnd", "overpaintingStart", "personaId", "pollInterval", "prompt", "replaceSectionEnd", "replaceSectionStart", "samplesEnd", "samplesStart", "style", "styleInfluence", "title", "underpaintingEnd", "underpaintingStart", "variationCategory", "vocalGender", "wait", "weirdness"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    body.async = options.async ?? true;
    const result = (await this.transport.request('POST', "/suno/audios", { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), "/suno/tasks", this.transport, result);
    if (options.wait) {
      await handle.wait({ pollInterval: options.pollInterval, maxWait: options.maxWait });
    }
    return handle;
  }

  /** Suno Persona */
  async persona(options: SunoPersonaOptions): Promise<Record<string, unknown>> {
    const body: Record<string, unknown> = {};
    body["name"] = options.name;
    body["audio_id"] = options.audioId;
    if (options.voxAudioId !== undefined) body["vox_audio_id"] = options.voxAudioId;
    if (options.vocalStart !== undefined) body["vocal_start"] = options.vocalStart;
    if (options.vocalEnd !== undefined) body["vocal_end"] = options.vocalEnd;
    if (options.description !== undefined) body["description"] = options.description;
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "audioId", "callbackUrl", "description", "maxWait", "name", "pollInterval", "vocalEnd", "vocalStart", "voxAudioId", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    return (await this.transport.request('POST', "/suno/persona", { json: body })) as Record<string, unknown>;
  }

  /** Suno Mp4 */
  async mp4(options: SunoMp4Options): Promise<Record<string, unknown>> {
    const body: Record<string, unknown> = {};
    body["audio_id"] = options.audioId;
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "audioId", "callbackUrl", "maxWait", "pollInterval", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    return (await this.transport.request('POST', "/suno/mp4", { json: body })) as Record<string, unknown>;
  }

  /** Suno Voices */
  async voices(options: SunoVoicesOptions): Promise<Record<string, unknown>> {
    const body: Record<string, unknown> = {};
    body["audio_url"] = options.audioUrl;
    if (options.name !== undefined) body["name"] = options.name;
    if (options.description !== undefined) body["description"] = options.description;
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "audioUrl", "callbackUrl", "description", "maxWait", "name", "pollInterval", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    return (await this.transport.request('POST', "/suno/voices", { json: body })) as Record<string, unknown>;
  }

  /** Suno Timing */
  async timing(options: SunoTimingOptions): Promise<Record<string, unknown>> {
    const body: Record<string, unknown> = {};
    body["audio_id"] = options.audioId;
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "audioId", "callbackUrl", "maxWait", "pollInterval", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    return (await this.transport.request('POST', "/suno/timing", { json: body })) as Record<string, unknown>;
  }

  /** Suno Vox */
  async vox(options: SunoVoxOptions): Promise<TaskHandle> {
    const body: Record<string, unknown> = {};
    body["audio_id"] = options.audioId;
    body["vocal_start"] = options.vocalStart;
    body["vocal_end"] = options.vocalEnd;
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "audioId", "callbackUrl", "maxWait", "pollInterval", "vocalEnd", "vocalStart", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    body.async = options.async ?? true;
    const result = (await this.transport.request('POST', "/suno/vox", { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), "/suno/tasks", this.transport, result);
    if (options.wait) {
      await handle.wait({ pollInterval: options.pollInterval, maxWait: options.maxWait });
    }
    return handle;
  }

  /** Suno Wav */
  async wav(options: SunoWavOptions): Promise<TaskHandle> {
    const body: Record<string, unknown> = {};
    body["audio_id"] = options.audioId;
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "audioId", "callbackUrl", "maxWait", "pollInterval", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    body.async = options.async ?? true;
    const result = (await this.transport.request('POST', "/suno/wav", { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), "/suno/tasks", this.transport, result);
    if (options.wait) {
      await handle.wait({ pollInterval: options.pollInterval, maxWait: options.maxWait });
    }
    return handle;
  }

  /** Suno Midi */
  async midi(options: SunoMidiOptions): Promise<TaskHandle> {
    const body: Record<string, unknown> = {};
    body["audio_id"] = options.audioId;
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "audioId", "callbackUrl", "maxWait", "pollInterval", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    body.async = options.async ?? true;
    const result = (await this.transport.request('POST', "/suno/midi", { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), "/suno/tasks", this.transport, result);
    if (options.wait) {
      await handle.wait({ pollInterval: options.pollInterval, maxWait: options.maxWait });
    }
    return handle;
  }

  /** Suno Style */
  async style(options: SunoStyleOptions): Promise<Record<string, unknown>> {
    const body: Record<string, unknown> = {};
    body["prompt"] = options.prompt;
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "callbackUrl", "maxWait", "pollInterval", "prompt", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    return (await this.transport.request('POST', "/suno/style", { json: body })) as Record<string, unknown>;
  }

  /** Suno Lyrics */
  async lyrics(options: SunoLyricsOptions): Promise<Record<string, unknown>> {
    const body: Record<string, unknown> = {};
    body["model"] = options.model;
    body["prompt"] = options.prompt;
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "callbackUrl", "maxWait", "model", "pollInterval", "prompt", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    return (await this.transport.request('POST', "/suno/lyrics", { json: body })) as Record<string, unknown>;
  }

  /** Suno Mashup Lyrics */
  async mashup_lyrics(options: SunoMashupLyricsOptions): Promise<Record<string, unknown>> {
    const body: Record<string, unknown> = {};
    body["lyrics_a"] = options.lyricsA;
    body["lyrics_b"] = options.lyricsB;
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "callbackUrl", "lyricsA", "lyricsB", "maxWait", "pollInterval", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    return (await this.transport.request('POST', "/suno/mashup-lyrics", { json: body })) as Record<string, unknown>;
  }

  /** Suno Upload */
  async upload(options: SunoUploadOptions): Promise<Record<string, unknown>> {
    const body: Record<string, unknown> = {};
    body["audio_url"] = options.audioUrl;
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "audioUrl", "callbackUrl", "maxWait", "pollInterval", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    return (await this.transport.request('POST', "/suno/upload", { json: body })) as Record<string, unknown>;
  }

}
