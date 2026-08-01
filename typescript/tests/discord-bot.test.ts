import { DiscordBotClient } from '../src/resources/discord-bot';

const BASE = 'https://discord-bot-test.app.acedata.cloud';
const TOKEN = 'test-access-token';

function makeClient() {
  return new DiscordBotClient({ baseURL: BASE, token: TOKEN });
}

function mockFetch(body: unknown, status = 200) {
  return jest.spyOn(global, 'fetch').mockResolvedValue(
    new Response(JSON.stringify(body), {
      status,
      headers: { 'content-type': 'application/json' },
    }),
  );
}

afterEach(() => jest.restoreAllMocks());

// ── health ────────────────────────────────────────────────────────────

it('health returns gateway status', async () => {
  const fetchMock = mockFetch({ status: 'ok', gateway_ready: true });
  const client = makeClient();
  const result = await client.health();
  expect(result.status).toBe('ok');
  expect(result.gateway_ready).toBe(true);
  expect(fetchMock).toHaveBeenCalledWith(`${BASE}/health`);
});

// ── whoami ────────────────────────────────────────────────────────────

it('whoami returns account info', async () => {
  const fetchMock = mockFetch({ data: { id: '123', username: 'bot' } });
  const result = await makeClient().whoami();
  expect(result['id']).toBe('123');
  expect(fetchMock).toHaveBeenCalledWith(`${BASE}/api/whoami`, expect.any(Object));
});

// ── guilds ────────────────────────────────────────────────────────────

it('listGuilds returns guild list', async () => {
  mockFetch({ data: [{ id: 'g1', name: 'My Server' }] });
  const result = await makeClient().listGuilds();
  expect((result[0] as Record<string, unknown>)['id']).toBe('g1');
});

it('listChannels calls correct path', async () => {
  const fetchMock = mockFetch({ data: [{ id: 'c1', name: 'general' }] });
  await makeClient().listChannels('g1');
  expect(fetchMock).toHaveBeenCalledWith(
    `${BASE}/api/guilds/g1/channels`,
    expect.any(Object),
  );
});

it('createChannel posts channel name', async () => {
  const fetchMock = mockFetch({ data: { id: 'c2', name: 'announcements' } });
  const result = await makeClient().createChannel('g1', { name: 'announcements' });
  expect((result as Record<string, unknown>)['name']).toBe('announcements');
  const call = fetchMock.mock.calls[0][1] as RequestInit;
  expect(JSON.parse(call.body as string)).toMatchObject({ name: 'announcements' });
});

it('listMembers appends limit param', async () => {
  const fetchMock = mockFetch({ data: [{ id: 'u1' }] });
  await makeClient().listMembers('g1', { limit: 50 });
  expect(fetchMock.mock.calls[0][0]).toContain('limit=50');
});

// ── messages ──────────────────────────────────────────────────────────

it('sendMessage posts to /api/messages', async () => {
  const fetchMock = mockFetch({ data: { id: 'm1' } });
  const result = await makeClient().sendMessage({ channel_id: 'c1', content: 'hello' });
  const call = fetchMock.mock.calls[0][1] as RequestInit;
  expect(JSON.parse(call.body as string)).toMatchObject({ channel_id: 'c1', content: 'hello' });
  expect((result as Record<string, unknown>)['id']).toBe('m1');
});

it('sendMessage includes reply_to when provided', async () => {
  const fetchMock = mockFetch({ data: { id: 'm2' } });
  await makeClient().sendMessage({ channel_id: 'c1', content: 'reply', reply_to: 'm0' });
  const call = fetchMock.mock.calls[0][1] as RequestInit;
  expect(JSON.parse(call.body as string)).toMatchObject({ reply_to: 'm0' });
});

it('listMessages calls correct path', async () => {
  const fetchMock = mockFetch({ data: [{ id: 'm1' }] });
  await makeClient().listMessages('c1');
  expect(fetchMock.mock.calls[0][0]).toContain('/api/channels/c1/messages');
});

