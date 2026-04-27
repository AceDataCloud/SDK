// Package acedatacloud is the official Go SDK for the AceDataCloud API.
//
// It mirrors the design of the Python and TypeScript SDKs:
//
//   - A top-level Client with pluggable options.
//   - Domain resources: OpenAI (chat/responses), Chat (native messages),
//     Images, Tasks.
//   - Automatic retries with exponential backoff + jitter.
//   - Task polling via TaskHandle for long-running generation jobs.
//   - A pluggable PaymentHandler hook that is invoked on 402 Payment
//     Required, enabling on-chain x402 USDC payments via a companion
//     package.
//
// Basic usage:
//
//	client := acedatacloud.NewClient(acedatacloud.WithAPIToken("..."))
//	resp, err := client.OpenAI().Chat().Completions().Create(
//	    context.Background(),
//	    acedatacloud.ChatCompletionRequest{
//	        Model:    "gpt-4o-mini",
//	        Messages: []map[string]any{{"role": "user", "content": "hi"}},
//	    },
//	)
//
// See README.md for the full guide.
package acedatacloud
