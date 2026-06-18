/** Suno-specific music generation resources. */

import { Transport } from '../runtime/transport';
import { TaskHandle } from '../runtime/tasks';

export type SunoModel =
  | 'chirp-v5-5'
  | 'chirp-v5'
  | 'chirp-v4-5-plus'
  | 'chirp-v4-5'
  | 'chirp-v4'
  | 'chirp-v3-5'
  | 'chirp-v3-0'
  | (string & {});

export type SunoAction =
  | 'generate'
  | 'extend'
  | 'upload_extend'
  | 'upload_cover'
  | 'concat'
  | 'cover'
  | 'artist_consistency'
  | 'artist_consistency_vox'
  | 'stems'
  | 'all_stems'
  | 'replace_section'
  | 'underpainting'
  | 'overpainting'
  | 'remaster'
  | 'mashup'
  | 'samples'
  | 'inspo'
  | (string & {});

export class Suno {
  constructor(private transport: Transport) {}

  async generate(opts: {
    lyric?: string;
    model?: SunoModel;
    style?: string;
    variationCategory?: string;
    title?: string;
    action?: SunoAction;
    custom?: boolean;
    prompt?: unknown;
    lyricPrompt?: unknown;
    audioId?: string;
    mashupAudioIds?: string[];
    audioUrls?: string[];
    weirdness?: number;
    personaId?: string;
    overpaintingStart?: number;
    overpaintingEnd?: number;
    samplesStart?: number;
    samplesEnd?: number;
    underpaintingStart?: number;
    underpaintingEnd?: number;
    continueAt?: number;
    callbackUrl?: string;
    async?: boolean;
    instrumental?: boolean;
    vocalGender?: string;
    styleNegative?: string;
    styleInfluence?: number;
    audioWeight?: number;
    replaceSectionEnd?: number;
    replaceSectionStart?: number;
    wait?: boolean;
    pollInterval?: number;
    maxWait?: number;
    [key: string]: unknown;
  }): Promise<Record<string, unknown> | TaskHandle> {
    const {
      lyric,
      model,
      style,
      variationCategory,
      title,
      action,
      custom,
      prompt,
      lyricPrompt,
      audioId,
      mashupAudioIds,
      audioUrls,
      weirdness,
      personaId,
      overpaintingStart,
      overpaintingEnd,
      samplesStart,
      samplesEnd,
      underpaintingStart,
      underpaintingEnd,
      continueAt,
      callbackUrl,
      instrumental,
      vocalGender,
      styleNegative,
      styleInfluence,
      audioWeight,
      replaceSectionEnd,
      replaceSectionStart,
      wait: shouldWait,
      pollInterval,
      maxWait,
      ...rest
    } = opts;
    const body: Record<string, unknown> = { ...rest };
    if (lyric !== undefined) body.lyric = lyric;
    if (model !== undefined) body.model = model;
    if (style !== undefined) body.style = style;
    if (variationCategory !== undefined) body.variation_category = variationCategory;
    if (title !== undefined) body.title = title;
    if (action !== undefined) body.action = action;
    if (custom !== undefined) body.custom = custom;
    if (prompt !== undefined) body.prompt = prompt;
    if (lyricPrompt !== undefined) body.lyric_prompt = lyricPrompt;
    if (audioId !== undefined) body.audio_id = audioId;
    if (mashupAudioIds !== undefined) body.mashup_audio_ids = mashupAudioIds;
    if (audioUrls !== undefined) body.audio_urls = audioUrls;
    if (weirdness !== undefined) body.weirdness = weirdness;
    if (personaId !== undefined) body.persona_id = personaId;
    if (overpaintingStart !== undefined) body.overpainting_start = overpaintingStart;
    if (overpaintingEnd !== undefined) body.overpainting_end = overpaintingEnd;
    if (samplesStart !== undefined) body.samples_start = samplesStart;
    if (samplesEnd !== undefined) body.samples_end = samplesEnd;
    if (underpaintingStart !== undefined) body.underpainting_start = underpaintingStart;
    if (underpaintingEnd !== undefined) body.underpainting_end = underpaintingEnd;
    if (continueAt !== undefined) body.continue_at = continueAt;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    if (instrumental !== undefined) body.instrumental = instrumental;
    if (vocalGender !== undefined) body.vocal_gender = vocalGender;
    if (styleNegative !== undefined) body.style_negative = styleNegative;
    if (styleInfluence !== undefined) body.style_influence = styleInfluence;
    if (audioWeight !== undefined) body.audio_weight = audioWeight;
    if (replaceSectionEnd !== undefined) body.replace_section_end = replaceSectionEnd;
    if (replaceSectionStart !== undefined) body.replace_section_start = replaceSectionStart;
    const result = await this.transport.request('POST', '/suno/audios', { json: body });
    const taskId = result.task_id as string | undefined;
    if (!taskId || (result.data && !shouldWait)) return result;
    const handle = new TaskHandle(taskId, '/suno/tasks', this.transport);
    if (shouldWait) return handle.wait({ pollInterval, maxWait });
    return handle;
  }

