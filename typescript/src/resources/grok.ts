/** Grok resources — chat completions and video generation. */

import { Transport } from '../runtime/transport';
import { TaskHandle } from '../runtime/tasks';

export const GROK_CHAT_MODELS = ['grok-4.5', 'grok-4', 'grok-3'] as const;
export type GrokChatModel = (typeof GROK_CHAT_MODELS)[number];

export const GROK_VIDEO_MODELS = [
  'grok-imagine-video-1.5-fast:reverse',
  'grok-imagine-video:reverse',
  'grok-imagine-video:official',
  'grok-imagine-video-1.5:official',
  'grok-imagine-video',
] as const;
export type GrokVideoModel = (typeof GROK_VIDEO_MODELS)[number];

function taskId(result: Record<string, unknown>): string {
  if (typeof result?.task_id === 'string') return result.task_id;
  const data = result?.data as Record<string, unknown> | undefined;
  if (data && typeof data.task_id === 'string') return data.task_id;
  return typeof result?.id === 'string' ? result.id : '';
}

class GrokCompletions {
  constructor(private transport: Transport) {}

  async create(opts: {
    model: GrokChatModel | string;
    messages: Array<Record<string, unknown>>;
    stream?: false;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>>;
  async create(opts: {
    model: GrokChatModel | string;
    messages: Array<Record<string, unknown>>;
    stream: true;
    [key: string]: unknown;
  }): Promise<AsyncGenerator<Record<string, unknown>>>;
  async create(opts: {
    model: GrokChatModel | string;
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
    return this.transport.request('POST', '/grok/chat/completions', { json: body });
  }

  private async *streamResponse(body: Record<string, unknown>): AsyncGenerator<Record<string, unknown>> {
    for await (const chunk of this.transport.requestStream('POST', '/grok/chat/completions', { json: body })) {
      yield JSON.parse(chunk);
    }
  }
}

class GrokChat {
  readonly completions: GrokCompletions;
  constructor(transport: Transport) {
    this.completions = new GrokCompletions(transport);
  }
}

export class Grok {
  readonly chat: GrokChat;

  constructor(private transport: Transport) {
    this.chat = new GrokChat(transport);
  }

  async generate(opts: {
    prompt?: string;
    model?: GrokVideoModel | string;
    imageUrl?: string;
    referenceImageUrls?: string[];
    aspectRatio?: '1:1' | '16:9' | '9:16' | '4:3' | '3:4' | '3:2' | '2:3';
    resolution?: '480p' | '720p' | '1080p';
    duration?: number;
    callbackUrl?: string;
    async?: boolean;
    [key: string]: unknown;
  }): Promise<TaskHandle> {
    const { prompt, model, imageUrl, referenceImageUrls, aspectRatio, resolution, duration, callbackUrl, ...rest } = opts;
    const body: Record<string, unknown> = { ...rest };
    if (prompt !== undefined) body.prompt = prompt;
    if (model !== undefined) body.model = model;
    if (imageUrl !== undefined) body.image_url = imageUrl;
    if (referenceImageUrls !== undefined) body.reference_image_urls = referenceImageUrls;
    if (aspectRatio !== undefined) body.aspect_ratio = aspectRatio;
    if (resolution !== undefined) body.resolution = resolution;
    if (duration !== undefined) body.duration = duration;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    const result = (await this.transport.request('POST', '/grok/videos', { json: body })) as Record<string, unknown>;
    return new TaskHandle(taskId(result), '/grok/tasks', this.transport, result);
  }
}
