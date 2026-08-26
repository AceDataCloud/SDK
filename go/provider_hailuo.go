// Code generated from the platform OpenAPI spec. DO NOT EDIT.
// Regenerate with: python scripts/generate_providers.py

package acedatacloud

import "context"

// Hailuo is the hailuo provider client.
type Hailuo struct {
	t *transport
}

// HailuoGenerateRequest is the input to hailuo.Generate.
type HailuoGenerateRequest struct {
	// The operation type for video generation. When set to `generate`, it will generate a video based on the prompt.
	Action string
	// The model used for generating videos has a default value of `minimax-t2v`.
	Model string
	// Prompts for generating videos.
	Prompt string
	// You can specify the URL of the first frame image to generate a video from the image.
	FirstImageURL string
	// Async submits without blocking; poll the returned handle.
	Async *bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r HailuoGenerateRequest) toBody() map[string]any {
	body := map[string]any{}
	body["action"] = r.Action
	if r.Model != "" {
		body["model"] = r.Model
	}
	if r.Prompt != "" {
		body["prompt"] = r.Prompt
	}
	if r.FirstImageURL != "" {
		body["first_image_url"] = r.FirstImageURL
	}
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

// Generate Minimax Hailuo AI video generation API. Supports minimax-t2v for text-to-video, minimax-i2v for image-to-video, and minimax-i2v-director for director
func (c *Hailuo) Generate(ctx context.Context, req HailuoGenerateRequest) (*TaskHandle, error) {
	result, err := c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/hailuo/videos",
		Body:   req.toBody(),
	})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/hailuo/tasks", c.t, result), nil
}
