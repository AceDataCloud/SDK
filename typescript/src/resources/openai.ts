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
    outputFormat?: string;
    outputCompression?: number;
    quality?: string;
    size?: string;
    responseFormat?: string;
    callbackUrl?: string;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { image, prompt, inputFidelity, outputFormat, outputCompression, responseFormat, callbackUrl, ...rest } = opts;
    const body: Record<string, unknown> = { image, prompt, ...rest };
    if (inputFidelity !== undefined) body.input_fidelity = inputFidelity;
    if (outputFormat !== undefined) body.output_format = outputFormat;
    if (outputCompression !== undefined) body.output_compression = outputCompression;
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

export class OpenAI {
  readonly chat: ChatNamespace;
  readonly responses: Responses;
  readonly images: Images;
  readonly embeddings: Embeddings;

  constructor(transport: Transport) {
    this.chat = new ChatNamespace(transport);
    this.responses = new Responses(transport);
    this.images = new Images(transport);
    this.embeddings = new Embeddings(transport);
  }
}
