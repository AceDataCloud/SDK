/**
 * Minimax (minimax) — generated from the platform OpenAPI spec.
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

export interface MinimaxGenerateOptions {
  /** Minimax Videos Model */
  model?: 'minimax-h3';
  /** Minimax Videos Prompt */
  prompt?: string;
  /** Minimax Videos Image Urls */
  imageUrls?: string[];
  /** Minimax Videos Audio Urls */
  audioUrls?: string[];
  /** Minimax Videos Ratio */
  ratio?: '16:9' | '9:16';
  /** Minimax Videos Duration */
  duration?: number;
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

/** minimax client. */
export class Minimax {
  constructor(private transport: Transport) {}

  /** MiniMax H3 video generation API. */
  async generate(options: MinimaxGenerateOptions = {}): Promise<TaskHandle> {
    const body: Record<string, unknown> = {};
    body.model = options.model ?? 'minimax-h3';
    body.prompt =
      options.prompt ?? 'A red fox running through a snowy forest at dawn, cinematic tracking shot';
    if (options.imageUrls !== undefined) body.image_urls = options.imageUrls;
    if (options.audioUrls !== undefined) body.audio_urls = options.audioUrls;
    body.ratio = options.ratio ?? '16:9';
    body.duration = options.duration ?? 4;
    for (const [key, value] of Object.entries(options)) {
      if (
        ![
          'async',
          'audioUrls',
          'callbackUrl',
          'duration',
          'imageUrls',
          'maxWait',
          'model',
          'pollInterval',
          'prompt',
          'ratio',
          'wait',
        ].includes(key) &&
        value !== undefined
      ) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    body.async = options.async ?? true;
    const result = (await this.transport.request('POST', '/minimax/videos', { json: body })) as Record<
      string,
      unknown
    >;
    const handle = new TaskHandle(taskId(result), '/minimax/tasks', this.transport, result);
    if (options.wait) {
      await handle.wait({ pollInterval: options.pollInterval, maxWait: options.maxWait });
    }
    return handle;
  }
}
