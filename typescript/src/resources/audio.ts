/** Audio/music generation resources. */

import { Transport } from '../runtime/transport';
import { TaskHandle } from '../runtime/tasks';

export type AudioProvider = 'suno' | 'producer' | 'fish' | (string & {});

export class Audio {
  constructor(private transport: Transport) {}

  async generate(opts: {
    prompt: string;
    text?: string;
    provider?: AudioProvider;
    model?: string;
    tags?: string;
    callbackUrl?: string;
    wait?: boolean;
    pollInterval?: number;
    maxWait?: number;
    [key: string]: unknown;
  }): Promise<Record<string, unknown> | TaskHandle> {
    const { prompt, text, provider = 'suno', model, tags, callbackUrl, wait: shouldWait, pollInterval, maxWait, ...rest } = opts;
    const isFish = provider === 'fish';
    const body: Record<string, unknown> = { ...rest };
    if (isFish) body.text = text ?? prompt;
    else body.prompt = prompt;
    const headers: Record<string, string> = {};
    if (model !== undefined) {
      if (isFish) headers.model = model;
      else body.model = model;
    }
    if (tags !== undefined) body.tags = tags;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;

    const endpoint = isFish ? '/fish/tts' : `/${provider}/audios`;
    const result = await this.transport.request('POST', endpoint, { json: body, headers });
    const taskId = result.task_id as string | undefined;

    if (!taskId || (result.data && !shouldWait)) return result;

    const handle = new TaskHandle(taskId, `/${provider}/tasks`, this.transport);
    if (shouldWait) return handle.wait({ pollInterval, maxWait });
    return handle;
  }
}
