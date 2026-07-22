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
      const body: Record<string, unknown> = { text: prompt, ...rest };
      if (opts.referenceId !== undefined) {
        delete body.referenceId;
        body.reference_id = opts.referenceId;
      }
      if (opts.sampleRate !== undefined) {
        delete body.sampleRate;
        body.sample_rate = opts.sampleRate;
      }
      if (opts.mp3Bitrate !== undefined) {
        delete body.mp3Bitrate;
        body.mp3_bitrate = opts.mp3Bitrate;
      }
      if (opts.opusBitrate !== undefined) {
        delete body.opusBitrate;
        body.opus_bitrate = opts.opusBitrate;
      }
      if (opts.chunkLength !== undefined) {
        delete body.chunkLength;
        body.chunk_length = opts.chunkLength;
      }
      if (opts.minChunkLength !== undefined) {
        delete body.minChunkLength;
        body.min_chunk_length = opts.minChunkLength;
      }
      if (opts.topP !== undefined) {
        delete body.topP;
        body.top_p = opts.topP;
      }
      if (opts.repetitionPenalty !== undefined) {
        delete body.repetitionPenalty;
        body.repetition_penalty = opts.repetitionPenalty;
      }
      if (opts.maxNewTokens !== undefined) {
        delete body.maxNewTokens;
        body.max_new_tokens = opts.maxNewTokens;
      }
      if (callbackUrl !== undefined) body.callback_url = callbackUrl;
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
