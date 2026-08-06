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

// GlmResource groups GLM endpoints.
type GlmResource struct {
	t *transport
}

// Chat returns the chat sub-namespace.
func (g *GlmResource) Chat() *GlmChat { return &GlmChat{t: g.t} }

// GlmChat exposes GLM chat endpoints.
type GlmChat struct{ t *transport }

// Completions returns the completions sub-namespace.
func (g *GlmChat) Completions() *GlmChatCompletions { return &GlmChatCompletions{t: g.t} }

// GlmChatCompletions exposes glm.chat.completions.create.
type GlmChatCompletions struct{ t *transport }

// Create performs a blocking GLM chat completion.
func (g *GlmChatCompletions) Create(ctx context.Context, req ChatCompletionRequest) (map[string]any, error) {
	body := req.toBody()
	delete(body, "stream")
	return g.t.do(ctx, requestOpts{Method: "POST", Path: "/glm/chat/completions", Body: body})
}

// CreateStream performs a streaming GLM chat completion.
func (g *GlmChatCompletions) CreateStream(ctx context.Context, req ChatCompletionRequest) (<-chan map[string]any, <-chan error) {
	req.Stream = true
	return streamDecode(g.t, "/glm/chat/completions", req.toBody())
}
