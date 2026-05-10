/** Audio/music generation resources. */

import { Transport } from '../runtime/transport';
import { TaskHandle } from '../runtime/tasks';

export type AudioProvider = 'suno' | 'producer' | 'fish' | (string & {});

export class Audio {
  constructor(private transport: Transport) {}

  async generate(opts: {
    prompt?: string;
    provider?: AudioProvider;
    model?: string;
    tags?: string;
    callbackUrl?: string;
    wait?: boolean;
    pollInterval?: number;
    maxWait?: number;
    [key: string]: unknown;
  }): Promise<Record<string, unknown> | TaskHandle> {
    const { prompt, provider = 'suno', model, tags, callbackUrl, wait: shouldWait, pollInterval, maxWait, ...rest } = opts;

    let endpoint: string;
    let body: Record<string, unknown>;
    let headers: Record<string, string> | undefined;

    if (provider === 'fish') {
      // Fish uses /fish/tts with 'text' body field and 'model' as a request header.
      // 'prompt' is accepted as an alias for 'text' for convenience.
      endpoint = '/fish/tts';
      body = { text: prompt, ...rest };
      if (callbackUrl !== undefined) body.callback_url = callbackUrl;
      if (model !== undefined) headers = { model };
    } else {
      endpoint = `/${provider}/audios`;
      body = { prompt, ...rest };
      if (model !== undefined) body.model = model;
      if (tags !== undefined) body.tags = tags;
      if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    }

    const result = await this.transport.request('POST', endpoint, { json: body, headers });
    const taskId = result.task_id as string | undefined;

    if (!taskId || (result.data && !shouldWait)) return result;

    const handle = new TaskHandle(taskId, `/${provider}/tasks`, this.transport);
    if (shouldWait) return handle.wait({ pollInterval, maxWait });
    return handle;
  }

  async listFishModels(opts: {
    pageSize?: number;
    pageNumber?: number;
    title?: string;
    tag?: string;
    self?: boolean;
    authorId?: string;
    language?: string;
    titleLanguage?: string;
    sortBy?: string;
  } = {}): Promise<Record<string, unknown>> {
    const params: Record<string, string> = {};
    if (opts.pageSize !== undefined) params.page_size = String(opts.pageSize);
    if (opts.pageNumber !== undefined) params.page_number = String(opts.pageNumber);
    if (opts.title !== undefined) params.title = opts.title;
    if (opts.tag !== undefined) params.tag = opts.tag;
    if (opts.self !== undefined) params.self = String(opts.self);
    if (opts.authorId !== undefined) params.author_id = opts.authorId;
    if (opts.language !== undefined) params.language = opts.language;
    if (opts.titleLanguage !== undefined) params.title_language = opts.titleLanguage;
    if (opts.sortBy !== undefined) params.sort_by = opts.sortBy;
    return this.transport.request('GET', '/fish/model', { params });
  }
}
