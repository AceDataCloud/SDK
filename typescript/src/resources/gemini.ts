/** Gemini chat, content generation, and video resources. */

import { Transport } from '../runtime/transport';
import { TaskHandle } from '../runtime/tasks';

export type GeminiModel =
  | 'gemini-3.1-pro' | 'gemini-3.0-pro' | 'gemini-3.6-flash' | 'gemini-3.5-flash'
  | 'gemini-3-flash-preview' | 'gemini-2.5-pro' | 'gemini-2.5-flash'
  | 'gemini-2.5-flash-lite' | 'gemini-2.0-flash' | 'gemini-3.1-flash-lite-preview';

export interface GeminiVideoOptions {
  prompt: string;
  model?: 'omni-flash';
  aspectRatio?: '16:9' | '9:16';
  resolution?: '720p' | '1080p';
  imageUrls?: string[];
  videoUrls?: string[];
  callbackUrl?: string;
  async?: boolean;
  wait?: boolean;
  pollInterval?: number;
  maxWait?: number;
}

function taskId(result: Record<string, unknown>): string {
  return typeof result.task_id === 'string' ? result.task_id : typeof result.id === 'string' ? result.id : '';
}

class Completions {
  constructor(private transport: Transport) {}

  async create(options: { model: GeminiModel; messages: Array<Record<string, unknown>>; stream?: boolean; [key: string]: unknown }): Promise<Record<string, unknown> | AsyncGenerator<Record<string, unknown>>> {
    const { model, messages, stream, ...rest } = options;
    const body = { model, messages, ...rest, ...(stream ? { stream: true } : {}) };
    if (!stream) return this.transport.request('POST', '/gemini/chat/completions', { json: body });
    return this.stream(body);
  }

  private async *stream(body: Record<string, unknown>): AsyncGenerator<Record<string, unknown>> {
    for await (const chunk of this.transport.requestStream('POST', '/gemini/chat/completions', { json: body })) yield JSON.parse(chunk);
  }
}

export class Gemini {
  readonly chat: { completions: Completions };

  constructor(private transport: Transport) {
    this.chat = { completions: new Completions(transport) };
  }

  async generateContent(options: { model: string; contents: Array<Record<string, unknown>>; [key: string]: unknown }): Promise<Record<string, unknown>> {
    const { model, contents, ...rest } = options;
    return this.transport.request('POST', `/v1beta/models/${model}:generateContent`, { json: { contents, ...rest } });
  }

  async streamGenerateContent(options: { model: string; contents: Array<Record<string, unknown>>; [key: string]: unknown }): Promise<AsyncGenerator<Record<string, unknown>>> {
    const { model, contents, ...rest } = options;
    return this.streamContent(`/v1beta/models/${model}:streamGenerateContent`, { contents, ...rest });
  }

  private async *streamContent(path: string, body: Record<string, unknown>): AsyncGenerator<Record<string, unknown>> {
    for await (const chunk of this.transport.requestStream('POST', path, { json: body })) yield JSON.parse(chunk);
  }

  async generate(options: GeminiVideoOptions): Promise<TaskHandle> {
    const body: Record<string, unknown> = {
      prompt: options.prompt, model: options.model ?? 'omni-flash',
      aspect_ratio: options.aspectRatio ?? '16:9', resolution: options.resolution ?? '720p',
      async: options.async ?? true,
    };
    if (options.imageUrls) body.image_urls = options.imageUrls;
    if (options.videoUrls) body.video_urls = options.videoUrls;
    if (options.callbackUrl) body.callback_url = options.callbackUrl;
    const result = await this.transport.request('POST', '/gemini/videos', { json: body }) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), '/gemini/tasks', this.transport, result);
    if (options.wait) await handle.wait({ pollInterval: options.pollInterval, maxWait: options.maxWait });
    return handle;
  }
}
