/** Kimi chat completions resource. */

import { Transport } from '../runtime/transport';

export type KimiModel =
  | 'kimi-k3'
  | 'kimi-k2.6'
  | 'kimi-k2-thinking-turbo'
  | 'kimi-k2.5'
  | 'kimi-k2-thinking'
  | 'kimi-k2-instruct-0905'
  | 'kimi-k2-0905-preview'
  | 'kimi-k2-turbo-preview'
  | 'kimi-k2-0711-preview'
  | (string & {});

class Completions {
  constructor(private transport: Transport) {}

  async create(opts: {
    model: KimiModel;
    messages: Array<Record<string, unknown>>;
    stream?: false;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>>;
  async create(opts: {
    model: KimiModel;
    messages: Array<Record<string, unknown>>;
    stream: true;
    [key: string]: unknown;
  }): Promise<AsyncGenerator<Record<string, unknown>>>;
  async create(opts: {
    model: KimiModel;
    messages: Array<Record<string, unknown>>;
    stream?: boolean;
    [key: string]: unknown;
  }): Promise<Record<string, unknown> | AsyncGenerator<Record<string, unknown>>> {
    const { model, messages, stream, ...rest } = opts;
    const body: Record<string, unknown> = { model, messages, ...rest };

    if (stream) {
      body.stream = true;
      return this.streamResponse(body);
    }
    return this.transport.request('POST', '/kimi/chat/completions', { json: body });
  }

  private async *streamResponse(body: Record<string, unknown>): AsyncGenerator<Record<string, unknown>> {
    for await (const chunk of this.transport.requestStream('POST', '/kimi/chat/completions', { json: body })) {
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

export class Kimi {
  readonly chat: ChatNamespace;

  constructor(transport: Transport) {
    this.chat = new ChatNamespace(transport);
  }
}
