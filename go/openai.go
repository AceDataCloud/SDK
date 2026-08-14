package acedatacloud

import (
	"context"
	"encoding/json"
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
	Model             string           `json:"model"`
	Input             any              `json:"input"`
	Background        *bool            `json:"background,omitempty"`
	Include           []string         `json:"include,omitempty"`
	MaxOutputTokens   int              `json:"max_output_tokens,omitempty"`
	MaxTokens         int              `json:"max_tokens,omitempty"`
	N                 int              `json:"n,omitempty"`
	ParallelToolCalls *bool            `json:"parallel_tool_calls,omitempty"`
	Reasoning         map[string]any   `json:"reasoning,omitempty"`
	ResponseFormat    map[string]any   `json:"response_format,omitempty"`
	Store             *bool            `json:"store,omitempty"`
	Stream            bool             `json:"stream,omitempty"`
	StreamOptions     map[string]any   `json:"stream_options,omitempty"`
	Temperature       *float64         `json:"temperature,omitempty"`
	Text              map[string]any   `json:"text,omitempty"`
	ToolChoice        any              `json:"tool_choice,omitempty"`
	Tools             []map[string]any `json:"tools,omitempty"`
	Extra             map[string]any   `json:"-"`
}

func (r ResponsesRequest) toBody() map[string]any {
	body := map[string]any{"model": r.Model, "input": r.Input}
	if r.Background != nil {
		body["background"] = *r.Background
	}
	if len(r.Include) > 0 {
		body["include"] = r.Include
	}
	if r.MaxOutputTokens > 0 {
		body["max_output_tokens"] = r.MaxOutputTokens
	}
	if r.MaxTokens > 0 {
		body["max_tokens"] = r.MaxTokens
	}
	if r.N > 0 {
		body["n"] = r.N
	}
	if r.ParallelToolCalls != nil {
		body["parallel_tool_calls"] = *r.ParallelToolCalls
	}
	if r.Reasoning != nil {
		body["reasoning"] = r.Reasoning
	}
	if r.ResponseFormat != nil {
		body["response_format"] = r.ResponseFormat
	}
	if r.Store != nil {
		body["store"] = *r.Store
	}
	if r.Stream {
		body["stream"] = true
	}
	if r.StreamOptions != nil {
		body["stream_options"] = r.StreamOptions
	}
	if r.Temperature != nil {
		body["temperature"] = *r.Temperature
	}
	if r.Text != nil {
		body["text"] = r.Text
	}
	if r.ToolChoice != nil {
		body["tool_choice"] = r.ToolChoice
	}
	if len(r.Tools) > 0 {
		body["tools"] = r.Tools
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
