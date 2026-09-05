/**
 * Claude (claude) — generated from the platform OpenAPI spec.
 *
 * Do not edit by hand: run `python scripts/generate_providers.py`. Parameter
 * names, types, enums and required-ness all come from the live spec.
 */

import { Transport } from '../../runtime/transport';


export interface ClaudeCompletionsOptions {
  /** V1 Chat Completions Model */
  model: "claude-fable-5-1" | "claude-fable-5" | "claude-opus-5" | "claude-opus-4-8" | "claude-sonnet-5" | "claude-sonnet-4-6" | "claude-opus-4-7" | "claude-opus-4-6" | "claude-opus-4-5-20251101" | "claude-haiku-4-5-20251001" | "claude-sonnet-4-5-20250929" | "claude-opus-4-1-20250805" | "claude-sonnet-4-20250514" | "claude-opus-4-20250514" | "claude-3-7-sonnet-20250219" | "claude-3-5-sonnet-20241022" | "claude-3-5-haiku-20241022" | "claude-3-5-sonnet-20240620" | "claude-3-haiku-20240307" | "claude-3-sonnet-20240229";
  /** V1 Chat Completions Messages 4 */
  messages: Array<Record<string, unknown>>;
  /** V1 Chat Completions N */
  n?: number;
  /** V1 Chat Completions Stream */
  stream?: boolean;
  /** V1 Chat Completions Max Tokens */
  maxTokens?: number;
  /** V1 Chat Completions Temperature */
  temperature?: number;
  /** V1 Chat Completions Response Format 4 */
  responseFormat?: Record<string, unknown>;
  /** V1 Chat Completions Top P */
  topP?: number;
  /** V1 Chat Completions Frequency Penalty */
  frequencyPenalty?: number;
  /** V1 Chat Completions Presence Penalty */
  presencePenalty?: number;
  /** V1 Chat Completions Seed */
  seed?: number;
  /** V1 Chat Completions Stop 3 */
  stop?: string | string[];
  /** V1 Chat Completions Max Completion Tokens */
  maxCompletionTokens?: number;
  /** V1 Chat Completions Logprobs */
  logprobs?: boolean;
  /** V1 Chat Completions Top Logprobs */
  topLogprobs?: number;
  /** V1 Chat Completions Stream Options */
  streamOptions?: Record<string, unknown>;
  /** V1 Chat Completions Parallel Tool Calls */
  parallelToolCalls?: boolean;
  /** V1 Chat Completions User */
  user?: string;
  /** V1 Chat Completions Reasoning Effort */
  reasoningEffort?: "minimal" | "low" | "medium" | "high";
  /** V1 Chat Completions Service Tier */
  serviceTier?: "auto" | "default" | "flex" | "scale" | "priority";
  /** V1 Chat Completions Store */
  store?: boolean;
  /** V1 Chat Completions Metadata */
  metadata?: Record<string, unknown>;
  /** V1 Chat Completions Logit Bias */
  logitBias?: Record<string, unknown>;
  /** V1 Chat Completions Modalities */
  modalities?: string[];
  /** V1 Chat Completions Audio */
  audio?: Record<string, unknown>;
  /** V1 Chat Completions Prediction 3 */
  prediction?: Record<string, unknown>;
  /** V1 Chat Completions Web Search Options */
  webSearchOptions?: Record<string, unknown>;
  /** V1 Chat Completions Tools */
  tools?: Array<Record<string, unknown>>;
  /** V1 Chat Completions Tool Choice 3 */
  toolChoice?: "none" | "auto" | "required" | Record<string, unknown>;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

export interface ClaudeMessagesOptions {
  /** V1 Messages Model */
  model: "claude-fable-5-1" | "claude-fable-5" | "claude-opus-5" | "claude-opus-4-8" | "claude-sonnet-5" | "claude-sonnet-4-6" | "claude-opus-4-7" | "claude-opus-4-6" | "claude-opus-4-5-20251101" | "claude-haiku-4-5-20251001" | "claude-sonnet-4-5-20250929" | "claude-opus-4-1-20250805" | "claude-sonnet-4-20250514" | "claude-opus-4-20250514" | "claude-3-7-sonnet-20250219" | "claude-3-5-sonnet-20241022" | "claude-3-5-haiku-20241022" | "claude-3-5-sonnet-20240620" | "claude-3-haiku-20240307" | "claude-3-sonnet-20240229";
  messages: Array<Record<string, unknown>>;
  /** V1 Messages Max Tokens */
  maxTokens: number;
  metadata?: Record<string, unknown>;
  /** V1 Messages Stop Sequences */
  stopSequences?: string[];
  /** V1 Messages Stream */
  stream?: boolean;
  system?: string | string[];
  /** V1 Messages Temperature */
  temperature?: number;
  toolChoice?: Record<string, unknown>;
  /** V1 Messages Tools */
  tools?: Array<Record<string, unknown>>;
  /** V1 Messages Top K */
  topK?: number;
  /** V1 Messages Top P */
  topP?: number;
  thinking?: Record<string, unknown>;
  /** V1 Messages Output Config */
  outputConfig?: Record<string, unknown>;
  cacheControl?: Record<string, unknown>;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

export interface ClaudeCountTokensOptions {
  /** V1 Messages Count Tokens Model */
  model: "claude-fable-5-1" | "claude-fable-5" | "claude-opus-5" | "claude-opus-4-8" | "claude-sonnet-5" | "claude-sonnet-4-6" | "claude-opus-4-7" | "claude-opus-4-6" | "claude-opus-4-5-20251101" | "claude-haiku-4-5-20251001" | "claude-sonnet-4-5-20250929" | "claude-opus-4-1-20250805" | "claude-sonnet-4-20250514" | "claude-opus-4-20250514" | "claude-3-7-sonnet-20250219" | "claude-3-5-sonnet-20241022" | "claude-3-5-haiku-20241022" | "claude-3-5-sonnet-20240620" | "claude-3-haiku-20240307" | "claude-3-sonnet-20240229";
  messages: Array<Record<string, unknown>>;
  system?: string | string[];
  thinking?: Record<string, unknown>;
  toolChoice?: Record<string, unknown>;
  /** V1 Messages Count Tokens Tools */
  tools?: Array<Record<string, unknown>>;
  cacheControl?: Record<string, unknown>;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

/** claude client. */
export class Claude {
  constructor(private transport: Transport) {}

