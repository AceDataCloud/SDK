/** Gemini provider resource. */

import { Transport } from '../../runtime/transport';
import { TaskHandle } from '../../runtime/tasks';

export type GeminiChatModel =
  | 'gemini-3.1-pro'
  | 'gemini-3.0-pro'
  | 'gemini-3.5-flash'
  | 'gemini-3-flash-preview'
  | 'gemini-2.5-pro'
  | 'gemini-2.5-flash'
  | 'gemini-2.5-flash-lite'
  | 'gemini-2.0-flash'
  | 'gemini-3.1-flash-lite-preview';
export type GeminiVideoModel = 'omni-flash';

function taskId(result: Record<string, unknown>): string {
  if (typeof result.task_id === 'string') return result.task_id;
  const data = result.data as Record<string, unknown> | undefined;
  if (typeof data?.task_id === 'string') return data.task_id;
  return typeof result.id === 'string' ? result.id : '';
}

class Completions {
  constructor(private transport: Transport) {}

  async create(opts: {
    model: GeminiChatModel;
    messages: Array<Record<string, unknown>>;
    stream?: false;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>>;
  async create(opts: {
    model: GeminiChatModel;
    messages: Array<Record<string, unknown>>;
    stream: true;
    [key: string]: unknown;
  }): Promise<AsyncGenerator<Record<string, unknown>>>;
  async create(opts: {
    model: GeminiChatModel;
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

class Chat {
  readonly completions: Completions;

  constructor(transport: Transport) {
    this.completions = new Completions(transport);
  }
}

export class Gemini {
  readonly chat: Chat;

  constructor(private transport: Transport) {
    this.chat = new Chat(transport);
  }

  async generateContent(
    model: string,
    contents: Array<Record<string, unknown>>,
    options: Record<string, unknown> = {},
  ): Promise<Record<string, unknown>> {
    return this.transport.request('POST', `/v1beta/models/${model}:generateContent`, {
      json: { contents, ...options },
    });
  }

  async *streamGenerateContent(
    model: string,
    contents: Array<Record<string, unknown>>,
    options: Record<string, unknown> = {},
  ): AsyncGenerator<Record<string, unknown>> {
    for await (const chunk of this.transport.requestStream('POST', `/v1beta/models/${model}:streamGenerateContent`, {
      json: { contents, ...options },
    })) {
      yield JSON.parse(chunk);
    }
  }

  async videos(opts: {
    prompt: string;
    model?: GeminiVideoModel;
    aspectRatio?: '16:9' | '9:16';
    resolution?: '720p' | '1080p';
    imageUrls?: string[];
    videoUrls?: string[];
    callbackUrl?: string;
    async?: boolean;
    wait?: boolean;
    pollInterval?: number;
    maxWait?: number;
  }): Promise<TaskHandle> {
    const { prompt, model = 'omni-flash', aspectRatio = '16:9', resolution = '720p', imageUrls, videoUrls,
      callbackUrl, async = true, wait, pollInterval, maxWait } = opts;
    const body: Record<string, unknown> = {
      prompt, model, aspect_ratio: aspectRatio, resolution, async,
    };
    if (imageUrls !== undefined) body.image_urls = imageUrls;
    if (videoUrls !== undefined) body.video_urls = videoUrls;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    const result = await this.transport.request('POST', '/gemini/videos', { json: body }) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), '/gemini/tasks', this.transport, result);
    if (wait) await handle.wait({ pollInterval, maxWait });
    return handle;
  }
}
