const CHAT_URL = 'https://api.acedata.cloud/v1/chat/completions';
const CATALOG_URL = 'https://platform.acedata.cloud/api/v1/models/?type=chat';

const getModelChoices = async (z) => {
  const response = await z.request({ url: CATALOG_URL });
  const models = response.data?.data;
  if (!Array.isArray(models)) {
    throw new z.errors.Error('AceDataCloud could not load chat models. Try again later.', 'InvalidResponse');
  }
  return {
    results: models
      .filter((model) => model.type === 'chat' && typeof model.id === 'string')
      .map((model) => ({ id: model.id, label: model.label || model.id })),
  };
};

const throwApiError = (z, response) => {
  const traceId = response.data?.trace_id;
  const reference = typeof traceId === 'string' && /^[\da-f-]{36}$/i.test(traceId)
    ? ` Reference: ${traceId}.`
    : '';
  const code = response.data?.error?.code;
  if (code === 'token_mismatched') {
    throw new z.errors.Error('This API token cannot use Chat Completions. Check its API access.', 'TokenMismatched', response.status);
  }
  if (code === 'used_up') {
    throw new z.errors.Error('Your AceDataCloud balance is insufficient. Check your balance in the console.', 'BalanceUsedUp', response.status);
  }
  if (response.status === 401) {
    throw new z.errors.ExpiredAuthError('Your AceDataCloud API token is invalid. Reconnect your account.');
  }
  if (response.status === 429) {
    throw new z.errors.ThrottledError('AceDataCloud rate limit reached. Zapier will retry.', 60);
  }
  const messages = {
    400: 'AceDataCloud rejected the request. Check the model and prompt.',
    402: 'AceDataCloud requires payment for this request. Check your account and API token.',
    403: 'AceDataCloud blocked this request or the selected model is unavailable to this token.',
    404: 'The selected chat model is unavailable. Select another model.',
  };
  const message = messages[response.status]
    || 'AceDataCloud could not complete the chat request. Check the request before replaying it.';
  throw new z.errors.Error(`${message}${reference}`, 'ChatRequestFailed', response.status);
};

const perform = async (z, bundle) => {
  const { model, prompt, system_prompt: systemPrompt, max_completion_tokens: maxCompletionTokens } = bundle.inputData;
  if (typeof model !== 'string' || !model.trim() || typeof prompt !== 'string' || !prompt.trim()) {
    throw new z.errors.Error('Select a model and enter a prompt.', 'InvalidData', 400);
  }
  const messages = [];
  if (typeof systemPrompt === 'string' && systemPrompt.trim()) {
    messages.push({ role: 'system', content: systemPrompt });
  }
  messages.push({ role: 'user', content: prompt });

  const body = { model, messages, stream: false };
  if (maxCompletionTokens !== undefined && maxCompletionTokens !== null && maxCompletionTokens !== '') {
    const limit = Number(maxCompletionTokens);
    if (!Number.isSafeInteger(limit) || limit < 1) {
      throw new z.errors.Error('Max completion tokens must be a positive integer.', 'InvalidData', 400);
    }
    body.max_completion_tokens = limit;
  }

  const response = await z.request({
    url: CHAT_URL,
    method: 'POST',
    headers: {
      Authorization: `Bearer ${bundle.authData.api_key}`,
      'Content-Type': 'application/json',
    },
    body,
    skipThrowForStatus: true,
  });
  if (response.status >= 400) {
    throwApiError(z, response);
  }
  const data = response.data;
  const choice = data?.choices?.[0];
  const content = choice?.message?.content || choice?.message?.refusal;
  if (typeof data?.id !== 'string' || typeof content !== 'string' || !content) {
    throw new z.errors.Error(
      'AceDataCloud returned no chat text. Check the model and try a different prompt.',
      'InvalidResponse',
    );
  }
  const result = {
    id: data.id,
    content,
    model: data.model,
    finish_reason: choice.finish_reason,
  };
  for (const key of ['prompt_tokens', 'completion_tokens', 'total_tokens']) {
    if (Number.isSafeInteger(data.usage?.[key])) result[key] = data.usage[key];
  }
  if (Number.isFinite(data.created)) result.created_at = new Date(data.created * 1000).toISOString();
  return result;
};

module.exports = {
  key: 'send_chat',
  noun: 'Chat Response',
  display: {
    label: 'Create Chat Response',
    description: 'Creates a text response from a chat model. Each test and Zap run uses your AceDataCloud balance.',
  },
  operation: {
    cleanInputData: false,
    inputFields: [
      {
        key: 'model', label: 'Model', type: 'string', required: true,
        choices: { perform: getModelChoices },
        helpText: 'Choose a chat model from the current AceDataCloud catalog.',
      },
      { key: 'prompt', label: 'Prompt', type: 'text', required: true },
      { key: 'system_prompt', label: 'System instructions', type: 'text', required: false },
      {
        key: 'max_completion_tokens', label: 'Max completion tokens', type: 'integer', required: false,
        helpText: 'Optional output limit. Some models may not support this parameter.',
      },
    ],
    perform,
    sample: {
      id: 'chatcmpl-example', content: 'Hello! How can I help?', model: 'gpt-5.5',
      finish_reason: 'stop', created_at: '2026-10-06T00:00:00.000Z',
    },
    outputFields: [
      { key: 'id', label: 'Response ID' },
      { key: 'content', label: 'Response text' },
      { key: 'model', label: 'Model' },
      { key: 'finish_reason', label: 'Finish reason' },
      { key: 'prompt_tokens', label: 'Input tokens', type: 'integer' },
      { key: 'completion_tokens', label: 'Output tokens', type: 'integer' },
      { key: 'total_tokens', label: 'Total tokens', type: 'integer' },
      { key: 'created_at', label: 'Created at', type: 'datetime' },
    ],
  },
};
