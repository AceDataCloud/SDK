/** Gemini chat completions and native generate content resources. */

import { Transport } from '../runtime/transport';

export type GeminiModel =
  | 'gemini-3.1-pro'
  | 'gemini-3.0-pro'
  | 'gemini-3.5-flash'
  | 'gemini-3-flash-preview'
  | 'gemini-2.5-pro'
  | 'gemini-2.5-flash'
  | 'gemini-2.0-flash'
  | (string & {});

class Completions {
  constructor(private transport: Transport) {}

  async create(opts: {
    model: GeminiModel;
    messages: Array<Record<string, unknown>>;
    stream?: false;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>>;
  async create(opts: {
    model: GeminiModel;
    messages: Array<Record<string, unknown>>;
    stream: true;
    [key: string]: unknown;
  }): Promise<AsyncGenerator<Record<string, unknown>>>;
  async create(opts: {
    model: GeminiModel;
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
    return this.transport.request('POST', '/gemini/chat/completions', { json: body });
  }

  private async *streamResponse(body: Record<string, unknown>): AsyncGenerator<Record<string, unknown>> {
    for await (const chunk of this.transport.requestStream('POST', '/gemini/chat/completions', { json: body })) {
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

export class Gemini {
  readonly chat: ChatNamespace;

  constructor(private transport: Transport) {
    this.chat = new ChatNamespace(transport);
  }

  async generateContent(opts: {
    model: GeminiModel;
    contents: Array<Record<string, unknown>>;
    systemInstruction?: Record<string, unknown>;
    generationConfig?: Record<string, unknown>;
    tools?: Array<Record<string, unknown>>;
    toolConfig?: Record<string, unknown>;
    safetySettings?: Array<Record<string, unknown>>;
    cachedContent?: string;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { model, contents, systemInstruction, generationConfig, tools, toolConfig, safetySettings, cachedContent, ...rest } = opts;
    const body: Record<string, unknown> = { contents, ...rest };
    if (systemInstruction !== undefined) body.systemInstruction = systemInstruction;
    if (generationConfig !== undefined) body.generationConfig = generationConfig;
    if (tools !== undefined) body.tools = tools;
    if (toolConfig !== undefined) body.toolConfig = toolConfig;
    if (safetySettings !== undefined) body.safetySettings = safetySettings;
    if (cachedContent !== undefined) body.cachedContent = cachedContent;
    return this.transport.request('POST', `/v1beta/models/${model}:generateContent`, { json: body });
  }

  async *streamGenerateContent(opts: {
    model: GeminiModel;
    contents: Array<Record<string, unknown>>;
    systemInstruction?: Record<string, unknown>;
    generationConfig?: Record<string, unknown>;
    tools?: Array<Record<string, unknown>>;
    toolConfig?: Record<string, unknown>;
    safetySettings?: Array<Record<string, unknown>>;
    cachedContent?: string;
    [key: string]: unknown;
  }): AsyncGenerator<Record<string, unknown>> {
    const { model, contents, systemInstruction, generationConfig, tools, toolConfig, safetySettings, cachedContent, ...rest } = opts;
    const body: Record<string, unknown> = { contents, ...rest };
    if (systemInstruction !== undefined) body.systemInstruction = systemInstruction;
    if (generationConfig !== undefined) body.generationConfig = generationConfig;
    if (tools !== undefined) body.tools = tools;
    if (toolConfig !== undefined) body.toolConfig = toolConfig;
    if (safetySettings !== undefined) body.safetySettings = safetySettings;
    if (cachedContent !== undefined) body.cachedContent = cachedContent;
    for await (const chunk of this.transport.requestStream('POST', `/v1beta/models/${model}:streamGenerateContent`, { json: body })) {
      yield JSON.parse(chunk);
    }
  }
}
