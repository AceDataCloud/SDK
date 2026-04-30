/** Audio/music generation resources. */

import { Transport } from '../runtime/transport';
import { TaskHandle } from '../runtime/tasks';

export type AudioProvider = 'suno' | 'producer' | 'fish' | (string & {});

export class Audio {
  constructor(private transport: Transport) {}

  async generate(opts: {
    prompt: string;
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
    const body: Record<string, unknown> = { prompt, ...rest };
    if (model !== undefined) body.model = model;
    if (tags !== undefined) body.tags = tags;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;

    const result = await this.transport.request('POST', `/${provider}/audios`, { json: body });
    const taskId = result.task_id as string | undefined;

    if (!taskId || (result.data && !shouldWait)) return result;

    const handle = new TaskHandle(taskId, `/${provider}/tasks`, this.transport);
    if (shouldWait) return handle.wait({ pollInterval, maxWait });
    return handle;
  }

  async voices(opts: {
    audioUrl: string;
    name?: string;
    description?: string;
    wait?: boolean;
    pollInterval?: number;
    maxWait?: number;
  }): Promise<Record<string, unknown> | TaskHandle> {
    const { audioUrl, name, description, wait: shouldWait, pollInterval, maxWait } = opts;
    const body: Record<string, unknown> = { audio_url: audioUrl };
    if (name !== undefined) body.name = name;
    if (description !== undefined) body.description = description;

    const result = await this.transport.request('POST', '/suno/voices', { json: body });
    const taskId = result.task_id as string | undefined;

    if (!taskId || (result.data && !shouldWait)) return result;

    const handle = new TaskHandle(taskId, '/suno/tasks', this.transport);
    if (shouldWait) return handle.wait({ pollInterval, maxWait });
    return handle;
  }
}
