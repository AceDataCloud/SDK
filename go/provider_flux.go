// Code generated from the platform OpenAPI spec. DO NOT EDIT.
// Regenerate with: python scripts/generate_providers.py

package acedatacloud

import "context"

// Flux is the flux provider client.
type Flux struct {
	t *transport
}

// FluxGenerateRequest is the input to flux.Generate.
type FluxGenerateRequest struct {
	// Image size specifications.
	Size string
	// Types of operations for generating images. If it is `generate`, a new image will be created based on the promp
	Action string
	// Prompts for generating images.
	Prompt string
	// Number of generated images.
	Count float64
	// Model used for generating images.
	Model string
	// Link to the original image that needs editing.
	ImageURL string
	// Async submits without blocking; poll the returned handle. Defaults true.
	Async *bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r FluxGenerateRequest) toBody() map[string]any {
	body := map[string]any{}
	body["size"] = r.Size
	body["action"] = r.Action
	body["prompt"] = r.Prompt
	if r.Count != 0 {
		body["count"] = r.Count
	}
	if r.Model != "" {
		body["model"] = r.Model
	}
	if r.ImageURL != "" {
		body["image_url"] = r.ImageURL
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

// Generate Flux AI image generation API, generates 1 image per request.
func (c *Flux) Generate(ctx context.Context, req FluxGenerateRequest) (*TaskHandle, error) {
	result, err := c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/flux/images",
		Body:   req.toBody(),
	})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/flux/tasks", c.t, result), nil
}
