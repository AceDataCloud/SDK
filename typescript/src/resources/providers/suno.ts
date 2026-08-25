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
  /** Lyrics for generating music under custom mode (`custom` is `true`). `chirp-v3-5` and `chirp-v4` have a maximum of 3000 characters; `chirp-v4-5` and above (including `chirp-v5`, `chirp-v5-5`) have a maximum of 5000 characters. */
  lyric?: string;
  /** The model used for generating music has a default value of `chirp-v4`. */
  model?: "chirp-v5-5" | "chirp-v5" | "chirp-v4-5-plus" | "chirp-v4-5" | "chirp-v4" | "chirp-v3-5" | "chirp-v3-0";
  /** Music style description. `chirp-v3-5` and `chirp-v4` up to 200 characters; `chirp-v4-5` and above (including `chirp-v5`, `chirp-v5-5`) up to 1000 characters. */
  style?: string;
  /** Music Title (Custom Mode). `chirp-v3-5` and `chirp-v4` up to 80 characters; `chirp-v4-5` and above (including `chirp-v5`, `chirp-v5-5`) up to 100 characters. */
  title?: string;
  /** Types of operations for generating music. `generate`: Generate audio based on prompts; `extend`: Continue generating based on existing audio; `concat`: Stitch existing audio clips into a complete track; `cover`: Copy the musical style of an existing track and reinterpret it; `upload_cover`: Style cover of uploaded audio; `upload_extend`: Extend and continue generating uploaded audio; `artist_consistency`: Sing new songs in the style of a specified artist (Persona); `artist_consistency_vox`: Sing new songs in the style of a specified artist using VOX mode; `stems`: Separate the song into vocal and accompaniment tracks; `all_stems`: Separate the song into all independent tracks (vocals, drums, bass, other instruments); `replace_section`: Replace segments within a specified time period; `underpainting`: Generate and add AI accompaniment to the uploaded vocal track; `overpainting`: Generate and add AI vocals to the uploaded accompaniment track; `samples`: Add AI samples to the uploaded audio within a specified time period; `remaster`: Remaster existing audio to enhance sound quality; `mashup`: Mix and stitch multiple songs into one track; `inspo`: Generate new music inspired by 1 to 4 reference audio segments. */
  action?: "generate" | "extend" | "upload_extend" | "upload_cover" | "concat" | "cover" | "artist_consistency" | "artist_consistency_vox" | "stems" | "all_stems" | "replace_section" | "underpainting" | "overpainting" | "remaster" | "mashup" | "samples" | "inspo";
  /** Whether to enable the custom mode flag. If `true`, the audio will be generated based on the lyrics; otherwise, it will be generated based on the prompts. */
  custom?: boolean;
  /** The prompt words for generating music in inspiration mode (when `custom` is set to `false`) must not exceed 500 characters. For custom mode, please use `lyric` and `style`. */
  prompt?: string;
  /** Audio ID used for generating additional audio based on existing audio. This field is required when `action` is `extend` or `concat`. */
  audioId?: string;
  /** Target length of the generated track in seconds, given as an integer, typically between 10 and 360. It is mainly used for generation in custom mode (`custom` is `true`); some models or actions may not support it, in which case the value is ignored or an error is returned. It is a target only — the finished length is reported by the `duration` field in the response and may differ slightly. */
  duration?: number;
  /** The "Weirdness" advanced parameter in the Suno official custom mode has a value range of 0 to 1, with higher values resulting in more creative and experimental outputs. It is only effective in custom mode. */
  weirdness?: number;
  /** A list of reference audio URLs for inspiration, requiring 1 to 4 publicly accessible audio addresses. This field is mandatory when `action` is `inspo`. */
  audioUrls?: string[];
  /** Generate the singer Persona ID used when creating songs based on the unique style characteristics of the specified singer. */
  personaId?: string;
  /** Continue generating from the specified time point (seconds) of the existing audio. For example, 213.5 means to continue from 3 minutes and 33.5 seconds. */
  continueAt?: number;
  /** Add the end time of the sample for the uploaded audio, which must be less than the total duration of the song. */
  samplesEnd?: number;
  /** The weight of the uploaded reference audio, with a value range from 0 to 1, where a higher value indicates greater reliance on the reference audio. This only takes effect during the cover operation. */
  audioWeight?: number;
  /** Pure accompaniment mode (no lyrics), default is `false`. When set to `true`, the lyrics filled in above will be ignored. */
  instrumental?: boolean;
  /** Prompts for automatically generating lyrics, effective only when `custom` is `true` and `lyric` is empty. */
  lyricPrompt?: string;
  /** Voice gender preference, selectable values are `'m'` (male voice) or `'f'` (female voice). Models `chirp-v4-5` and above are effective; this parameter is a preference item that can increase the probability of the target gender, but it does not guarantee strict adherence. */
  vocalGender?: string;
  /** Add a default start time for the uploaded audio sample, with a default value of 0. */
  samplesStart?: number;
  /** Styles of description that are not desired in music generation. */
  negativeTags?: string;
  /** The "Style Influence" advanced parameter in the Suno official custom mode has a value range of 0 to 1, with higher values being closer to the selected style. It is only effective in custom mode. */
  styleInfluence?: number;
  /** Audio ID list for mixing and mashup. This field is required when `action` is `mashup`. */
  mashupAudioIds?: string[];
  /** Add the end time of the AI voice to the uploaded audio, which must be less than the total duration of the song. */
  overpaintingEnd?: number;
  /** Add the end time for the AI accompaniment to the uploaded audio, which must be less than the total duration of the song. */
  underpaintingEnd?: number;
  /** Set the default start time for the AI voice of the uploaded audio to 0. */
  overpaintingStart?: number;
  /** `variation_category` only supports version v5 and above, with only three optional values: `high`, `normal`, `subtle`. */
  variationCategory?: string;
  /** When `action` is `replace_section`, specify the end time (in seconds) of the segment to be replaced. */
  replaceSectionEnd?: number;
  /** Set the default start time for the AI accompaniment added to the uploaded audio, with a default value of 0. */
  underpaintingStart?: number;
  /** When `action` is `replace_section`, specify the start time (in seconds) of the segment to be replaced. */
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
  /** Names of singer styles. */
  name: string;
  /** Used to create generated song IDs in the style of the singer. */
  audioId: string;
  /** The end time of the vocal segment in the audio (seconds). */
  vocalEnd?: number;
  /** A textual description of the singer's style. */
  description?: string;
  /** The starting time (in seconds) of the vocal segment in the audio. */
  vocalStart?: number;
  /** Used to generate audio IDs in the style of new singers (vocal reference audio). */
  voxAudioId?: string;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

