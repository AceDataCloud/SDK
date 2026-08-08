/** Gemini provider resource. */

import { Transport } from '../../runtime/transport';
import { TaskHandle } from '../../runtime/tasks';

export type GeminiChatModel =
  | 'gemini-3.1-pro'
  | 'gemini-3.0-pro'
  | 'gemini-3.5-flash'
  | 'gemini-3-flash-preview'
  | 'gemini-2.5-pro'
  | 'gemini-2.5-flash'
  | 'gemini-2.5-flash-lite'
  | 'gemini-2.0-flash'
  | 'gemini-3.1-flash-lite-preview';
export type GeminiNativeModel =
  | 'gemini-2.0-flash'
  | 'gemini-2.5-flash'
  | 'gemini-2.5-flash-lite'
  | 'gemini-2.5-pro'
  | 'gemini-3-flash-preview'
  | 'gemini-3.5-flash'
  | 'gemini-3.0-pro'
  | 'gemini-3.1-pro'
  | 'gemini-3.1-flash-lite-preview'
  | 'gemini-3.1-flash-image'
  | 'gemini-2.5-flash-image'
  | 'gemini-3-pro-image';
export type GeminiVideoModel = 'omni-flash';

type ReasoningEffort = 'minimal' | 'low' | 'medium' | 'high';
type ServiceTier = 'auto' | 'default' | 'flex' | 'scale' | 'priority';

export interface GeminiChatCompletionOptions {
  model: GeminiChatModel;
  messages: Array<Record<string, unknown>>;
  n?: number;
  stream?: boolean;
  maxTokens?: number;
  temperature?: number;
  responseFormat?: unknown;
  topP?: number;
  frequencyPenalty?: number;
  presencePenalty?: number;
  seed?: number;
  stop?: unknown;
  maxCompletionTokens?: number;
  logprobs?: boolean;
  topLogprobs?: number;
  streamOptions?: Record<string, unknown>;
  parallelToolCalls?: boolean;
  user?: string;
  reasoningEffort?: ReasoningEffort;
  serviceTier?: ServiceTier;
  store?: boolean;
  metadata?: Record<string, unknown>;
  logitBias?: Record<string, unknown>;
  modalities?: unknown[];
  audio?: Record<string, unknown>;
  prediction?: Record<string, unknown>;
  webSearchOptions?: Record<string, unknown>;
  tools?: unknown[];
  toolChoice?: unknown;
  [key: string]: unknown;
}

export interface GeminiVideoOptions {
  prompt: string;
  model?: GeminiVideoModel;
  aspectRatio?: '16:9' | '9:16';
  resolution?: '720p' | '1080p';
  imageUrls?: string[];
  videoUrls?: string[];
  async?: boolean;
  wait?: boolean;
  pollInterval?: number;
  maxWait?: number;
  callbackUrl?: string;
  [key: string]: unknown;
}

export interface GeminiContentOptions {
  model: GeminiNativeModel;
  contents: Array<Record<string, unknown>>;
  systemInstruction?: Record<string, unknown>;
  generationConfig?: Record<string, unknown>;
  tools?: unknown[];
  toolConfig?: Record<string, unknown>;
  safetySettings?: unknown[];
  cachedContent?: string;
  [key: string]: unknown;
}

const CHAT_KEYS = new Set([
  'model', 'messages', 'n', 'stream', 'maxTokens', 'temperature', 'responseFormat', 'topP', 'frequencyPenalty',
  'presencePenalty', 'seed', 'stop', 'maxCompletionTokens', 'logprobs', 'topLogprobs', 'streamOptions',
  'parallelToolCalls', 'user', 'reasoningEffort', 'serviceTier', 'store', 'metadata', 'logitBias', 'modalities',
  'audio', 'prediction', 'webSearchOptions', 'tools', 'toolChoice',
]);
const VIDEO_KEYS = new Set([
  'prompt', 'model', 'aspectRatio', 'resolution', 'imageUrls', 'videoUrls', 'async', 'wait', 'pollInterval', 'maxWait',
  'callbackUrl',
]);
const CONTENT_KEYS = new Set([
  'model', 'contents', 'systemInstruction', 'generationConfig', 'tools', 'toolConfig', 'safetySettings', 'cachedContent',
]);

function taskId(result: Record<string, unknown>): string {
  if (typeof result?.task_id === 'string') return result.task_id;
  const data = result?.data as Record<string, unknown> | undefined;
  if (data && typeof data.task_id === 'string') return data.task_id;
  return typeof result?.id === 'string' ? result.id : '';
}

function copyExtra(body: Record<string, unknown>, options: Record<string, unknown>, known: Set<string>): void {
  for (const [key, value] of Object.entries(options)) {
    if (!known.has(key) && value !== undefined) body[key] = value;
  }
}

function setIfDefined(body: Record<string, unknown>, key: string, value: unknown): void {
  if (value !== undefined) body[key] = value;
}

