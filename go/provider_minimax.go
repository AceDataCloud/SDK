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
	// Minimax Videos Prompt
	Prompt string
	// Minimax Videos Model
	Model string
	// Minimax Videos Image Urls
	ImageURLs []string
	// Minimax Videos Audio Urls
	AudioURLs []string
	// Minimax Videos Resolution
	Resolution string
	// Minimax Videos Ratio
	Ratio string
	// Minimax Videos Duration
	Duration int
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
	body["prompt"] = r.Prompt
	if r.Model != "" {
		body["model"] = r.Model
	} else {
		body["model"] = "minimax-h3"
	}
	if r.ImageURLs != nil {
		body["image_urls"] = r.ImageURLs
	}
	if r.AudioURLs != nil {
		body["audio_urls"] = r.AudioURLs
	}
	if r.Resolution != "" {
		body["resolution"] = r.Resolution
	} else {
		body["resolution"] = "2K"
	}
	if r.Ratio != "" {
		body["ratio"] = r.Ratio
	} else {
		body["ratio"] = "16:9"
	}
	if r.Duration != 0 {
		body["duration"] = r.Duration
	} else {
		body["duration"] = 4
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

// Generate Minimax Videos
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
