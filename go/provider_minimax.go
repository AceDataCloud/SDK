// Code generated from the platform OpenAPI spec. DO NOT EDIT.
// Regenerate with: python scripts/generate_providers.py

package acedatacloud

import "context"

// Minimax is the minimax provider client.
type Minimax struct {
	t *transport
}

// MinimaxGenerateRequest is the input to minimax.Generate.
type MinimaxGenerateRequest struct {
	// Minimax Videos Model
	Model string
	// Minimax Videos Content
	Content []any
	// Minimax Videos Resolution
	Resolution string
	// Minimax Videos Duration
	Duration int
	// Minimax Videos Ratio
	Ratio string
	// Minimax Videos Aigc Watermark
	AigcWatermark bool
	// Async submits without blocking; poll the returned handle. Defaults true.
	Async *bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r MinimaxGenerateRequest) toBody() map[string]any {
	body := map[string]any{}
	body["model"] = r.Model
	body["content"] = r.Content
	body["resolution"] = r.Resolution
	body["duration"] = r.Duration
	if r.Ratio != "" {
		body["ratio"] = r.Ratio
	}
	body["aigc_watermark"] = r.AigcWatermark
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

// Generate Call /minimax/videos.
func (c *Minimax) Generate(ctx context.Context, req MinimaxGenerateRequest) (*TaskHandle, error) {
	result, err := c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/minimax/videos",
		Body:   req.toBody(),
	})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/minimax/tasks", c.t, result), nil
}
