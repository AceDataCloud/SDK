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
export type GeminiContentModel =
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
  | 'gemini-3-pro-image';
export type GeminiVideoModel = 'omni-flash';
export type GeminiVideoAspectRatio = '16:9' | '9:16';
export type GeminiVideoResolution = '720p' | '1080p';

function taskId(result: Record<string, unknown>): string {
  if (typeof result.task_id === 'string') return result.task_id;
  const data = result.data as Record<string, unknown> | undefined;
  if (data && typeof data.task_id === 'string') return data.task_id;
  return typeof result.id === 'string' ? result.id : '';
}

function contentPath(model: string, stream = false): string {
  const suffix = stream ? 'streamGenerateContent?alt=sse' : 'generateContent';
  return `/v1beta/models/${encodeURIComponent(model)}:${suffix}`;
}

interface ChatCreateOptions {
  model: GeminiChatModel;
  messages: Array<Record<string, unknown>>;
  stream?: boolean;
  n?: number;
  max_tokens?: number;
  temperature?: number;
  response_format?: unknown;
  top_p?: number;
  frequency_penalty?: number;
  presence_penalty?: number;
  seed?: number;
  stop?: unknown;
  max_completion_tokens?: number;
  logprobs?: boolean;
  top_logprobs?: number;
  stream_options?: Record<string, unknown>;
  parallel_tool_calls?: boolean;
  user?: string;
  reasoning_effort?: 'minimal' | 'low' | 'medium' | 'high';
  service_tier?: 'auto' | 'default' | 'flex' | 'scale' | 'priority';
  store?: boolean;
  metadata?: Record<string, unknown>;
  logit_bias?: Record<string, unknown>;
  modalities?: unknown[];
  audio?: Record<string, unknown>;
  prediction?: Record<string, unknown>;
  web_search_options?: Record<string, unknown>;
  tools?: Array<Record<string, unknown>>;
  tool_choice?: unknown;
  [key: string]: unknown;
}

interface GenerateContentOptions {
  model: GeminiContentModel;
  contents: Array<Record<string, unknown>>;
  systemInstruction?: Record<string, unknown>;
  generationConfig?: Record<string, unknown>;
  tools?: Array<Record<string, unknown>>;
  toolConfig?: Record<string, unknown>;
  safetySettings?: Array<Record<string, unknown>>;
  [key: string]: unknown;
}

interface VideoGenerateOptions {
  prompt: string;
  model?: GeminiVideoModel;
  aspectRatio?: GeminiVideoAspectRatio;
  resolution?: GeminiVideoResolution;
  imageUrls?: string[];
  videoUrls?: string[];
  async?: boolean;
  wait?: boolean;
  pollInterval?: number;
  maxWait?: number;
  callbackUrl?: string;
  [key: string]: unknown;
}

function chatBody(opts: ChatCreateOptions): Record<string, unknown> {
  const { model, messages, stream, ...rest } = opts;
  return {
    model,
    messages,
    stream: stream ?? false,
    n: rest.n ?? 1,
    temperature: rest.temperature ?? 1,
    top_p: rest.top_p ?? 1,
    frequency_penalty: rest.frequency_penalty ?? 0,
    presence_penalty: rest.presence_penalty ?? 0,
    logprobs: rest.logprobs ?? false,
    parallel_tool_calls: rest.parallel_tool_calls ?? true,
    reasoning_effort: rest.reasoning_effort ?? 'medium',
    service_tier: rest.service_tier ?? 'auto',
    store: rest.store ?? false,
    ...rest,
  };
}

function contentBody(opts: GenerateContentOptions): Record<string, unknown> {
  const { model: _model, contents, ...rest } = opts;
  return { contents, ...rest };
}

class Completions {
  constructor(private transport: Transport) {}

  async create(opts: ChatCreateOptions & { stream: true }): Promise<AsyncGenerator<Record<string, unknown>>>;
  async create(opts: ChatCreateOptions & { stream?: false }): Promise<Record<string, unknown>>;
  async create(opts: ChatCreateOptions): Promise<Record<string, unknown> | AsyncGenerator<Record<string, unknown>>> {
    const body = chatBody(opts);
    if (opts.stream) return this.streamResponse(body);
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

class Videos {
  constructor(private transport: Transport) {}

  async generate(opts: VideoGenerateOptions): Promise<TaskHandle> {
    const { prompt, model, aspectRatio, imageUrls, videoUrls, callbackUrl, wait, pollInterval, maxWait, ...rest } = opts;
    const body: Record<string, unknown> = {
      prompt,
      model: model ?? 'omni-flash',
      aspect_ratio: aspectRatio ?? '16:9',
      resolution: opts.resolution ?? '720p',
      async: opts.async ?? true,
      ...rest,
    };
    if (imageUrls !== undefined) body.image_urls = imageUrls;
    if (videoUrls !== undefined) body.video_urls = videoUrls;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    const result = await this.transport.request('POST', '/gemini/videos', { json: body });
    const handle = new TaskHandle(taskId(result), '/gemini/tasks', this.transport, result);
    if (wait) await handle.wait({ pollInterval, maxWait });
    return handle;
  }
}

class Tasks {
  constructor(private transport: Transport) {}

  async retrieve(opts: { id: string; [key: string]: unknown }): Promise<Record<string, unknown>> {
    return this.transport.request('POST', '/gemini/tasks', { json: { action: 'retrieve', ...opts } });
  }

  async retrieveBatch(opts: { ids?: string[]; [key: string]: unknown } = {}): Promise<Record<string, unknown>> {
    return this.transport.request('POST', '/gemini/tasks', { json: { action: 'retrieve_batch', ...opts } });
  }
}

export class Gemini {
  readonly chat: ChatNamespace;
  readonly videos: Videos;
  readonly tasks: Tasks;

  constructor(private transport: Transport) {
    this.chat = new ChatNamespace(transport);
    this.videos = new Videos(transport);
    this.tasks = new Tasks(transport);
  }

  async generateContent(opts: GenerateContentOptions): Promise<Record<string, unknown>> {
    return this.transport.request('POST', contentPath(opts.model), { json: contentBody(opts) });
  }

  async *streamGenerateContent(opts: GenerateContentOptions): AsyncGenerator<Record<string, unknown>> {
    for await (const chunk of this.transport.requestStream('POST', contentPath(opts.model, true), {
      json: contentBody(opts),
    })) {
      yield JSON.parse(chunk);
    }
  }
}
