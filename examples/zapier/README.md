# Zapier chat POC

This is a **local Platform CLI POC**, not a Zapier App Directory listing. It defines one custom API-token connection and one Chat Completions action. The connection test calls the non-billable `/v1/models` route. The action sends one billable request to `/v1/chat/completions` and returns text and usage.

```bash
npm install
npm test
```

The token is supplied through Zapier's authentication field. No token or real API call is included in the tests. Before a public integration, run a real Zap in a Zapier developer account, validate its UI and error handling, provide support/privacy details, then submit it for Zapier review. The POC is intentionally private and has not been uploaded.