export interface SunoMp4Options {
  /** Used to obtain the song ID for the corresponding MP4 of the song. */
  audioId: string;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

export interface SunoVoicesOptions {
  /** Publicly accessible URL for audio files used to create sound. Must be in MP3 or WAV format, at least 10 seconds long, and must contain clear human voice of a single speaker, without background noise or background music. */
  audioUrl: string;
  /** Custom voice personality name. */
  name?: string;
  /** Description information for custom voice personality. */
  description?: string;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

export interface SunoTimingOptions {
  /** Need to obtain the audio ID for timing/caption data, which is the generated Suno song ID. */
  audioId: string;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

export interface SunoVoxOptions {
  /** The source audio ID used to extract human voice, which is the unique identifier of the Suno audio segment to be processed. */
  audioId: string;
  /** End time point for vocal extraction (unit: seconds). */
  vocalEnd: number;
  /** The starting time point for vocal extraction (unit: seconds). */
  vocalStart: number;
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
  /** Used to obtain the existing audio ID of WAV format audio. */
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
  /** The source audio ID for generating MIDI will extract MIDI content based on the existing audio. */
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
  /** Style prompts that need optimization. */
  prompt: string;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

export interface SunoLyricsOptions {
  /** The model used for generating lyrics has a default value of `default`, with optional values including `default` and `remi-v1`. */
  model: "default" | "remi-v1";
  /** Prompts for generating lyrics, describing the desired theme or style of the lyrics. */
  prompt: Record<string, unknown>;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

export interface SunoMashupLyricsOptions {
  /** The first paragraph of lyrics content used for mixed generation. */
  lyricsA: string;
  /** The content of the second verse for mixed-generated lyrics. */
  lyricsB: string;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

export interface SunoUploadOptions {
  /** The CDN address (URL) for the custom audio file to be uploaded. */
  audioUrl: string;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

/** suno client. */
export class Suno {
  constructor(private transport: Transport) {}

