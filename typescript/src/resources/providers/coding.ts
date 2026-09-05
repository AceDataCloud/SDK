/**
 * Coding (coding) — generated from the platform OpenAPI spec.
 *
 * Do not edit by hand: run `python scripts/generate_providers.py`. Parameter
 * names, types, enums and required-ness all come from the live spec.
 */

import { Transport } from '../../runtime/transport';


export interface CodingCountTokensOptions {
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

export interface CodingMessagesOptions {
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

export interface CodingCompletionsOptions {
  /** Openai Chat Completions Model */
  model: "gpt-6-astra" | "gpt-oss:free" | "gpt-5.5:free" | "gpt-5:free" | "gpt-4.1:free" | "gpt-4o:free" | "gpt-4o-mini:free" | "gpt-5.6-luna" | "gpt-5.6-terra" | "gpt-5.6-sol" | "gpt-5.5" | "gpt-5.5-pro" | "gpt-5.4" | "gpt-5.4-mini" | "gpt-5.4-nano" | "gpt-5.4-pro" | "gpt-5.2" | "gpt-5.1" | "gpt-5.1-all" | "gpt-5" | "gpt-5-mini" | "gpt-5-nano" | "gpt-4" | "gpt-4.1" | "gpt-4.1-mini" | "gpt-4.1-nano" | "gpt-4o" | "gpt-4o-2024-05-13" | "gpt-4o-all" | "gpt-4o-image" | "gpt-4o-mini" | "gpt-35-turbo-16k" | "o1" | "o1-mini" | "o1-pro" | "o3" | "o3-mini" | "o3-pro" | "o4-mini";
  /** Openai Chat Completions Messages 4 */
  messages: Array<Record<string, unknown>>;
  /** Openai Chat Completions N */
  n?: number;
  /** Openai Chat Completions Stream */
  stream?: boolean;
  /** Openai Chat Completions Max Tokens */
  maxTokens?: number;
  /** Openai Chat Completions Temperature */
  temperature?: number;
  /** Openai Chat Completions Response Format 4 */
  responseFormat?: Record<string, unknown>;
  /** Openai Chat Completions Tools */
  tools?: Array<Record<string, unknown>>;
  /** Openai Chat Completions Tool Choice 3 */
  toolChoice?: "none" | "auto" | "required" | Record<string, unknown>;
  /** Openai Chat Completions Top P */
  topP?: number;
  /** Openai Chat Completions Frequency Penalty */
  frequencyPenalty?: number;
  /** Openai Chat Completions Presence Penalty */
  presencePenalty?: number;
  /** Openai Chat Completions Seed */
  seed?: number;
  /** Openai Chat Completions Stop 3 */
  stop?: string | string[];
  /** Openai Chat Completions Max Completion Tokens */
  maxCompletionTokens?: number;
  /** Openai Chat Completions Logprobs */
  logprobs?: boolean;
  /** Openai Chat Completions Top Logprobs */
  topLogprobs?: number;
  /** Openai Chat Completions Stream Options */
  streamOptions?: Record<string, unknown>;
  /** Openai Chat Completions Parallel Tool Calls */
  parallelToolCalls?: boolean;
  /** Openai Chat Completions User */
  user?: string;
  /** Openai Chat Completions Reasoning Effort */
  reasoningEffort?: "minimal" | "low" | "medium" | "high";
  /** Openai Chat Completions Service Tier */
  serviceTier?: "auto" | "default" | "flex" | "scale" | "priority";
  /** Openai Chat Completions Store */
  store?: boolean;
  /** Openai Chat Completions Metadata */
  metadata?: Record<string, unknown>;
  /** Openai Chat Completions Logit Bias */
  logitBias?: Record<string, unknown>;
  /** Openai Chat Completions Modalities */
  modalities?: string[];
  /** Openai Chat Completions Audio */
  audio?: Record<string, unknown>;
  /** Openai Chat Completions Prediction 3 */
  prediction?: Record<string, unknown>;
  /** Openai Chat Completions Web Search Options */
  webSearchOptions?: Record<string, unknown>;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

export interface CodingV1ChatCompletionsOptions {
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

export interface CodingDeepseekChatCompletionsOptions {
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

export interface CodingGlmChatCompletionsOptions {
  /** Glm Chat Completions Model */
  model: "glm-5.3" | "glm-5.2" | "glm-5" | "glm-5-turbo" | "glm-5.1" | "glm-4.7" | "glm-4.6" | "glm-3-turbo";
  /** Glm Chat Completions Messages 4 */
  messages: Array<Record<string, unknown>>;
  /** Glm Chat Completions N */
  n?: number;
  /** Glm Chat Completions Stream */
  stream?: boolean;
  /** Glm Chat Completions Max Tokens */
  maxTokens?: number;
  /** Glm Chat Completions Temperature */
  temperature?: number;
  /** Glm Chat Completions Response Format 4 */
  responseFormat?: Record<string, unknown>;
  /** Glm Chat Completions Top P */
  topP?: number;
  /** Glm Chat Completions Frequency Penalty */
  frequencyPenalty?: number;
  /** Glm Chat Completions Presence Penalty */
  presencePenalty?: number;
  /** Glm Chat Completions Seed */
  seed?: number;
  /** Glm Chat Completions Stop 3 */
  stop?: string | string[];
  /** Glm Chat Completions Max Completion Tokens */
  maxCompletionTokens?: number;
  /** Glm Chat Completions Logprobs */
  logprobs?: boolean;
  /** Glm Chat Completions Top Logprobs */
  topLogprobs?: number;
  /** Glm Chat Completions Stream Options */
  streamOptions?: Record<string, unknown>;
  /** Glm Chat Completions Parallel Tool Calls */
  parallelToolCalls?: boolean;
  /** Glm Chat Completions User */
  user?: string;
  /** Glm Chat Completions Reasoning Effort */
  reasoningEffort?: "minimal" | "low" | "medium" | "high";
  /** Glm Chat Completions Service Tier */
  serviceTier?: "auto" | "default" | "flex" | "scale" | "priority";
  /** Glm Chat Completions Store */
  store?: boolean;
  /** Glm Chat Completions Metadata */
  metadata?: Record<string, unknown>;
  /** Glm Chat Completions Logit Bias */
  logitBias?: Record<string, unknown>;
  /** Glm Chat Completions Modalities */
  modalities?: string[];
  /** Glm Chat Completions Audio */
  audio?: Record<string, unknown>;
  /** Glm Chat Completions Prediction 3 */
  prediction?: Record<string, unknown>;
  /** Glm Chat Completions Web Search Options */
  webSearchOptions?: Record<string, unknown>;
  /** Glm Chat Completions Tools */
  tools?: Array<Record<string, unknown>>;
  /** Glm Chat Completions Tool Choice 3 */
  toolChoice?: "none" | "auto" | "required" | Record<string, unknown>;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

export interface CodingGeminiChatCompletionsOptions {
  /** Gemini Chat Completions Model */
  model: "gemini-3.7-flash" | "gemini-3.6-flash" | "gemini-3.5-flash" | "gemini-3.5-flash-lite" | "gemini-3.1-flash-lite" | "gemini-3.1-pro-preview" | "gemini-3-flash-preview" | "gemini-2.5-pro" | "gemini-2.5-flash" | "gemini-2.5-flash-lite";
  /** Gemini Chat Completions Messages 4 */
  messages: Array<Record<string, unknown>>;
  /** Gemini Chat Completions N */
  n?: number;
  /** Gemini Chat Completions Stream */
  stream?: boolean;
  /** Gemini Chat Completions Max Tokens */
  maxTokens?: number;
  /** Gemini Chat Completions Temperature */
  temperature?: number;
  /** Gemini Chat Completions Response Format 4 */
  responseFormat?: Record<string, unknown>;
  /** Gemini Chat Completions Top P */
  topP?: number;
  /** Gemini Chat Completions Frequency Penalty */
  frequencyPenalty?: number;
  /** Gemini Chat Completions Presence Penalty */
  presencePenalty?: number;
  /** Gemini Chat Completions Seed */
  seed?: number;
  /** Gemini Chat Completions Stop 3 */
  stop?: string | string[];
  /** Gemini Chat Completions Max Completion Tokens */
  maxCompletionTokens?: number;
  /** Gemini Chat Completions Logprobs */
  logprobs?: boolean;
  /** Gemini Chat Completions Top Logprobs */
  topLogprobs?: number;
  /** Gemini Chat Completions Stream Options */
  streamOptions?: Record<string, unknown>;
  /** Gemini Chat Completions Parallel Tool Calls */
  parallelToolCalls?: boolean;
  /** Gemini Chat Completions User */
  user?: string;
  /** Gemini Chat Completions Reasoning Effort */
  reasoningEffort?: "minimal" | "low" | "medium" | "high";
  /** Gemini Chat Completions Service Tier */
  serviceTier?: "auto" | "default" | "flex" | "scale" | "priority";
  /** Gemini Chat Completions Store */
  store?: boolean;
  /** Gemini Chat Completions Metadata */
  metadata?: Record<string, unknown>;
  /** Gemini Chat Completions Logit Bias */
  logitBias?: Record<string, unknown>;
  /** Gemini Chat Completions Modalities */
  modalities?: string[];
  /** Gemini Chat Completions Audio */
  audio?: Record<string, unknown>;
  /** Gemini Chat Completions Prediction 3 */
  prediction?: Record<string, unknown>;
  /** Gemini Chat Completions Web Search Options */
  webSearchOptions?: Record<string, unknown>;
  /** Gemini Chat Completions Tools */
  tools?: Array<Record<string, unknown>>;
  /** Gemini Chat Completions Tool Choice 3 */
  toolChoice?: "none" | "auto" | "required" | Record<string, unknown>;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

export interface CodingGrokChatCompletionsOptions {
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
  stop?: string | string[];
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
  toolChoice?: "none" | "auto" | "required" | Record<string, unknown>;
  /** Grok Chat Completions Response Format 4 */
  responseFormat?: Record<string, unknown>;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

export interface CodingKimiChatCompletionsOptions {
  /** Kimi Chat Completions Model */
  model: "kimi-k3" | "kimi-k2.6" | "kimi-k2-thinking-turbo" | "kimi-k2.5" | "kimi-k2-thinking";
  /** Kimi Chat Completions Messages 4 */
  messages: Array<Record<string, unknown>>;
  /** Kimi Chat Completions N */
  n?: number;
  /** Kimi Chat Completions Stream */
  stream?: boolean;
  /** Kimi Chat Completions Max Tokens */
  maxTokens?: number;
  /** Kimi Chat Completions Temperature */
  temperature?: number;
  /** Kimi Chat Completions Response Format 4 */
  responseFormat?: Record<string, unknown>;
  /** Kimi Chat Completions Top P */
  topP?: number;
  /** Kimi Chat Completions Frequency Penalty */
  frequencyPenalty?: number;
  /** Kimi Chat Completions Presence Penalty */
  presencePenalty?: number;
  /** Kimi Chat Completions Seed */
  seed?: number;
  /** Kimi Chat Completions Stop 3 */
  stop?: string | string[];
  /** Kimi Chat Completions Max Completion Tokens */
  maxCompletionTokens?: number;
  /** Kimi Chat Completions Logprobs */
  logprobs?: boolean;
  /** Kimi Chat Completions Top Logprobs */
  topLogprobs?: number;
  /** Kimi Chat Completions Stream Options */
  streamOptions?: Record<string, unknown>;
  /** Kimi Chat Completions Parallel Tool Calls */
  parallelToolCalls?: boolean;
  /** Kimi Chat Completions User */
  user?: string;
  /** Kimi Chat Completions Reasoning Effort */
  reasoningEffort?: "low" | "high" | "max";
  /** Kimi Chat Completions Service Tier */
  serviceTier?: "auto" | "default" | "flex" | "scale" | "priority";
  /** Kimi Chat Completions Store */
  store?: boolean;
  /** Kimi Chat Completions Metadata */
  metadata?: Record<string, unknown>;
  /** Kimi Chat Completions Logit Bias */
  logitBias?: Record<string, unknown>;
  /** Kimi Chat Completions Modalities */
  modalities?: string[];
  /** Kimi Chat Completions Audio */
  audio?: Record<string, unknown>;
  /** Kimi Chat Completions Prediction 3 */
  prediction?: Record<string, unknown>;
  /** Kimi Chat Completions Web Search Options */
  webSearchOptions?: Record<string, unknown>;
  /** Kimi Chat Completions Tools */
  tools?: Array<Record<string, unknown>>;
  /** Kimi Chat Completions Tool Choice 3 */
  toolChoice?: "none" | "auto" | "required" | Record<string, unknown>;
  /** Kimi Chat Completions Thinking */
  thinking?: Record<string, unknown>;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

export interface CodingResponsesOptions {
  /** Openai Responses Model */
  model: "gpt-6-astra" | "gpt-5.6-luna" | "gpt-5.6-terra" | "gpt-5.6-sol" | "gpt-5.5" | "gpt-5.5-pro" | "gpt-5.4" | "gpt-5.4-mini" | "gpt-5.4-nano" | "gpt-5.4-pro" | "gpt-5.1" | "gpt-5.1-all" | "gpt-5" | "gpt-5-mini" | "gpt-5-nano" | "gpt-4" | "gpt-4-all" | "gpt-4-turbo" | "gpt-4-turbo-preview" | "gpt-4-vision-preview" | "gpt-4.1" | "gpt-4.1-2025-04-14" | "gpt-4.1-mini" | "gpt-4.1-mini-2025-04-14" | "gpt-4.1-nano" | "gpt-4.1-nano-2025-04-14" | "gpt-4.5-preview" | "gpt-4.5-preview-2025-02-27" | "gpt-4o" | "gpt-4o-2024-05-13" | "gpt-4o-2024-08-06" | "gpt-4o-2024-11-20" | "gpt-4o-all" | "gpt-4o-image" | "gpt-4o-mini" | "gpt-4o-mini-2024-07-18" | "gpt-4o-mini-search-preview" | "gpt-4o-mini-search-preview-2025-03-11" | "gpt-4o-search-preview" | "gpt-4o-search-preview-2025-03-11" | "gpt-35-turbo-16k" | "o1" | "o1-2024-12-17" | "o1-all" | "o1-mini" | "o1-mini-2024-09-12" | "o1-mini-all" | "o1-preview" | "o1-preview-2024-09-12" | "o1-preview-all" | "o1-pro" | "o1-pro-2025-03-19" | "o1-pro-all" | "o3" | "o3-2025-04-16" | "o3-all" | "o3-mini" | "o3-mini-2025-01-31" | "o3-mini-2025-01-31-high" | "o3-mini-2025-01-31-low" | "o3-mini-2025-01-31-medium" | "o3-mini-all" | "o3-mini-high" | "o3-mini-high-all" | "o3-mini-low" | "o3-mini-medium" | "o3-pro" | "o3-pro-2025-06-10" | "o4-mini" | "o4-mini-2025-04-16" | "o4-mini-all" | "o4-mini-high-all";
  /** Openai Responses Input 2 */
  input: string | string[];
  /** Openai Responses N */
  n?: number;
  /** Openai Responses Background */
  background?: boolean;
  /** Openai Responses Stream */
  stream?: boolean;
  /** Openai Responses Tools */
  tools?: Array<Record<string, unknown>>;
  /** Openai Responses Max Tokens */
  maxTokens?: number;
  /** Openai Responses Temperature */
  temperature?: number;
  /** Openai Responses Response Format */
  responseFormat?: Record<string, unknown>;
  /** Openapi.Ed972A38Ecef4Fcbaf33750De42D25Dc.Tool Choice.C7B5D99A6584 */
  toolChoice?: "none" | "auto" | "required" | Record<string, unknown>;
  parallelToolCalls?: boolean;
  include?: string[];
  reasoning?: Record<string, unknown>;
  text?: Record<string, unknown>;
  maxOutputTokens?: number;
  store?: boolean;
  streamOptions?: Record<string, unknown>;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

/** coding client. */
export class Coding {
  constructor(private transport: Transport) {}

