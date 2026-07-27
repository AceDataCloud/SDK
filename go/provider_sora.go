// Code generated from the platform OpenAPI spec. DO NOT EDIT.
// Regenerate with: python scripts/generate_providers.py

package acedatacloud

import "context"


// Sora is the sora provider client.
type Sora struct {
	t *transport
}

// SoraGenerateRequest is the input to sora.Generate.
type SoraGenerateRequest struct {
	// Text prompt for the video.
	Prompt string
	// The model to use for generation.
	Model string
	// Duration in seconds (4, 8, 10, 12, 15, 25).
	Duration int
	// Video orientation: landscape or portrait.
	Orientation string
	// Output video size.
	Size string
	// URL of a character reference image or video.
	CharacterURL string
	// Character reference start time (seconds).
	CharacterStart int
	// Character reference end time (seconds).
	CharacterEnd int
	// Array of image URLs to use as visual references.
	ImageURLs []string
	// API version to use: 1.0 or 2.0.
	Version string
	// Async submits without blocking; poll the returned handle. Defaults true.
	Async *bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r SoraGenerateRequest) toBody() map[string]any {
	body := map[string]any{
		"prompt": r.Prompt,
		"model":  r.Model,
	}
	if r.Duration != 0 {
		body["duration"] = r.Duration
	}
	if r.Orientation != "" {
		body["orientation"] = r.Orientation
	}
	if r.Size != "" {
		body["size"] = r.Size
	}
	if r.CharacterURL != "" {
		body["character_url"] = r.CharacterURL
	}
	if r.CharacterStart != 0 {
		body["character_start"] = r.CharacterStart
	}
	if r.CharacterEnd != 0 {
		body["character_end"] = r.CharacterEnd
	}
	if len(r.ImageURLs) > 0 {
		body["image_urls"] = r.ImageURLs
	}
	if r.Version != "" {
		body["version"] = r.Version
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

// Generate submits a Sora video generation request.
func (c *Sora) Generate(ctx context.Context, req SoraGenerateRequest) (*TaskHandle, error) {
	result, err := c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/sora/videos",
		Body:   req.toBody(),
	})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/sora/tasks", c.t, result), nil
}
