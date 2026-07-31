/**
 * Gemini (gemini) — generated from the platform OpenAPI spec.
 *
 * Do not edit by hand: run `python scripts/generate_providers.py`. Parameter
 * names, types, enums and required-ness all come from the live spec.
 */

import { Transport } from '../../runtime/transport';
import { TaskHandle } from '../../runtime/tasks';

function taskId(result: Record<string, unknown>): string {
  if (typeof result?.task_id === 'string') return result.task_id;
  const data = result?.data as Record<string, unknown> | undefined;
  if (data && typeof data.task_id === 'string') return data.task_id;
  return typeof result?.id === 'string' ? result.id : '';
}

export type GeminiChatModel =
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
  | 'gemini-3-pro-image';
export type GeminiVideoModel = 'omni-flash';
export type GeminiAspectRatio = '16:9' | '9:16';
export type GeminiResolution = '720p' | '1080p';

export interface GeminiChatOptions {
  model: GeminiChatModel;
  messages: Record<string, unknown>[];
  stream?: boolean;
  temperature?: number;
  topP?: number;
  maxTokens?: number;
  maxCompletionTokens?: number;
  frequencyPenalty?: number;
  presencePenalty?: number;
  n?: number;
  stop?: unknown;
  seed?: number;
  logprobs?: boolean;
  topLogprobs?: number;
  streamOptions?: Record<string, unknown>;
  parallelToolCalls?: boolean;
  user?: string;
  reasoningEffort?: 'minimal' | 'low' | 'medium' | 'high';
  serviceTier?: 'auto' | 'default' | 'flex' | 'scale' | 'priority';
  store?: boolean;
  metadata?: Record<string, unknown>;
  logitBias?: Record<string, unknown>;
  modalities?: unknown[];
  audio?: Record<string, unknown>;
  prediction?: Record<string, unknown>;
  webSearchOptions?: Record<string, unknown>;
  tools?: unknown[];
  toolChoice?: unknown;
  responseFormat?: Record<string, unknown>;
}

class GeminiChatCompletions {
  constructor(private transport: Transport) {}

