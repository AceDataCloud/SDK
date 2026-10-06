const perform = async (z, bundle) => {
  const response = await z.request({
    url: 'https://api.acedata.cloud/v1/chat/completions',
    method: 'POST',
    headers: {
      Authorization: `Bearer ${bundle.authData.api_key}`,
      'Content-Type': 'application/json',
    },
    body: {
      model: bundle.inputData.model,
      messages: [{ role: 'user', content: bundle.inputData.prompt }],
      stream: false,
    },
  });
  if (response.status >= 400) {
    throw new z.errors.Error('AceDataCloud chat request failed', 'ApiError', response.status);
  }
  const data = response.data;
  return {
    id: data.id,
    content: data.choices?.[0]?.message?.content ?? '',
    model: data.model,
    total_tokens: data.usage?.total_tokens,
  };
};

module.exports = {
  key: 'send_chat',
  noun: 'Chat Response',
  display: {
    label: 'Send Chat Prompt',
    description: 'Send one prompt to an AceDataCloud chat model.',
  },
  operation: {
    inputFields: [
      { key: 'model', label: 'Model', type: 'string', required: true, default: 'gpt-5.5' },
      { key: 'prompt', label: 'Prompt', type: 'text', required: true },
    ],
    perform,
    sample: { id: 'chatcmpl-example', content: 'Example response.', model: 'gpt-5.5', total_tokens: 10 },
    outputFields: [
      { key: 'id', label: 'Response ID' },
      { key: 'content', label: 'Text' },
      { key: 'model', label: 'Model' },
      { key: 'total_tokens', label: 'Total tokens', type: 'integer' },
    ],
  },
};
