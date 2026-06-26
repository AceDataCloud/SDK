/** Audio/music generation resources. */

import { Transport } from '../runtime/transport';
import { TaskHandle } from '../runtime/tasks';

export type AudioProvider = 'suno' | 'producer' | 'fish' | (string & {});

export class Audio {
  constructor(private transport: Transport) {}

  async listFishModels(opts: {
    pageSize?: number;
    pageNumber?: number;
    title?: string;
    tag?: string;
    selfOnly?: boolean;
    authorId?: string;
    language?: string;
    titleLanguage?: string;
    sortBy?: string;
  } = {}): Promise<Record<string, unknown>> {
    const { pageSize, pageNumber, title, tag, selfOnly, authorId, language, titleLanguage, sortBy } = opts;
    const params: Record<string, string> = {};
    if (pageSize !== undefined) params.page_size = String(pageSize);
    if (pageNumber !== undefined) params.page_number = String(pageNumber);
    if (title !== undefined) params.title = title;
    if (tag !== undefined) params.tag = tag;
    if (selfOnly !== undefined) params.self = String(selfOnly);
    if (authorId !== undefined) params.author_id = authorId;
    if (language !== undefined) params.language = language;
    if (titleLanguage !== undefined) params.title_language = titleLanguage;
    if (sortBy !== undefined) params.sort_by = sortBy;
    return this.transport.request('GET', '/fish/model', { params });
  }

  async getFishModel(id: string): Promise<Record<string, unknown>> {
    return this.transport.request('GET', `/fish/model/${id}`);
  }

  async generate(opts: {
    prompt: string | Record<string, unknown>;
    provider?: AudioProvider;
    model?: string;
    tags?: string;
    lyric?: string;
    style?: string;
    variationCategory?: string;
    title?: string;
    action?: string;
    custom?: boolean;
    lyricPrompt?: string | Record<string, unknown>;
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
      prompt,
      provider = 'suno',
      model,
      tags,
      lyric,
      style,
      variationCategory,
      title,
      action,
      custom,
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
    let result: Record<string, unknown>;
    if (provider === 'fish') {
      const body: Record<string, unknown> = { text: prompt, ...rest };
      if (callbackUrl !== undefined) body.callback_url = callbackUrl;
      result = await this.transport.request('POST', '/fish/tts', {
        json: body,
        headers: model !== undefined ? { model } : undefined,
      });
    } else {
      const body: Record<string, unknown> = { prompt, ...rest };
      if (model !== undefined) body.model = model;
      if (tags !== undefined) body.tags = tags;
      if (lyric !== undefined) body.lyric = lyric;
      if (style !== undefined) body.style = style;
      if (variationCategory !== undefined) body.variation_category = variationCategory;
      if (title !== undefined) body.title = title;
      if (action !== undefined) body.action = action;
      if (custom !== undefined) body.custom = custom;
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
      result = await this.transport.request('POST', `/${provider}/audios`, { json: body });
    }
    const taskId = result.task_id as string | undefined;

    if (!taskId || (result.data && !shouldWait)) return result;

    const handle = new TaskHandle(taskId, `/${provider}/tasks`, this.transport);
    if (shouldWait) return handle.wait({ pollInterval, maxWait });
    return handle;
  }
}
