/** Gemini resources. */

import { TaskHandle } from '../runtime/tasks';
import { Transport } from '../runtime/transport';

export type GeminiModel =
  | 'gemini-3.7-flash'
  | 'gemini-3.6-flash'
  | 'gemini-3.5-flash'
  | 'gemini-3.5-flash-lite'
  | 'gemini-3.1-flash-lite'
  | 'gemini-3.1-pro-preview'
  | 'gemini-3-flash-preview'
  | 'gemini-2.5-pro'
  | 'gemini-2.5-flash'
  | 'gemini-2.5-flash-lite'
  | 'gemini-3.1-flash-image'
  | 'gemini-2.5-flash-image'
  | 'gemini-3-pro-image';

function taskId(result: Record<string, unknown>): string {
  return typeof result.task_id === 'string' ? result.task_id : typeof result.id === 'string' ? result.id : '';
}

export class Gemini {
  constructor(private transport: Transport) {}

  async chatCompletions(opts: {
    model: GeminiModel;
    messages: Array<Record<string, unknown>>;
    stream?: false;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>>;
  async chatCompletions(opts: {
    model: GeminiModel;
    messages: Array<Record<string, unknown>>;
    stream: true;
    [key: string]: unknown;
  }): Promise<AsyncGenerator<Record<string, unknown>>>;
  async chatCompletions(opts: {
    model: GeminiModel;
    messages: Array<Record<string, unknown>>;
    stream?: boolean;
    [key: string]: unknown;
  }): Promise<Record<string, unknown> | AsyncGenerator<Record<string, unknown>>> {
    const { stream, ...body } = opts;
    if (stream) return this.stream('/gemini/chat/completions', { ...body, stream: true });
    return this.transport.request('POST', '/gemini/chat/completions', { json: body });
  }

  async generateContent(
    model: GeminiModel,
    contents: Array<Record<string, unknown>>,
    extra: Record<string, unknown> = {}
  ): Promise<Record<string, unknown>> {
    return this.transport.request('POST', `/v1beta/models/${model}:generateContent`, {
      json: { contents, ...extra },
    });
  }

  streamGenerateContent(
    model: GeminiModel,
    contents: Array<Record<string, unknown>>,
    extra: Record<string, unknown> = {}
  ): AsyncGenerator<Record<string, unknown>> {
    return this.stream(`/v1beta/models/${model}:streamGenerateContent`, { contents, ...extra });
  }

  async generateVideo(opts: {
    prompt: string;
    model?: 'omni-flash';
    aspectRatio?: '16:9' | '9:16';
    resolution?: '720p' | '1080p';
    imageUrls?: string[];
    videoUrls?: string[];
    async?: boolean;
    wait?: boolean;
    pollInterval?: number;
    maxWait?: number;
    callbackUrl?: string;
  }): Promise<TaskHandle> {
    const { async: async_, wait, pollInterval, maxWait, callbackUrl, imageUrls, videoUrls, ...rest } = opts;
    const body: Record<string, unknown> = {
      ...rest,
      model: opts.model ?? 'omni-flash',
      aspect_ratio: opts.aspectRatio ?? '16:9',
      resolution: opts.resolution ?? '720p',
      async: async_ ?? true,
    };
    if (imageUrls !== undefined) body.image_urls = imageUrls;
    if (videoUrls !== undefined) body.video_urls = videoUrls;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    const result = (await this.transport.request('POST', '/gemini/videos', { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), '/gemini/tasks', this.transport, result);
    if (wait) await handle.wait({ pollInterval, maxWait });
    return handle;
  }

  async tasks(opts: { id?: string; ids?: string[]; action?: 'retrieve' | 'retrieve_batch' } = {}): Promise<Record<string, unknown>> {
    const { id, ids, action = 'retrieve' } = opts;
    const body: Record<string, unknown> = { action };
    if (id !== undefined) body.id = id;
    if (ids !== undefined) body.ids = ids;
    return this.transport.request('POST', '/gemini/tasks', { json: body });
  }

  private async *stream(path: string, body: Record<string, unknown>): AsyncGenerator<Record<string, unknown>> {
    for await (const chunk of this.transport.requestStream('POST', path, { json: body })) yield JSON.parse(chunk);
  }
}
