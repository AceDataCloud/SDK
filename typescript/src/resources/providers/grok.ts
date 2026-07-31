/**
 * Grok (grok) — generated from the platform OpenAPI spec.
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

export type GrokChatModel = 'grok-4.5' | 'grok-4' | 'grok-3';
export type GrokVideoModel =
  | 'grok-imagine-video-1.5-fast:reverse'
  | 'grok-imagine-video:reverse'
  | 'grok-imagine-video:official'
  | 'grok-imagine-video-1.5:official'
  | 'grok-imagine-video';
export type GrokAspectRatio = '1:1' | '16:9' | '9:16' | '4:3' | '3:4' | '3:2' | '2:3';
export type GrokResolution = '480p' | '720p' | '1080p';

export interface GrokChatOptions {
  model: GrokChatModel;
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

class GrokChatCompletions {
  constructor(private transport: Transport) {}

  async create(opts: GrokChatOptions): Promise<unknown> {
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
    return this.transport.request('POST', '/grok/chat/completions', { json: body });
  }
}

class GrokChat {
  readonly completions: GrokChatCompletions;
  constructor(transport: Transport) {
    this.completions = new GrokChatCompletions(transport);
  }
}

class GrokVideos {
  constructor(private transport: Transport) {}

  async generate(opts: {
    prompt?: string;
    model?: GrokVideoModel;
    imageUrl?: string;
    referenceImageUrls?: string[];
    aspectRatio?: GrokAspectRatio;
    resolution?: GrokResolution;
    duration?: number;
    async?: boolean;
    callbackUrl?: string;
    wait?: boolean;
    pollInterval?: number;
    maxWait?: number;
  } = {}): Promise<TaskHandle> {
    const body: Record<string, unknown> = {};
    if (opts.prompt !== undefined) body.prompt = opts.prompt;
    if (opts.model !== undefined) body.model = opts.model;
    if (opts.imageUrl !== undefined) body.image_url = opts.imageUrl;
    if (opts.referenceImageUrls !== undefined) body.reference_image_urls = opts.referenceImageUrls;
    if (opts.aspectRatio !== undefined) body.aspect_ratio = opts.aspectRatio;
    if (opts.resolution !== undefined) body.resolution = opts.resolution;
    if (opts.duration !== undefined) body.duration = opts.duration;
    if (opts.callbackUrl !== undefined) body.callback_url = opts.callbackUrl;
    body.async = opts.async ?? true;
    const result = (await this.transport.request('POST', '/grok/videos', { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), '/grok/tasks', this.transport, result);
    if (opts.wait) {
      await handle.wait({ pollInterval: opts.pollInterval, maxWait: opts.maxWait });
    }
    return handle;
  }
}

export class Grok {
  readonly chat: GrokChat;
  readonly videos: GrokVideos;

  constructor(transport: Transport) {
    this.chat = new GrokChat(transport);
    this.videos = new GrokVideos(transport);
  }
}
