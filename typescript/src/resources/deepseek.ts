/** DeepSeek chat completions resource. */

import { Transport } from '../runtime/transport';

export type DeepseekModel =
  | 'deepseek-r1'
  | 'deepseek-r1-0528'
  | 'deepseek-v3'
  | 'deepseek-v3-250324'
  | 'deepseek-v3.2-exp'
  | 'deepseek-v4-flash'
  | 'deepseek-v4-pro'
  | (string & {});
export type DeepseekReasoningEffort = 'minimal' | 'low' | 'medium' | 'high';
export type DeepseekServiceTier = 'auto' | 'default' | 'flex' | 'scale' | 'priority';
export type DeepseekModality = 'text' | 'audio';

export interface DeepseekCreateOptions {
  model: DeepseekModel;
  messages: Array<Record<string, unknown>>;
  n?: number;
  stream?: boolean;
  max_tokens?: number;
  temperature?: number;
  response_format?: unknown;
  top_p?: number;
  frequency_penalty?: number;
  presence_penalty?: number;
  seed?: number;
  stop?: unknown;
  max_completion_tokens?: number;
  logprobs?: boolean;
  top_logprobs?: number;
  stream_options?: Record<string, unknown>;
  parallel_tool_calls?: boolean;
  user?: string;
  reasoning_effort?: DeepseekReasoningEffort;
  service_tier?: DeepseekServiceTier;
  store?: boolean;
  metadata?: Record<string, unknown>;
  logit_bias?: Record<string, unknown>;
  modalities?: DeepseekModality[];
  audio?: Record<string, unknown>;
  prediction?: Record<string, unknown>;
  web_search_options?: Record<string, unknown>;
  tools?: Array<Record<string, unknown>>;
  tool_choice?: unknown;
  [key: string]: unknown;
}

class Completions {
  constructor(private transport: Transport) {}

  async create(opts: DeepseekCreateOptions & { stream: true }): Promise<AsyncGenerator<Record<string, unknown>>>;
  async create(opts: DeepseekCreateOptions & { stream?: false }): Promise<Record<string, unknown>>;
  async create(opts: DeepseekCreateOptions): Promise<Record<string, unknown> | AsyncGenerator<Record<string, unknown>>> {
    const { model, messages, stream, ...rest } = opts;
    const body: Record<string, unknown> = { model, messages, ...rest };

    if (stream) {
      body.stream = true;
      return this.streamResponse(body);
    }
    return this.transport.request('POST', '/deepseek/chat/completions', { json: body });
  }

  private async *streamResponse(body: Record<string, unknown>): AsyncGenerator<Record<string, unknown>> {
    for await (const chunk of this.transport.requestStream('POST', '/deepseek/chat/completions', { json: body })) {
      yield JSON.parse(chunk);
    }
  }
}

class ChatNamespace {
  readonly completions: Completions;
  constructor(transport: Transport) {
    this.completions = new Completions(transport);
  }
}

export class Deepseek {
  readonly chat: ChatNamespace;

  constructor(transport: Transport) {
    this.chat = new ChatNamespace(transport);
  }
}
