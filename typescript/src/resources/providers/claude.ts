/** Claude provider resource. */

import { Transport } from '../../runtime/transport';

export type ClaudeModel =
  | 'claude-fable-5'
  | 'claude-opus-5'
  | 'claude-opus-4-8'
  | 'claude-sonnet-5'
  | 'claude-sonnet-4-6'
  | 'claude-opus-4-7'
  | 'claude-opus-4-6'
  | 'claude-opus-4-5-20251101'
  | 'claude-haiku-4-5-20251001'
  | 'claude-sonnet-4-5-20250929'
  | 'claude-opus-4-1-20250805'
  | 'claude-sonnet-4-20250514'
  | 'claude-opus-4-20250514'
  | 'claude-3-7-sonnet-20250219'
  | 'claude-3-5-sonnet-20241022'
  | 'claude-3-5-haiku-20241022'
  | 'claude-3-5-sonnet-20240620'
  | 'claude-3-haiku-20240307'
  | 'claude-3-sonnet-20240229'
  | 'claude-3-opus-20240229';

type ReasoningEffort = 'minimal' | 'low' | 'medium' | 'high';
type ServiceTier = 'auto' | 'default' | 'flex' | 'scale' | 'priority';

export interface ClaudeChatCompletionOptions {
  model: ClaudeModel;
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

export interface ClaudeMessageOptions {
  model: ClaudeModel;
  messages: Array<Record<string, unknown>>;
  maxTokens: number;
  metadata?: Record<string, unknown>;
  stopSequences?: string[];
  stream?: boolean;
  system?: string;
  temperature?: number;
  toolChoice?: Record<string, unknown>;
  tools?: unknown[];
  topK?: number;
  topP?: number;
  thinking?: unknown;
  [key: string]: unknown;
}

export interface ClaudeCountTokensOptions {
  model: ClaudeModel;
  messages: Array<Record<string, unknown>>;
  system?: string;
  thinking?: Record<string, unknown>;
  toolChoice?: Record<string, unknown>;
  tools?: unknown[];
  [key: string]: unknown;
}

const COMPLETION_KEYS = new Set([
  'model', 'messages', 'n', 'stream', 'maxTokens', 'temperature', 'responseFormat', 'topP', 'frequencyPenalty',
  'presencePenalty', 'seed', 'stop', 'maxCompletionTokens', 'logprobs', 'topLogprobs', 'streamOptions',
  'parallelToolCalls', 'user', 'reasoningEffort', 'serviceTier', 'store', 'metadata', 'logitBias', 'modalities',
  'audio', 'prediction', 'webSearchOptions', 'tools', 'toolChoice',
]);
const MESSAGE_KEYS = new Set([
  'model', 'messages', 'maxTokens', 'metadata', 'stopSequences', 'stream', 'system', 'temperature', 'toolChoice',
  'tools', 'topK', 'topP', 'thinking',
]);
const COUNT_KEYS = new Set(['model', 'messages', 'system', 'thinking', 'toolChoice', 'tools']);

function copyExtra(body: Record<string, unknown>, options: Record<string, unknown>, known: Set<string>): void {
  for (const [key, value] of Object.entries(options)) {
    if (!known.has(key) && value !== undefined) body[key] = value;
  }
}

function setIfDefined(body: Record<string, unknown>, key: string, value: unknown): void {
  if (value !== undefined) body[key] = value;
}

function completionBody(options: ClaudeChatCompletionOptions): Record<string, unknown> {
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
  copyExtra(body, options, COMPLETION_KEYS);
  return body;
}

function messageBody(options: ClaudeMessageOptions): Record<string, unknown> {
  const body: Record<string, unknown> = {
    model: options.model,
    messages: options.messages,
    max_tokens: options.maxTokens,
    stream: options.stream ?? false,
  };
  setIfDefined(body, 'metadata', options.metadata);
  setIfDefined(body, 'stop_sequences', options.stopSequences);
  setIfDefined(body, 'system', options.system);
  setIfDefined(body, 'temperature', options.temperature);
  setIfDefined(body, 'tool_choice', options.toolChoice);
  setIfDefined(body, 'tools', options.tools);
  setIfDefined(body, 'top_k', options.topK);
  setIfDefined(body, 'top_p', options.topP);
  setIfDefined(body, 'thinking', options.thinking);
  copyExtra(body, options, MESSAGE_KEYS);
  return body;
}

function countBody(options: ClaudeCountTokensOptions): Record<string, unknown> {
  const body: Record<string, unknown> = { model: options.model, messages: options.messages };
  setIfDefined(body, 'system', options.system);
  setIfDefined(body, 'thinking', options.thinking);
  setIfDefined(body, 'tool_choice', options.toolChoice);
  setIfDefined(body, 'tools', options.tools);
  copyExtra(body, options, COUNT_KEYS);
  return body;
}

class ClaudeChatCompletions {
  constructor(private transport: Transport) {}

  async create(options: ClaudeChatCompletionOptions): Promise<Record<string, unknown> | AsyncGenerator<Record<string, unknown>>> {
    const body = completionBody(options);
    if (body.stream) return this.stream(body);
    return this.transport.request('POST', '/v1/chat/completions', { json: body });
  }

  private async *stream(body: Record<string, unknown>): AsyncGenerator<Record<string, unknown>> {
    for await (const chunk of this.transport.requestStream('POST', '/v1/chat/completions', { json: body })) {
      yield JSON.parse(chunk) as Record<string, unknown>;
    }
  }
}

class ClaudeChat {
  readonly completions: ClaudeChatCompletions;
  constructor(transport: Transport) {
    this.completions = new ClaudeChatCompletions(transport);
  }
}

class ClaudeMessages {
  constructor(private transport: Transport) {}

  async create(options: ClaudeMessageOptions): Promise<Record<string, unknown> | AsyncGenerator<Record<string, unknown>>> {
    const body = messageBody(options);
    if (body.stream) return this.stream(body);
    return this.transport.request('POST', '/v1/messages', { json: body });
  }

  private async *stream(body: Record<string, unknown>): AsyncGenerator<Record<string, unknown>> {
    for await (const chunk of this.transport.requestStream('POST', '/v1/messages', { json: body })) {
      yield JSON.parse(chunk) as Record<string, unknown>;
    }
  }

  async countTokens(options: ClaudeCountTokensOptions): Promise<Record<string, unknown>> {
    return this.transport.request('POST', '/v1/messages/count_tokens', { json: countBody(options) });
  }
}

export class Claude {
  readonly chat: ClaudeChat;
  readonly messages: ClaudeMessages;

  constructor(transport: Transport) {
    this.chat = new ClaudeChat(transport);
    this.messages = new ClaudeMessages(transport);
  }
}
