/** Maestro AI Video Studio resources (`/maestro/*`). */

import { Transport } from '../runtime/transport';
import { TaskHandle } from '../runtime/tasks';

export class Maestro {
  constructor(private transport: Transport) {}

  async videos(opts: {
    prompt: string;
    action?: 'generate' | 'remix' | 'edit' | 'extend' | (string & {});
    refTaskId?: string;
    fileUrls?: string[];
    langs?: string[];
    aspect?: '9:16' | '16:9' | '1:1' | (string & {});
    duration?: number;
    quality?: 'draft' | 'standard' | 'premium' | (string & {});
    scenario?: 'auto' | 'narrated' | 'drama' | 'avatar' | 'motion' | 'slideshow' | (string & {});
    style?: string;
    voice?: string;
    callbackUrl?: string;
    wait?: boolean;
    pollInterval?: number;
    maxWait?: number;
    [key: string]: unknown;
  }): Promise<Record<string, unknown> | TaskHandle> {
    const { prompt, action, refTaskId, fileUrls, langs, aspect, duration, quality, scenario, style, voice, callbackUrl, wait: shouldWait, pollInterval, maxWait, ...rest } = opts;
    const body: Record<string, unknown> = { prompt, ...rest };
    if (action !== undefined) body.action = action;
    if (refTaskId !== undefined) body.ref_task_id = refTaskId;
    if (fileUrls !== undefined) body.file_urls = fileUrls;
    if (langs !== undefined) body.langs = langs;
    if (aspect !== undefined) body.aspect = aspect;
    if (duration !== undefined) body.duration = duration;
    if (quality !== undefined) body.quality = quality;
    if (scenario !== undefined) body.scenario = scenario;
    if (style !== undefined) body.style = style;
    if (voice !== undefined) body.voice = voice;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;

    const result = await this.transport.request('POST', '/maestro/videos', { json: body });
    const taskId = result.task_id as string | undefined;

    if (!taskId || !shouldWait) return result;

    const handle = new TaskHandle(taskId, '/maestro/tasks', this.transport);
    if (shouldWait) return handle.wait({ pollInterval, maxWait });
    return handle;
  }
}
