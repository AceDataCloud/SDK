package acedatacloud

import "context"

// MessagesRequest is the input to chat.messages.create (native Anthropic shape).
type MessagesRequest struct {
	Model     string           `json:"model"`
	Messages  []map[string]any `json:"messages"`
	MaxTokens int              `json:"max_tokens"`
	Stream    bool             `json:"stream,omitempty"`
	System    string           `json:"system,omitempty"`
	Extra     map[string]any   `json:"-"`
}

func (r MessagesRequest) toBody() map[string]any {
	maxTok := r.MaxTokens
	if maxTok == 0 {
		maxTok = 4096
	}
	body := map[string]any{
		"model":      r.Model,
		"messages":   r.Messages,
		"max_tokens": maxTok,
	}
	if r.Stream {
		body["stream"] = true
	}
	if r.System != "" {
		body["system"] = r.System
	}
	for k, v := range r.Extra {
		if _, exists := body[k]; !exists {
			body[k] = v
		}
	}
	return body
}

// ChatResource groups native chat endpoints.
type ChatResource struct {
	t *transport
}

// Messages returns the messages sub-namespace.
func (c *ChatResource) Messages() *ChatMessages { return &ChatMessages{t: c.t} }

// ChatMessages exposes ``/v1/messages`` and ``/v1/messages/count_tokens``.
type ChatMessages struct{ t *transport }

// Create performs a blocking messages.create.
func (m *ChatMessages) Create(ctx context.Context, req MessagesRequest) (map[string]any, error) {
	body := req.toBody()
	delete(body, "stream")
	return m.t.do(ctx, requestOpts{Method: "POST", Path: "/v1/messages", Body: body})
}

// CreateStream performs a streaming messages.create.
func (m *ChatMessages) CreateStream(ctx context.Context, req MessagesRequest) (<-chan map[string]any, <-chan error) {
	req.Stream = true
	return streamDecode(m.t, "/v1/messages", req.toBody())
}

// CountTokens exposes ``/v1/messages/count_tokens``.
func (m *ChatMessages) CountTokens(ctx context.Context, req MessagesRequest) (map[string]any, error) {
	body := req.toBody()
	delete(body, "stream")
	delete(body, "max_tokens")
	return m.t.do(ctx, requestOpts{Method: "POST", Path: "/v1/messages/count_tokens", Body: body})
}
