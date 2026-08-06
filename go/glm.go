package acedatacloud

import "context"

// GlmModel identifies a GLM chat completion model.
type GlmModel string

const (
	GlmModel52     GlmModel = "glm-5.2"
	GlmModel5      GlmModel = "glm-5"
	GlmModel5Turbo GlmModel = "glm-5-turbo"
	GlmModel51     GlmModel = "glm-5.1"
	GlmModel47     GlmModel = "glm-4.7"
	GlmModel46     GlmModel = "glm-4.6"
	GlmModel3Turbo GlmModel = "glm-3-turbo"
)

// GlmCompletionRequest is the input to glm.chat.completions.create.
type GlmCompletionRequest struct {
	Model    GlmModel         `json:"model"`
	Messages []map[string]any `json:"messages"`
	Stream   bool             `json:"stream,omitempty"`
	Extra    map[string]any   `json:"-"`
}

func (r GlmCompletionRequest) toBody() map[string]any {
	body := map[string]any{
		"model":    r.Model,
		"messages": r.Messages,
	}
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

// GlmResource groups GLM endpoints.
type GlmResource struct{ t *transport }

// Chat returns the GLM chat sub-namespace.
func (g *GlmResource) Chat() *GlmChat { return &GlmChat{t: g.t} }

// GlmChat exposes GLM chat endpoints.
type GlmChat struct{ t *transport }

// Completions returns the GLM chat completions sub-namespace.
func (c *GlmChat) Completions() *GlmChatCompletions { return &GlmChatCompletions{t: c.t} }

// GlmChatCompletions exposes /glm/chat/completions.
type GlmChatCompletions struct{ t *transport }

// Create performs a blocking GLM chat completion.
func (c *GlmChatCompletions) Create(ctx context.Context, req GlmCompletionRequest) (map[string]any, error) {
	body := req.toBody()
	delete(body, "stream")
	return c.t.do(ctx, requestOpts{Method: "POST", Path: "/glm/chat/completions", Body: body})
}

// CreateStream performs a streaming GLM chat completion.
func (c *GlmChatCompletions) CreateStream(ctx context.Context, req GlmCompletionRequest) (<-chan map[string]any, <-chan error) {
	req.Stream = true
	return streamDecode(c.t, "/glm/chat/completions", req.toBody())
}
