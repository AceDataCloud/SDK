/** Chat resources — native provider APIs (Claude Messages). */

import { Transport } from '../runtime/transport';

export class Messages {
  constructor(private transport: Transport) {}

  async create(opts: {
    model: string;
    messages: Array<Record<string, unknown>>;
    maxTokens?: number;
    stream?: false;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>>;
  async create(opts: {
    model: string;
    messages: Array<Record<string, unknown>>;
    maxTokens?: number;
    stream: true;
    [key: string]: unknown;
  }): Promise<AsyncGenerator<Record<string, unknown>>>;
  async create(opts: {
    model: string;
    messages: Array<Record<string, unknown>>;
    maxTokens?: number;
    stream?: boolean;
    [key: string]: unknown;
  }): Promise<Record<string, unknown> | AsyncGenerator<Record<string, unknown>>> {
    const { model, messages, maxTokens = 4096, stream, ...rest } = opts;
    const body: Record<string, unknown> = { model, messages, max_tokens: maxTokens, ...rest };

    if (stream) {
      body.stream = true;
      return this.stream(body);
    }
    return this.transport.request('POST', '/v1/messages', { json: body });
  }

  private async *stream(body: Record<string, unknown>): AsyncGenerator<Record<string, unknown>> {
    for await (const chunk of this.transport.requestStream('POST', '/v1/messages', { json: body })) {
      yield JSON.parse(chunk);
    }
  }

  async countTokens(opts: {
    model: string;
    messages: Array<Record<string, unknown>>;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { model, messages, ...rest } = opts;
    return this.transport.request('POST', '/v1/messages/count_tokens', {
      json: { model, messages, ...rest },
    });
  }
}

export class Chat {
  readonly messages: Messages;

  constructor(transport: Transport) {
    this.messages = new Messages(transport);
  }
}
