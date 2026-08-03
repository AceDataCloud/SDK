/** OpenAI-compatible facade resources. */

import { Transport } from '../runtime/transport';

class Completions {
  constructor(private transport: Transport) {}

  async create(opts: {
    model: string;
    messages: Array<Record<string, unknown>>;
    stream?: false;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>>;
  async create(opts: {
    model: string;
    messages: Array<Record<string, unknown>>;
    stream: true;
    [key: string]: unknown;
  }): Promise<AsyncGenerator<Record<string, unknown>>>;
  async create(opts: {
    model: string;
    messages: Array<Record<string, unknown>>;
    stream?: boolean;
    [key: string]: unknown;
  }): Promise<Record<string, unknown> | AsyncGenerator<Record<string, unknown>>> {
    const { model, messages, stream, ...rest } = opts;
    const body: Record<string, unknown> = { model, messages, ...rest };

    if (stream) {
      body.stream = true;
      return this.streamResponse(body);
    }
    return this.transport.request('POST', '/openai/chat/completions', { json: body });
  }

  private async *streamResponse(body: Record<string, unknown>): AsyncGenerator<Record<string, unknown>> {
    for await (const chunk of this.transport.requestStream('POST', '/openai/chat/completions', { json: body })) {
      yield JSON.parse(chunk);
    }
  }
}

class ChatNamespace {
  readonly completions: Completions;
  constructor(transport: Transport) {
    this.completions = new Completions(transport);
  }
}

class Responses {
  constructor(private transport: Transport) {}

  async create(opts: {
    model: string;
    input: string | Array<Record<string, unknown>>;
    stream?: false;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>>;
  async create(opts: {
    model: string;
    input: string | Array<Record<string, unknown>>;
    stream: true;
    [key: string]: unknown;
  }): Promise<AsyncGenerator<Record<string, unknown>>>;
  async create(opts: {
    model: string;
    input: string | Array<Record<string, unknown>>;
    stream?: boolean;
    [key: string]: unknown;
  }): Promise<Record<string, unknown> | AsyncGenerator<Record<string, unknown>>> {
    const { model, input, stream, ...rest } = opts;
    const body: Record<string, unknown> = { model, input, ...rest };

    if (stream) {
      body.stream = true;
      return this.streamResponse(body);
    }
    return this.transport.request('POST', '/openai/responses', { json: body });
  }

  private async *streamResponse(body: Record<string, unknown>): AsyncGenerator<Record<string, unknown>> {
    for await (const chunk of this.transport.requestStream('POST', '/openai/responses', { json: body })) {
      yield JSON.parse(chunk);
    }
  }
}

class Images {
  constructor(private transport: Transport) {}

  async generate(opts: {
    prompt: string;
    model: string;
    background?: string;
    moderation?: string;
    n?: number;
    outputCompression?: number;
    outputFormat?: string;
    partialImages?: number;
    size?: string;
    quality?: string;
    responseFormat?: string;
    style?: string;
    callbackUrl?: string;
    async?: boolean;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { prompt, model, outputCompression, outputFormat, partialImages, responseFormat, callbackUrl, ...rest } = opts;
    const body: Record<string, unknown> = { prompt, model, ...rest };
    if (outputCompression !== undefined) body.output_compression = outputCompression;
    if (outputFormat !== undefined) body.output_format = outputFormat;
    if (partialImages !== undefined) body.partial_images = partialImages;
    if (responseFormat !== undefined) body.response_format = responseFormat;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    return this.transport.request('POST', '/openai/images/generations', { json: body });
  }

  async edit(opts: {
    image: string | string[];
    prompt: string;
    model?: string;
    n?: number;
    background?: string;
    inputFidelity?: string;
    mask?: string;
    outputFormat?: string;
    outputCompression?: number;
    partialImages?: number;
    quality?: string;
    size?: string;
    responseFormat?: string;
    callbackUrl?: string;
    async?: boolean;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { image, prompt, inputFidelity, mask, outputFormat, outputCompression, partialImages, responseFormat, callbackUrl, ...rest } = opts;
    const body: Record<string, unknown> = { image, prompt, ...rest };
    if (inputFidelity !== undefined) body.input_fidelity = inputFidelity;
    if (mask !== undefined) body.mask = mask;
    if (outputFormat !== undefined) body.output_format = outputFormat;
    if (outputCompression !== undefined) body.output_compression = outputCompression;
    if (partialImages !== undefined) body.partial_images = partialImages;
    if (responseFormat !== undefined) body.response_format = responseFormat;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    return this.transport.request('POST', '/openai/images/edits', { json: body });
  }
}

class Embeddings {
  constructor(private transport: Transport) {}

  async create(opts: {
    model: string;
    input: string | string[];
    encodingFormat?: string;
    dimensions?: number;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { model, input, encodingFormat, dimensions, ...rest } = opts;
    const body: Record<string, unknown> = { model, input, ...rest };
    if (encodingFormat !== undefined) body.encoding_format = encodingFormat;
    if (dimensions !== undefined) body.dimensions = dimensions;
    return this.transport.request('POST', '/openai/embeddings', { json: body });
  }
}

export type SpeechModel = 'tts-1' | 'tts-1-hd';
export type SpeechVoice = 'alloy' | 'echo' | 'fable' | 'onyx' | 'nova' | 'shimmer';
export type SpeechResponseFormat = 'mp3' | 'opus' | 'aac' | 'flac' | 'wav' | 'pcm';
export type TranscriptionModel = 'whisper-1' | 'gpt-transcribe';
export type TranscriptionResponseFormat = 'json' | 'text' | 'srt' | 'verbose_json' | 'vtt';
export type TimestampGranularity = 'word' | 'segment';

class Speech {
  constructor(private transport: Transport) {}

  /** Synthesize speech, resolving to the raw audio bytes. */
  async create(opts: {
    input: string;
    model?: SpeechModel | string;
    voice?: SpeechVoice | string;
    responseFormat?: SpeechResponseFormat | string;
    speed?: number;
    [key: string]: unknown;
  }): Promise<Uint8Array> {
    const { input, model, voice, responseFormat, speed, ...rest } = opts;
    const body: Record<string, unknown> = { input, ...rest };
    if (model !== undefined) body.model = model;
    if (voice !== undefined) body.voice = voice;
    if (responseFormat !== undefined) body.response_format = responseFormat;
    if (speed !== undefined) body.speed = speed;
    return this.transport.requestRaw('POST', '/v1/audio/speech', { json: body });
  }
}

class Transcriptions {
  constructor(private transport: Transport) {}

  /** Transcribe an audio file. `file` is the audio payload to upload. */
  async create(opts: {
    file: Uint8Array | Buffer | Blob;
    filename?: string;
    model?: TranscriptionModel | string;
    language?: string;
    prompt?: string;
    responseFormat?: TranscriptionResponseFormat | string;
    temperature?: number;
    timestampGranularities?: Array<TimestampGranularity | string>;
    stream?: boolean;
    languages?: string[];
    keywords?: string[];
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const {
      file,
      filename,
      model,
      language,
      prompt,
      responseFormat,
      temperature,
      timestampGranularities,
      stream,
      languages,
      keywords,
      ...rest
    } = opts;

    const form = new FormData();
    const blob = file instanceof Blob ? file : new Blob([file]);
    form.append('file', blob, filename ?? 'audio.mp3');
    if (model !== undefined) form.append('model', String(model));
    if (language !== undefined) form.append('language', language);
    if (prompt !== undefined) form.append('prompt', prompt);
    if (responseFormat !== undefined) form.append('response_format', String(responseFormat));
    if (temperature !== undefined) form.append('temperature', String(temperature));
    for (const granularity of timestampGranularities ?? []) {
      form.append('timestamp_granularities[]', String(granularity));
    }
    if (stream !== undefined) form.append('stream', String(stream));
    for (const value of languages ?? []) form.append('languages[]', value);
    for (const value of keywords ?? []) form.append('keywords[]', value);
    for (const [key, value] of Object.entries(rest)) {
      if (value !== undefined) form.append(key, String(value));
    }

    const raw = await this.transport.requestRaw('POST', '/v1/audio/transcriptions', { form });
    const text = new TextDecoder().decode(raw);
    // `response_format` other than json/verbose_json answers with plain text.
    try {
      const parsed = JSON.parse(text) as unknown;
      if (parsed && typeof parsed === 'object' && !Array.isArray(parsed)) {
        return parsed as Record<string, unknown>;
      }
    } catch {
      // fall through
    }
    return { text };
  }
}

class AudioNamespace {
  readonly speech: Speech;
  readonly transcriptions: Transcriptions;
  constructor(transport: Transport) {
    this.speech = new Speech(transport);
    this.transcriptions = new Transcriptions(transport);
  }
}

class Models {
  constructor(private transport: Transport) {}

  /** List the models the token may call. */
  async list(): Promise<Record<string, unknown>> {
    return this.transport.request('GET', '/openai/models');
  }
}

class Tasks {
  constructor(private transport: Transport) {}

  async retrieve(opts: {
    id?: string;
    traceId?: string;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { id, traceId, ...rest } = opts;
    const body: Record<string, unknown> = { action: 'retrieve', ...rest };
    if (id !== undefined) body.id = id;
    if (traceId !== undefined) body.trace_id = traceId;
    return this.transport.request('POST', '/openai/tasks', { json: body });
  }

  async retrieveBatch(opts: {
    ids?: string[];
    traceIds?: string[];
    applicationId?: string;
    userId?: string;
    type?: string;
    offset?: number;
    limit?: number;
    createdAtMin?: number;
    createdAtMax?: number;
    [key: string]: unknown;
  } = {}): Promise<Record<string, unknown>> {
    const { ids, traceIds, applicationId, userId, type, offset, limit, createdAtMin, createdAtMax, ...rest } = opts;
    const body: Record<string, unknown> = { action: 'retrieve_batch', ...rest };
    if (ids !== undefined) body.ids = ids;
    if (traceIds !== undefined) body.trace_ids = traceIds;
    if (applicationId !== undefined) body.application_id = applicationId;
    if (userId !== undefined) body.user_id = userId;
    if (type !== undefined) body.type = type;
    if (offset !== undefined) body.offset = offset;
    if (limit !== undefined) body.limit = limit;
    if (createdAtMin !== undefined) body.created_at_min = createdAtMin;
    if (createdAtMax !== undefined) body.created_at_max = createdAtMax;
    return this.transport.request('POST', '/openai/tasks', { json: body });
  }
}

export class OpenAI {
  readonly chat: ChatNamespace;
  readonly responses: Responses;
  readonly images: Images;
  readonly embeddings: Embeddings;
  readonly audio: AudioNamespace;
  readonly models: Models;
  readonly tasks: Tasks;

  constructor(transport: Transport) {
    this.chat = new ChatNamespace(transport);
    this.responses = new Responses(transport);
    this.images = new Images(transport);
    this.embeddings = new Embeddings(transport);
    this.audio = new AudioNamespace(transport);
    this.models = new Models(transport);
    this.tasks = new Tasks(transport);
  }
}
