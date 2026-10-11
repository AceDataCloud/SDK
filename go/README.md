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

## Maestro video production

Use the provider client to request one finished video in one language:

```go
handle, err := client.Maestro().Generate(ctx, acedatacloud.MaestroGenerateRequest{
    Prompt: "Explain vector databases to beginners in 20 seconds",
    Langs: []string{"en"},
    Aspect: "9:16",
    Duration: 20,
    Scenario: "narrated",
})
if err != nil { panic(err) }
result, err := handle.Wait(ctx, 3*time.Second, 10*time.Minute)
if err != nil { panic(err) }
```

Omitting `Langs` defaults to `[]string{"zh-cn"}`; an explicit slice must contain
exactly one language. Create separate tasks for other languages. The completed
result contains one video in `response.data.variants`. To revise a video, use
`Action: "remix"`, `"edit"`, or `"extend"` with `RefTaskID: handle.ID`.

There is no quality tier: all videos use 1080p/30fps and target durations of
5–300 seconds. Successful tasks cost **0.7 Credits per actual delivered second**,
with integer billed seconds capped at the requested duration (falling back to
that duration if it cannot be read). All scenarios, actions, and languages have
the same rate; failed tasks and `/maestro/tasks` polling are free.

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
