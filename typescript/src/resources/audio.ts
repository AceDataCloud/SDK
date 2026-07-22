/** Audio/music generation resources. */

import { Transport } from '../runtime/transport';
import { TaskHandle } from '../runtime/tasks';

export type AudioProvider = 'suno' | 'producer' | 'fish' | (string & {});

export type FishAudioFormat = 'mp3' | 'wav' | 'pcm' | 'opus';
export type FishAudioLatency = 'normal' | 'balanced';

export interface AudioGenerateOptions {
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
  references?: Record<string, unknown>[];
  async?: boolean;
  wait?: boolean;
  pollInterval?: number;
  maxWait?: number;
  [key: string]: unknown;
}

const FISH_AUDIO_FIELD_ALIASES = {
  referenceId: 'reference_id',
  sampleRate: 'sample_rate',
  mp3Bitrate: 'mp3_bitrate',
  opusBitrate: 'opus_bitrate',
  chunkLength: 'chunk_length',
  minChunkLength: 'min_chunk_length',
  topP: 'top_p',
  repetitionPenalty: 'repetition_penalty',
  maxNewTokens: 'max_new_tokens',
} as const;

const FISH_AUDIO_CAMEL_CASE_FIELDS = new Set(Object.keys(FISH_AUDIO_FIELD_ALIASES));

function buildFishAudioBody(opts: AudioGenerateOptions): Record<string, unknown> {
  const {
    prompt,
    provider: _provider,
    model: _model,
    tags: _tags,
    callbackUrl: _callbackUrl,
    wait: _wait,
    pollInterval: _pollInterval,
    maxWait: _maxWait,
    ...rest
  } = opts;
  const body: Record<string, unknown> = { text: prompt };
  for (const [key, value] of Object.entries(rest)) {
    if (!FISH_AUDIO_CAMEL_CASE_FIELDS.has(key)) body[key] = value;
  }
  for (const [camelCaseField, snakeCaseField] of Object.entries(FISH_AUDIO_FIELD_ALIASES)) {
    const value = opts[camelCaseField];
    if (value !== undefined) {
      body[snakeCaseField] = value;
    }
  }
  if (opts.callbackUrl !== undefined) body.callback_url = opts.callbackUrl;
  return body;
}

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

  async generate(opts: AudioGenerateOptions): Promise<Record<string, unknown> | TaskHandle> {
    const { prompt, provider = 'suno', model, tags, callbackUrl, wait: shouldWait, pollInterval, maxWait, ...rest } = opts;
    let result: Record<string, unknown>;
    if (provider === 'fish') {
      const body = buildFishAudioBody(opts);
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
