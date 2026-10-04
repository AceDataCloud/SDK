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
	// Public URL for audio (mp3/wav). The character will lip-sync to it, and it is recommended that the duration be
	AudioURL string
	// Public URL of portrait images. Clear frontal face effects are best.
	ImageURL string
	// The model being used is OmniHuman 1.5.
	Model string
	// Optional text prompts for guiding expressions, emotions, stability, and style.
	Prompt string
	// Optional subject mask URL (from object detection) to specify and drive a particular person in a multi-person i
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
	body["audio_url"] = r.AudioURL
	body["image_url"] = r.ImageURL
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

// Generate Audio-driven talking-photo digital human video generation (OmniHuman 1.5)
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
