/** MiniMax H3 video generation provider. */

import { Transport } from '../../runtime/transport';
import { TaskHandle } from '../../runtime/tasks';

export type MinimaxModel = 'MiniMax-H3';
export type MinimaxResolution = '768P' | '2K';
export type MinimaxRatio = 'adaptive' | '21:9' | '16:9' | '4:3' | '1:1' | '3:4' | '9:16';
export type MinimaxContentType = 'text' | 'image_url' | 'video_url' | 'audio_url';
export type MinimaxContentRole =
  | 'first_frame'
  | 'last_frame'
  | 'reference_image'
  | 'reference_video'
  | 'reference_audio';

export interface MinimaxMediaUrl {
  url: string;
}

export interface MinimaxContent {
  type: MinimaxContentType;
  text?: string;
  imageUrl?: MinimaxMediaUrl;
  videoUrl?: MinimaxMediaUrl;
  audioUrl?: MinimaxMediaUrl;
  role?: MinimaxContentRole;
}

export interface MinimaxGenerateOptions {
  model: MinimaxModel;
  content: MinimaxContent[];
  resolution: MinimaxResolution;
  duration: number;
  ratio?: MinimaxRatio;
  aigcWatermark?: boolean;
  async?: boolean;
  wait?: boolean;
  pollInterval?: number;
  maxWait?: number;
  callbackUrl?: string;
}

function taskId(result: Record<string, unknown>): string {
  if (typeof result.task_id === 'string') return result.task_id;
  const data = result.data as Record<string, unknown> | undefined;
  if (data && typeof data.task_id === 'string') return data.task_id;
  return typeof result.id === 'string' ? result.id : '';
}

function validate(content: MinimaxContent[], duration: number): void {
  if (!Number.isInteger(duration) || duration < 4 || duration > 15) {
    throw new Error('duration must be an integer between 4 and 15 seconds');
  }
  if (content.length === 0) throw new Error('content must contain at least one item');
}

/** MiniMax H3 video generation client. */
export class Minimax {
  constructor(private transport: Transport) {}

  async generate(options: MinimaxGenerateOptions): Promise<TaskHandle> {
    validate(options.content, options.duration);
    const content = options.content.map(({ imageUrl, videoUrl, audioUrl, ...item }) => ({
      ...item,
      ...(imageUrl && { image_url: imageUrl }),
      ...(videoUrl && { video_url: videoUrl }),
      ...(audioUrl && { audio_url: audioUrl }),
    }));
    const body: Record<string, unknown> = {
      model: options.model,
      content,
      resolution: options.resolution,
      duration: options.duration,
      aigc_watermark: options.aigcWatermark ?? false,
    };
    if (options.ratio !== undefined) body.ratio = options.ratio;
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    const result = (await this.transport.request('POST', '/minimax/videos', { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), '/minimax/tasks', this.transport, result);
    if (options.wait) {
      await handle.wait({ pollInterval: options.pollInterval, maxWait: options.maxWait });
    }
    return handle;
  }
}
