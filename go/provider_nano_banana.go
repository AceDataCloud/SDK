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
	// Image operation type. If it is `generate`, then generate an image based on the prompt; if it is `edit`, then e
	Action string
	// Prompts for generating images.
	Prompt string
	// The number of images to be generated or edited supports 1 to 4, with a default of 1. If some images fail to ge
	Count int
	// Models used for generating images. If not specified, the default is `nano-banana`. `nano-banana-2-lite` is an
	Model string
	// Link to the image that needs to be edited. It can be an accessible http or https URL, or a Base64 encoded imag
	ImageURLs []string
	// Resolution of generated images. Supported values are `1K`, `2K`, `4K`, with a default of `1K`. If this paramet
	Resolution string
	// Aspect ratio for generating images. Supported values are `1:1`, `3:2`, `2:3`, `16:9`, `9:16`, `4:3`, `3:4`. If
	AspectRatio string
	// Async submits without blocking; poll the returned handle.
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
	if r.Count != 0 {
		body["count"] = r.Count
	} else {
		body["count"] = 1
	}
	if r.Model != "" {
		body["model"] = r.Model
	}
	if r.ImageURLs != nil {
		body["image_urls"] = r.ImageURLs
	}
	if r.Resolution != "" {
		body["resolution"] = r.Resolution
	}
	if r.AspectRatio != "" {
		body["aspect_ratio"] = r.AspectRatio
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

// Generate Google Nano Banana image generation and editing API. Supports nano-banana, nano-banana-2, and nano-banana-pro for text-to-image generation and referen
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