  /** Claude Chat Completions */
  async completions(options: ClaudeCompletionsOptions): Promise<Record<string, unknown>> {
    const body: Record<string, unknown> = {};
    body["model"] = options.model;
    body["messages"] = options.messages;
    body["n"] = options.n ?? 1;
    body["stream"] = options.stream ?? false;
    if (options.maxTokens !== undefined) body["max_tokens"] = options.maxTokens;
    body["temperature"] = options.temperature ?? 1;
    if (options.responseFormat !== undefined) body["response_format"] = options.responseFormat;
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
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "audio", "callbackUrl", "frequencyPenalty", "logitBias", "logprobs", "maxCompletionTokens", "maxTokens", "maxWait", "messages", "metadata", "modalities", "model", "n", "parallelToolCalls", "pollInterval", "prediction", "presencePenalty", "reasoningEffort", "responseFormat", "seed", "serviceTier", "stop", "store", "stream", "streamOptions", "temperature", "toolChoice", "tools", "topLogprobs", "topP", "user", "wait", "webSearchOptions"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    return (await this.transport.request('POST', "/v1/chat/completions", { json: body })) as Record<string, unknown>;
  }

  /** Claude Messages */
  async messages(options: ClaudeMessagesOptions): Promise<Record<string, unknown>> {
    const body: Record<string, unknown> = {};
    body["model"] = options.model;
    body["messages"] = options.messages;
    body["max_tokens"] = options.maxTokens;
    if (options.metadata !== undefined) body["metadata"] = options.metadata;
    if (options.stopSequences !== undefined) body["stop_sequences"] = options.stopSequences;
    body["stream"] = options.stream ?? false;
    if (options.system !== undefined) body["system"] = options.system;
    if (options.temperature !== undefined) body["temperature"] = options.temperature;
    if (options.toolChoice !== undefined) body["tool_choice"] = options.toolChoice;
    if (options.tools !== undefined) body["tools"] = options.tools;
    if (options.topK !== undefined) body["top_k"] = options.topK;
    if (options.topP !== undefined) body["top_p"] = options.topP;
    if (options.thinking !== undefined) body["thinking"] = options.thinking;
    if (options.outputConfig !== undefined) body["output_config"] = options.outputConfig;
    if (options.cacheControl !== undefined) body["cache_control"] = options.cacheControl;
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "cacheControl", "callbackUrl", "maxTokens", "maxWait", "messages", "metadata", "model", "outputConfig", "pollInterval", "stopSequences", "stream", "system", "temperature", "thinking", "toolChoice", "tools", "topK", "topP", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    return (await this.transport.request('POST', "/v1/messages", { json: body })) as Record<string, unknown>;
  }

  /** Claude Messages Count Tokens */
  async count_tokens(options: ClaudeCountTokensOptions): Promise<Record<string, unknown>> {
    const body: Record<string, unknown> = {};
    body["model"] = options.model;
    body["messages"] = options.messages;
    if (options.system !== undefined) body["system"] = options.system;
    if (options.thinking !== undefined) body["thinking"] = options.thinking;
    if (options.toolChoice !== undefined) body["tool_choice"] = options.toolChoice;
    if (options.tools !== undefined) body["tools"] = options.tools;
    if (options.cacheControl !== undefined) body["cache_control"] = options.cacheControl;
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "cacheControl", "callbackUrl", "maxWait", "messages", "model", "pollInterval", "system", "thinking", "toolChoice", "tools", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    return (await this.transport.request('POST', "/v1/messages/count_tokens", { json: body })) as Record<string, unknown>;
  }

}
