/** X/Twitter data resources (`/x/*`). */

import { Transport } from '../runtime/transport';

export class Tw {
  constructor(private transport: Transport) {}

  posts(opts: { userId: string; [key: string]: unknown }): Promise<Record<string, unknown>> {
    const { userId, ...rest } = opts;
    return this.transport.request('POST', '/x/posts', { json: { user_id: userId, ...rest } });
  }

  users(opts: { username: string; [key: string]: unknown }): Promise<Record<string, unknown>> {
    return this.transport.request('POST', '/x/users', { json: opts });
  }

  retweets(opts: { keyword: string; [key: string]: unknown }): Promise<Record<string, unknown>> {
    return this.transport.request('POST', '/x/retweets', { json: opts });
  }
}
