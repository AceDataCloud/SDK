package acedatacloud

import "context"

// GLMResource exposes the GLM chat completions endpoint.
type GLMResource struct {
	t *transport
}

// GLMChat returns the chat sub-namespace.
func (g *GLMResource) Chat() *GLMChat { return &GLMChat{t: g.t} }

// GLMChat exposes GLM chat endpoints.
type GLMChat struct{ t *transport }

// Completions returns the completions sub-namespace.
func (g *GLMChat) Completions() *GLMChatCompletions { return &GLMChatCompletions{t: g.t} }

// GLMChatCompletions exposes glm.chat.completions.create.
type GLMChatCompletions struct{ t *transport }

// GLMChatCompletionRequest is the input to GLM chat.completions.create.
type GLMChatCompletionRequest struct {
	Model    string
	Messages []map[string]any
	Stream   bool
	Extra    map[string]any
}

func (r GLMChatCompletionRequest) toBody() map[string]any {
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

// Create performs a blocking GLM chat completion.
func (c *GLMChatCompletions) Create(ctx context.Context, req GLMChatCompletionRequest) (map[string]any, error) {
	body := req.toBody()
	delete(body, "stream")
	return c.t.do(ctx, requestOpts{Method: "POST", Path: "/glm/chat/completions", Body: body})
}

// CreateStream streams a GLM chat completion.
func (c *GLMChatCompletions) CreateStream(ctx context.Context, req GLMChatCompletionRequest) (<-chan map[string]any, <-chan error) {
	req.Stream = true
	return streamDecode(c.t, "/glm/chat/completions", req.toBody())
}
