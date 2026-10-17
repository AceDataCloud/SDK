const assert = require('node:assert/strict');
const { test, before, after, afterEach } = require('node:test');
const nock = require('nock');
const zapier = require('zapier-platform-core');
const app = require('../index');

const bundle = {
  authData: { api_key: 'offline-test-token', connection_name: 'Private connection label' },
  inputData: { model: 'gpt-5.5', prompt: 'Offline fixture only.' },
};
const appTester = zapier.createAppTester(app);

// Exercise Zapier's real request, response, schema and error middleware.
// Every API response is intercepted; unexpected requests cannot leave the test.
before(() => nock.disableNetConnect());
after(() => nock.enableNetConnect());
afterEach(() => {
  const pending = nock.pendingMocks();
  nock.cleanAll();
  assert.deepEqual(pending, []);
});

test('core authenticates with a read-only request without forwarding the connection label', async () => {
  nock('https://api.acedata.cloud')
    .get('/v1/models')
    .matchHeader('authorization', 'Bearer offline-test-token')
    .reply(200, { object: 'list', data: [{ id: 'gpt-5.5' }] });
  const result = await appTester(app.authentication.test, bundle);
  assert.equal(result.object, 'list');

  nock('https://api.acedata.cloud').get('/v1/models').reply(401, { error: { code: 'invalid_token' } });
  await assert.rejects(appTester(app.authentication.test, bundle), /API token could not be verified/);
});

test('core loads only chat choices from the public catalog without sending the token', async () => {
  nock('https://platform.acedata.cloud', { badheaders: ['authorization'] })
    .get('/api/v1/models/').query({ type: 'chat' })
    .reply(200, { object: 'list', data: [
      { id: 'gpt-5.5', type: 'chat', label: 'GPT-5.5' },
      { id: 'embedding', type: 'embedding', label: 'Embedding' },
    ] });
  const result = await appTester(app.creates.send_chat.operation.inputFields[0].choices.perform, bundle);
  assert.deepEqual(result, { results: [{ id: 'gpt-5.5', label: 'GPT-5.5' }] });
});

test('core serializes exactly one chat POST and exposes fields for the next Zap step', async () => {
  nock('https://api.acedata.cloud')
    .post('/v1/chat/completions', {
      model: 'gpt-5.5', stream: false,
      messages: [{ role: 'user', content: 'Offline fixture only.' }],
      max_completion_tokens: 32,
    })
    .matchHeader('authorization', 'Bearer offline-test-token')
    .reply(200, {
      id: 'offline-response', model: 'gpt-5.5', created: 1760000000,
      choices: [{ finish_reason: 'stop', message: { content: 'Fixture response.' } }],
      usage: { prompt_tokens: 8, completion_tokens: 4, total_tokens: 12 },
    });
  const result = await appTester(app.creates.send_chat.operation.perform, {
    ...bundle, inputData: { ...bundle.inputData, max_completion_tokens: 32 },
  });
  assert.equal(result.id, 'offline-response');
  assert.equal(result.content, 'Fixture response.');
  assert.equal(result.total_tokens, 12);
  assert.equal(result.created_at, '2025-10-09T08:53:20.000Z');
  assert.ok(!JSON.stringify(result).includes(bundle.authData.api_key));
  assert.ok(!JSON.stringify(result).includes(bundle.authData.connection_name));
});

test('core preserves custom auth, access, balance and moderation errors', async () => {
  const cases = [
    [401, {}, 'ExpiredAuthError'],
    [401, { error: { code: 'token_mismatched' } }, 'TokenMismatched'],
    [403, { error: { code: 'used_up' } }, 'BalanceUsedUp'],
    [403, { error: { message: 'private upstream detail' } }, 'ChatRequestFailed'],
  ];
  for (const [status, data, code] of cases) {
    nock('https://api.acedata.cloud').post('/v1/chat/completions').reply(status, data);
    await assert.rejects(appTester(app.creates.send_chat.operation.perform, bundle), (error) => {
      if (code === 'ExpiredAuthError') {
        assert.equal(error.name, code);
      } else {
        assert.equal(error.name, 'AppError');
        const details = JSON.parse(error.message);
        assert.equal(details.code, code);
        assert.equal(details.status, status);
      }
      assert.ok(!error.message.includes('private upstream detail'));
      return true;
    });
  }
});

test('core returns the safe throttle message with server delay or a 60-second fallback', async () => {
  for (const [header, expected] of [[undefined, 60], ['7', 7], ['invalid', 60], ['-1', 60]]) {
    nock('https://api.acedata.cloud').post('/v1/chat/completions')
      .reply(429, { error: { message: 'private upstream detail' } }, header ? { 'Retry-After': header } : {});
    await assert.rejects(appTester(app.creates.send_chat.operation.perform, bundle), (error) => {
      assert.equal(error.name, 'ThrottledError');
      const details = JSON.parse(error.message);
      assert.equal(details.delay, expected);
      assert.equal(details.message, 'AceDataCloud rate limit reached. Zapier will retry.');
      return true;
    });
  }
});

test('core auth-template extraction uses an API-token placeholder, never the connection label', async () => {
  const handler = zapier.createAppHandler(app);
  const response = await handler({ command: 'getAuthTemplate', bundle: {} });
  assert.equal(response.status, 'SUCCESS');
  assert.equal(response.results.supported, true);
  assert.equal(response.results.source, 'authentication.test');
  const headers = response.results.template.headers;
  assert.equal(headers.Authorization, 'Bearer {{bundle.authData.api_key}}');
  assert.ok(!JSON.stringify(response.results).includes('connection_name'));
  assert.ok(!JSON.stringify(response.results).includes(bundle.authData.api_key));
});