  /** Claude Messages Count Tokens */
  async count_tokens(options: CodingCountTokensOptions): Promise<Record<string, unknown>> {
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

  /** Claude Messages */
  async messages(options: CodingMessagesOptions): Promise<Record<string, unknown>> {
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

  /** Openai Chat Completions */
  async completions(options: CodingCompletionsOptions): Promise<Record<string, unknown>> {
    const body: Record<string, unknown> = {};
    body["model"] = options.model;
    body["messages"] = options.messages;
    body["n"] = options.n ?? 1;
    body["stream"] = options.stream ?? false;
    if (options.maxTokens !== undefined) body["max_tokens"] = options.maxTokens;
    body["temperature"] = options.temperature ?? 1;
    if (options.responseFormat !== undefined) body["response_format"] = options.responseFormat;
    if (options.tools !== undefined) body["tools"] = options.tools;
    if (options.toolChoice !== undefined) body["tool_choice"] = options.toolChoice;
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
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "audio", "callbackUrl", "frequencyPenalty", "logitBias", "logprobs", "maxCompletionTokens", "maxTokens", "maxWait", "messages", "metadata", "modalities", "model", "n", "parallelToolCalls", "pollInterval", "prediction", "presencePenalty", "reasoningEffort", "responseFormat", "seed", "serviceTier", "stop", "store", "stream", "streamOptions", "temperature", "toolChoice", "tools", "topLogprobs", "topP", "user", "wait", "webSearchOptions"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    return (await this.transport.request('POST', "/openai/chat/completions", { json: body })) as Record<string, unknown>;
  }

  /** Claude Chat Completions */
  async v1_chat_completions(options: CodingV1ChatCompletionsOptions): Promise<Record<string, unknown>> {
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

  /** Deepseek Chat Completions */
  async deepseek_chat_completions(options: CodingDeepseekChatCompletionsOptions): Promise<Record<string, unknown>> {
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

  /** Glm Chat Completions */
  async glm_chat_completions(options: CodingGlmChatCompletionsOptions): Promise<Record<string, unknown>> {
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
    return (await this.transport.request('POST', "/glm/chat/completions", { json: body })) as Record<string, unknown>;
  }

  /** Gemini Chat Completions */
  async gemini_chat_completions(options: CodingGeminiChatCompletionsOptions): Promise<Record<string, unknown>> {
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
    return (await this.transport.request('POST', "/gemini/chat/completions", { json: body })) as Record<string, unknown>;
  }

  /** Grok Chat Completions */
  async grok_chat_completions(options: CodingGrokChatCompletionsOptions): Promise<Record<string, unknown>> {
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

  /** Kimi Chat Completions */
  async kimi_chat_completions(options: CodingKimiChatCompletionsOptions): Promise<Record<string, unknown>> {
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
    if (options.reasoningEffort !== undefined) body["reasoning_effort"] = options.reasoningEffort;
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
    if (options.thinking !== undefined) body["thinking"] = options.thinking;
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "audio", "callbackUrl", "frequencyPenalty", "logitBias", "logprobs", "maxCompletionTokens", "maxTokens", "maxWait", "messages", "metadata", "modalities", "model", "n", "parallelToolCalls", "pollInterval", "prediction", "presencePenalty", "reasoningEffort", "responseFormat", "seed", "serviceTier", "stop", "store", "stream", "streamOptions", "temperature", "thinking", "toolChoice", "tools", "topLogprobs", "topP", "user", "wait", "webSearchOptions"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    return (await this.transport.request('POST', "/kimi/chat/completions", { json: body })) as Record<string, unknown>;
  }

  /** Openai V1 Responses */
  async responses(options: CodingResponsesOptions): Promise<Record<string, unknown>> {
    const body: Record<string, unknown> = {};
    body["model"] = options.model;
    body["input"] = options.input;
    body["n"] = options.n ?? 1;
    body["background"] = options.background ?? false;
    body["stream"] = options.stream ?? false;
    if (options.tools !== undefined) body["tools"] = options.tools;
    if (options.maxTokens !== undefined) body["max_tokens"] = options.maxTokens;
    body["temperature"] = options.temperature ?? 1;
    if (options.responseFormat !== undefined) body["response_format"] = options.responseFormat;
    if (options.toolChoice !== undefined) body["tool_choice"] = options.toolChoice;
    body["parallel_tool_calls"] = options.parallelToolCalls ?? true;
    if (options.include !== undefined) body["include"] = options.include;
    if (options.reasoning !== undefined) body["reasoning"] = options.reasoning;
    if (options.text !== undefined) body["text"] = options.text;
    if (options.maxOutputTokens !== undefined) body["max_output_tokens"] = options.maxOutputTokens;
    body["store"] = options.store ?? true;
    if (options.streamOptions !== undefined) body["stream_options"] = options.streamOptions;
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "background", "callbackUrl", "include", "input", "maxOutputTokens", "maxTokens", "maxWait", "model", "n", "parallelToolCalls", "pollInterval", "reasoning", "responseFormat", "store", "stream", "streamOptions", "temperature", "text", "toolChoice", "tools", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    return (await this.transport.request('POST', "/openai/responses", { json: body })) as Record<string, unknown>;
  }

}
