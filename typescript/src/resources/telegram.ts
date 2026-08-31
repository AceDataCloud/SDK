import { Transport } from '../runtime/transport';

export class Telegram {
  constructor(private transport: Transport) {}

  createQR() { return this.transport.request('POST', '/api/auth/qr'); }
  authStatus() { return this.transport.request('GET', '/api/auth/status'); }
  submitPassword(password: string) { return this.transport.request('POST', '/api/auth/password', { json: { password } }); }
  logout() { return this.transport.request('POST', '/api/auth/logout'); }
  whoami() { return this.transport.request('GET', '/api/whoami'); }
  chats(limit?: number, unreadOnly?: string) {
    return this.transport.request('GET', '/api/chats', { params: { ...(limit === undefined ? {} : { limit: String(limit) }), ...(unreadOnly === undefined ? {} : { unread_only: unreadOnly }) } });
  }
  contacts() { return this.transport.request('GET', '/api/contacts'); }
  messages(target: string, limit?: number) { return this.transport.request('GET', `/api/chats/${target}/messages`, { params: limit === undefined ? undefined : { limit: String(limit) } }); }
  searchMessages(q: string, target?: string, limit?: number) { return this.transport.request('GET', '/api/messages/search', { params: { q, ...(target === undefined ? {} : { target }), ...(limit === undefined ? {} : { limit: String(limit) }) } }); }
  sendMessage(target: string, text: string, replyTo?: string) { return this.transport.request('POST', '/api/messages', { json: { target, text, ...(replyTo === undefined ? {} : { reply_to: replyTo }) } }); }
  deleteMessage(target: string, messageId: string) { return this.transport.request('DELETE', `/api/chats/${target}/messages/${messageId}`); }
  addReaction(target: string, messageId: string, emoji: string) { return this.transport.request('POST', `/api/chats/${target}/messages/${messageId}/reactions`, { json: { emoji } }); }
  markRead(target: string) { return this.transport.request('POST', `/api/chats/${target}/read`); }
}
