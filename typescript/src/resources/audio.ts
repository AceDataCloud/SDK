/** Audio/music generation resources. */

import { Transport } from '../runtime/transport';
import { TaskHandle } from '../runtime/tasks';

export type AudioProvider = 'suno' | 'producer' | 'fish' | (string & {});

export class Audio {
  constructor(private transport: Transport) {}

  async generate(opts: {
    prompt: string;
    provider?: AudioProvider;
    model?: string;
    /** Fish TTS text; `prompt` remains supported as a backward-compatible alias. */
    text?: string;
    referenceId?: string;
    format?: 'mp3' | 'wav' | 'pcm' | 'opus' | (string & {});
    sampleRate?: number;
    mp3Bitrate?: 64 | 128 | 192 | number;
    opusBitrate?: number;
    latency?: 'normal' | 'balanced' | (string & {});
    chunkLength?: number;
    minChunkLength?: number;
    temperature?: number;
    topP?: number;
    repetitionPenalty?: number;
    maxNewTokens?: number;
    normalize?: boolean;
    prosody?: Record<string, unknown>;
    references?: Record<string, unknown>[];
    tags?: string;
    callbackUrl?: string;
    wait?: boolean;
    pollInterval?: number;
    maxWait?: number;
    [key: string]: unknown;
  }): Promise<Record<string, unknown> | TaskHandle> {
    const {
      prompt,
      provider = 'suno',
      model,
      text,
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
      tags,
      callbackUrl,
      wait: shouldWait,
      pollInterval,
      maxWait,
      ...rest
    } = opts;

    let endpoint = `/${provider}/audios`;
    let headers: Record<string, string> | undefined;
    let body: Record<string, unknown> = {};
    if (provider === 'fish') {
      endpoint = '/fish/tts';
      body = { text: text ?? prompt, ...rest };
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
      if (callbackUrl !== undefined) body.callback_url = callbackUrl;
      if (model !== undefined) headers = { model };
    } else {
      body = { prompt, ...rest };
      if (model !== undefined) body.model = model;
      if (tags !== undefined) body.tags = tags;
      if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    }

    const result = await this.transport.request('POST', endpoint, { json: body, headers });
    const taskId = result.task_id as string | undefined;

    if (!taskId || (result.data && !shouldWait)) return result;

    const handle = new TaskHandle(taskId, `/${provider}/tasks`, this.transport);
    if (shouldWait) return handle.wait({ pollInterval, maxWait });
    return handle;
  }

  async listFishModels(params?: Record<string, string>): Promise<Record<string, unknown>> {
    return this.transport.request('GET', '/fish/model', { params });
  }

  async getFishModel(modelId: string): Promise<Record<string, unknown>> {
    return this.transport.request('GET', `/fish/model/${modelId}`);
  }
}
