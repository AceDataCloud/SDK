package acedatacloud

import (
	"context"
	"encoding/json"
	"net/url"
	"strings"
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

// Models returns the models sub-namespace.
func (o *OpenAIResource) Models() *OpenAIModels { return &OpenAIModels{t: o.t} }

// Audio returns the audio sub-namespace.
func (o *OpenAIResource) Audio() *OpenAIAudio { return &OpenAIAudio{t: o.t} }

// Realtime returns the realtime helpers.
func (o *OpenAIResource) Realtime() *OpenAIRealtime { return &OpenAIRealtime{t: o.t} }

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

// OpenAIModels exposes “/openai/models“.
type OpenAIModels struct{ t *transport }

// List fetches available OpenAI-compatible models.
func (m *OpenAIModels) List(ctx context.Context) (map[string]any, error) {
	return m.t.do(ctx, requestOpts{Method: "GET", Path: "/openai/models"})
}

// SpeechRequest is the input to OpenAI audio.speech.
type SpeechRequest struct {
	Input          string         `json:"input"`
	Model          string         `json:"model,omitempty"`
	Voice          string         `json:"voice,omitempty"`
	ResponseFormat string         `json:"response_format,omitempty"`
	Speed          *float64       `json:"speed,omitempty"`
	Extra          map[string]any `json:"-"`
}

func (r SpeechRequest) toBody() map[string]any {
	body := map[string]any{"input": r.Input}
	if r.Model != "" {
		body["model"] = r.Model
	}
	if r.Voice != "" {
		body["voice"] = r.Voice
	}
	if r.ResponseFormat != "" {
		body["response_format"] = r.ResponseFormat
	}
	if r.Speed != nil {
		body["speed"] = *r.Speed
	}
	for k, v := range r.Extra {
		if _, exists := body[k]; !exists {
			body[k] = v
		}
	}
	return body
}

// OpenAIAudio exposes “/v1/audio/speech“.
type OpenAIAudio struct{ t *transport }

// Speech performs OpenAI-compatible text-to-speech synthesis.
func (a *OpenAIAudio) Speech(ctx context.Context, req SpeechRequest) (map[string]any, error) {
	return a.t.do(ctx, requestOpts{Method: "POST", Path: "/v1/audio/speech", Body: req.toBody()})
}

// OpenAIRealtime provides helpers for realtime endpoint URLs.
type OpenAIRealtime struct{ t *transport }

// URL returns a websocket URL for OpenAI-compatible realtime API.
func (r *OpenAIRealtime) URL(model string) string {
	base := strings.TrimRight(r.t.opts.baseURL, "/")
	wsBase := strings.Replace(base, "https://", "wss://", 1)
	wsBase = strings.Replace(wsBase, "http://", "ws://", 1)
	return wsBase + "/v1/realtime?model=" + url.QueryEscape(model)
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
