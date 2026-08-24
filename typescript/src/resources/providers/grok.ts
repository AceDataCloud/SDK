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

export interface GrokCompletionsOptions {
  /** Grok Chat Completions Model */
  model: "grok-4.5" | "grok-4" | "grok-3";
  /** Grok Chat Completions Messages 4 */
  messages: Array<Record<string, unknown>>;
  /** Grok Chat Completions N */
  n?: number;
  /** Grok Chat Completions Stream */
  stream?: boolean;
  /** Grok Chat Completions Max Tokens */
  maxTokens?: number;
  /** Grok Chat Completions Temperature */
  temperature?: number;
  /** Grok Chat Completions Top P */
  topP?: number;
  /** Grok Chat Completions Frequency Penalty */
  frequencyPenalty?: number;
  /** Grok Chat Completions Presence Penalty */
  presencePenalty?: number;
  /** Grok Chat Completions Seed */
  seed?: number;
  /** Grok Chat Completions Stop 3 */
  stop?: unknown;
  /** Grok Chat Completions Max Completion Tokens */
  maxCompletionTokens?: number;
  /** Grok Chat Completions Logprobs */
  logprobs?: boolean;
  /** Grok Chat Completions Top Logprobs */
  topLogprobs?: number;
  /** Grok Chat Completions Stream Options */
  streamOptions?: Record<string, unknown>;
  /** Grok Chat Completions Parallel Tool Calls */
  parallelToolCalls?: boolean;
  /** Grok Chat Completions User */
  user?: string;
  /** Grok Chat Completions Reasoning Effort */
  reasoningEffort?: "minimal" | "low" | "medium" | "high";
  /** Grok Chat Completions Service Tier */
  serviceTier?: "auto" | "default" | "flex" | "scale" | "priority";
  /** Grok Chat Completions Store */
  store?: boolean;
  /** Grok Chat Completions Metadata */
  metadata?: Record<string, unknown>;
  /** Grok Chat Completions Logit Bias */
  logitBias?: Record<string, unknown>;
  /** Grok Chat Completions Modalities */
  modalities?: string[];
  /** Grok Chat Completions Audio */
  audio?: Record<string, unknown>;
  /** Grok Chat Completions Prediction 3 */
  prediction?: Record<string, unknown>;
  /** Grok Chat Completions Web Search Options */
  webSearchOptions?: Record<string, unknown>;
  /** Grok Chat Completions Tools */
  tools?: Array<Record<string, unknown>>;
  /** Grok Chat Completions Tool Choice 3 */
  toolChoice?: unknown;
  /** Grok Chat Completions Response Format 4 */
  responseFormat?: unknown;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

export interface GrokGenerateOptions {
  /** Grok Videos Prompt */
  prompt?: string;
  /** Grok Videos Model */
  model?: "grok-imagine-video-1.5-fast:reverse" | "grok-imagine-video:reverse" | "grok-imagine-video:official" | "grok-imagine-video-1.5:official" | "grok-imagine-video";
  /** Grok Videos Image Url */
  imageUrl?: string;
  /** Grok Videos Reference Image Urls */
  referenceImageUrls?: string[];
  /** Grok Videos Aspect Ratio */
  aspectRatio?: "1:1" | "16:9" | "9:16" | "4:3" | "3:4" | "3:2" | "2:3";
  /** Grok Videos Resolution */
  resolution?: "480p" | "720p" | "1080p";
  /** Grok Videos Duration */
  duration?: number;
  /** Submit asynchronously and poll. Defaults to true. */
  async?: boolean;
  /** Wait for completion before returning the handle. */
  wait?: boolean;
  pollInterval?: number;
  maxWait?: number;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

/** grok client. */
export class Grok {
  constructor(private transport: Transport) {}

