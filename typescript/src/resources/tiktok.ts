/** TikTok data resources (`/tiktok/*`). */

import { Transport } from '../runtime/transport';

export class Tiktok {
  constructor(private transport: Transport) {}

  posts(opts: Record<string, unknown> = {}): Promise<Record<string, unknown>> {
    return this.transport.request('POST', '/tiktok/posts', { json: opts });
  }

  search(opts: { type: 'user' | 'video'; keywords: string; [key: string]: unknown }): Promise<Record<string, unknown>> {
    return this.transport.request('POST', '/tiktok/search', { json: opts });
  }

  user(opts: { type: string; keywords: string; [key: string]: unknown }): Promise<Record<string, unknown>> {
    return this.transport.request('POST', '/tiktok/user', { json: opts });
  }

  video(opts: { videoUrl: string; [key: string]: unknown }): Promise<Record<string, unknown>> {
    const { videoUrl, ...rest } = opts;
    return this.transport.request('POST', '/tiktok/video', { json: { video_url: videoUrl, ...rest } });
  }
}
