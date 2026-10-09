const chat = require('./send-chat');

const testAuthentication = async (z, bundle) => {
  const response = await z.request({
    url: 'https://api.acedata.cloud/v1/models',
    headers: { Authorization: `Bearer ${bundle.authData.api_key}` },
    skipThrowForStatus: true,
  });

  if (response.status === 400 || response.status === 401 || response.status === 403) {
    throw new z.errors.Error(
      'The API token could not be verified. Check it in the AceDataCloud console and reconnect.',
      'InvalidAuth',
      response.status,
    );
  }
  if (response.status >= 400) {
    throw new z.errors.Error(
      'AceDataCloud could not verify the connection. Try again later.',
      'AuthTestFailed',
      response.status,
    );
  }
  if (response.data?.object !== 'list' || !Array.isArray(response.data.data)) {
    throw new z.errors.Error('AceDataCloud returned an unexpected model list.', 'InvalidResponse');
  }
  return response.data;
};

module.exports = {
  version: require('./package.json').version,
  platformVersion: require('zapier-platform-core').version,
  authentication: {
    type: 'custom',
    fields: [
      {
        key: 'api_key',
        label: 'API token',
        type: 'password',
        required: true,
        helpText: 'Copy your API token from [AceDataCloud Applications](https://platform.acedata.cloud/console/applications).',
      },
      {
        key: 'connection_name',
        label: 'Connection name',
        type: 'string',
        required: true,
        helpText: 'Choose a short label, such as Work. Do not enter your API token here.',
      },
    ],
    test: testAuthentication,
    connectionLabel: '{{connection_name}}',
  },
  beforeRequest: [],
  afterResponse: [],
  triggers: {},
  searches: {},
  creates: { [chat.key]: chat },
  resources: {},
};
