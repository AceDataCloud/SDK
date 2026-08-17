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
  const task = result?.task as Record<string, unknown> | undefined;
  if (task && typeof task.id === 'string') return task.id;
  return typeof result?.id === 'string' ? result.id : '';
}


export interface MinimaxGenerateOptions {
  /** Minimax Videos Model */
  model: "MiniMax-H3";
  /** Minimax Videos Content */
  content: Array<Record<string, unknown>>;
  /** Minimax Videos Resolution */
  resolution: "768P" | "2K";
  /** Minimax Videos Duration */
  duration: number;
  /** Minimax Videos Ratio */
  ratio?: "adaptive" | "21:9" | "16:9" | "4:3" | "1:1" | "3:4" | "9:16";
  /** Submit asynchronously and poll. Defaults to false. */
  async?: boolean;
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

  /** Minimax Videos */
  async generate(options: MinimaxGenerateOptions): Promise<TaskHandle> {
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
    body.async = options.async ?? false;
    const result = (await this.transport.request('POST', "/minimax/videos", { json: body })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), "/minimax/tasks", this.transport, result);
    if (options.wait) {
      await handle.wait({ pollInterval: options.pollInterval, maxWait: options.maxWait });
    }
    return handle;
  }

}
