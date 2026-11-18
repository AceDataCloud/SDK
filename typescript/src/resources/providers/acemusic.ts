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
  /** generate creates new songs, upload imports one audio reference, cover reworks one owned track, and mashup blends exactly two owned tracks. */
  action?: "generate" | "upload" | "cover" | "mashup";
  /** Generation supports both models. Cover and mashup use acemusic-v1.1. Omit for upload. */
  model?: "acemusic-v1.1" | "acemusic-v1";
  /** Only used by generate: false for an idea, true for supplied lyrics. */
  custom?: boolean;
  /** Creation idea. Required when custom is false. */
  prompt?: string;
  /** Lyrics for custom generation, cover or mashup. */
  lyric?: string;
  /** Musical style for custom generation, cover or mashup. */
  style?: string;
  /** Required for custom generation; optional for cover and mashup. */
  title?: string;
  /** HTTPS source audio URL for upload. Use audio_id or mashup_audio_ids for already imported or generated tracks. */
  audioUrl?: string;
  /** Optional display name for an upload. */
  name?: string;
  /** Public platform track ID owned by the caller. Required for cover; optional on upload to associate the import with an existing reference track. */
  audioId?: string;
  /** Exactly two distinct caller-owned public track IDs. The selected references must be compatible with each other. */
  mashupAudioIds?: string[];
  /** Audio reference strength for cover and mashup. Defaults to 60. */
  audioInfluence?: number;
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
    if (options.model !== undefined) body["model"] = options.model;
    if (options.custom !== undefined) body["custom"] = options.custom;
    if (options.prompt !== undefined) body["prompt"] = options.prompt;
    if (options.lyric !== undefined) body["lyric"] = options.lyric;
    if (options.style !== undefined) body["style"] = options.style;
    if (options.title !== undefined) body["title"] = options.title;
    if (options.audioUrl !== undefined) body["audio_url"] = options.audioUrl;
    if (options.name !== undefined) body["name"] = options.name;
    if (options.audioId !== undefined) body["audio_id"] = options.audioId;
    if (options.mashupAudioIds !== undefined) body["mashup_audio_ids"] = options.mashupAudioIds;
    if (options.audioInfluence !== undefined) body["audio_influence"] = options.audioInfluence;
    for (const [key, value] of Object.entries(options)) {
      if (!["action", "async", "audioId", "audioInfluence", "audioUrl", "callbackUrl", "custom", "idempotencyKey", "lyric", "mashupAudioIds", "maxWait", "model", "name", "pollInterval", "prompt", "style", "title", "wait"].includes(key) && value !== undefined) {
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
