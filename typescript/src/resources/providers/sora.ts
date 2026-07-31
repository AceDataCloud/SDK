/**
 * Sora (sora) — generated from the platform OpenAPI spec.
 *
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

export type SoraModel = 'sora-2' | 'sora-2-pro';
export type SoraDuration = 4 | 8 | 10 | 12 | 15 | 25;
export type SoraOrientation = 'landscape' | 'portrait';
export type SoraSize = 'small' | 'large' | '720x1280' | '1280x720' | '1024x1792' | '1792x1024';
export type SoraVersion = '1.0' | '2.0';

export interface SoraGenerateOptions {
  model: SoraModel;
  prompt: string;
  duration?: SoraDuration;
  orientation?: SoraOrientation;
  size?: SoraSize;
  characterUrl?: string;
  characterStart?: number;
  characterEnd?: number;
  imageUrls?: string[];
  version?: SoraVersion;
  async?: boolean;
  callbackUrl?: string;
}

export class Sora {
  constructor(private transport: Transport) {}

  async generate(
    opts: SoraGenerateOptions & { wait?: boolean; pollInterval?: number; maxWait?: number },
  ): Promise<TaskHandle> {
    const { model, prompt, duration, orientation, size, characterUrl, characterStart, characterEnd, imageUrls, version, callbackUrl } = opts;
    const body: Record<string, unknown> = { model, prompt };
    if (duration !== undefined) body.duration = duration;
    if (orientation !== undefined) body.orientation = orientation;
    if (size !== undefined) body.size = size;
    if (characterUrl !== undefined) body.character_url = characterUrl;
    if (characterStart !== undefined) body.character_start = characterStart;
    if (characterEnd !== undefined) body.character_end = characterEnd;
    if (imageUrls !== undefined) body.image_urls = imageUrls;
    if (version !== undefined) body.version = version;
    if (callbackUrl !== undefined) body.callback_url = callbackUrl;
    body.async = opts.async ?? true;
    const result = (await this.transport.request('POST', '/sora/videos', { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), '/sora/tasks', this.transport, result);
    if (opts.wait) {
      await handle.wait({ pollInterval: opts.pollInterval, maxWait: opts.maxWait });
    }
    return handle;
  }
}
