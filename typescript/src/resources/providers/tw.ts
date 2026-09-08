/**
 * Tw (tw) — generated from the platform OpenAPI spec.
 *
 * Do not edit by hand: run `python scripts/generate_providers.py`. Parameter
 * names, types, enums and required-ness all come from the live spec.
 */

import { Transport } from '../../runtime/transport';


export interface TwCommentsOptions {
  /** X Comments Note Id */
  noteId: string;
  /** X Comments Cursor */
  cursor?: string;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

export interface TwSearchOptions {
  /** X Search Keyword */
  keyword: string;
  /** X Search Cursor */
  cursor?: string;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

export interface TwPostsOptions {
  /** X Posts User Id */
  userId: string;
  /** X Posts Cursor */
  cursor?: string;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

export interface TwUsersOptions {
  /** X Users Username */
  username: string;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

export interface TwRetweetsOptions {
  /** X Retweets Post Id */
  noteId: string;
  /** X Retweets Cursor */
  cursor?: string;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

/** tw client. */
export class Tw {
  constructor(private transport: Transport) {}

  /** Get all the comment information for a tweet by entering the id of the tweet. */
  async comments(options: TwCommentsOptions): Promise<Record<string, unknown>> {
    const body: Record<string, unknown> = {};
    body["note_id"] = options.noteId;
    if (options.cursor !== undefined) body["cursor"] = options.cursor;
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "callbackUrl", "cursor", "maxWait", "noteId", "pollInterval", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    return (await this.transport.request('POST', "/x/comments", { json: body })) as Record<string, unknown>;
  }

  /** Find chronological tweets by keyword. */
  async search(options: TwSearchOptions): Promise<Record<string, unknown>> {
    const body: Record<string, unknown> = {};
    body["keyword"] = options.keyword;
    if (options.cursor !== undefined) body["cursor"] = options.cursor;
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "callbackUrl", "cursor", "keyword", "maxWait", "pollInterval", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    return (await this.transport.request('POST', "/x/search", { json: body })) as Record<string, unknown>;
  }

  /** Get all the post information for a tweet by entering the user_id of the tweet. */
  async posts(options: TwPostsOptions): Promise<Record<string, unknown>> {
    const body: Record<string, unknown> = {};
    body["user_id"] = options.userId;
    if (options.cursor !== undefined) body["cursor"] = options.cursor;
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "callbackUrl", "cursor", "maxWait", "pollInterval", "userId", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    return (await this.transport.request('POST', "/x/posts", { json: body })) as Record<string, unknown>;
  }

  /** Get user details by Twitter username. */
  async users(options: TwUsersOptions): Promise<Record<string, unknown>> {
    const body: Record<string, unknown> = {};
    body["username"] = options.username;
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "callbackUrl", "maxWait", "pollInterval", "username", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    return (await this.transport.request('POST', "/x/users", { json: body })) as Record<string, unknown>;
  }

  /** Find retweets of a tweet. */
  async retweets(options: TwRetweetsOptions): Promise<Record<string, unknown>> {
    const body: Record<string, unknown> = {};
    body["note_id"] = options.noteId;
    if (options.cursor !== undefined) body["cursor"] = options.cursor;
    for (const [key, value] of Object.entries(options)) {
      if (!["async", "callbackUrl", "cursor", "maxWait", "noteId", "pollInterval", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    return (await this.transport.request('POST', "/x/retweets", { json: body })) as Record<string, unknown>;
  }

}