  /** Suno AI music generation API, generates 2 songs per request with extension support. */
  async generate(options: SunoGenerateOptions = {}): Promise<TaskHandle> {
    const body: Record<string, unknown> = {};
    if (options.lyric !== undefined) body["lyric"] = options.lyric;
    if (options.model !== undefined) body["model"] = options.model;
    if (options.style !== undefined) body["style"] = options.style;
    if (options.title !== undefined) body["title"] = options.title;
    if (options.action !== undefined) body["action"] = options.action;
    if (options.custom !== undefined) body["custom"] = options.custom;
    if (options.prompt !== undefined) body["prompt"] = options.prompt;
    if (options.audioId !== undefined) body["audio_id"] = options.audioId;
    if (options.duration !== undefined) body["duration"] = options.duration;
    if (options.weirdness !== undefined) body["weirdness"] = options.weirdness;
    if (options.audioUrls !== undefined) body["audio_urls"] = options.audioUrls;
    if (options.personaId !== undefined) body["persona_id"] = options.personaId;
    if (options.continueAt !== undefined) body["continue_at"] = options.continueAt;
    if (options.samplesEnd !== undefined) body["samples_end"] = options.samplesEnd;
    if (options.audioWeight !== undefined) body["audio_weight"] = options.audioWeight;
    if (options.instrumental !== undefined) body["instrumental"] = options.instrumental;
    if (options.lyricPrompt !== undefined) body["lyric_prompt"] = options.lyricPrompt;
    if (options.vocalGender !== undefined) body["vocal_gender"] = options.vocalGender;
    if (options.samplesStart !== undefined) body["samples_start"] = options.samplesStart;
    if (options.negativeTags !== undefined) body["negative_tags"] = options.negativeTags;
    if (options.styleInfluence !== undefined) body["style_influence"] = options.styleInfluence;
    if (options.mashupAudioIds !== undefined) body["mashup_audio_ids"] = options.mashupAudioIds;
    if (options.overpaintingEnd !== undefined) body["overpainting_end"] = options.overpaintingEnd;
    if (options.underpaintingEnd !== undefined) body["underpainting_end"] = options.underpaintingEnd;
    if (options.overpaintingStart !== undefined) body["overpainting_start"] = options.overpaintingStart;
    if (options.variationCategory !== undefined) body["variation_category"] = options.variationCategory;
    if (options.replaceSectionEnd !== undefined) body["replace_section_end"] = options.replaceSectionEnd;
    if (options.underpaintingStart !== undefined) body["underpainting_start"] = options.underpaintingStart;
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

  /** Suno singer style API, set song style based on a generated song ID. */
  async persona(options: SunoPersonaOptions): Promise<Record<string, unknown>> {
    const body: Record<string, unknown> = {};
    body["name"] = options.name;
    body["audio_id"] = options.audioId;
    if (options.vocalEnd !== undefined) body["vocal_end"] = options.vocalEnd;
    if (options.description !== undefined) body["description"] = options.description;
    if (options.vocalStart !== undefined) body["vocal_start"] = options.vocalStart;
    if (options.voxAudioId !== undefined) body["vox_audio_id"] = options.voxAudioId;
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "audioId", "callbackUrl", "description", "maxWait", "name", "pollInterval", "vocalEnd", "vocalStart", "voxAudioId", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    return (await this.transport.request('POST', "/suno/persona", { json: body })) as Record<string, unknown>;
  }

  /** Suno MP4 API, get MP4 file link via audio_id. */
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

  /** Suno Voice Clone API. Create a custom voice persona from an uploaded audio file for voice cloning in music generation. */
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

  /** Suno timeline API, get lyrics and audio timeline of generated music. */
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

  /** Suno vocal/instrumental stems API. Pass an audio_id to asynchronously produce vocal-only and instrumental-only stem files for remixing and creative reuse. */
  async vox(options: SunoVoxOptions): Promise<TaskHandle> {
    const body: Record<string, unknown> = {};
    body["audio_id"] = options.audioId;
    body["vocal_end"] = options.vocalEnd;
    body["vocal_start"] = options.vocalStart;
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

  /** SUNO allows generating higher quality wav files based on the existing audio_id. */
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

  /** Suno MIDI API, retrieve MIDI data from generated music. */
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

  /** SUNO allows us to input prompts to generate enhanced song styles. */
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

  /** Suno lyrics generation API. Generates structured song lyrics from a prompt; supports the default and remi-v1 models. */
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

  /** Suno mashup lyrics API, merge two lyrics into a blended version. */
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

  /** Suno reference audio upload API, upload audio to get an audio_id for extended generation. */
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
