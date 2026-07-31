/**
 * Grok (grok) — provider client for Grok chat completions and video generation.
 */

import { Transport } from '../../runtime/transport';
import { TaskHandle } from '../../runtime/tasks';

export type GrokChatModel = 'grok-4.5' | 'grok-4' | 'grok-3';
export type GrokVideoModel =
  | 'grok-imagine-video-1.5-fast:reverse'
  | 'grok-imagine-video:reverse'
  | 'grok-imagine-video:official'
  | 'grok-imagine-video-1.5:official'
  | 'grok-imagine-video';
export type GrokVideoAspectRatio = '1:1' | '16:9' | '9:16' | '4:3' | '3:4' | '3:2' | '2:3';
export type GrokVideoResolution = '480p' | '720p' | '1080p';

function taskId(result: Record<string, unknown>): string {
  if (typeof result?.task_id === 'string') return result.task_id;
  const data = result?.data as Record<string, unknown> | undefined;
  if (data && typeof data.task_id === 'string') return data.task_id;
  return typeof result?.id === 'string' ? result.id : '';
}

class GrokCompletions {
  constructor(private transport: Transport) {}

  async create(opts: {
    model: string;
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

class GrokChatNamespace {
  readonly completions: GrokCompletions;
  constructor(transport: Transport) {
    this.completions = new GrokCompletions(transport);
  }
}

export interface GrokVideoGenerateOptions {
  prompt?: string;
  model?: GrokVideoModel;
  imageUrl?: string;
  referenceImageUrls?: string[];
  aspectRatio?: GrokVideoAspectRatio;
  resolution?: GrokVideoResolution;
  duration?: number;
  async?: boolean;
  wait?: boolean;
  pollInterval?: number;
  maxWait?: number;
  callbackUrl?: string;
  [key: string]: unknown;
}

class GrokVideos {
  constructor(private transport: Transport) {}

  async generate(opts: GrokVideoGenerateOptions): Promise<TaskHandle> {
    const { prompt, model, imageUrl, referenceImageUrls, aspectRatio, resolution, duration, callbackUrl, ...rest } = opts;
    const body: Record<string, unknown> = {};
    if (prompt !== undefined) body.prompt = prompt;
    if (model !== undefined) body.model = model;
    if (imageUrl !== undefined) body.image_url = imageUrl;
    if (referenceImageUrls !== undefined) body.reference_image_urls = referenceImageUrls;
    if (aspectRatio !== undefined) body.aspect_ratio = aspectRatio;
    if (resolution !== undefined) body.resolution = resolution;
    if (duration !== undefined) body.duration = duration;
    for (const [key, value] of Object.entries(rest)) {
      if (!['async', 'maxWait', 'pollInterval', 'wait'].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    if (opts.async !== undefined) body.async = opts.async;
    const result = (await this.transport.request('POST', '/grok/videos', { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), '/grok/tasks', this.transport, result);
    if (opts.wait) {
      await handle.wait({ pollInterval: opts.pollInterval, maxWait: opts.maxWait });
    }
    return handle;
  }
}

export class Grok {
  readonly chat: GrokChatNamespace;
  readonly videos: GrokVideos;

  constructor(transport: Transport) {
    this.chat = new GrokChatNamespace(transport);
    this.videos = new GrokVideos(transport);
  }
}
