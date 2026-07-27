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

export interface SoraGenerateOptions {
  /** Text prompt for the video. */
  prompt: string;
  /** The model to use for generation. */
  model: 'sora-2' | 'sora-2-pro';
  /** Duration in seconds. */
  duration?: 4 | 8 | 10 | 12 | 15 | 25;
  /** Video orientation. */
  orientation?: 'landscape' | 'portrait';
  /** Output video size. */
  size?: 'small' | 'large' | '720x1280' | '1280x720' | '1024x1792' | '1792x1024';
  /** URL of a character reference image or video. */
  characterUrl?: string;
  /** Character reference start time (seconds). */
  characterStart?: number;
  /** Character reference end time (seconds). */
  characterEnd?: number;
  /** Array of image URLs to use as visual references. */
  imageUrls?: string[];
  /** API version to use. */
  version?: '1.0' | '2.0';
  /** Submit asynchronously and poll. Defaults to true. */
  async?: boolean;
  /** Wait for completion before returning the handle. */
  wait?: boolean;
  pollInterval?: number;
  maxWait?: number;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

/** sora client. */
export class Sora {
  constructor(private transport: Transport) {}

  /** Sora video generation API. */
  async generate(options: SoraGenerateOptions): Promise<TaskHandle> {
    const body: Record<string, unknown> = {
      prompt: options.prompt,
      model: options.model,
    };
    if (options.duration !== undefined) body.duration = options.duration;
    if (options.orientation !== undefined) body.orientation = options.orientation;
    if (options.size !== undefined) body.size = options.size;
    if (options.characterUrl !== undefined) body.character_url = options.characterUrl;
    if (options.characterStart !== undefined) body.character_start = options.characterStart;
    if (options.characterEnd !== undefined) body.character_end = options.characterEnd;
    if (options.imageUrls !== undefined) body.image_urls = options.imageUrls;
    if (options.version !== undefined) body.version = options.version;
    for (const [key, value] of Object.entries(options)) {
      if (!['async', 'callbackUrl', 'characterEnd', 'characterStart', 'characterUrl', 'duration', 'imageUrls', 'maxWait', 'model', 'orientation', 'pollInterval', 'prompt', 'size', 'version', 'wait'].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    body.async = options.async ?? true;
    const result = (await this.transport.request('POST', '/sora/videos', { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), '/sora/tasks', this.transport, result);
    if (options.wait) {
      await handle.wait({ pollInterval: options.pollInterval, maxWait: options.maxWait });
    }
    return handle;
  }

}