  async createPersona(opts: {
    audioId: string;
    name: string;
    voxAudioId?: string;
    vocalStart?: number;
    vocalEnd?: number;
    description?: string;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { audioId, name, voxAudioId, vocalStart, vocalEnd, description, ...rest } = opts;
    const body: Record<string, unknown> = { audio_id: audioId, name, ...rest };
    if (voxAudioId !== undefined) body.vox_audio_id = voxAudioId;
    if (vocalStart !== undefined) body.vocal_start = vocalStart;
    if (vocalEnd !== undefined) body.vocal_end = vocalEnd;
    if (description !== undefined) body.description = description;
    return this.transport.request('POST', '/suno/persona', { json: body });
  }

  async listPersonas(opts: {
    userId: string;
    limit?: number;
    offset?: number;
  }): Promise<Record<string, unknown>> {
    const { userId, limit, offset } = opts;
    const params: Record<string, string> = { user_id: userId };
    if (limit !== undefined) params.limit = String(limit);
    if (offset !== undefined) params.offset = String(offset);
    return this.transport.request('GET', '/suno/persona', { params });
  }

  async deletePersona(opts: {
    personaId: string;
    userId?: string;
  }): Promise<Record<string, unknown>> {
    const { personaId, userId } = opts;
    const params: Record<string, string> = { persona_id: personaId };
    if (userId !== undefined) params.user_id = userId;
    return this.transport.request('DELETE', '/suno/persona', { params });
  }

  async mp4(opts: {
    audioId: string;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { audioId, ...rest } = opts;
    const body: Record<string, unknown> = { audio_id: audioId, ...rest };
    return this.transport.request('POST', '/suno/mp4', { json: body });
  }

  async voices(opts: {
    audioUrl: string;
    name?: string;
    description?: string;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { audioUrl, name, description, ...rest } = opts;
    const body: Record<string, unknown> = { audio_url: audioUrl, ...rest };
    if (name !== undefined) body.name = name;
    if (description !== undefined) body.description = description;
    return this.transport.request('POST', '/suno/voices', { json: body });
  }

  async timing(opts: {
    audioId: string;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { audioId, ...rest } = opts;
    const body: Record<string, unknown> = { audio_id: audioId, ...rest };
    return this.transport.request('POST', '/suno/timing', { json: body });
  }

  async vox(opts: {
    audioId: string;
    vocalStart?: number;
    vocalEnd?: number;
    callbackUrl?: string;
    async?: boolean;
    wait?: boolean;
    pollInterval?: number;
    maxWait?: number;
    [key: string]: unknown;
  }): Promise<Record<string, unknown> | TaskHandle> {
    const { audioId, vocalStart, vocalEnd, callbackUrl, wait: shouldWait, pollInterval, maxWait, ...rest } = opts;
    const body: Record<string, unknown> = { audio_id: audioId, ...rest };
    if (vocalStart !== undefined) body.vocal_start = vocalStart;
    if (vocalEnd !== undefined) body.vocal_end = vocalEnd;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    const result = await this.transport.request('POST', '/suno/vox', { json: body });
    const taskId = result.task_id as string | undefined;
    if (!taskId || (result.data && !shouldWait)) return result;
    const handle = new TaskHandle(taskId, '/suno/tasks', this.transport);
    if (shouldWait) return handle.wait({ pollInterval, maxWait });
    return handle;
  }

  async wav(opts: {
    audioId: string;
    callbackUrl?: string;
    async?: boolean;
    wait?: boolean;
    pollInterval?: number;
    maxWait?: number;
    [key: string]: unknown;
  }): Promise<Record<string, unknown> | TaskHandle> {
    const { audioId, callbackUrl, wait: shouldWait, pollInterval, maxWait, ...rest } = opts;
    const body: Record<string, unknown> = { audio_id: audioId, ...rest };
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    const result = await this.transport.request('POST', '/suno/wav', { json: body });
    const taskId = result.task_id as string | undefined;
    if (!taskId || (result.data && !shouldWait)) return result;
    const handle = new TaskHandle(taskId, '/suno/tasks', this.transport);
    if (shouldWait) return handle.wait({ pollInterval, maxWait });
    return handle;
  }

  async midi(opts: {
    audioId: string;
    callbackUrl?: string;
    async?: boolean;
    wait?: boolean;
    pollInterval?: number;
    maxWait?: number;
    [key: string]: unknown;
  }): Promise<Record<string, unknown> | TaskHandle> {
    const { audioId, callbackUrl, wait: shouldWait, pollInterval, maxWait, ...rest } = opts;
    const body: Record<string, unknown> = { audio_id: audioId, ...rest };
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    const result = await this.transport.request('POST', '/suno/midi', { json: body });
    const taskId = result.task_id as string | undefined;
    if (!taskId || (result.data && !shouldWait)) return result;
    const handle = new TaskHandle(taskId, '/suno/tasks', this.transport);
    if (shouldWait) return handle.wait({ pollInterval, maxWait });
    return handle;
  }

  async style(opts: {
    prompt: string;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { prompt, ...rest } = opts;
    const body: Record<string, unknown> = { prompt, ...rest };
    return this.transport.request('POST', '/suno/style', { json: body });
  }

  async lyrics(opts: {
    prompt: unknown;
    model: 'default' | 'remi-v1' | (string & {});
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { prompt, model, ...rest } = opts;
    const body: Record<string, unknown> = { prompt, model, ...rest };
    return this.transport.request('POST', '/suno/lyrics', { json: body });
  }

  async mashupLyrics(opts: {
    lyricsA: string;
    lyricsB: string;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { lyricsA, lyricsB, ...rest } = opts;
    const body: Record<string, unknown> = { lyrics_a: lyricsA, lyrics_b: lyricsB, ...rest };
    return this.transport.request('POST', '/suno/mashup-lyrics', { json: body });
  }

  async upload(opts: {
    audioUrl: string;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { audioUrl, ...rest } = opts;
    const body: Record<string, unknown> = { audio_url: audioUrl, ...rest };
    return this.transport.request('POST', '/suno/upload', { json: body });
  }
}
