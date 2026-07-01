/** Gemini AI resources. */

import { Transport } from '../runtime/transport';
import { TaskHandle } from '../runtime/tasks';

export type GeminiModel =
  | 'gemini-3.1-pro'
  | 'gemini-3.0-pro'
  | 'gemini-3.5-flash'
  | 'gemini-3-flash-preview'
  | 'gemini-2.5-pro'
  | 'gemini-2.5-flash'
  | 'gemini-2.5-flash-lite'
  | 'gemini-2.0-flash'
  | 'gemini-3.1-flash-lite-preview'
  | 'gemini-3.1-flash-image-preview'
  | 'gemini-2.5-flash-image'
  | 'gemini-3-pro-image-preview'
  | (string & {});

export type GeminiVideoModel = 'omni-flash' | (string & {});

class Completions {
  constructor(private transport: Transport) {}

  async create(opts: {
    model: GeminiModel;
    messages: Array<Record<string, unknown>>;
    stream?: false;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>>;
  async create(opts: {
    model: GeminiModel;
    messages: Array<Record<string, unknown>>;
    stream: true;
    [key: string]: unknown;
  }): Promise<AsyncGenerator<Record<string, unknown>>>;
  async create(opts: {
    model: GeminiModel;
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
    return this.transport.request('POST', '/gemini/chat/completions', { json: body });
  }

  private async *streamResponse(body: Record<string, unknown>): AsyncGenerator<Record<string, unknown>> {
    for await (const chunk of this.transport.requestStream('POST', '/gemini/chat/completions', { json: body })) {
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

class Models {
  constructor(private transport: Transport) {}

  async generateContent(
    model: string,
    opts: {
      contents: Array<Record<string, unknown>>;
      systemInstruction?: Record<string, unknown>;
      generationConfig?: Record<string, unknown>;
      tools?: Array<Record<string, unknown>>;
      toolConfig?: Record<string, unknown>;
      safetySettings?: Array<Record<string, unknown>>;
      cachedContent?: string;
      [key: string]: unknown;
    }
  ): Promise<Record<string, unknown>> {
    return this.transport.request('POST', `/v1beta/models/${model}:generateContent`, { json: opts });
  }

  async *streamGenerateContent(
    model: string,
    opts: {
      contents: Array<Record<string, unknown>>;
      systemInstruction?: Record<string, unknown>;
      generationConfig?: Record<string, unknown>;
      tools?: Array<Record<string, unknown>>;
      toolConfig?: Record<string, unknown>;
      safetySettings?: Array<Record<string, unknown>>;
      cachedContent?: string;
      [key: string]: unknown;
    }
  ): AsyncGenerator<Record<string, unknown>> {
    for await (const chunk of this.transport.requestStream(
      'POST',
      `/v1beta/models/${model}:streamGenerateContent`,
      { json: opts }
    )) {
      yield JSON.parse(chunk);
    }
  }
}

class Videos {
  constructor(private transport: Transport) {}

  async generate(opts: {
    prompt: string;
    model?: GeminiVideoModel;
    aspectRatio?: '16:9' | '9:16';
    imageUrls?: string[];
    callbackUrl?: string;
    async?: boolean;
    wait?: boolean;
    pollInterval?: number;
    maxWait?: number;
    [key: string]: unknown;
  }): Promise<Record<string, unknown> | TaskHandle> {
    const { prompt, model, aspectRatio, imageUrls, callbackUrl, wait: shouldWait, pollInterval, maxWait, ...rest } = opts;
    const body: Record<string, unknown> = { prompt, ...rest };
    if (model !== undefined) body.model = model;
    if (aspectRatio !== undefined) body.aspect_ratio = aspectRatio;
    if (imageUrls !== undefined) body.image_urls = imageUrls;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;

    const result = await this.transport.request('POST', '/gemini/videos', { json: body });
    const taskId = result.task_id as string | undefined;

    if (!taskId || (result.data && !shouldWait)) return result;

    const handle = new TaskHandle(taskId, '/gemini/tasks', this.transport);
    if (shouldWait) return handle.wait({ pollInterval, maxWait });
    return handle;
  }
}

class GeminiTasks {
  constructor(private transport: Transport) {}

  async retrieve(opts: {
    id?: string;
    ids?: string[];
    action?: 'retrieve' | 'retrieve_batch';
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { id, ids, action = 'retrieve', ...rest } = opts;
    const body: Record<string, unknown> = { action, ...rest };
    if (id !== undefined) body.id = id;
    if (ids !== undefined) body.ids = ids;
    return this.transport.request('POST', '/gemini/tasks', { json: body });
  }
}

export class Gemini {
  readonly chat: ChatNamespace;
  readonly models: Models;
  readonly videos: Videos;
  readonly tasks: GeminiTasks;

  constructor(transport: Transport) {
    this.chat = new ChatNamespace(transport);
    this.models = new Models(transport);
    this.videos = new Videos(transport);
    this.tasks = new GeminiTasks(transport);
  }
}
