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
	// Text prompt describing the video to generate.
	Prompt string
	// The model used for generating videos.
	Model string
	// Duration of the video in seconds (4, 8, 10, 12, 15, or 25).
	Duration int
	// Orientation of the video: landscape or portrait.
	Orientation string
	// Size/resolution of the video.
	Size string
	// URL of a character reference video or image.
	CharacterURL string
	// Start time (in seconds) for the character reference clip.
	CharacterStart int
	// End time (in seconds) for the character reference clip.
	CharacterEnd int
	// URLs of images to use as reference frames for the video.
	ImageURLs []string
	// API version to use.
	Version string
	// Async submits without blocking; poll the returned handle. Defaults true.
	Async *bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r SoraGenerateRequest) toBody() map[string]any {
	body := map[string]any{}
	body["prompt"] = r.Prompt
	body["model"] = r.Model
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
