/**
 * Tiktok (tiktok) — generated from the platform OpenAPI spec.
 *
 * Do not edit by hand: run `python scripts/generate_providers.py`. Parameter
 * names, types, enums and required-ness all come from the live spec.
 */

import { Transport } from '../../runtime/transport';


export interface TiktokPostsOptions {
  /** Tiktok Posts Cursor */
  cursor?: string;
  /** Tiktok Posts User Id */
  userId?: string;
  /** Tiktok Posts Unique Id */
  uniqueId?: string;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

export interface TiktokSearchOptions {
  /** Tiktok Search Type */
  type: "user" | "video";
  /** Tiktok Search Keywords */
  keywords: string;
  /** Tiktok Search Cursor */
  cursor?: number;
  /** Tiktok Search Region */
  region?: "us" | "jp" | "kr" | "vn" | "br" | "ru";
  /** Tiktok Search Sort Type */
  sortType?: number;
  /** Tiktok Search Publish Time */
  publishTime?: number;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

export interface TiktokUserOptions {
  /** Tiktok User Cursor */
  cursor?: string;
  /** Tiktok User User Id */
  userId?: string;
  /** Tiktok User Unique Id */
  uniqueId?: string;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

export interface TiktokVideoOptions {
  /** Tiktok Video Video Url */
  videoUrl: string;
  /** Tiktok Video Original Quality */
  originalQuality?: number;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

/** tiktok client. */
export class Tiktok {
  constructor(private transport: Transport) {}

  /** Get a TikTok user's work based on their unique id. */
  async posts(options: TiktokPostsOptions = {}): Promise<Record<string, unknown>> {
    const body: Record<string, unknown> = {};
    if (options.cursor !== undefined) body["cursor"] = options.cursor;
    if (options.userId !== undefined) body["user_id"] = options.userId;
    if (options.uniqueId !== undefined) body["unique_id"] = options.uniqueId;
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "callbackUrl", "cursor", "maxWait", "pollInterval", "uniqueId", "userId", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    return (await this.transport.request('POST', "/tiktok/posts", { json: body })) as Record<string, unknown>;
  }

  /** Search TikTok users and video resources by keyword. */
  async search(options: TiktokSearchOptions): Promise<Record<string, unknown>> {
    const body: Record<string, unknown> = {};
    body["type"] = options.type;
    body["keywords"] = options.keywords;
    if (options.cursor !== undefined) body["cursor"] = options.cursor;
    if (options.region !== undefined) body["region"] = options.region;
    if (options.sortType !== undefined) body["sort_type"] = options.sortType;
    if (options.publishTime !== undefined) body["publish_time"] = options.publishTime;
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "callbackUrl", "cursor", "keywords", "maxWait", "pollInterval", "publishTime", "region", "sortType", "type", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    return (await this.transport.request('POST', "/tiktok/search", { json: body })) as Record<string, unknown>;
  }

  /** Get user details based on a TikTok user's unique id. */
  async user(options: TiktokUserOptions = {}): Promise<Record<string, unknown>> {
    const body: Record<string, unknown> = {};
    if (options.cursor !== undefined) body["cursor"] = options.cursor;
    if (options.userId !== undefined) body["user_id"] = options.userId;
    if (options.uniqueId !== undefined) body["unique_id"] = options.uniqueId;
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "callbackUrl", "cursor", "maxWait", "pollInterval", "uniqueId", "userId", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    return (await this.transport.request('POST', "/tiktok/user", { json: body })) as Record<string, unknown>;
  }

  /** Follow the link to the video on TikTok for more details. */
  async video(options: TiktokVideoOptions): Promise<Record<string, unknown>> {
    const body: Record<string, unknown> = {};
    body["video_url"] = options.videoUrl;
    if (options.originalQuality !== undefined) body["original_quality"] = options.originalQuality;
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "callbackUrl", "maxWait", "originalQuality", "pollInterval", "videoUrl", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    return (await this.transport.request('POST', "/tiktok/video", { json: body })) as Record<string, unknown>;
  }

}
