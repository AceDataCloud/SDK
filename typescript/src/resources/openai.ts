/** OpenAI-compatible facade resources. */

import { Transport } from '../runtime/transport';
import { mapError } from '../runtime/transport';
import { TimeoutError } from '../runtime/errors';

function isAbortError(error: unknown): boolean {
  return typeof error === 'object' && error !== null && 'name' in error && error.name === 'AbortError';
}

async function rawRequest(
  transport: Transport,
  method: string,
  path: string,
  opts: { json?: Record<string, unknown>; headers?: Record<string, string> } = {}
): Promise<Response> {
  const internal = transport as unknown as {
    baseURL: string;
    headers: Record<string, string>;
    timeout: number;
  };
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), internal.timeout);
  try {
    const resp = await fetch(`${internal.baseURL}${path}`, {
      method,
      headers: { ...internal.headers, ...(opts.headers ?? {}) },
      body: opts.json ? JSON.stringify(opts.json) : undefined,
      signal: controller.signal,
    });
    if (resp.status >= 400) {
      const text = await resp.text();
      let body: Record<string, unknown>;
      try {
        body = JSON.parse(text) as Record<string, unknown>;
      } catch {
        body = { error: { code: 'unknown', message: text } };
      }
      throw mapError(resp.status, body);
    }
    return resp;
  } catch (error) {
    if (isAbortError(error)) {
      throw new TimeoutError({ message: 'Request timed out', statusCode: 0, code: 'timeout' });
    }
    throw error;
  } finally {
    clearTimeout(timer);
  }
}

function buildRealtimeURL(
  transport: Transport,
  params: Record<string, string | number | boolean | undefined>
): string {
  const internal = transport as unknown as { baseURL: string };
  const url = new URL('/v1/realtime', internal.baseURL);
  url.protocol = url.protocol === 'https:' ? 'wss:' : 'ws:';
  for (const [key, value] of Object.entries(params)) {
    if (value !== undefined) {
      url.searchParams.set(key, typeof value === 'boolean' ? String(value) : `${value}`);
    }
  }
  return url.toString();
}

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

class Models {
  constructor(private transport: Transport) {}

  async list(): Promise<Record<string, unknown>> {
    return this.transport.request('GET', '/openai/models');
  }
}

class AudioNamespace {
  constructor(private transport: Transport) {}

  async speech(opts: {
    input: string;
    model?: string;
    voice?: string;
    responseFormat?: string;
    speed?: number;
    [key: string]: unknown;
  }): Promise<Uint8Array> {
    const { input, model, voice, responseFormat, speed, ...rest } = opts;
    const body: Record<string, unknown> = { input, ...rest };
    if (model !== undefined) body.model = model;
    if (voice !== undefined) body.voice = voice;
    if (responseFormat !== undefined) body.response_format = responseFormat;
    if (speed !== undefined) body.speed = speed;
    const resp = await rawRequest(this.transport, 'POST', '/v1/audio/speech', {
      json: body,
      headers: { accept: 'audio/mpeg' },
    });
    return new Uint8Array(await resp.arrayBuffer());
  }

  async transcriptions(opts: {
    file: string;
    model?: string;
    language?: string;
    prompt?: string;
    responseFormat?: string;
    temperature?: number;
    timestampGranularities?: string[];
    stream?: boolean;
    languages?: string[];
    keywords?: string[];
    [key: string]: unknown;
  }): Promise<Record<string, unknown> | string> {
    const {
      file,
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
    const body: Record<string, unknown> = { file, ...rest };
    if (model !== undefined) body.model = model;
    if (language !== undefined) body.language = language;
    if (prompt !== undefined) body.prompt = prompt;
    if (responseFormat !== undefined) body.response_format = responseFormat;
    if (temperature !== undefined) body.temperature = temperature;
    if (timestampGranularities !== undefined) body['timestamp_granularities[]'] = timestampGranularities;
    if (stream !== undefined) body.stream = stream;
    if (languages !== undefined) body['languages[]'] = languages;
    if (keywords !== undefined) body['keywords[]'] = keywords;
    if (responseFormat === 'text' || responseFormat === 'srt' || responseFormat === 'vtt') {
      const resp = await rawRequest(this.transport, 'POST', '/v1/audio/transcriptions', {
        json: body,
        headers: { accept: 'text/plain' },
      });
      return resp.text();
    }
    return this.transport.request('POST', '/v1/audio/transcriptions', { json: body });
  }
}

class Realtime {
  constructor(private transport: Transport) {}

  url(opts: { model: string; [key: string]: string | number | boolean | undefined }): string {
    return buildRealtimeURL(this.transport, opts);
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
  readonly models: Models;
  readonly audio: AudioNamespace;
  readonly realtime: Realtime;
  readonly tasks: Tasks;

  constructor(transport: Transport) {
    this.chat = new ChatNamespace(transport);
    this.responses = new Responses(transport);
    this.images = new Images(transport);
    this.embeddings = new Embeddings(transport);
    this.models = new Models(transport);
    this.audio = new AudioNamespace(transport);
    this.realtime = new Realtime(transport);
    this.tasks = new Tasks(transport);
  }
}
