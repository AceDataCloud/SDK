import { Transport } from '../runtime/transport';

export class Discord {
  constructor(private transport: Transport) {}

  whoami() { return this.transport.request('GET', '/api/whoami'); }
  guilds() { return this.transport.request('GET', '/api/guilds'); }
  createChannel(guildId: string, name: string) {
    return this.transport.request('POST', `/api/guilds/${guildId}/channels`, { json: { name } });
  }
  members(guildId: string, limit?: number) {
    return this.transport.request('GET', `/api/guilds/${guildId}/members`, { params: limit === undefined ? undefined : { limit: String(limit) } });
  }
  sendMessage(channelId: string, content: string, replyTo?: string) {
    return this.transport.request('POST', '/api/messages', { json: { channel_id: channelId, content, ...(replyTo === undefined ? {} : { reply_to: replyTo }) } });
  }
  messages(channelId: string, limit?: number) {
    return this.transport.request('GET', `/api/channels/${channelId}/messages`, { params: limit === undefined ? undefined : { limit: String(limit) } });
  }
  searchMessages(channelId: string, q: string, limit?: number) {
    return this.transport.request('GET', `/api/channels/${channelId}/messages/search`, { params: { q, ...(limit === undefined ? {} : { limit: String(limit) }) } });
  }
  deleteMessage(channelId: string, messageId: string) { return this.transport.request('DELETE', `/api/channels/${channelId}/messages/${messageId}`); }
  addReaction(channelId: string, messageId: string, emoji: string) { return this.transport.request('POST', `/api/channels/${channelId}/messages/${messageId}/reactions`, { json: { emoji } }); }
  pinMessage(channelId: string, messageId: string) { return this.transport.request('POST', `/api/channels/${channelId}/messages/${messageId}/pin`); }
  createDM(recipientId: string) { return this.transport.request('POST', '/api/dms', { json: { recipient_id: recipientId } }); }
  sendDM(recipientId: string, content: string) { return this.transport.request('POST', '/api/dms/send', { json: { recipient_id: recipientId, content } }); }
}
