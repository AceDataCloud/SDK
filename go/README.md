# AceDataCloud Go SDK

Official Go client for the [AceDataCloud API](https://platform.acedata.cloud).

Mirrors the design of the [Python](../python) and [TypeScript](../typescript) SDKs:

- Top-level `Client` with functional options.
- Domain resources: `OpenAI` (chat / responses), `Chat` (native messages), `Images`, `Tasks`.
- Automatic retries with exponential backoff on 408/409/429/5xx.
- `TaskHandle` for polling long-running image / audio / video tasks.
- Pluggable `PaymentHandler` hook for on-chain x402 payments — see the
  companion [X402Client Go package](https://github.com/AceDataCloud/X402Client/tree/main/go).

## Install

```bash
go get github.com/AceDataCloud/SDK/go@latest
```

## Quick start

```go
package main

import (
    "context"
    "fmt"

    acedatacloud "github.com/AceDataCloud/SDK/go"
)

func main() {
    client, err := acedatacloud.NewClient(acedatacloud.WithAPIToken("<token>"))
    if err != nil { panic(err) }

    resp, err := client.OpenAI().Chat().Completions().Create(context.Background(),
        acedatacloud.ChatCompletionRequest{
            Model: "gpt-4o-mini",
            Messages: []map[string]any{
                {"role": "user", "content": "Say hi in 3 words."},
            },
        })
    if err != nil { panic(err) }
    fmt.Printf("%+v\n", resp)
}
```

If you omit `WithAPIToken`, the SDK reads `ACEDATACLOUD_API_TOKEN` from the
environment. If that is also empty, you must supply a `PaymentHandler`
(typically from `x402-client`).

## Streaming

```go
chunks, errs := client.OpenAI().Chat().Completions().CreateStream(ctx,
    acedatacloud.ChatCompletionRequest{
        Model: "gpt-4o-mini",
        Messages: []map[string]any{{"role": "user", "content": "hi"}},
    })
for chunk := range chunks {
    fmt.Printf("%v\n", chunk)
}
if err := <-errs; err != nil { panic(err) }
```

## Images (task-based)

```go
handle, _, err := client.Images().Generate(ctx, acedatacloud.ImageGenerateRequest{
    Prompt:   "a cyberpunk cat",
    Provider: "nano-banana",
})
// Poll until completion (or use handle.Get(ctx) to check once)
res, err := handle.Wait(ctx, 3*time.Second, 5*time.Minute)
```

## Paying per request with x402

```go
import (
    acedatacloud "github.com/AceDataCloud/SDK/go"
    x402 "github.com/AceDataCloud/X402Client/go"
)

signer, _ := x402.NewEVMSignerFromPrivateKey("0x<your-key>")
handler := x402.NewHandler(x402.HandlerOptions{
    Network:   "base",
    EVMSigner: signer,
})

client, _ := acedatacloud.NewClient(acedatacloud.WithPaymentHandler(handler))
// Any call to a paid endpoint will be settled on-chain automatically.
```

## Errors

All API-level errors implement the `Error` interface and are typed:

| Error                      | Condition |
|----------------------------|-----------|
| `*AuthenticationError`     | 401 / missing token / expired token |
| `*RateLimitError`          | 429 |
| `*ValidationError`         | 400 / bad request |
| `*InsufficientBalanceError`| code=`used_up` |
| `*ResourceDisabledError`   | code=`disabled` |
| `*ModerationError`         | 403 |
| `*TimeoutError`            | network/task timeout |
| `*APIError`                | generic catch-all |

Use `errors.As` to type-assert:

```go
var rl *acedatacloud.RateLimitError
if errors.As(err, &rl) { /* backoff */ }
```

## Testing

```bash
cd go
go vet ./...
go test ./...
```
