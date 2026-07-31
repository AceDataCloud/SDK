/**
 * DrawAI (drawai) — generated from the platform OpenAPI spec.
 *
 * Paths live under /headshots/* as this service provides AI ID Photo Production.
 * Do not edit by hand: run `python scripts/generate_providers.py`. Parameter
 * names, types, enums and required-ness all come from the live spec.
 */

import { Transport } from '../../runtime/transport';
import { TaskHandle } from '../../runtime/tasks';

function taskId(result: Record<string, unknown>): string {
  if (typeof result?.task_id === 'string') return result.task_id;
  const data = result?.data as Record<string, unknown> | undefined;
  if (data && typeof data.task_id === 'string') return data.task_id;
  return typeof result?.id === 'string' ? result.id : '';
}

export type DrawAIMode = 'fast' | 'relax';
export type DrawAITemplate =
  | 'male_portrait'
  | 'male_portrait2'
  | 'kindergarten'
  | 'logo_tshirt'
  | 'wedding'
  | 'business_photo'
  | 'bob_suit'
  | 'female_portrait';

export interface DrawAIGenerateOptions {
  mode: DrawAIMode;
  template: DrawAITemplate;
  imageUrls: string[];
  async?: boolean;
  callbackUrl?: string;
}

export class DrawAI {
  constructor(private transport: Transport) {}

  async generate(
    opts: DrawAIGenerateOptions & { wait?: boolean; pollInterval?: number; maxWait?: number },
  ): Promise<TaskHandle> {
    const body: Record<string, unknown> = {
      mode: opts.mode,
      template: opts.template,
      image_urls: opts.imageUrls,
    };
    if (opts.callbackUrl !== undefined) body.callback_url = opts.callbackUrl;
    body.async = opts.async ?? true;
    const result = (await this.transport.request('POST', '/headshots/generate', { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), '/headshots/tasks', this.transport, result);
    if (opts.wait) {
      await handle.wait({ pollInterval: opts.pollInterval, maxWait: opts.maxWait });
    }
    return handle;
  }
}
