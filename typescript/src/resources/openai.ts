/** OpenAI-compatible facade resources. */

import { mapError, Transport } from '../runtime/transport';

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

class Models {
  constructor(private transport: Transport) {}

  async list(): Promise<Record<string, unknown>> {
    return this.transport.request('GET', '/openai/models');
  }
}

class Audio {
  constructor(private transport: Transport) {}

  async speech(opts: {
    input: string;
    model?: string;
    voice?: string;
    responseFormat?: string;
    speed?: number;
    [key: string]: unknown;
  }): Promise<ArrayBuffer> {
    const { input, responseFormat, ...rest } = opts;
    const body: Record<string, unknown> = { input, ...rest };
    if (responseFormat !== undefined) body.response_format = responseFormat;
    return this.fetchRaw('/v1/audio/speech', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify(body),
    });
  }

  async transcriptions(opts: {
    file: Buffer | Uint8Array;
    filename?: string;
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
      filename = 'audio',
      responseFormat,
      timestampGranularities,
      languages,
      keywords,
      ...rest
    } = opts;
    const form = new FormData();
    form.append('file', new Blob([file]), filename);
    for (const [key, value] of Object.entries(rest)) {
      if (value !== undefined) form.append(key, String(value));
    }
    if (responseFormat !== undefined) form.append('response_format', responseFormat);
    for (const value of timestampGranularities ?? []) form.append('timestamp_granularities[]', value);
    for (const value of languages ?? []) form.append('languages[]', value);
    for (const value of keywords ?? []) form.append('keywords[]', value);

    const data = await this.fetchResponse('/v1/audio/transcriptions', {
      method: 'POST',
      body: form,
    });
    const contentType = data.headers.get('content-type') ?? '';
    if (contentType.startsWith('text/plain')) return data.text();
    return (await data.json()) as Record<string, unknown>;
  }

  private async fetchRaw(path: string, init: RequestInit): Promise<ArrayBuffer> {
    const response = await this.fetchResponse(path, init);
    return response.arrayBuffer();
  }

  private async fetchResponse(path: string, init: RequestInit): Promise<Response> {
    const transport = this.transport as unknown as {
      baseURL: string;
      headers: Record<string, string>;
      timeout: number;
    };
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), transport.timeout);
    try {
      const headers = { ...transport.headers, ...(init.headers as Record<string, string> | undefined) };
      if (init.body instanceof FormData) delete headers['content-type'];
      const response = await fetch(`${transport.baseURL}${path}`, {
        ...init,
        headers,
        signal: controller.signal,
      });
      if (response.status >= 400) {
        const text = await response.text();
        let body: Record<string, unknown>;
        try {
          body = JSON.parse(text) as Record<string, unknown>;
        } catch {
          body = { error: { code: 'unknown', message: text } };
        }
        throw mapError(response.status, body);
      }
      return response;
    } finally {
      clearTimeout(timer);
    }
  }
}

class Realtime {
  constructor(private transport: Transport) {}

  url(opts: { model?: string } = {}): string {
    const transport = this.transport as unknown as { baseURL: string };
    const url = new URL('/v1/realtime', transport.baseURL);
    url.protocol = url.protocol === 'https:' ? 'wss:' : 'ws:';
    url.searchParams.set('model', opts.model ?? 'gpt-realtime-2.1');
    return url.toString();
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
  readonly models: Models;
  readonly audio: Audio;
  readonly realtime: Realtime;
  readonly embeddings: Embeddings;
  readonly tasks: Tasks;

  constructor(transport: Transport) {
    this.chat = new ChatNamespace(transport);
    this.responses = new Responses(transport);
    this.images = new Images(transport);
    this.models = new Models(transport);
    this.audio = new Audio(transport);
    this.realtime = new Realtime(transport);
    this.embeddings = new Embeddings(transport);
    this.tasks = new Tasks(transport);
  }
}
