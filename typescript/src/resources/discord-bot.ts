/** Discord Agent Proxy client.
 *
 * The Discord Agent Proxy is an independently deployed service.  Users
 * deploy it from the AceData Cloud console at
 * https://platform.acedata.cloud/console/applications and receive a
 * deployment-specific base URL and access token.
 *
 * Use {@link DiscordBotClient} to interact with the REST API exposed by
 * that deployment.
 */

export interface DiscordBotClientOptions {
  /** Deployment URL, e.g. `https://discord-bot-xxxxxxxxxxxx.app.acedata.cloud` */
  baseURL: string;
  /** Access token shown in the console for this deployment */
  token: string;
  /** Request timeout in milliseconds (default 300_000) */
  timeout?: number;
}

export class DiscordBotClient {
  private base: string;
  private token: string;
  private timeout: number;

  constructor(opts: DiscordBotClientOptions) {
    this.base = opts.baseURL.replace(/\/$/, '');
    this.token = opts.token;
    this.timeout = opts.timeout ?? 300_000;
  }

  private async request<T = unknown>(
    method: string,
    path: string,
    opts?: { json?: unknown; params?: Record<string, string | number> },
  ): Promise<T> {
    let url = `${this.base}${path}`;
    if (opts?.params) {
      const qs = new URLSearchParams(
        Object.entries(opts.params).map(([k, v]): [string, string] => [k, String(v)]),
      );
      url = `${url}?${qs}`;
    }
    const controller = new AbortController();
    const id = setTimeout(() => controller.abort(), this.timeout);
    try {
      const resp = await fetch(url, {
        method,
        headers: {
          accept: 'application/json',
          'content-type': 'application/json',
          authorization: this.token,
        },
        body: opts?.json != null ? JSON.stringify(opts.json) : undefined,
        signal: controller.signal,
      });
      const body = (await resp.json()) as Record<string, unknown>;
      if (!resp.ok) {
        const msg = typeof body.error === 'string' ? body.error : resp.statusText;
        const err = new Error(msg) as Error & { statusCode: number };
        err.statusCode = resp.status;
        throw err;
      }
      return ('data' in body ? body.data : body) as T;
    } finally {
      clearTimeout(id);
    }
  }

  // ── No-auth endpoint ───────────────────────────────────────────────

  /** Check service health (no auth required). */
  async health(): Promise<{ status: string; gateway_ready: boolean }> {
    const resp = await fetch(`${this.base}/health`);
    return resp.json() as Promise<{ status: string; gateway_ready: boolean }>;
  }

  // ── Account ────────────────────────────────────────────────────────

  /** Return information about the proxied Discord account. */
  async whoami(): Promise<Record<string, unknown>> {
    return this.request('GET', '/api/whoami');
  }

  // ── Guilds ─────────────────────────────────────────────────────────

  /** List all guilds (servers) the account has joined. */
  async listGuilds(): Promise<unknown[]> {
    return this.request('GET', '/api/guilds');
  }

  /** List channels in a guild. */
  async listChannels(guildId: string): Promise<unknown[]> {
    return this.request('GET', `/api/guilds/${guildId}/channels`);
  }

  /** Create a text channel in a guild. */
  async createChannel(
    guildId: string,
    opts: { name: string },
  ): Promise<Record<string, unknown>> {
    return this.request('POST', `/api/guilds/${guildId}/channels`, { json: opts });
  }

  /** List members of a guild (default limit 100). */
  async listMembers(
    guildId: string,
    opts?: { limit?: number },
  ): Promise<unknown[]> {
    return this.request('GET', `/api/guilds/${guildId}/members`, {
      params: opts?.limit != null ? { limit: opts.limit } : undefined,
    });
  }

  // ── Messages ───────────────────────────────────────────────────────

  /** Send a message to a channel. */
  async sendMessage(opts: {
    channel_id: string;
    content: string;
    reply_to?: string;
  }): Promise<Record<string, unknown>> {
    return this.request('POST', '/api/messages', { json: opts });
  }

  /** Read recent messages from a channel (default 50, max 100). */
  async listMessages(
    channelId: string,
    opts?: { limit?: number },
  ): Promise<unknown[]> {
    return this.request('GET', `/api/channels/${channelId}/messages`, {
      params: opts?.limit != null ? { limit: opts.limit } : undefined,
    });
  }

  /** Search messages in a channel. */
  async searchMessages(
    channelId: string,
    opts: { q: string; limit?: number },
  ): Promise<unknown[]> {
    return this.request('GET', `/api/channels/${channelId}/messages/search`, {
      params: {
        q: opts.q,
        ...(opts.limit != null ? { limit: opts.limit } : {}),
      },
    });
  }

  /** Edit a message you own. */
  async editMessage(
    channelId: string,
    messageId: string,
    opts: { content: string },
  ): Promise<Record<string, unknown>> {
    return this.request('PATCH', `/api/channels/${channelId}/messages/${messageId}`, {
      json: opts,
    });
  }

  /** Delete a message. */
  async deleteMessage(
    channelId: string,
    messageId: string,
  ): Promise<Record<string, unknown>> {
    return this.request('DELETE', `/api/channels/${channelId}/messages/${messageId}`);
  }

  /** Add an emoji reaction to a message. */
  async addReaction(
    channelId: string,
    messageId: string,
    opts: { emoji: string },
  ): Promise<Record<string, unknown>> {
    return this.request(
      'POST',
      `/api/channels/${channelId}/messages/${messageId}/reactions`,
      { json: opts },
    );
  }

  /** Pin a message in a channel. */
  async pinMessage(
    channelId: string,
    messageId: string,
  ): Promise<Record<string, unknown>> {
    return this.request('POST', `/api/channels/${channelId}/messages/${messageId}/pin`);
  }

  // ── Direct messages ────────────────────────────────────────────────

  /** Open a DM channel with a user; returns the channel info. */
  async createDm(opts: { recipient_id: string }): Promise<Record<string, unknown>> {
    return this.request('POST', '/api/dms', { json: opts });
  }

  /** Send a direct message to a user. */
  async sendDm(opts: {
    recipient_id: string;
    content: string;
  }): Promise<Record<string, unknown>> {
    return this.request('POST', '/api/dms/send', { json: opts });
  }
}