  async create(opts: GeminiChatOptions): Promise<unknown> {
    const body: Record<string, unknown> = { model: opts.model, messages: opts.messages };
    if (opts.stream !== undefined) body.stream = opts.stream;
    if (opts.temperature !== undefined) body.temperature = opts.temperature;
    if (opts.topP !== undefined) body.top_p = opts.topP;
    if (opts.maxTokens !== undefined) body.max_tokens = opts.maxTokens;
    if (opts.maxCompletionTokens !== undefined) body.max_completion_tokens = opts.maxCompletionTokens;
    if (opts.frequencyPenalty !== undefined) body.frequency_penalty = opts.frequencyPenalty;
    if (opts.presencePenalty !== undefined) body.presence_penalty = opts.presencePenalty;
    if (opts.n !== undefined) body.n = opts.n;
    if (opts.stop !== undefined) body.stop = opts.stop;
    if (opts.seed !== undefined) body.seed = opts.seed;
    if (opts.logprobs !== undefined) body.logprobs = opts.logprobs;
    if (opts.topLogprobs !== undefined) body.top_logprobs = opts.topLogprobs;
    if (opts.streamOptions !== undefined) body.stream_options = opts.streamOptions;
    if (opts.parallelToolCalls !== undefined) body.parallel_tool_calls = opts.parallelToolCalls;
    if (opts.user !== undefined) body.user = opts.user;
    if (opts.reasoningEffort !== undefined) body.reasoning_effort = opts.reasoningEffort;
    if (opts.serviceTier !== undefined) body.service_tier = opts.serviceTier;
    if (opts.store !== undefined) body.store = opts.store;
    if (opts.metadata !== undefined) body.metadata = opts.metadata;
    if (opts.logitBias !== undefined) body.logit_bias = opts.logitBias;
    if (opts.modalities !== undefined) body.modalities = opts.modalities;
    if (opts.audio !== undefined) body.audio = opts.audio;
    if (opts.prediction !== undefined) body.prediction = opts.prediction;
    if (opts.webSearchOptions !== undefined) body.web_search_options = opts.webSearchOptions;
    if (opts.tools !== undefined) body.tools = opts.tools;
    if (opts.toolChoice !== undefined) body.tool_choice = opts.toolChoice;
    if (opts.responseFormat !== undefined) body.response_format = opts.responseFormat;
    return this.transport.request('POST', '/gemini/chat/completions', { json: body });
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

  async generate(opts: {
    prompt: string;
    model?: GeminiVideoModel;
    aspectRatio?: GeminiAspectRatio;
    resolution?: GeminiResolution;
    imageUrls?: string[];
    videoUrls?: string[];
    async?: boolean;
    callbackUrl?: string;
    wait?: boolean;
    pollInterval?: number;
    maxWait?: number;
  }): Promise<TaskHandle> {
    const body: Record<string, unknown> = { prompt: opts.prompt };
    if (opts.model !== undefined) body.model = opts.model;
    if (opts.aspectRatio !== undefined) body.aspect_ratio = opts.aspectRatio;
    if (opts.resolution !== undefined) body.resolution = opts.resolution;
    if (opts.imageUrls !== undefined) body.image_urls = opts.imageUrls;
    if (opts.videoUrls !== undefined) body.video_urls = opts.videoUrls;
    if (opts.callbackUrl !== undefined) body.callback_url = opts.callbackUrl;
    body.async = opts.async ?? true;
    const result = (await this.transport.request('POST', '/gemini/videos', { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), '/gemini/tasks', this.transport, result);
    if (opts.wait) {
      await handle.wait({ pollInterval: opts.pollInterval, maxWait: opts.maxWait });
    }
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

  async generateContent(opts: {
    model: string;
    contents: unknown[];
    systemInstruction?: Record<string, unknown>;
    generationConfig?: Record<string, unknown>;
    tools?: unknown[];
    toolConfig?: Record<string, unknown>;
    safetySettings?: unknown[];
    cachedContent?: string;
  }): Promise<unknown> {
    const body: Record<string, unknown> = { contents: opts.contents };
    if (opts.systemInstruction !== undefined) body.systemInstruction = opts.systemInstruction;
    if (opts.generationConfig !== undefined) body.generationConfig = opts.generationConfig;
    if (opts.tools !== undefined) body.tools = opts.tools;
    if (opts.toolConfig !== undefined) body.toolConfig = opts.toolConfig;
    if (opts.safetySettings !== undefined) body.safetySettings = opts.safetySettings;
    if (opts.cachedContent !== undefined) body.cachedContent = opts.cachedContent;
    return this.transport.request('POST', `/v1beta/models/${opts.model}:generateContent`, { json: body });
  }

  async streamGenerateContent(opts: {
    model: string;
    contents: unknown[];
    systemInstruction?: Record<string, unknown>;
    generationConfig?: Record<string, unknown>;
    tools?: unknown[];
    toolConfig?: Record<string, unknown>;
    safetySettings?: unknown[];
    cachedContent?: string;
  }): Promise<unknown> {
    const body: Record<string, unknown> = { contents: opts.contents };
    if (opts.systemInstruction !== undefined) body.systemInstruction = opts.systemInstruction;
    if (opts.generationConfig !== undefined) body.generationConfig = opts.generationConfig;
    if (opts.tools !== undefined) body.tools = opts.tools;
    if (opts.toolConfig !== undefined) body.toolConfig = opts.toolConfig;
    if (opts.safetySettings !== undefined) body.safetySettings = opts.safetySettings;
    if (opts.cachedContent !== undefined) body.cachedContent = opts.cachedContent;
    return this.transport.request('POST', `/v1beta/models/${opts.model}:streamGenerateContent`, { json: body });
  }
}
