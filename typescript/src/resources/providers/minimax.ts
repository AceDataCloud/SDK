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
  model: "MiniMax-H3";
  /** Minimax Videos Content */
  content: MinimaxContentItem[];
  /** Minimax Videos Resolution */
  resolution: "768P" | "2K";
  /** Minimax Videos Duration */
  duration: number;
  /** Minimax Videos Ratio */
  ratio?: "adaptive" | "21:9" | "16:9" | "4:3" | "1:1" | "3:4" | "9:16";
  async?: boolean;
  wait?: boolean;
  pollInterval?: number;
  maxWait?: number;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

export interface MinimaxMediaUrl {
  url: string;
}

export interface MinimaxTextContent {
  type: 'text';
  text: string;
}

export interface MinimaxImageContent {
  type: 'image_url';
  image_url: MinimaxMediaUrl;
  role?: 'first_frame' | 'last_frame' | 'reference_image';
}

export interface MinimaxVideoContent {
  type: 'video_url';
  video_url: MinimaxMediaUrl;
  role: 'reference_video';
}

export interface MinimaxAudioContent {
  type: 'audio_url';
  audio_url: MinimaxMediaUrl;
  role: 'reference_audio';
}

export type MinimaxContentItem =
  | MinimaxTextContent
  | MinimaxImageContent
  | MinimaxVideoContent
  | MinimaxAudioContent;

function validateContentItem(item: MinimaxContentItem): void {
  if (item.type === 'text') {
    if (!item.text) throw new Error("minimax.content item with type='text' requires non-empty text");
    return;
  }
  if (item.type === 'image_url') {
    if (!item.image_url?.url) throw new Error("minimax.content item with type='image_url' requires image_url.url");
    if (
      item.role !== undefined &&
      item.role !== 'first_frame' &&
      item.role !== 'last_frame' &&
      item.role !== 'reference_image'
    ) {
      throw new Error(
        "minimax.content item with type='image_url' role must be first_frame, last_frame, or reference_image",
      );
    }
    return;
  }
  if (item.type === 'video_url') {
    if (!item.video_url?.url) throw new Error("minimax.content item with type='video_url' requires video_url.url");
    if (item.role !== 'reference_video') {
      throw new Error("minimax.content item with type='video_url' requires role='reference_video'");
    }
    return;
  }
  if (item.type === 'audio_url') {
    if (!item.audio_url?.url) throw new Error("minimax.content item with type='audio_url' requires audio_url.url");
    if (item.role !== 'reference_audio') {
      throw new Error("minimax.content item with type='audio_url' requires role='reference_audio'");
    }
  }
}

function validateGenerateOptions(options: MinimaxGenerateOptions): void {
  if (!options.content.length) throw new Error('minimax.content must contain at least one item');
  for (const item of options.content) validateContentItem(item);
  if (options.duration < 4 || options.duration > 15) {
    throw new Error('minimax.duration must be between 4 and 15 seconds');
  }
}

/** minimax client. */
export class Minimax {
  constructor(private transport: Transport) {}

  /** Minimax Videos */
  async generate(options: MinimaxGenerateOptions): Promise<TaskHandle> {
    validateGenerateOptions(options);
    const body: Record<string, unknown> = {};
    body["model"] = options.model;
    body["content"] = options.content;
    body["resolution"] = options.resolution;
    body["duration"] = options.duration;
    if (options.ratio !== undefined) body["ratio"] = options.ratio;
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "callbackUrl", "content", "duration", "maxWait", "model", "pollInterval", "ratio", "resolution", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    body.async = options.async ?? true;
    const result = (await this.transport.request('POST', "/minimax/videos", { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), "/minimax/tasks", this.transport, result);
    if (options.wait) {
      await handle.wait({ pollInterval: options.pollInterval, maxWait: options.maxWait });
    }
    return handle;
  }

}
