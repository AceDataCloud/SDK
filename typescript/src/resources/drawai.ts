/** DrawAI headshot generation resources. */

import { Transport } from '../runtime/transport';
import { TaskHandle } from '../runtime/tasks';

export type HeadshotTemplate = 'male_portrait' | 'male_portrait2' | 'kindergarten' | 'logo_tshirt' | 'wedding' | 'business_photo' | 'bob_suit' | 'female_portrait' | (string & {});

export class DrawAI {
  constructor(private transport: Transport) {}

  async generate(opts: {
    template: HeadshotTemplate;
    mode?: 'fast' | 'relax';
    imageUrls: string[];
    callbackUrl?: string;
    async?: boolean;
    wait?: boolean;
    pollInterval?: number;
    maxWait?: number;
    [key: string]: unknown;
  }): Promise<Record<string, unknown> | TaskHandle> {
    const { template, mode = 'fast', imageUrls, callbackUrl, wait: shouldWait, pollInterval, maxWait, ...rest } = opts;
    const body: Record<string, unknown> = { template, mode, image_urls: imageUrls, ...rest };
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;

    const result = await this.transport.request('POST', '/headshots/generate', { json: body });
    const taskId = result.task_id as string | undefined;

    if (!taskId || (result.data && !shouldWait)) return result;

    const handle = new TaskHandle(taskId, '/headshots/tasks', this.transport);
    if (shouldWait) return handle.wait({ pollInterval, maxWait });
    return handle;
  }
}
