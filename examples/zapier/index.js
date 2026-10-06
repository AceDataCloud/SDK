const chat = require('./send-chat');

module.exports = {
  version: require('./package.json').version,
  platformVersion: require('zapier-platform-core').version,
  authentication: {
    type: 'custom',
    fields: [{ key: 'api_key', label: 'AceDataCloud API token', type: 'password', required: true }],
    test: (z, bundle) => z.request({
      url: 'https://api.acedata.cloud/v1/models',
      headers: { Authorization: `Bearer ${bundle.authData.api_key}` },
    }),
    connectionLabel: 'AceDataCloud',
  },
  beforeRequest: [],
  afterResponse: [],
  triggers: {},
  searches: {},
  creates: { [chat.key]: chat },
  resources: {},
};
