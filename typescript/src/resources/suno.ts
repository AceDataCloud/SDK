/** Suno-specific music generation resources. */

import { Transport } from '../runtime/transport';
import { TaskHandle } from '../runtime/tasks';

export class Suno {
  constructor(private transport: Transport) {}

  async generate(opts: {
    prompt?: string;
    lyric?: string;
    model?: string;
    style?: string;
    variationCategory?: string;
    title?: string;
    action?: 'generate' | 'extend' | 'replace_section' | 'inpaint' | 'cover' | 'mashup' | 'overpainting' | 'samples' | 'underpainting' | (string & {});
    custom?: boolean;
    lyricPrompt?: Record<string, unknown>;
    audioId?: string;
    mashupAudioIds?: string[];
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
    instrumental?: boolean;
    vocalGender?: 'm' | 'f' | (string & {});
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
      prompt, lyric, model, style, variationCategory, title, action, custom,
      lyricPrompt, audioId, mashupAudioIds, weirdness, personaId,
      overpaintingStart, overpaintingEnd, samplesStart, samplesEnd,
      underpaintingStart, underpaintingEnd, continueAt, callbackUrl,
      instrumental, vocalGender, styleNegative, styleInfluence, audioWeight,
      replaceSectionEnd, replaceSectionStart,
      wait: shouldWait, pollInterval, maxWait, ...rest
    } = opts;
    const body: Record<string, unknown> = { ...rest };
    if (prompt !== undefined) body.prompt = prompt;
    if (lyric !== undefined) body.lyric = lyric;
    if (model !== undefined) body.model = model;
    if (style !== undefined) body.style = style;
    if (variationCategory !== undefined) body.variation_category = variationCategory;
    if (title !== undefined) body.title = title;
    if (action !== undefined) body.action = action;
    if (custom !== undefined) body.custom = custom;
    if (lyricPrompt !== undefined) body.lyric_prompt = lyricPrompt;
    if (audioId !== undefined) body.audio_id = audioId;
    if (mashupAudioIds !== undefined) body.mashup_audio_ids = mashupAudioIds;
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
    name: string;
    audioId: string;
    voxAudioId?: string;
    vocalStart?: number;
    vocalEnd?: number;
    description?: string;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { name, audioId, voxAudioId, vocalStart, vocalEnd, description, ...rest } = opts;
    const body: Record<string, unknown> = { name, audio_id: audioId, ...rest };
    if (voxAudioId !== undefined) body.vox_audio_id = voxAudioId;
    if (vocalStart !== undefined) body.vocal_start = vocalStart;
    if (vocalEnd !== undefined) body.vocal_end = vocalEnd;
    if (description !== undefined) body.description = description;
    return this.transport.request('POST', '/suno/persona', { json: body });
  }

  async listPersonas(opts: {
    userId?: string;
    limit?: number;
    offset?: number;
  } = {}): Promise<Record<string, unknown>> {
    const params: Record<string, string> = {};
    if (opts.userId !== undefined) params.user_id = opts.userId;
    if (opts.limit !== undefined) params.limit = String(opts.limit);
    if (opts.offset !== undefined) params.offset = String(opts.offset);
    return this.transport.request('GET', '/suno/persona', { params });
  }

  async deletePersona(opts: {
    personaId: string;
    userId?: string;
  }): Promise<Record<string, unknown>> {
    const params: Record<string, string> = { persona_id: opts.personaId };
    if (opts.userId !== undefined) params.user_id = opts.userId;
    return this.transport.request('DELETE', '/suno/persona', { params });
  }

  async mp4(opts: {
    audioId: string;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { audioId, ...rest } = opts;
    return this.transport.request('POST', '/suno/mp4', { json: { audio_id: audioId, ...rest } });
  }

  async voices(opts: {
    audioUrl: string;
    name: string;
    description?: string;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { audioUrl, name, description, ...rest } = opts;
    const body: Record<string, unknown> = { audio_url: audioUrl, name, ...rest };
    if (description !== undefined) body.description = description;
    return this.transport.request('POST', '/suno/voices', { json: body });
  }

  async timing(opts: {
    audioId: string;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { audioId, ...rest } = opts;
    return this.transport.request('POST', '/suno/timing', { json: { audio_id: audioId, ...rest } });
  }

  async vox(opts: {
    audioId: string;
    vocalStart?: number;
    vocalEnd?: number;
    callbackUrl?: string;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { audioId, vocalStart, vocalEnd, callbackUrl, ...rest } = opts;
    const body: Record<string, unknown> = { audio_id: audioId, ...rest };
    if (vocalStart !== undefined) body.vocal_start = vocalStart;
    if (vocalEnd !== undefined) body.vocal_end = vocalEnd;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    return this.transport.request('POST', '/suno/vox', { json: body });
  }

  async wav(opts: {
    audioId: string;
    callbackUrl?: string;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { audioId, callbackUrl, ...rest } = opts;
    const body: Record<string, unknown> = { audio_id: audioId, ...rest };
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    return this.transport.request('POST', '/suno/wav', { json: body });
  }

  async midi(opts: {
    audioId: string;
    callbackUrl?: string;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { audioId, callbackUrl, ...rest } = opts;
    const body: Record<string, unknown> = { audio_id: audioId, ...rest };
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    return this.transport.request('POST', '/suno/midi', { json: body });
  }

  async style(opts: {
    prompt: string;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { prompt, ...rest } = opts;
    return this.transport.request('POST', '/suno/style', { json: { prompt, ...rest } });
  }

  async lyrics(opts: {
    prompt: string;
    model: string;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { prompt, model, ...rest } = opts;
    return this.transport.request('POST', '/suno/lyrics', { json: { prompt, model, ...rest } });
  }

  async mashupLyrics(opts: {
    lyricsA: string;
    lyricsB: string;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { lyricsA, lyricsB, ...rest } = opts;
    return this.transport.request('POST', '/suno/mashup-lyrics', { json: { lyrics_a: lyricsA, lyrics_b: lyricsB, ...rest } });
  }

  async upload(opts: {
    audioUrl: string;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { audioUrl, ...rest } = opts;
    return this.transport.request('POST', '/suno/upload', { json: { audio_url: audioUrl, ...rest } });
  }
}
