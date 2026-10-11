# AceDataCloud Go SDK

Official Go client for the [AceDataCloud API](https://platform.acedata.cloud?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=sdk_go_readme_platform).

Mirrors the design of the [Python](../python) and [TypeScript](../typescript) SDKs:

- Top-level `Client` with functional options.
- Domain resources: `OpenAI` (chat / responses), `Chat` (native messages), `Images`, `Tasks`.
- Automatic retries with exponential backoff on 408/409/429/5xx.
- `TaskHandle` for polling long-running image / audio / video tasks.
- Pluggable `PaymentHandler` hook for on-chain x402 payments — see the
  companion [X402Client Go package](https://github.com/AceDataCloud/X402Client/tree/main/go).

## Get your Ace Data Cloud API key

1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=sdk_go_readme_api_key). Sign in, or register an account first.
2. Find **General application**. If it has not been created, choose **Initialize General Application**. A general key can use the services available to your account; a dedicated application's key is limited to its service. Check the required service/model access and [current pricing](https://platform.acedata.cloud/models?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=sdk_go_readme_pricing).
3. Copy the **API Key** from the application card, or open **Keys / Manage Keys → Create** to create a separate key for this integration. Give it a recognizable name so you can revoke or rotate it independently.
4. When creating a key, review **Expiration Time**, **Set Usage Limitation**, and **Allowed APIs**. Enable only the restrictions you need, allow the operations you will call, then click **Create** and copy the token from the key list. Task lookup does not grant permission to submit a generation. Confirm the application's balance can cover your first request; any trial allowance is whatever your account currently displays.
5. Copy only the token value, without quotation marks, spaces, or `Bearer `. An API Key / API Token field expects this raw value; only a manually configured HTTP `Authorization` header needs the `Bearer ` prefix. A `platform-...` account-management token cannot replace a generation API key.

![Copy an application API key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

![Create a separately named key with optional restrictions](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/create-api-key-en.png)

Save the key in the client's credential store or the environment variable shown below. Never put it in a prompt, shared workflow, screenshot, or Git commit. If authentication fails, check the full copied value, application/service access, expiration, usage limit, and balance before creating another key.

Use this application key for API requests. SDK account-management methods require the separate credential described in their management documentation; do not interchange it with the API key. The optional x402 payment flow below is a separate way to pay for supported requests.

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

## Native Claude Messages

Use `MessagesRequest.Extra` for thinking and output configuration. These fields
are passed through without SDK model-specific enum or combination checks; the
selected model determines which values it accepts. For the beta `display: "updates"`
mode, set the required header on a dedicated client (headers apply to every request):

```go
client, err := acedatacloud.NewClient(
    acedatacloud.WithAPIToken("<token>"),
    acedatacloud.WithHeaders(map[string]string{
        "anthropic-beta": "thinking-display-updates-2026-08-18",
    }),
)
if err != nil { panic(err) }

response, err := client.Chat().Messages().Create(ctx, acedatacloud.MessagesRequest{
    Model: "claude-sonnet-5-5",
    Messages: []map[string]any{{"role": "user", "content": "Explain this code."}},
    Extra: map[string]any{
        "thinking": map[string]any{"type": "adaptive", "display": "updates"},
        "output_config": map[string]any{"effort": "high"},
    },
})
if err != nil { panic(err) }
```

`CreateStream` and `CountTokens` also preserve thinking configuration. Parameter
pass-through does not guarantee model support; API errors are returned through
the SDK's normal error handling.

## Images (task-based)

```go
handle, _, err := client.Images().Generate(ctx, acedatacloud.ImageGenerateRequest{
    Prompt:   "a cyberpunk cat",
    Provider: "nano-banana",
})
// Poll until completion (or use handle.Get(ctx) to check once)
res, err := handle.Wait(ctx, 3*time.Second, 5*time.Minute)
```

### Nano Banana 2.1

Select `Model: "nano-banana-2.1"` explicitly for generation or editing at
1K, 2K, or 4K. Omitting `Model` still uses `nano-banana`; there is no
`nano-banana-2.1:official` variant.

```go
handle, err := client.NanoBanana().Generate(ctx, acedatacloud.NanoBananaGenerateRequest{
    Action: "generate",
    Model: "nano-banana-2.1",
    Prompt: "A blue ceramic vase on a cream background",
    Resolution: "2K",
    AspectRatio: "1:1",
})
if err != nil { panic(err) }
if _, err = handle.Wait(ctx, 3*time.Second, 5*time.Minute); err != nil { panic(err) }

editHandle, err := client.NanoBanana().Generate(ctx, acedatacloud.NanoBananaGenerateRequest{
    Action: "edit",
    Model: "nano-banana-2.1",
    Prompt: "Change the vase to green; preserve the background",
    ImageURLs: handle.URLs(),
    Resolution: "4K",
})
if err != nil { panic(err) }
if _, err = editHandle.Wait(ctx, 3*time.Second, 5*time.Minute); err != nil { panic(err) }
```

`OpenAIImageModelNanoBanana21` also works with `client.OpenAI().Images().Generate`
and `.Edit` using `OpenAIImageRequest` (`Image` for editing). Those methods use
the OpenAI-compatible fields and return response maps, not task handles.

## More resources

```go
// Video / audio task-based generation (sora|luma|veo|kling|hailuo|seedance|wan|pixverse, suno|producer|fish)
vh, _, _ := client.Video().Generate(ctx, acedatacloud.VideoGenerateRequest{Prompt: "a cat", Provider: "kling"})
ah, _, _ := client.Audio().Generate(ctx, acedatacloud.AudioGenerateRequest{Prompt: "lofi beat", Provider: "suno"})

// Web search, face transforms, short URLs
client.Search().Google(ctx, acedatacloud.SearchRequest{Query: "AceDataCloud"})
client.Face().Swap(ctx, "https://a.png", "https://b.png", nil)
client.ShortURL().Create(ctx, "https://acedata.cloud", "", nil)
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
