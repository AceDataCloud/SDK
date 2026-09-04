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

export interface GeminiCompletionsOptions {
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
  responseFormat?: unknown;
  /** Gemini Chat Completions Top P */
  topP?: number;
  /** Gemini Chat Completions Frequency Penalty */
  frequencyPenalty?: number;
  /** Gemini Chat Completions Presence Penalty */
  presencePenalty?: number;
  /** Gemini Chat Completions Seed */
  seed?: number;
  /** Gemini Chat Completions Stop 3 */
  stop?: unknown;
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
  toolChoice?: unknown;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

export interface GeminiModelGeneratecontentOptions {
  /** V1Beta Models Model Generatecontent Contents */
  contents: Array<Record<string, unknown>>;
  model: "gemini-3.7-flash" | "gemini-3.6-flash" | "gemini-3.5-flash" | "gemini-3.5-flash-lite" | "gemini-3.1-flash-lite" | "gemini-3.1-pro-preview" | "gemini-3-flash-preview" | "gemini-2.5-pro" | "gemini-2.5-flash" | "gemini-2.5-flash-lite" | "gemini-3.1-flash-image" | "gemini-2.5-flash-image" | "gemini-3-pro-image";
  /** V1Beta Models Model Generatecontent Systeminstruction */
  systeminstruction?: Record<string, unknown>;
  /** V1Beta Models Model Generatecontent Generationconfig */
  generationconfig?: Record<string, unknown>;
  /** V1Beta Models Model Generatecontent Tools */
  tools?: Array<Record<string, unknown>>;
  /** V1Beta Models Model Generatecontent Toolconfig */
  toolconfig?: Record<string, unknown>;
  /** V1Beta Models Model Generatecontent Safetysettings */
  safetysettings?: Array<Record<string, unknown>>;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

export interface GeminiModelStreamgeneratecontentOptions {
  /** V1Beta Models Model Generatecontent Contents */
  contents: Array<Record<string, unknown>>;
  model: "gemini-3.7-flash" | "gemini-3.6-flash" | "gemini-3.5-flash" | "gemini-3.5-flash-lite" | "gemini-3.1-flash-lite" | "gemini-3.1-pro-preview" | "gemini-3-flash-preview" | "gemini-2.5-pro" | "gemini-2.5-flash" | "gemini-2.5-flash-lite" | "gemini-3.1-flash-image" | "gemini-2.5-flash-image" | "gemini-3-pro-image";
  /** V1Beta Models Model Generatecontent Systeminstruction */
  systeminstruction?: Record<string, unknown>;
  /** V1Beta Models Model Generatecontent Generationconfig */
  generationconfig?: Record<string, unknown>;
  /** V1Beta Models Model Generatecontent Tools */
  tools?: Array<Record<string, unknown>>;
  /** V1Beta Models Model Generatecontent Toolconfig */
  toolconfig?: Record<string, unknown>;
  /** V1Beta Models Model Generatecontent Safetysettings */
  safetysettings?: Array<Record<string, unknown>>;
  alt?: "sse";
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

export interface GeminiGenerateOptions {
  /** Gemini Videos Prompt */
  prompt: string;
  /** Gemini Videos Model */
  model?: "omni-flash";
  /** Gemini Videos Aspect Ratio */
  aspectRatio?: "16:9" | "9:16";
  /** Gemini Videos Resolution */
  resolution?: "720p" | "1080p";
  /** Gemini Videos Image Urls */
  imageUrls?: string[];
  /** Gemini Videos Video Urls */
  videoUrls?: string[];
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

/** gemini client. */
export class Gemini {
  constructor(private transport: Transport) {}

  /** Gemini Chat Completions */
  async completions(options: GeminiCompletionsOptions): Promise<Record<string, unknown>> {
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

  /** Gemini Generate Content */
  async model_generatecontent(options: GeminiModelGeneratecontentOptions): Promise<Record<string, unknown>> {
    let path = "/v1beta/models/{model}:generateContent";
    path = path.replace("{model}", encodeURIComponent(String(options.model)));
    const body: Record<string, unknown> = {};
    body["contents"] = options.contents;
    if (options.systeminstruction !== undefined) body["systemInstruction"] = options.systeminstruction;
    if (options.generationconfig !== undefined) body["generationConfig"] = options.generationconfig;
    if (options.tools !== undefined) body["tools"] = options.tools;
    if (options.toolconfig !== undefined) body["toolConfig"] = options.toolconfig;
    if (options.safetysettings !== undefined) body["safetySettings"] = options.safetysettings;
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "callbackUrl", "contents", "generationconfig", "maxWait", "model", "pollInterval", "safetysettings", "systeminstruction", "toolconfig", "tools", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    return (await this.transport.request('POST', path, { json: body })) as Record<string, unknown>;
  }

  /** Gemini Stream Generate Content */
  async model_streamgeneratecontent(options: GeminiModelStreamgeneratecontentOptions): Promise<Record<string, unknown>> {
    let path = "/v1beta/models/{model}:streamGenerateContent";
    path = path.replace("{model}", encodeURIComponent(String(options.model)));
    const body: Record<string, unknown> = {};
    body["contents"] = options.contents;
    if (options.systeminstruction !== undefined) body["systemInstruction"] = options.systeminstruction;
    if (options.generationconfig !== undefined) body["generationConfig"] = options.generationconfig;
    if (options.tools !== undefined) body["tools"] = options.tools;
    if (options.toolconfig !== undefined) body["toolConfig"] = options.toolconfig;
    if (options.safetysettings !== undefined) body["safetySettings"] = options.safetysettings;
    for (const [key, value] of Object.entries(options)) {
      if (!["alt", "async", "callbackUrl", "contents", "generationconfig", "maxWait", "model", "pollInterval", "safetysettings", "systeminstruction", "toolconfig", "tools", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    const params: Record<string, string> = {};
    if (options.alt !== undefined) params["alt"] = String(options.alt);
    return (await this.transport.request('POST', path, { json: body, params })) as Record<string, unknown>;
  }

  /** Gemini Videos */
  async generate(options: GeminiGenerateOptions): Promise<TaskHandle> {
    const body: Record<string, unknown> = {};
    body["prompt"] = options.prompt;
    body["model"] = options.model ?? "omni-flash";
    body["aspect_ratio"] = options.aspectRatio ?? "16:9";
    body["resolution"] = options.resolution ?? "720p";
    if (options.imageUrls !== undefined) body["image_urls"] = options.imageUrls;
    if (options.videoUrls !== undefined) body["video_urls"] = options.videoUrls;
    for (const [key, value] of Object.entries(options)) {
      if (!["aspectRatio", "async", "callbackUrl", "imageUrls", "maxWait", "model", "pollInterval", "prompt", "resolution", "videoUrls", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    body.async = options.async ?? true;
    const result = (await this.transport.request('POST', "/gemini/videos", { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), "/gemini/tasks", this.transport, result);
    if (options.wait) {
      await handle.wait({ pollInterval: options.pollInterval, maxWait: options.maxWait });
    }
    return handle;
  }

}