function chatBody(options: GeminiChatCompletionOptions): Record<string, unknown> {
  const body: Record<string, unknown> = { model: options.model, messages: options.messages, stream: options.stream ?? false };
  setIfDefined(body, 'n', options.n ?? 1);
  setIfDefined(body, 'max_tokens', options.maxTokens);
  setIfDefined(body, 'temperature', options.temperature ?? 1);
  setIfDefined(body, 'response_format', options.responseFormat);
  setIfDefined(body, 'top_p', options.topP ?? 1);
  setIfDefined(body, 'frequency_penalty', options.frequencyPenalty ?? 0);
  setIfDefined(body, 'presence_penalty', options.presencePenalty ?? 0);
  setIfDefined(body, 'seed', options.seed);
  setIfDefined(body, 'stop', options.stop);
  setIfDefined(body, 'max_completion_tokens', options.maxCompletionTokens);
  setIfDefined(body, 'logprobs', options.logprobs ?? false);
  setIfDefined(body, 'top_logprobs', options.topLogprobs);
  setIfDefined(body, 'stream_options', options.streamOptions);
  setIfDefined(body, 'parallel_tool_calls', options.parallelToolCalls ?? true);
  setIfDefined(body, 'user', options.user);
  setIfDefined(body, 'reasoning_effort', options.reasoningEffort ?? 'medium');
  setIfDefined(body, 'service_tier', options.serviceTier ?? 'auto');
  setIfDefined(body, 'store', options.store ?? false);
  setIfDefined(body, 'metadata', options.metadata);
  setIfDefined(body, 'logit_bias', options.logitBias);
  setIfDefined(body, 'modalities', options.modalities);
  setIfDefined(body, 'audio', options.audio);
  setIfDefined(body, 'prediction', options.prediction);
  setIfDefined(body, 'web_search_options', options.webSearchOptions);
  setIfDefined(body, 'tools', options.tools);
  setIfDefined(body, 'tool_choice', options.toolChoice);
  copyExtra(body, options, CHAT_KEYS);
  return body;
}

function videoBody(options: GeminiVideoOptions): Record<string, unknown> {
  const body: Record<string, unknown> = {
    prompt: options.prompt,
    model: options.model ?? 'omni-flash',
    aspect_ratio: options.aspectRatio ?? '16:9',
    resolution: options.resolution ?? '720p',
    async: options.async ?? true,
  };
  setIfDefined(body, 'image_urls', options.imageUrls);
  setIfDefined(body, 'video_urls', options.videoUrls);
  setIfDefined(body, 'callback_url', options.callbackUrl);
  copyExtra(body, options, VIDEO_KEYS);
  return body;
}

function contentBody(options: GeminiContentOptions): Record<string, unknown> {
  const body: Record<string, unknown> = { contents: options.contents };
  setIfDefined(body, 'systemInstruction', options.systemInstruction);
  setIfDefined(body, 'generationConfig', options.generationConfig);
  setIfDefined(body, 'tools', options.tools);
  setIfDefined(body, 'toolConfig', options.toolConfig);
  setIfDefined(body, 'safetySettings', options.safetySettings);
  setIfDefined(body, 'cachedContent', options.cachedContent);
  copyExtra(body, options, CONTENT_KEYS);
  return body;
}

class GeminiChatCompletions {
  constructor(private transport: Transport) {}

  async create(options: GeminiChatCompletionOptions): Promise<Record<string, unknown> | AsyncGenerator<Record<string, unknown>>> {
    const body = chatBody(options);
    if (body.stream) return this.stream(body);
    return this.transport.request('POST', '/gemini/chat/completions', { json: body });
  }

  private async *stream(body: Record<string, unknown>): AsyncGenerator<Record<string, unknown>> {
    for await (const chunk of this.transport.requestStream('POST', '/gemini/chat/completions', { json: body })) {
      yield JSON.parse(chunk) as Record<string, unknown>;
    }
  }
}

class GeminiChat {
  readonly completions: GeminiChatCompletions;
  constructor(transport: Transport) {
    this.completions = new GeminiChatCompletions(transport);
  }
}

class GeminiVideos {
  constructor(private transport: Transport) {}

  async generate(options: GeminiVideoOptions): Promise<TaskHandle> {
    const result = (await this.transport.request('POST', '/gemini/videos', { json: videoBody(options) })) as Record<
      string,
      unknown
    >;
    const handle = new TaskHandle(taskId(result), '/gemini/tasks', this.transport, result);
    if (options.wait) await handle.wait({ pollInterval: options.pollInterval, maxWait: options.maxWait });
    return handle;
  }
}

export class Gemini {
  readonly chat: GeminiChat;
  readonly videos: GeminiVideos;

  constructor(private transport: Transport) {
    this.chat = new GeminiChat(transport);
    this.videos = new GeminiVideos(transport);
  }

  async generateContent(options: GeminiContentOptions): Promise<Record<string, unknown>> {
    const path = `/v1beta/models/${encodeURIComponent(options.model)}:generateContent`;
    return this.transport.request('POST', path, { json: contentBody(options) });
  }

  async *streamGenerateContent(options: GeminiContentOptions): AsyncGenerator<Record<string, unknown>> {
    const path = `/v1beta/models/${encodeURIComponent(options.model)}:streamGenerateContent?alt=sse`;
    for await (const chunk of this.transport.requestStream('POST', path, { json: contentBody(options) })) {
      yield JSON.parse(chunk) as Record<string, unknown>;
    }
  }
}
