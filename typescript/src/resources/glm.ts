/** GLM chat completions resource. */

import { Transport } from '../runtime/transport';

export type GlmModel =
  | 'glm-5.3'
  | 'glm-5.2'
  | 'glm-5'
  | 'glm-5-turbo'
  | 'glm-5.1'
  | 'glm-4.7'
  | 'glm-4.6'
  | 'glm-3-turbo'
  | (string & {});

export type GlmReasoningEffort =
  'minimal' | 'low' | 'medium' | 'high' | (string & {});
export type GlmServiceTier =
  'auto' | 'default' | 'flex' | 'scale' | 'priority' | (string & {});

class Completions {
  constructor(private transport: Transport) {}

  async create(opts: {
    model: GlmModel;
    messages: Array<Record<string, unknown>>;
    n?: number | null;
    stream?: false | null;
    max_tokens?: number | null;
    temperature?: number | null;
    response_format?: Record<string, unknown>;
    top_p?: number | null;
    frequency_penalty?: number | null;
    presence_penalty?: number | null;
    seed?: number | null;
    stop?: string | string[] | null;
    max_completion_tokens?: number | null;
    logprobs?: boolean | null;
    top_logprobs?: number | null;
    stream_options?: Record<string, unknown> | null;
    parallel_tool_calls?: boolean;
    user?: string;
    reasoning_effort?: GlmReasoningEffort | null;
    service_tier?: GlmServiceTier | null;
    store?: boolean | null;
    metadata?: Record<string, string> | null;
    logit_bias?: Record<string, number> | null;
    modalities?: Array<'text' | 'audio'> | null;
    audio?: Record<string, unknown> | null;
    prediction?: Record<string, unknown> | null;
    web_search_options?: Record<string, unknown>;
    tools?: Array<Record<string, unknown>> | null;
    tool_choice?: string | Record<string, unknown>;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>>;
  async create(opts: {
    model: GlmModel;
    messages: Array<Record<string, unknown>>;
    stream: true;
    [key: string]: unknown;
  }): Promise<AsyncGenerator<Record<string, unknown>>>;
  async create(opts: {
    model: GlmModel;
    messages: Array<Record<string, unknown>>;
    stream?: boolean | null;
    [key: string]: unknown;
  }): Promise<
    Record<string, unknown> | AsyncGenerator<Record<string, unknown>>
  > {
    const { model, messages, stream, ...rest } = opts;
    const body: Record<string, unknown> = { model, messages, ...rest };

    if (stream) {
      body.stream = true;
      return this.streamResponse(body);
    }
    return this.transport.request('POST', '/glm/chat/completions', {
      json: body,
    });
  }

  private async *streamResponse(
    body: Record<string, unknown>,
  ): AsyncGenerator<Record<string, unknown>> {
    for await (const chunk of this.transport.requestStream(
      'POST',
      '/glm/chat/completions',
      { json: body },
    )) {
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

export class Glm {
  readonly chat: ChatNamespace;

  constructor(transport: Transport) {
    this.chat = new ChatNamespace(transport);
  }
}
