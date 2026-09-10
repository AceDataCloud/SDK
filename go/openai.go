package acedatacloud

import (
	"context"
	"encoding/json"
)

// OpenAIImageModel identifies a model supported by OpenAI image endpoints.
type OpenAIImageModel = string

const (
	OpenAIImageModelDallE2                     OpenAIImageModel = "dall-e-2"
	OpenAIImageModelDallE3                     OpenAIImageModel = "dall-e-3"
	OpenAIImageModelGPTImage1                  OpenAIImageModel = "gpt-image-1"
	OpenAIImageModelGPTImage15                 OpenAIImageModel = "gpt-image-1.5"
	OpenAIImageModelGPTImage2                  OpenAIImageModel = "gpt-image-2"
	OpenAIImageModelGPTImage25Flare            OpenAIImageModel = "gpt-image-2.5-flare"
	OpenAIImageModelGPTImage25FlareOfficial    OpenAIImageModel = "gpt-image-2.5-flare:official"
	OpenAIImageModelGPTImage25Sunburst         OpenAIImageModel = "gpt-image-2.5-sunburst"
	OpenAIImageModelGPTImage25SunburstOfficial OpenAIImageModel = "gpt-image-2.5-sunburst:official"
	OpenAIImageModelGPTImage2Reverse           OpenAIImageModel = "gpt-image-2:reverse"
	OpenAIImageModelGPTImage2Official          OpenAIImageModel = "gpt-image-2:official"
	OpenAIImageModelNanoBanana                 OpenAIImageModel = "nano-banana"
	OpenAIImageModelNanoBanana2Lite            OpenAIImageModel = "nano-banana-2-lite"
	OpenAIImageModelNanoBanana2                OpenAIImageModel = "nano-banana-2"
	OpenAIImageModelNanoBananaPro              OpenAIImageModel = "nano-banana-pro"
)

// ChatCompletionRequest is the input to OpenAI chat.completions.create.
//
// The struct exposes the common fields explicitly and an “Extra“ map
// for forward-compatible fields (tools, response_format, etc.).
type ChatCompletionRequest struct {
	Model       string           `json:"model"`
	Messages    []map[string]any `json:"messages"`
	Stream      bool             `json:"stream,omitempty"`
	MaxTokens   int              `json:"max_tokens,omitempty"`
	Temperature *float64         `json:"temperature,omitempty"`
	TopP        *float64         `json:"top_p,omitempty"`

	// Extra is merged into the request body. Keys here take precedence
	// over nothing — they are only added if the explicit field is zero.
	Extra map[string]any `json:"-"`
}

func (r ChatCompletionRequest) toBody() map[string]any {
	body := map[string]any{
		"model":    r.Model,
		"messages": r.Messages,
	}
	if r.Stream {
		body["stream"] = true
	}
	if r.MaxTokens > 0 {
		body["max_tokens"] = r.MaxTokens
	}
	if r.Temperature != nil {
		body["temperature"] = *r.Temperature
	}
	if r.TopP != nil {
		body["top_p"] = *r.TopP
	}
	for k, v := range r.Extra {
		if _, exists := body[k]; !exists {
			body[k] = v
		}
	}
	return body
}

// ResponsesRequest is the input to OpenAI responses.create.
type ResponsesRequest struct {
	Model  string         `json:"model"`
	Input  any            `json:"input"`
	Stream bool           `json:"stream,omitempty"`
	Extra  map[string]any `json:"-"`
}

func (r ResponsesRequest) toBody() map[string]any {
	body := map[string]any{"model": r.Model, "input": r.Input}
	if r.Stream {
		body["stream"] = true
	}
	for k, v := range r.Extra {
		if _, exists := body[k]; !exists {
			body[k] = v
		}
	}
	return body
}

// OpenAIResource groups the OpenAI-compatible endpoints.
type OpenAIResource struct {
	t *transport
}

// Chat returns the chat sub-namespace.
func (o *OpenAIResource) Chat() *OpenAIChat { return &OpenAIChat{t: o.t} }

// Responses returns the responses sub-namespace.
func (o *OpenAIResource) Responses() *OpenAIResponses { return &OpenAIResponses{t: o.t} }