  /** Grok Chat Completions */
  async completions(options: GrokCompletionsOptions): Promise<Record<string, unknown>> {
    const body: Record<string, unknown> = {};
    body["model"] = options.model;
    body["messages"] = options.messages;
    body["n"] = options.n ?? 1;
    body["stream"] = options.stream ?? false;
    if (options.maxTokens !== undefined) body["max_tokens"] = options.maxTokens;
    body["temperature"] = options.temperature ?? 1;
    body["top_p"] = options.topP ?? 1;
    body["frequency_penalty"] = options.frequencyPenalty ?? 0;
    body["presence_penalty"] = options.presencePenalty ?? 0;
    if (options.seed !== undefined) body["seed"] = options.seed;
    if (options.stop !== undefined) body["stop"] = options.stop;
    if (options.maxCompletionTokens !== undefined) body["max_completion_tokens"] = options.maxCompletionTokens;
    body["logprobs"] = options.logprobs ?? false;
    if (options.topLogprobs !== undefined) body["top_logprobs"] = options.topLogprobs;
    if (options.streamOptions !== undefined) body["stream_options"] = options.streamOptions;
    body["parallel_tool_calls"] = options.parallelToolCalls ?? true;
    if (options.user !== undefined) body["user"] = options.user;
    body["reasoning_effort"] = options.reasoningEffort ?? "medium";
    body["service_tier"] = options.serviceTier ?? "auto";
    body["store"] = options.store ?? false;
    if (options.metadata !== undefined) body["metadata"] = options.metadata;
    if (options.logitBias !== undefined) body["logit_bias"] = options.logitBias;
    if (options.modalities !== undefined) body["modalities"] = options.modalities;
    if (options.audio !== undefined) body["audio"] = options.audio;
    if (options.prediction !== undefined) body["prediction"] = options.prediction;
    if (options.webSearchOptions !== undefined) body["web_search_options"] = options.webSearchOptions;
    if (options.tools !== undefined) body["tools"] = options.tools;
    if (options.toolChoice !== undefined) body["tool_choice"] = options.toolChoice;
    if (options.responseFormat !== undefined) body["response_format"] = options.responseFormat;
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "audio", "callbackUrl", "frequencyPenalty", "logitBias", "logprobs", "maxCompletionTokens", "maxTokens", "maxWait", "messages", "metadata", "modalities", "model", "n", "parallelToolCalls", "pollInterval", "prediction", "presencePenalty", "reasoningEffort", "responseFormat", "seed", "serviceTier", "stop", "store", "stream", "streamOptions", "temperature", "toolChoice", "tools", "topLogprobs", "topP", "user", "wait", "webSearchOptions"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    return (await this.transport.request('POST', "/grok/chat/completions", { json: body })) as Record<string, unknown>;
  }

  /** Grok Videos */
  async generate(options: GrokGenerateOptions = {}): Promise<TaskHandle> {
    const body: Record<string, unknown> = {};
    if (options.prompt !== undefined) body["prompt"] = options.prompt;
    body["model"] = options.model ?? "grok-imagine-video-1.5-fast:reverse";
    if (options.imageUrl !== undefined) body["image_url"] = options.imageUrl;
    if (options.referenceImageUrls !== undefined) body["reference_image_urls"] = options.referenceImageUrls;
    if (options.aspectRatio !== undefined) body["aspect_ratio"] = options.aspectRatio;
    body["resolution"] = options.resolution ?? "480p";
    body["duration"] = options.duration ?? 6;
    for (const [key, value] of Object.entries(options)) {
      if (!["aspectRatio", "async", "callbackUrl", "duration", "imageUrl", "maxWait", "model", "pollInterval", "prompt", "referenceImageUrls", "resolution", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    body.async = options.async ?? true;
    const result = (await this.transport.request('POST', "/grok/videos", { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), "/grok/tasks", this.transport, result);
    if (options.wait) {
      await handle.wait({ pollInterval: options.pollInterval, maxWait: options.maxWait });
    }
    return handle;
  }

}
