/** Gemini resources — chat completions, video generation, and native API. */

import { Transport } from '../runtime/transport';
import { TaskHandle } from '../runtime/tasks';

export const GEMINI_CHAT_MODELS = [
  'gemini-3.1-pro',
  'gemini-3.0-pro',
  'gemini-3.5-flash',
  'gemini-3-flash-preview',
  'gemini-2.5-pro',
  'gemini-2.5-flash',
  'gemini-2.5-flash-lite',
  'gemini-2.0-flash',
  'gemini-3.1-flash-lite-preview',
  'gemini-3.1-flash-image',
  'gemini-2.5-flash-image',
  'gemini-3-pro-image',
] as const;
export type GeminiChatModel = (typeof GEMINI_CHAT_MODELS)[number];

export type GeminiVideoModel = 'omni-flash';

function taskId(result: Record<string, unknown>): string {
  if (typeof result?.task_id === 'string') return result.task_id;
  const data = result?.data as Record<string, unknown> | undefined;
  if (data && typeof data.task_id === 'string') return data.task_id;
  return typeof result?.id === 'string' ? result.id : '';
}

class GeminiCompletions {
  constructor(private transport: Transport) {}

  async create(opts: {
    model: GeminiChatModel | string;
    messages: Array<Record<string, unknown>>;
    stream?: false;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>>;
  async create(opts: {
    model: GeminiChatModel | string;
    messages: Array<Record<string, unknown>>;
    stream: true;
    [key: string]: unknown;
  }): Promise<AsyncGenerator<Record<string, unknown>>>;
  async create(opts: {
    model: GeminiChatModel | string;
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

class GeminiChat {
  readonly completions: GeminiCompletions;
  constructor(transport: Transport) {
    this.completions = new GeminiCompletions(transport);
  }
}

export class Gemini {
  readonly chat: GeminiChat;

  constructor(private transport: Transport) {
    this.chat = new GeminiChat(transport);
  }

  async generate(opts: {
    prompt: string;
    model?: GeminiVideoModel | string;
    aspectRatio?: '16:9' | '9:16';
    resolution?: '720p' | '1080p';
    imageUrls?: string[];
    videoUrls?: string[];
    callbackUrl?: string;
    async?: boolean;
    [key: string]: unknown;
  }): Promise<TaskHandle> {
    const { prompt, model, aspectRatio, resolution, imageUrls, videoUrls, callbackUrl, ...rest } = opts;
    const body: Record<string, unknown> = { prompt, ...rest };
    if (model !== undefined) body.model = model;
    if (aspectRatio !== undefined) body.aspect_ratio = aspectRatio;
    if (resolution !== undefined) body.resolution = resolution;
    if (imageUrls !== undefined) body.image_urls = imageUrls;
    if (videoUrls !== undefined) body.video_urls = videoUrls;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    const result = (await this.transport.request('POST', '/gemini/videos', { json: body })) as Record<string, unknown>;
    return new TaskHandle(taskId(result), '/gemini/tasks', this.transport, result);
  }

  async generateContent(opts: {
    model: string;
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
    model: string;
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
