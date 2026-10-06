const assert = require('node:assert/strict');
const test = require('node:test');
const app = require('../index');

test('authentication checks models with a Bearer token', async () => {
  let request;
  await app.authentication.test({ request: async (value) => { request = value; return { status: 200 }; } }, {
    authData: { api_key: 'test-token' },
  });
  assert.equal(request.url, 'https://api.acedata.cloud/v1/models');
  assert.equal(request.headers.Authorization, 'Bearer test-token');
});

test('chat action sends one request and returns useful fields', async () => {
  const requests = [];
  const result = await app.creates.send_chat.operation.perform({
    request: async (request) => {
      requests.push(request);
      return {
        status: 200,
        data: {
          id: 'chatcmpl-test', model: 'gpt-5.5',
          choices: [{ message: { content: 'Hello.' } }],
          usage: { total_tokens: 12 },
        },
      };
    },
  }, {
    authData: { api_key: 'test-token' },
    inputData: { model: 'gpt-5.5', prompt: 'Say hello.' },
  });
  assert.equal(requests.length, 1);
  assert.equal(requests[0].url, 'https://api.acedata.cloud/v1/chat/completions');
  assert.equal(requests[0].headers.Authorization, 'Bearer test-token');
  assert.deepEqual(requests[0].body.messages, [{ role: 'user', content: 'Say hello.' }]);
  assert.deepEqual(result, { id: 'chatcmpl-test', content: 'Hello.', model: 'gpt-5.5', total_tokens: 12 });
});
