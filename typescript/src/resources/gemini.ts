/**
 * Gemini resources — OpenAI-compatible chat, video generation, native v1beta.
 *
 * Hand-written rather than generated: the service spans three shapes the
 * provider generator does not model — an OpenAI-compatible chat surface, an
 * async video endpoint, and Google's native `generateContent` calls with the
 * model in the path.
 */

import { Transport } from '../runtime/transport';
import { TaskHandle } from '../runtime/tasks';

export type GeminiChatModel =
  | 'gemini-3.1-pro'
  | 'gemini-3.0-pro'
  | 'gemini-3.5-flash'
  | 'gemini-3-flash-preview'
  | 'gemini-2.5-pro'
  | 'gemini-2.5-flash'
  | 'gemini-2.5-flash-lite'
  | 'gemini-2.0-flash'
  | 'gemini-3.1-flash-lite-preview'
  | (string & {});

export type GeminiNativeModel =
  | 'gemini-2.0-flash'
  | 'gemini-2.5-flash'
  | 'gemini-2.5-flash-lite'
  | 'gemini-2.5-pro'
  | 'gemini-3-flash-preview'
  | 'gemini-3.5-flash'
  | 'gemini-3.0-pro'
  | 'gemini-3.1-pro'
  | 'gemini-3.1-flash-lite-preview'
  | 'gemini-3.1-flash-image'
  | 'gemini-2.5-flash-image'
  | 'gemini-3-pro-image'
  | (string & {});

export type GeminiVideoModel = 'omni-flash';
export type GeminiVideoAspectRatio = '16:9' | '9:16';
export type GeminiVideoResolution = '720p' | '1080p';

const CHAT_PATH = '/gemini/chat/completions';
const VIDEOS_PATH = '/gemini/videos';
const TASKS_PATH = '/gemini/tasks';

function taskId(result: Record<string, unknown>): string {
  if (typeof result?.task_id === 'string') return result.task_id;
  const data = result?.data as Record<string, unknown> | undefined;
  if (data && typeof data.task_id === 'string') return data.task_id;
  return typeof result?.id === 'string' ? result.id : '';
}

function nativePath(model: string, stream: boolean): string {
  return `/v1beta/models/${encodeURIComponent(model)}:${stream ? 'streamGenerateContent' : 'generateContent'}`;
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
    return this.transport.request('POST', CHAT_PATH, { json: body });
  }

  private async *streamResponse(body: Record<string, unknown>): AsyncGenerator<Record<string, unknown>> {
    for await (const chunk of this.transport.requestStream('POST', CHAT_PATH, { json: body })) {
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

export interface GeminiVideoGenerateOptions {
  /** Prompt describing the video to generate. */
  prompt: string;
  model?: GeminiVideoModel;
  aspectRatio?: GeminiVideoAspectRatio;
  resolution?: GeminiVideoResolution;
  imageUrls?: string[];
  /** At most one reference video URL. */
  videoUrls?: string[];
  callbackUrl?: string;
  /** Submit asynchronously and poll. Defaults to true. */
  async?: boolean;
  /** Wait for completion before returning the handle. */
  wait?: boolean;
  pollInterval?: number;
  maxWait?: number;
  /** Any parameter added upstream before the SDK is updated. */
  [key: string]: unknown;
}

const VIDEO_CONTROL_KEYS = [
  'prompt',
  'model',
  'aspectRatio',
  'resolution',
  'imageUrls',
  'videoUrls',
  'callbackUrl',
  'async',
  'wait',
  'pollInterval',
  'maxWait',
];

class Videos {
  constructor(private transport: Transport) {}

  async generate(options: GeminiVideoGenerateOptions): Promise<TaskHandle> {
    if (options.videoUrls !== undefined && options.videoUrls.length > 1) {
      throw new Error('videoUrls accepts at most 1 video URL');
    }
    const body: Record<string, unknown> = { prompt: options.prompt };
    body.model = options.model ?? 'omni-flash';
    body.aspect_ratio = options.aspectRatio ?? '16:9';
    body.resolution = options.resolution ?? '720p';
    if (options.imageUrls !== undefined) body.image_urls = options.imageUrls;
    if (options.videoUrls !== undefined) body.video_urls = options.videoUrls;
    for (const [key, value] of Object.entries(options)) {
      if (!VIDEO_CONTROL_KEYS.includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    body.async = options.async ?? true;

    const result = (await this.transport.request('POST', VIDEOS_PATH, { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), TASKS_PATH, this.transport, result);
    if (options.wait) {
      await handle.wait({ pollInterval: options.pollInterval, maxWait: options.maxWait });
    }
    return handle;
  }
}

/** Gemini client. */
export class Gemini {
  readonly chat: ChatNamespace;
  readonly videos: Videos;

  constructor(private transport: Transport) {
    this.chat = new ChatNamespace(transport);
    this.videos = new Videos(transport);
  }

  /** Google's native `POST /v1beta/models/{model}:generateContent`. */
  async generateContent(opts: {
    model: GeminiNativeModel;
    contents: Array<Record<string, unknown>>;
    [key: string]: unknown;
  }): Promise<Record<string, unknown>> {
    const { model, contents, ...rest } = opts;
    return this.transport.request('POST', nativePath(model, false), {
      json: { contents, ...rest },
    });
  }

  /** Google's native `POST /v1beta/models/{model}:streamGenerateContent`. */
  async *streamGenerateContent(opts: {
    model: GeminiNativeModel;
    contents: Array<Record<string, unknown>>;
    [key: string]: unknown;
  }): AsyncGenerator<Record<string, unknown>> {
    const { model, contents, ...rest } = opts;
    for await (const chunk of this.transport.requestStream('POST', nativePath(model, true), {
      json: { contents, ...rest },
    })) {
      yield JSON.parse(chunk);
    }
  }
}
