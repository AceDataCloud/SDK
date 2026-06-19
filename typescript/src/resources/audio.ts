/** Audio/music generation resources. */

import { Transport } from '../runtime/transport';
import { TaskHandle } from '../runtime/tasks';

export type AudioProvider = 'suno' | 'producer' | 'fish' | (string & {});
export type FishAudioFormat = 'mp3' | 'wav' | 'pcm' | 'opus';
export type FishAudioLatency = 'normal' | 'balanced';

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
    prompt: string;
    provider?: AudioProvider;
    model?: string;
    tags?: string;
    callbackUrl?: string;
    referenceId?: string;
    format?: FishAudioFormat;
    sampleRate?: number;
    mp3Bitrate?: 64 | 128 | 192;
    opusBitrate?: number;
    latency?: FishAudioLatency;
    chunkLength?: number;
    minChunkLength?: number;
    temperature?: number;
    topP?: number;
    repetitionPenalty?: number;
    maxNewTokens?: number;
    normalize?: boolean;
    prosody?: Record<string, unknown>;
    references?: Array<Record<string, unknown>>;
    async?: boolean;
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
      callbackUrl,
      referenceId,
      format,
      sampleRate,
      mp3Bitrate,
      opusBitrate,
      latency,
      chunkLength,
      minChunkLength,
      temperature,
      topP,
      repetitionPenalty,
      maxNewTokens,
      normalize,
      prosody,
      references,
      wait: shouldWait,
      pollInterval,
      maxWait,
      ...rest
    } = opts;
    let result: Record<string, unknown>;
    if (provider === 'fish') {
      const body: Record<string, unknown> = { text: prompt, ...rest };
      if (callbackUrl !== undefined) body.callback_url = callbackUrl;
      if (referenceId !== undefined) body.reference_id = referenceId;
      if (format !== undefined) body.format = format;
      if (sampleRate !== undefined) body.sample_rate = sampleRate;
      if (mp3Bitrate !== undefined) body.mp3_bitrate = mp3Bitrate;
      if (opusBitrate !== undefined) body.opus_bitrate = opusBitrate;
      if (latency !== undefined) body.latency = latency;
      if (chunkLength !== undefined) body.chunk_length = chunkLength;
      if (minChunkLength !== undefined) body.min_chunk_length = minChunkLength;
      if (temperature !== undefined) body.temperature = temperature;
      if (topP !== undefined) body.top_p = topP;
      if (repetitionPenalty !== undefined) body.repetition_penalty = repetitionPenalty;
      if (maxNewTokens !== undefined) body.max_new_tokens = maxNewTokens;
      if (normalize !== undefined) body.normalize = normalize;
      if (prosody !== undefined) body.prosody = prosody;
      if (references !== undefined) body.references = references;
      result = await this.transport.request('POST', '/fish/tts', {
        json: body,
        headers: model !== undefined ? { model } : undefined,
      });
    } else {
      const body: Record<string, unknown> = { prompt, ...rest };
      if (model !== undefined) body.model = model;
      if (tags !== undefined) body.tags = tags;
      if (callbackUrl !== undefined) body.callback_url = callbackUrl;
      result = await this.transport.request('POST', `/${provider}/audios`, { json: body });
    }
    const taskId = result.task_id as string | undefined;

    if (!taskId || (result.data && !shouldWait)) return result;

    const handle = new TaskHandle(taskId, `/${provider}/tasks`, this.transport);
    if (shouldWait) return handle.wait({ pollInterval, maxWait });
    return handle;
  }
}
