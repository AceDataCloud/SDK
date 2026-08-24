// Code generated from the platform OpenAPI spec. DO NOT EDIT.
// Regenerate with: python scripts/generate_providers.py

package acedatacloud

import "context"

// Drawai is the drawai provider client.
type Drawai struct {
	t *transport
}

// DrawaiGenerateRequest is the input to drawai.Generate.
type DrawaiGenerateRequest struct {
	// Headshots Generate Mode
	Mode string
	// Headshots Generate Template
	Template string
	// Headshots Generate Image Urls
	ImageURLs []string
	// Async submits without blocking; poll the returned handle. Defaults true.
	Async *bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r DrawaiGenerateRequest) toBody() map[string]any {
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

// Generate Generate
func (c *Drawai) Generate(ctx context.Context, req DrawaiGenerateRequest) (*TaskHandle, error) {
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
