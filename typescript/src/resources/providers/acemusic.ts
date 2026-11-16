/**
 * Acemusic (acemusic) — generated from the platform OpenAPI spec.
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

export interface AcemusicGenerateOptions {
  action?: "generate";
  model?: "acemusic-v1.1" | "acemusic-v1";
  custom?: boolean;
  /** Creation idea. Required when custom is false. */
  prompt?: string;
  /** Custom lyrics. Required when custom is true. */
  lyric?: string;
  /** Musical style for custom creation. */
  style?: string;
  title?: string;
  idempotencyKey?: string;
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

export interface AcemusicLyricsOptions {
  prompt: string;
  style?: string;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

export interface AcemusicTasksOptions {
  action: "retrieve" | "retrieve_batch" | "list";
  id?: string;
  ids?: string[];
  page?: number;
  pageSize?: number;
  /** Optional history type filter. */
  type?: "audios" | "lyrics";
  /** Alternative history page size; use page/page_size or limit/offset consistently. */
  limit?: number;
  offset?: number;
  /** Inclusive creation-time lower bound, Unix seconds. */
  createdAtMin?: number;
  /** Inclusive creation-time upper bound, Unix seconds. */
  createdAtMax?: number;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

/** acemusic client. */
export class Acemusic {
  constructor(private transport: Transport) {}

  /** ACE Music Audios */
  async generate(options: AcemusicGenerateOptions = {}): Promise<TaskHandle> {
    const body: Record<string, unknown> = {};
    body["action"] = options.action ?? "generate";
    body["model"] = options.model ?? "acemusic-v1.1";
    body["custom"] = options.custom ?? false;
    if (options.prompt !== undefined) body["prompt"] = options.prompt;
    if (options.lyric !== undefined) body["lyric"] = options.lyric;
    if (options.style !== undefined) body["style"] = options.style;
    if (options.title !== undefined) body["title"] = options.title;
    for (const [key, value] of Object.entries(options)) {
      if (!["action", "async", "callbackUrl", "custom", "idempotencyKey", "lyric", "maxWait", "model", "pollInterval", "prompt", "style", "title", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    body.async = options.async ?? true;
    const result = (await this.transport.request('POST', "/acemusic/audios", { json: body, headers: options.idempotencyKey !== undefined ? {"Idempotency-Key": options.idempotencyKey} : {} })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), "/acemusic/tasks", this.transport, result);
    if (options.wait) {
      await handle.wait({ pollInterval: options.pollInterval, maxWait: options.maxWait });
    }
    return handle;
  }

  /** ACE Music Lyrics */
  async lyrics(options: AcemusicLyricsOptions): Promise<Record<string, unknown>> {
    const body: Record<string, unknown> = {};
    body["prompt"] = options.prompt;
    if (options.style !== undefined) body["style"] = options.style;
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "callbackUrl", "maxWait", "pollInterval", "prompt", "style", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    return (await this.transport.request('POST', "/acemusic/lyrics", { json: body })) as Record<string, unknown>;
  }

  /** ACE Music Tasks */
  async tasks(options: AcemusicTasksOptions): Promise<Record<string, unknown>> {
    const body: Record<string, unknown> = {};
    body["action"] = options.action;
    if (options.id !== undefined) body["id"] = options.id;
    if (options.ids !== undefined) body["ids"] = options.ids;
    if (options.page !== undefined) body["page"] = options.page;
    if (options.pageSize !== undefined) body["page_size"] = options.pageSize;
    if (options.type !== undefined) body["type"] = options.type;
    if (options.limit !== undefined) body["limit"] = options.limit;
    if (options.offset !== undefined) body["offset"] = options.offset;
    if (options.createdAtMin !== undefined) body["created_at_min"] = options.createdAtMin;
    if (options.createdAtMax !== undefined) body["created_at_max"] = options.createdAtMax;
    for (const [key, value] of Object.entries(options)) {
      if (!["action", "async", "callbackUrl", "createdAtMax", "createdAtMin", "id", "ids", "limit", "maxWait", "offset", "page", "pageSize", "pollInterval", "type", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    return (await this.transport.request('POST', "/acemusic/tasks", { json: body })) as Record<string, unknown>;
  }

}
