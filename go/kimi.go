package acedatacloud

import "context"

// KimiModel is a Kimi chat completions model identifier.
type KimiModel string

const (
	KimiModelK3              KimiModel = "kimi-k3"
	KimiModelK26             KimiModel = "kimi-k2.6"
	KimiModelK2ThinkingTurbo KimiModel = "kimi-k2-thinking-turbo"
	KimiModelK25             KimiModel = "kimi-k2.5"
	KimiModelK2Thinking      KimiModel = "kimi-k2-thinking"
)

// KimiChatCompletionRequest is the input to kimi.chat.completions.create.
type KimiChatCompletionRequest struct {
	Model       KimiModel        `json:"model"`
	Messages    []map[string]any `json:"messages"`
	Stream      bool             `json:"stream,omitempty"`
	MaxTokens   int              `json:"max_tokens,omitempty"`
	Temperature *float64         `json:"temperature,omitempty"`
	TopP        *float64         `json:"top_p,omitempty"`
	Extra       map[string]any   `json:"-"`
}

func (r KimiChatCompletionRequest) toBody() map[string]any {
	body := map[string]any{
		"model":    string(r.Model),
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

// KimiResource groups the Kimi endpoints.
type KimiResource struct {
	t *transport
}

// Chat returns the chat sub-namespace.
func (k *KimiResource) Chat() *KimiChat { return &KimiChat{t: k.t} }

// KimiChat exposes Kimi chat endpoints.
type KimiChat struct{ t *transport }

// Completions returns the completions sub-namespace.
func (c *KimiChat) Completions() *KimiChatCompletions { return &KimiChatCompletions{t: c.t} }

// KimiChatCompletions exposes kimi.chat.completions.create.
type KimiChatCompletions struct{ t *transport }

// Create performs a blocking (non-streaming) Kimi chat completion.
func (c *KimiChatCompletions) Create(ctx context.Context, req KimiChatCompletionRequest) (map[string]any, error) {
	body := req.toBody()
	delete(body, "stream")
	return c.t.do(ctx, requestOpts{Method: "POST", Path: "/kimi/chat/completions", Body: body})
}

// CreateStream performs a streaming Kimi chat completion.
func (c *KimiChatCompletions) CreateStream(ctx context.Context, req KimiChatCompletionRequest) (<-chan map[string]any, <-chan error) {
	req.Stream = true
	return streamDecode(c.t, "/kimi/chat/completions", req.toBody())
}
