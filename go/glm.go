package acedatacloud

import "context"

// GLMModel identifies a GLM chat-completions model.
type GLMModel string

const (
	GLMModel52     GLMModel = "glm-5.2"
	GLMModel5      GLMModel = "glm-5"
	GLMModel5Turbo GLMModel = "glm-5-turbo"
	GLMModel51     GLMModel = "glm-5.1"
	GLMModel47     GLMModel = "glm-4.7"
	GLMModel46     GLMModel = "glm-4.6"
	GLMModel3Turbo GLMModel = "glm-3-turbo"
)

// GLMChatCompletionRequest is the input to GLM chat.completions.create.
type GLMChatCompletionRequest struct {
	Model       GLMModel         `json:"model"`
	Messages    []map[string]any `json:"messages"`
	Stream      bool             `json:"stream,omitempty"`
	MaxTokens   int              `json:"max_tokens,omitempty"`
	Temperature *float64         `json:"temperature,omitempty"`
	TopP        *float64         `json:"top_p,omitempty"`
	Extra       map[string]any   `json:"-"`
}

func (r GLMChatCompletionRequest) toBody() map[string]any {
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

// GLMResource groups the GLM-compatible endpoints.
type GLMResource struct {
	t *transport
}

// Chat returns the GLM chat sub-namespace.
func (g *GLMResource) Chat() *GLMChat { return &GLMChat{t: g.t} }

// GLMChat exposes GLM chat completions.
type GLMChat struct{ t *transport }

// Completions returns the completions sub-namespace.
func (c *GLMChat) Completions() *GLMChatCompletions { return &GLMChatCompletions{t: c.t} }

// GLMChatCompletions exposes GLM chat.completions.create.
type GLMChatCompletions struct{ t *transport }

// Create performs a blocking GLM chat completion.
func (c *GLMChatCompletions) Create(ctx context.Context, req GLMChatCompletionRequest) (map[string]any, error) {
	body := req.toBody()
	delete(body, "stream")
	return c.t.do(ctx, requestOpts{Method: "POST", Path: "/glm/chat/completions", Body: body})
}

// CreateStream performs a streaming GLM chat completion.
func (c *GLMChatCompletions) CreateStream(ctx context.Context, req GLMChatCompletionRequest) (<-chan map[string]any, <-chan error) {
	req.Stream = true
	return streamDecode(c.t, "/glm/chat/completions", req.toBody())
}
