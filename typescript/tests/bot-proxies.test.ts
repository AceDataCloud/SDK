import { Discord } from '../src/resources/discord';
import { Telegram } from '../src/resources/telegram';

test('Discord proxy uses documented channel search query', async () => {
  const request = jest.fn().mockResolvedValue({});
  await new Discord({ request } as any).searchMessages('channel', 'hello', 25);
  expect(request).toHaveBeenCalledWith('GET', '/api/channels/channel/messages/search', { params: { q: 'hello', limit: '25' } });
});

test('Telegram proxy keeps unread_only a string', async () => {
  const request = jest.fn().mockResolvedValue({});
  await new Telegram({ request } as any).chats(20, 'false');
  expect(request).toHaveBeenCalledWith('GET', '/api/chats', { params: { limit: '20', unread_only: 'false' } });
});
