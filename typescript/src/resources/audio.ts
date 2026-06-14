/** Audio/music generation resources. */

import { Transport } from '../runtime/transport';
import { TaskHandle } from '../runtime/tasks';

export type AudioProvider = 'suno' | 'producer' | 'fish' | (string & {});

export class Audio {
  constructor(private transport: Transport) {}

  async listFishModels(opts: {
    pageSize?: number;
    pageNumber?: number;
    title?: string;
    tag?: string;
    selfOnly?: boolean;
    authorId?: string;
    language?: string;
    titleLanguage?: string;
    sortBy?: string;
  } = {}): Promise<Record<string, unknown>> {
    const { pageSize, pageNumber, title, tag, selfOnly, authorId, language, titleLanguage, sortBy } = opts;
    const params: Record<string, string> = {};
    if (pageSize !== undefined) params.page_size = String(pageSize);
    if (pageNumber !== undefined) params.page_number = String(pageNumber);
    if (title !== undefined) params.title = title;
    if (tag !== undefined) params.tag = tag;
    if (selfOnly !== undefined) params.self = String(selfOnly);
    if (authorId !== undefined) params.author_id = authorId;
    if (language !== undefined) params.language = language;
    if (titleLanguage !== undefined) params.title_language = titleLanguage;
    if (sortBy !== undefined) params.sort_by = sortBy;
    return this.transport.request('GET', '/fish/model', { params });
  }

  async getFishModel(id: string): Promise<Record<string, unknown>> {
    return this.transport.request('GET', `/fish/model/${id}`);
  }

  async generate(opts: {
    prompt: string;
    provider?: AudioProvider;
    model?: string;
    tags?: string;
    callbackUrl?: string;
    async?: boolean;
    wait?: boolean;
    pollInterval?: number;
    maxWait?: number;
    [key: string]: unknown;
  }): Promise<Record<string, unknown> | TaskHandle> {
    const { prompt, provider = 'suno', model, tags, callbackUrl, wait: shouldWait, pollInterval, maxWait, ...rest } = opts;
    let result: Record<string, unknown>;
    if (provider === 'fish') {
      const body: Record<string, unknown> = { text: prompt, ...rest };
      if (callbackUrl !== undefined) body.callback_url = callbackUrl;
      result = await this.transport.request('POST', '/fish/tts', {
        json: body,
        headers: model !== undefined ? { model } : undefined,
      });
    } else {
      const body: Record<string, unknown> = { prompt, ...rest };
      if (model !== undefined) body.model = model;
      if (tags !== undefined) body.tags = tags;
      if (callbackUrl !== undefined) body.callback_url = callbackUrl;
      result = await this.transport.request('POST', `/${provider}/audios`, { json: body });
    }
    const taskId = result.task_id as string | undefined;

    if (!taskId || (result.data && !shouldWait)) return result;

    const handle = new TaskHandle(taskId, `/${provider}/tasks`, this.transport);
    if (shouldWait) return handle.wait({ pollInterval, maxWait });
    return handle;
  }
}
