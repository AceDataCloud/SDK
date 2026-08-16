package acedatacloud

import "context"

// AIChatRequest is the input to AIChat.Create.
type AIChatRequest struct {
	Model      string
	Question   string
	ID         string
	Preset     string
	Stateful   *bool
	References []string
}

func (r AIChatRequest) toBody() map[string]any {
	body := map[string]any{
		"model":    r.Model,
		"question": r.Question,
	}
	if r.ID != "" {
		body["id"] = r.ID
	}
	if r.Preset != "" {
		body["preset"] = r.Preset
	}
	if r.Stateful != nil {
		body["stateful"] = *r.Stateful
	}
	if r.References != nil {
		body["references"] = r.References
	}
	return body
}

// AIChat exposes the AI Chat conversations endpoint.
type AIChat struct {
	t *transport
}

// Create starts or continues an AI Chat conversation.
func (c *AIChat) Create(ctx context.Context, req AIChatRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/aichat/conversations",
		Body:   req.toBody(),
	})
}
