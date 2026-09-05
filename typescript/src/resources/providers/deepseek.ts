/**
 * Deepseek (deepseek) — generated from the platform OpenAPI spec.
 *
 * Do not edit by hand: run `python scripts/generate_providers.py`. Parameter
 * names, types, enums and required-ness all come from the live spec.
 */

import { Transport } from '../../runtime/transport';


export interface DeepseekCompletionsOptions {
  /** Deepseek Chat Completions Model */
  model: "deepseek-r1" | "deepseek-r1-0528" | "deepseek-v3" | "deepseek-v3-250324" | "deepseek-v3.2-exp" | "deepseek-v4-flash" | "deepseek-v4-pro";
  /** Deepseek Chat Completions Messages 4 */
  messages: Array<Record<string, unknown>>;
  /** Deepseek Chat Completions N */
  n?: number;
  /** Deepseek Chat Completions Stream */
  stream?: boolean;
  /** Deepseek Chat Completions Max Tokens */
  maxTokens?: number;
  /** Deepseek Chat Completions Temperature */
  temperature?: number;
  /** Deepseek Chat Completions Response Format 4 */
  responseFormat?: Record<string, unknown>;
  /** Deepseek Chat Completions Top P */
  topP?: number;
  /** Deepseek Chat Completions Frequency Penalty */
  frequencyPenalty?: number;
  /** Deepseek Chat Completions Presence Penalty */
  presencePenalty?: number;
  /** Deepseek Chat Completions Seed */
  seed?: number;
  /** Deepseek Chat Completions Stop 3 */
  stop?: string | string[];
  /** Deepseek Chat Completions Max Completion Tokens */
  maxCompletionTokens?: number;
  /** Deepseek Chat Completions Logprobs */
  logprobs?: boolean;
  /** Deepseek Chat Completions Top Logprobs */
  topLogprobs?: number;
  /** Deepseek Chat Completions Stream Options */
  streamOptions?: Record<string, unknown>;
  /** Deepseek Chat Completions Parallel Tool Calls */
  parallelToolCalls?: boolean;
  /** Deepseek Chat Completions User */
  user?: string;
  /** Deepseek Chat Completions Reasoning Effort */
  reasoningEffort?: "minimal" | "low" | "medium" | "high";
  /** Deepseek Chat Completions Service Tier */
  serviceTier?: "auto" | "default" | "flex" | "scale" | "priority";
  /** Deepseek Chat Completions Store */
  store?: boolean;
  /** Deepseek Chat Completions Metadata */
  metadata?: Record<string, unknown>;
  /** Deepseek Chat Completions Logit Bias */
  logitBias?: Record<string, unknown>;
  /** Deepseek Chat Completions Modalities */
  modalities?: string[];
  /** Deepseek Chat Completions Audio */
  audio?: Record<string, unknown>;
  /** Deepseek Chat Completions Prediction 3 */
  prediction?: Record<string, unknown>;
  /** Deepseek Chat Completions Web Search Options */
  webSearchOptions?: Record<string, unknown>;
  /** Deepseek Chat Completions Tools */
  tools?: Array<Record<string, unknown>>;
  /** Deepseek Chat Completions Tool Choice 3 */
  toolChoice?: "none" | "auto" | "required" | Record<string, unknown>;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

/** deepseek client. */
export class Deepseek {
  constructor(private transport: Transport) {}

  /** Deepseek Chat Completions */
  async completions(options: DeepseekCompletionsOptions): Promise<Record<string, unknown>> {
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
    return (await this.transport.request('POST', "/deepseek/chat/completions", { json: body })) as Record<string, unknown>;
  }

}
