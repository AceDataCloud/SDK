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

## Chat usage and billing

Accepted model requests through Chat Completions, Responses, and Messages are
billed by the selected model's input, output, and cache usage, not a fixed fee
per request. Switching protocol formats does not change this to per-call billing
or guarantee that a model accepts that format. Consult current model prices and
`usage.cost` for the charge; the SDK preserves reported usage without recalculating it.

- Chat Completions `prompt_tokens` includes reported cached tokens.
- Responses `input_tokens` includes reported cached tokens.
- Messages `input_tokens` excludes separately reported `cache_read_input_tokens`
  and `cache_creation_input_tokens`; those dimensions are charged separately.

Do not add cached tokens to the input total again for Chat Completions or
Responses, or treat Messages input alone as the full input/cache usage.

## Public Chat Completions models

Pass these public IDs in `ChatCompletionRequest.Model` to
`client.OpenAI().Chat().Completions().Create` or `CreateStream`. Put model-specific
fields in `ChatCompletionRequest.Extra`; the SDK does not rewrite IDs or enforce a catalog.

- `claude-opus-5-5`: supports text and streaming Chat Completions with `"n": 1`.
  Leave `Temperature` and `TopP` nil to use model defaults; do not set temperature
  below 1 or a non-default top-p. Use `"tool_choice": "auto"`, not forced tools.
  For native thinking blocks, signatures, and native tool semantics, use `client.Chat().Messages()`.
- `gemini-4-argon`: supports text and streaming Chat Completions. Thinking can
  consume output budget; Google recommends at least `MaxTokens: 32768` for ordinary
  tasks. This does not expose Interactions background long-output functionality.
- `kimi-k3.1-pro`: always reasons; pass `"reasoning_effort": "low"`, `"high"`, or `"max"`.
  Do not disable reasoning. Keep the full assistant message, including
  `reasoning_content` and `tool_calls`, in multi-turn and tool-call history.
  The existing `kimi-k3` alias remains available; use `"reasoning_effort": "max"` for it.

Check current account access and prices before calling. A model's advertised
context size does not guarantee the platform's per-request limit.

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

## Kling reference-video billing

Use `client.Kling().Generate` with `KlingGenerateRequest.VideoList` containing
`map[string]any{"video_url": referenceURL, "refer_type": "feature"}` and
`Model: "kling-o1"` or `"kling-v3-omni"`.
Reference videos use a separate billing tier: **1.202 Credits/second** in `std`
mode and **1.602 Credits/second** in `pro` mode. For a 5-second O1 result,
`std` / `pro` cost **4.005 / 5.340 Credits** without a reference video, or
**6.010 / 8.010 Credits** with one.

`refer_type: "base"` (the default) edits may follow the reference video's length;
billing uses the actual output duration rounded to the nearest integer second.
`refer_type: "feature"` uses the requested `Duration`. After `handle.Wait`, read
`usage.reference_video_seconds` in the completed task's `response` map for the final billed seconds;
the request-time estimate can differ from the final charge. This is response
usage, not a request parameter. Image references and first/last frames alone do
not trigger reference-video billing. Do not combine `VideoList` with
`GenerateAudio: true`.

## Suno music processing

Before a cover or extension, optionally call
`client.Suno().Availability(ctx, acedatacloud.SunoAvailabilityRequest{AudioID: audioID})`.
Use the song's `audio_id` from a completed task, not its `task_id`. This is a
synchronous API-token-authenticated check, currently without a Credits charge;
it returns the response map and an error, not a task handle to poll.
`result["data"].(map[string]any)["available"]` is only `true` on success: it is
positive evidence on the current channel, not a guarantee that a subsequent
operation will work. An inconclusive check returns an error, including
`503 availability_unknown`; never convert an error into `false`. Preserve the
error code and trace ID.

Use `client.Suno().Generate` with `SunoGenerateRequest{Custom: true, Lyric: lyric,
Style: style, NegativeTags: negativeTags}` for custom-mode music. `NegativeTags`
describes styles or genres to exclude; there is currently no fixed character
limit, but overly long input may still fail, so keep it concise. The SDK sends
it as `negative_tags` without truncation.

A downloadable audio file does not guarantee that its `audio_id` remains usable
for covers, extensions or stem separation. If processing returns
`suno_processing_unavailable`, keep the original `task_id` (the task handle's
`ID`, when available) and the error's `TraceID()` for support. The related codes
`suno_model_unavailable` and `suno_processing_failed` mean the selected model is
unavailable for that operation or processing returned no audio, respectively.
Suno can also return `api_error` with the message
`the account may have been offline`; this is a server error, not an SDK
authentication error.
These HTTP 500 errors retain their `Code()`, `TraceID()` and `Body()` through
the `Error` interface. Retrieve an existing task rather than submitting a
replacement generation just to check its result.

## Fish voice models

`client.Fish().Model(ctx, acedatacloud.FishModelRequest{Title: title, Voices: audioURL})`
creates a reusable voice from a single publicly downloadable audio URL string,
not an array or a multipart upload. Prefer a direct URL ending in `.mp3` or
`.wav`. Successful creation returns the model map directly (HTTP 201); its `_id`
can be used as `ReferenceID` in `client.Fish().Generate`.

Created voices are stored publicly long-term and may be searched and used by
other users. Omit `Visibility`: passing `private` or `unlist` does not make the
voice private. For temporary reference audio without creating a saved model,
use `FishGenerateRequest.References` instead of creating a model.

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