// Images returns the OpenAI-compatible image sub-namespace.
func (o *OpenAIResource) Images() *OpenAIImages { return &OpenAIImages{t: o.t} }

// OpenAIImageRequest is the JSON input for OpenAI-compatible image endpoints.
type OpenAIImageRequest struct {
	Model  OpenAIImageModel `json:"model"`
	Prompt string           `json:"prompt"`
	Image  any              `json:"image,omitempty"`
	Extra  map[string]any   `json:"-"`
}

func (r OpenAIImageRequest) toBody() map[string]any {
	body := map[string]any{"model": r.Model, "prompt": r.Prompt}
	if r.Image != nil {
		body["image"] = r.Image
	}
	for k, v := range r.Extra {
		if _, exists := body[k]; !exists {
			body[k] = v
		}
	}
	return body
}

// OpenAIImages exposes the OpenAI-compatible image generation and editing endpoints.
type OpenAIImages struct{ t *transport }

// Generate creates images from a text prompt.
func (i *OpenAIImages) Generate(ctx context.Context, req OpenAIImageRequest) (map[string]any, error) {
	return i.t.do(ctx, requestOpts{Method: "POST", Path: "/openai/images/generations", Body: req.toBody()})
}

// Edit edits one or more input images.
func (i *OpenAIImages) Edit(ctx context.Context, req OpenAIImageRequest) (map[string]any, error) {
	return i.t.do(ctx, requestOpts{Method: "POST", Path: "/openai/images/edits", Body: req.toBody()})
}

// OpenAIChat exposes “/v1/chat/completions“.
type OpenAIChat struct{ t *transport }

// Completions returns the completions sub-namespace.
func (c *OpenAIChat) Completions() *OpenAIChatCompletions { return &OpenAIChatCompletions{t: c.t} }

// OpenAIChatCompletions exposes chat.completions.create.
type OpenAIChatCompletions struct{ t *transport }

// Create performs a blocking (non-streaming) chat completion.
func (c *OpenAIChatCompletions) Create(ctx context.Context, req ChatCompletionRequest) (map[string]any, error) {
	body := req.toBody()
	delete(body, "stream")
	return c.t.do(ctx, requestOpts{Method: "POST", Path: "/v1/chat/completions", Body: body})
}

// CreateStream performs a streaming chat completion and returns a
// channel of decoded chunks (each a “map[string]any“ parsed from a
// single SSE “data:“ line).
func (c *OpenAIChatCompletions) CreateStream(ctx context.Context, req ChatCompletionRequest) (<-chan map[string]any, <-chan error) {
	req.Stream = true
	return streamDecode(c.t, "/v1/chat/completions", req.toBody())
}

// OpenAIResponses exposes “/openai/responses“.
type OpenAIResponses struct{ t *transport }

// Create performs a blocking responses.create.
func (r *OpenAIResponses) Create(ctx context.Context, req ResponsesRequest) (map[string]any, error) {
	body := req.toBody()
	delete(body, "stream")
	return r.t.do(ctx, requestOpts{Method: "POST", Path: "/openai/responses", Body: body})
}

// CreateStream performs a streaming responses.create.
func (r *OpenAIResponses) CreateStream(ctx context.Context, req ResponsesRequest) (<-chan map[string]any, <-chan error) {
	req.Stream = true
	return streamDecode(r.t, "/openai/responses", req.toBody())
}

// streamDecode wraps transport.stream and parses each SSE data line as JSON.
func streamDecode(t *transport, path string, body any) (<-chan map[string]any, <-chan error) {
	raw, rawErr := t.stream(context.Background(), path, body)
	out := make(chan map[string]any)
	errCh := make(chan error, 1)
	go func() {
		defer close(out)
		defer close(errCh)
		for {
			select {
			case chunk, ok := <-raw:
				if !ok {
					return
				}
				parsed := map[string]any{}
				if err := json.Unmarshal(chunk, &parsed); err == nil {
					out <- parsed
				}
			case err, ok := <-rawErr:
				if ok && err != nil {
					errCh <- err
					return
				}
				if !ok {
					return
				}
			}
		}
	}()
	return out, errCh
}
