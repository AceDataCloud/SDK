/** Gemini AI resources — chat completions, native generate content, and video generation. */

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
  | 'gemini-3.1-flash-image'
  | 'gemini-2.5-flash-image'
  | 'gemini-3-pro-image'
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

  async generateContent(opts: {
    model: GeminiModel;
    contents: Array<Record<string, unknown>>;
    systemInstruction?: Record<string, unknown>;
    generationConfig?: Record<string, unknown>;
    tools?: Array<Record<string, unknown>>;
    toolConfig?: Record<string, unknown>;
    safetySettings?: Array<Record<string, unknown>>;
    cachedContent?: string;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { model, contents, systemInstruction, generationConfig, tools, toolConfig, safetySettings, cachedContent, ...rest } = opts;
    const body: Record<string, unknown> = { contents, ...rest };
    if (systemInstruction !== undefined) body.systemInstruction = systemInstruction;
    if (generationConfig !== undefined) body.generationConfig = generationConfig;
    if (tools !== undefined) body.tools = tools;
    if (toolConfig !== undefined) body.toolConfig = toolConfig;
    if (safetySettings !== undefined) body.safetySettings = safetySettings;
    if (cachedContent !== undefined) body.cachedContent = cachedContent;
    return this.transport.request('POST', `/v1beta/models/${model}:generateContent`, { json: body });
  }

  async *streamGenerateContent(opts: {
    model: GeminiModel;
    contents: Array<Record<string, unknown>>;
    systemInstruction?: Record<string, unknown>;
    generationConfig?: Record<string, unknown>;
    tools?: Array<Record<string, unknown>>;
    toolConfig?: Record<string, unknown>;
    safetySettings?: Array<Record<string, unknown>>;
    cachedContent?: string;
    [key: string]: unknown;
  }): AsyncGenerator<Record<string, unknown>> {
    const { model, contents, systemInstruction, generationConfig, tools, toolConfig, safetySettings, cachedContent, ...rest } = opts;
    const body: Record<string, unknown> = { contents, ...rest };
    if (systemInstruction !== undefined) body.systemInstruction = systemInstruction;
    if (generationConfig !== undefined) body.generationConfig = generationConfig;
    if (tools !== undefined) body.tools = tools;
    if (toolConfig !== undefined) body.toolConfig = toolConfig;
    if (safetySettings !== undefined) body.safetySettings = safetySettings;
    if (cachedContent !== undefined) body.cachedContent = cachedContent;
    for await (const chunk of this.transport.requestStream('POST', `/v1beta/models/${model}:streamGenerateContent`, { json: body })) {
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

export class Gemini {
  readonly chat: ChatNamespace;
  readonly models: Models;
  readonly videos: Videos;

  constructor(transport: Transport) {
    this.chat = new ChatNamespace(transport);
    this.models = new Models(transport);
    this.videos = new Videos(transport);
  }
}
