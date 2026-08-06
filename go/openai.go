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

// OpenAITaskRetrieveRequest is the input to openai.tasks.retrieve.
type OpenAITaskRetrieveRequest struct {
	ID      string
	TraceID string
	Extra   map[string]any
}

func (r OpenAITaskRetrieveRequest) toBody() map[string]any {
	body := map[string]any{"action": "retrieve"}
	if r.ID != "" {
		body["id"] = r.ID
	}
	if r.TraceID != "" {
		body["trace_id"] = r.TraceID
	}
	for k, v := range r.Extra {
		if _, exists := body[k]; !exists {
			body[k] = v
		}
	}
	return body
}

// OpenAITaskRetrieveBatchRequest is the input to openai.tasks.retrieve_batch.
type OpenAITaskRetrieveBatchRequest struct {
	IDs           []string
	TraceIDs      []string
	ApplicationID string
	UserID        string
	Type          string
	Offset        int
	Limit         int
	CreatedAtMin  int64
	CreatedAtMax  int64
	Extra         map[string]any
}

func (r OpenAITaskRetrieveBatchRequest) toBody() map[string]any {
	body := map[string]any{"action": "retrieve_batch"}
	if len(r.IDs) > 0 {
		body["ids"] = r.IDs
	}
	if len(r.TraceIDs) > 0 {
		body["trace_ids"] = r.TraceIDs
	}
	if r.ApplicationID != "" {
		body["application_id"] = r.ApplicationID
	}
	if r.UserID != "" {
		body["user_id"] = r.UserID
	}
	if r.Type != "" {
		body["type"] = r.Type
	}
	if r.Offset != 0 {
		body["offset"] = r.Offset
	}
	if r.Limit != 0 {
		body["limit"] = r.Limit
	}
	if r.CreatedAtMin != 0 {
		body["created_at_min"] = r.CreatedAtMin
	}
	if r.CreatedAtMax != 0 {
		body["created_at_max"] = r.CreatedAtMax
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

// Tasks returns the OpenAI tasks sub-namespace.
func (o *OpenAIResource) Tasks() *OpenAITasks { return &OpenAITasks{t: o.t} }

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

// OpenAITasks exposes “/openai/tasks“.
type OpenAITasks struct{ t *transport }

// Retrieve fetches one OpenAI task.
func (t *OpenAITasks) Retrieve(ctx context.Context, req OpenAITaskRetrieveRequest) (map[string]any, error) {
	return t.t.do(ctx, requestOpts{Method: "POST", Path: "/openai/tasks", Body: req.toBody()})
}

// RetrieveBatch fetches multiple OpenAI tasks.
func (t *OpenAITasks) RetrieveBatch(ctx context.Context, req OpenAITaskRetrieveBatchRequest) (map[string]any, error) {
	return t.t.do(ctx, requestOpts{Method: "POST", Path: "/openai/tasks", Body: req.toBody()})
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
