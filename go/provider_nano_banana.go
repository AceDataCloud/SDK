// Code generated from the platform OpenAPI spec. DO NOT EDIT.
// Regenerate with: python scripts/generate_providers.py

package acedatacloud

import "context"

// NanoBanana is the nano-banana provider client.
type NanoBanana struct {
	t *transport
}

// NanoBananaGenerateRequest is the input to nano_banana.Generate.
type NanoBananaGenerateRequest struct {
	// Nano Banana Images Action
	Action string
	// Nano Banana Images Prompt
	Prompt string
	// Nano Banana Images Model
	Model string
	// Nano Banana Images Image Urls
	ImageURLs []string
	// Nano Banana Images Count
	Count int
	// Nano Banana Images Aspect Ratio
	AspectRatio string
	// Nano Banana Images Resolution
	Resolution string
	// Async submits without blocking; poll the returned handle. Defaults true.
	Async *bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r NanoBananaGenerateRequest) toBody() map[string]any {
	body := map[string]any{}
	body["action"] = r.Action
	body["prompt"] = r.Prompt
	if r.Model != "" {
		body["model"] = r.Model
	}
	if r.ImageURLs != nil {
		body["image_urls"] = r.ImageURLs
	}
	if r.Count != 0 {
		body["count"] = r.Count
	} else {
		body["count"] = 1
	}
	if r.AspectRatio != "" {
		body["aspect_ratio"] = r.AspectRatio
	}
	if r.Resolution != "" {
		body["resolution"] = r.Resolution
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

// Generate Nano Banana Images
func (c *NanoBanana) Generate(ctx context.Context, req NanoBananaGenerateRequest) (*TaskHandle, error) {
	result, err := c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/nano-banana/images",
		Body:   req.toBody(),
	})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/nano-banana/tasks", c.t, result), nil
}
