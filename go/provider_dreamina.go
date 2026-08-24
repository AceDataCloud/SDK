// Code generated from the platform OpenAPI spec. DO NOT EDIT.
// Regenerate with: python scripts/generate_providers.py

package acedatacloud

import "context"

// Dreamina is the dreamina provider client.
type Dreamina struct {
	t *transport
}

// DreaminaGenerateRequest is the input to dreamina.Generate.
type DreaminaGenerateRequest struct {
	// Dreamina Videos Image Url
	ImageURL string
	// Dreamina Videos Audio Url
	AudioURL string
	// Dreamina Videos Model
	Model string
	// Dreamina Videos Prompt
	Prompt string
	// Dreamina Videos Mask Url
	MaskURL []string
	// Async submits without blocking; poll the returned handle. Defaults true.
	Async *bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r DreaminaGenerateRequest) toBody() map[string]any {
	body := map[string]any{}
	body["image_url"] = r.ImageURL
	body["audio_url"] = r.AudioURL
	if r.Model != "" {
		body["model"] = r.Model
	} else {
		body["model"] = "omnihuman-1.5"
	}
	if r.Prompt != "" {
		body["prompt"] = r.Prompt
	}
	if r.MaskURL != nil {
		body["mask_url"] = r.MaskURL
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

// Generate Dreamina Videos
func (c *Dreamina) Generate(ctx context.Context, req DreaminaGenerateRequest) (*TaskHandle, error) {
	result, err := c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/dreamina/videos",
		Body:   req.toBody(),
	})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/dreamina/tasks", c.t, result), nil
}
