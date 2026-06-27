/** Grok chat completions and video generation resources. */

import { Transport } from '../runtime/transport';

export type GrokModel = 'grok-4' | 'grok-3' | (string & {});
export type GrokVideoModel = 'grok-imagine-video' | 'grok-imagine-video-1.5-preview' | (string & {});

class Completions {
  constructor(private transport: Transport) {}

  async create(opts: {
    model: GrokModel;
    messages: Array<Record<string, unknown>>;
    stream?: false;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>>;
  async create(opts: {
    model: GrokModel;
    messages: Array<Record<string, unknown>>;
    stream: true;
    [key: string]: unknown;
  }): Promise<AsyncGenerator<Record<string, unknown>>>;
  async create(opts: {
    model: GrokModel;
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

class ChatNamespace {
  readonly completions: Completions;
  constructor(transport: Transport) {
    this.completions = new Completions(transport);
  }
}

export class Grok {
  readonly chat: ChatNamespace;

  constructor(private transport: Transport) {
    this.chat = new ChatNamespace(transport);
  }

  async generateVideo(opts: {
    prompt?: string;
    model?: GrokVideoModel;
    imageUrl?: string;
    referenceImageUrls?: string[];
    aspectRatio?: '1:1' | '16:9' | '9:16' | '4:3' | '3:4' | '3:2' | '2:3';
    resolution?: '480p' | '720p' | '1080p';
    duration?: number;
    callbackUrl?: string;
    async?: boolean;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { prompt, model, imageUrl, referenceImageUrls, aspectRatio, resolution, duration, callbackUrl, async: asyncFlag, ...rest } = opts;
    const body: Record<string, unknown> = { ...rest };
    if (prompt !== undefined) body.prompt = prompt;
    if (model !== undefined) body.model = model;
    if (imageUrl !== undefined) body.image_url = imageUrl;
    if (referenceImageUrls !== undefined) body.reference_image_urls = referenceImageUrls;
    if (aspectRatio !== undefined) body.aspect_ratio = aspectRatio;
    if (resolution !== undefined) body.resolution = resolution;
    if (duration !== undefined) body.duration = duration;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    if (asyncFlag !== undefined) body.async = asyncFlag;
    return this.transport.request('POST', '/grok/videos', { json: body });
  }
}
