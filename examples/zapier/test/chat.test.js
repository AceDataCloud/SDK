const assert = require('node:assert/strict');
const test = require('node:test');
const zapier = require('zapier-platform-core');
const app = require('../index');

const bundle = {
  authData: { api_key: 'test-token', connection_name: 'Work' },
  inputData: { model: 'gpt-5.5', prompt: 'Say hello.' },
};

const zWithResponse = (response, requests = []) => ({
  errors: zapier.errors,
  request: async (request) => {
    requests.push(request);
    return response;
  },
});

test('connection test rejects an invalid token without making a billable request', async () => {
  assert.equal(app.authentication.fields[0].type, 'password');
  assert.equal(app.authentication.connectionLabel, '{{connection_name}}');
  const requests = [];
  await assert.rejects(
    app.authentication.test(zWithResponse({ status: 401, data: { error: { code: 'invalid_token' } } }, requests), bundle),
    /API token could not be verified/,
  );
  assert.equal(requests.length, 1);
  assert.equal(requests[0].url, 'https://api.acedata.cloud/v1/models');
  assert.equal(requests[0].headers.Authorization, 'Bearer test-token');
  assert.equal(requests[0].skipThrowForStatus, true);
});

test('connection test accepts a model list and rejects a misleading success response', async () => {
  const valid = { status: 200, data: { object: 'list', data: [{ id: 'gpt-5.5' }] } };
  assert.deepEqual(await app.authentication.test(zWithResponse(valid), bundle), valid.data);
  await assert.rejects(
    app.authentication.test(zWithResponse({ status: 200, data: { error: 'unauthorized' } }), bundle),
    /unexpected model list/,
  );
});

test('model selector returns chat models from the live catalog shape', async () => {
  const requests = [];
  const choices = await app.creates.send_chat.operation.inputFields[0].choices.perform(
    zWithResponse({ status: 200, data: { data: [
      { id: 'gpt-5.5', label: 'GPT-5.5', type: 'chat' },
      { id: 'text-embedding-3', label: 'Embedding', type: 'embedding' },
    ] } }, requests),
  );
  assert.deepEqual(choices, { results: [{ id: 'gpt-5.5', label: 'GPT-5.5' }] });
  assert.equal(requests[0].url, 'https://platform.acedata.cloud/api/v1/models/?type=chat');
});

test('chat action sends one paid, non-streaming request and exposes mapping fields', async () => {
  const requests = [];
  const result = await app.creates.send_chat.operation.perform(zWithResponse({
    status: 200,
    data: {
      id: 'chatcmpl-test', model: 'gpt-5.5', created: 1760000000,
      choices: [{ finish_reason: 'stop', message: { content: 'Hello.' } }],
      usage: { prompt_tokens: 8, completion_tokens: 4, total_tokens: 12 },
    },
  }, requests), {
    ...bundle,
    inputData: { ...bundle.inputData, system_prompt: 'Be brief.', max_completion_tokens: '32' },
  });
  assert.equal(requests.length, 1);
  assert.equal(requests[0].url, 'https://api.acedata.cloud/v1/chat/completions');
  assert.equal(requests[0].headers.Authorization, 'Bearer test-token');
  assert.deepEqual(requests[0].body, {
    model: 'gpt-5.5', stream: false, max_completion_tokens: 32,
    messages: [
      { role: 'system', content: 'Be brief.' },
      { role: 'user', content: 'Say hello.' },
    ],
  });
  assert.deepEqual(result, {
    id: 'chatcmpl-test', content: 'Hello.', model: 'gpt-5.5', finish_reason: 'stop',
    prompt_tokens: 8, completion_tokens: 4, total_tokens: 12,
    created_at: '2025-10-09T08:53:20.000Z',
  });
});

test('chat action accepts a model refusal as visible text and rejects empty results', async () => {
  const refusal = { status: 200, data: {
    id: 'refusal-1', model: 'gpt-5.5',
    choices: [{ finish_reason: 'content_filter', message: { content: null, refusal: 'I cannot help with that.' } }],
  } };
  const result = await app.creates.send_chat.operation.perform(zWithResponse(refusal), bundle);
  assert.equal(result.content, 'I cannot help with that.');
  await assert.rejects(
    app.creates.send_chat.operation.perform(zWithResponse({ status: 200, data: { id: 'empty', choices: [] } }), bundle),
    /returned no chat text/,
  );
});

test('auth failures, rate limits, and balance errors use Zapier error types', async () => {
  const run = (response) => app.creates.send_chat.operation.perform(zWithResponse(response), bundle);
  await assert.rejects(run({ status: 401, data: {} }), zapier.errors.ExpiredAuthError);
  await assert.rejects(run({ status: 429, data: {} }), zapier.errors.ThrottledError);
  await assert.rejects(run({ status: 403, data: { error: { code: 'used_up', message: 'internal supplier details' } } }),
    (error) => error.message.includes('balance is insufficient') && !error.message.includes('supplier'));
  await assert.rejects(run({ status: 401, data: { error: { code: 'token_mismatched' } } }),
    (error) => error.message.includes('cannot use Chat Completions') && !(error instanceof zapier.errors.ExpiredAuthError));
});

test('invalid inputs fail before a billable API request', async () => {
  const requests = [];
  const z = zWithResponse({ status: 200 }, requests);
  await assert.rejects(app.creates.send_chat.operation.perform(z, {
    ...bundle, inputData: { ...bundle.inputData, max_completion_tokens: '-2' },
  }), /positive integer/);
  await assert.rejects(app.creates.send_chat.operation.perform(z, {
    ...bundle, inputData: { model: 'gpt-5.5', prompt: ' ' },
  }), /Select a model and enter a prompt/);
  assert.equal(requests.length, 0);
});
