package acedatacloud

import "context"

// DrawAI is the drawai provider client (AI ID photo headshots at /headshots/*).
type DrawAI struct {
	t *transport
}

// DrawAIGenerateRequest is the input to drawai.Generate.
type DrawAIGenerateRequest struct {
	// Processing mode: fast or relax.
	Mode string
	// Portrait template name.
	Template string
	// List of reference image URLs.
	ImageURLs []string
	// Async submits without blocking; poll the returned handle. Defaults true.
	Async *bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r DrawAIGenerateRequest) toBody() map[string]any {
	body := map[string]any{}
	body["mode"] = r.Mode
	body["template"] = r.Template
	body["image_urls"] = r.ImageURLs
	body["async"] = true
	if r.Async != nil {
		body["async"] = *r.Async
	}
	if r.CallbackURL != "" {
		body["callback_url"] = r.CallbackURL
	}
	for k, v := range r.Extra {
		if _, exists := body[k]; !exists {
			body[k] = v
		}
	}
	return body
}

// Generate submits an AI ID photo generation request.
func (c *DrawAI) Generate(ctx context.Context, req DrawAIGenerateRequest) (*TaskHandle, error) {
	result, err := c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/headshots/generate",
		Body:   req.toBody(),
	})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/headshots/tasks", c.t, result), nil
}
