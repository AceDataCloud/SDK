/** Minimax provider-axis client. */

import { Transport } from '../../runtime/transport';
import { TaskHandle } from '../../runtime/tasks';

function taskId(result: Record<string, unknown>): string {
  if (typeof result?.task_id === 'string') return result.task_id;
  const data = result?.data as Record<string, unknown> | undefined;
  if (data && typeof data.task_id === 'string') return data.task_id;
  return typeof result?.id === 'string' ? result.id : '';
}

export type MinimaxModel = 'MiniMax-H3';
export type MinimaxContentType = 'text' | 'image_url' | 'video_url' | 'audio_url';
export type MinimaxContentRole = 'first_frame' | 'last_frame' | 'reference_image' | 'reference_video' | 'reference_audio';
export type MinimaxResolution = '768P' | '2K';
export type MinimaxRatio = 'adaptive' | '21:9' | '16:9' | '4:3' | '1:1' | '3:4' | '9:16';

export interface MinimaxMediaUrl {
  url: string;
}

export interface MinimaxContentItem {
  type: MinimaxContentType;
  text?: string;
  image_url?: MinimaxMediaUrl;
  video_url?: MinimaxMediaUrl;
  audio_url?: MinimaxMediaUrl;
  role?: MinimaxContentRole;
}

export interface MinimaxGenerateOptions {
  /** Minimax Videos Model */
  model: MinimaxModel;
  /** Minimax Videos Content */
  content: MinimaxContentItem[];
  /** Minimax Videos Resolution */
  resolution: MinimaxResolution;
  /** Minimax Videos Duration */
  duration: number;
  /** Minimax Videos Ratio */
  ratio?: MinimaxRatio;
  callbackUrl?: string;
  aigcWatermark?: boolean;
  /** Accepted for parity with async generation providers; MiniMax always returns a task. */
  async?: boolean;
  wait?: boolean;
  pollInterval?: number;
  maxWait?: number;
}

/** minimax client. */
export class Minimax {
  constructor(private transport: Transport) {}

  /** Minimax Videos. */
  async generate(options: MinimaxGenerateOptions): Promise<TaskHandle> {
    const body: Record<string, unknown> = {
      model: options.model,
      content: options.content,
      resolution: options.resolution,
      duration: options.duration,
    };
    if (options.ratio !== undefined) body.ratio = options.ratio;
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    if (options.aigcWatermark !== undefined) body.aigc_watermark = options.aigcWatermark;
    const result = (await this.transport.request('POST', '/minimax/videos', { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), '/minimax/tasks', this.transport, result);
    if (options.wait) {
      await handle.wait({ pollInterval: options.pollInterval, maxWait: options.maxWait });
    }
    return handle;
  }
}