it('listMessages appends limit param', async () => {
  const fetchMock = mockFetch({ data: [] });
  await makeClient().listMessages('c1', { limit: 10 });
  expect(fetchMock.mock.calls[0][0]).toContain('limit=10');
});

it('searchMessages sends q param', async () => {
  const fetchMock = mockFetch({ data: [{ id: 'm1' }] });
  await makeClient().searchMessages('c1', { q: 'hello' });
  expect(fetchMock.mock.calls[0][0]).toContain('q=hello');
});

it('editMessage patches message', async () => {
  const fetchMock = mockFetch({ data: { id: 'm1', content: 'updated' } });
  const result = await makeClient().editMessage('c1', 'm1', { content: 'updated' });
  expect(fetchMock.mock.calls[0][1]).toMatchObject({ method: 'PATCH' });
  expect((result as Record<string, unknown>)['content']).toBe('updated');
});

it('deleteMessage calls DELETE', async () => {
  const fetchMock = mockFetch({ data: {} });
  await makeClient().deleteMessage('c1', 'm1');
  expect(fetchMock.mock.calls[0][1]).toMatchObject({ method: 'DELETE' });
});

it('addReaction posts emoji', async () => {
  const fetchMock = mockFetch({ data: {} });
  await makeClient().addReaction('c1', 'm1', { emoji: '👍' });
  const call = fetchMock.mock.calls[0][1] as RequestInit;
  expect(JSON.parse(call.body as string)).toMatchObject({ emoji: '👍' });
  expect(fetchMock.mock.calls[0][0]).toContain('/reactions');
});

it('pinMessage posts to /pin', async () => {
  const fetchMock = mockFetch({ data: {} });
  await makeClient().pinMessage('c1', 'm1');
  expect(fetchMock.mock.calls[0][0]).toContain('/pin');
});

// ── DMs ───────────────────────────────────────────────────────────────

it('createDm posts recipient_id', async () => {
  const fetchMock = mockFetch({ data: { id: 'dm1' } });
  await makeClient().createDm({ recipient_id: 'u1' });
  const call = fetchMock.mock.calls[0][1] as RequestInit;
  expect(JSON.parse(call.body as string)).toMatchObject({ recipient_id: 'u1' });
});

it('sendDm posts to /api/dms/send', async () => {
  const fetchMock = mockFetch({ data: { id: 'm3' } });
  await makeClient().sendDm({ recipient_id: 'u1', content: 'hey' });
  expect(fetchMock.mock.calls[0][0]).toContain('/api/dms/send');
});

// ── auth header ───────────────────────────────────────────────────────

it('sends Authorization header on authenticated requests', async () => {
  const fetchMock = mockFetch({ data: { id: '123' } });
  await makeClient().whoami();
  const call = fetchMock.mock.calls[0][1] as RequestInit;
  expect((call.headers as Record<string, string>)['authorization']).toBe(TOKEN);
});

// ── data unwrapping ───────────────────────────────────────────────────

it('unwraps data field from response', async () => {
  mockFetch({ data: { id: 'u1', username: 'alice' } });
  const result = await makeClient().whoami();
  expect(result).toEqual({ id: 'u1', username: 'alice' });
});

it('returns full body when no data field', async () => {
  mockFetch({ id: 'u1', username: 'alice' });
  const result = await makeClient().whoami();
  expect(result).toEqual({ id: 'u1', username: 'alice' });
});

// ── trailing slash removal ────────────────────────────────────────────

it('strips trailing slash from baseURL', async () => {
  const fetchMock = mockFetch({ data: { id: '123' } });
  const client = new DiscordBotClient({
    baseURL: `${BASE}/`,
    token: TOKEN,
  });
  await client.whoami();
  expect(fetchMock.mock.calls[0][0]).toBe(`${BASE}/api/whoami`);
});
