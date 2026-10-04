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
	// Model name, currently only supports the official value `MiniMax-H3`.
	Model string
	// Official MiniMax H3 V2 multimodal input array. Each request must include a non-empty `text`; supports images a
	Content []map[string]any
	// Video duration, required, integer between 4 and 15 seconds.
	Duration int
	// Video resolution, required, optional `768P` or `2K`.
	Resolution string
	// Video aspect ratio. Text-to-video is required and cannot be `adaptive`; image-to-video defaults to `adaptive`;
	Ratio string
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
	body["duration"] = r.Duration
	body["resolution"] = r.Resolution
	if r.Ratio != "" {
		body["ratio"] = r.Ratio
	}
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
