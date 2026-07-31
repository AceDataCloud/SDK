package acedatacloud

import "context"

// Sora is the sora provider client.
type Sora struct {
	t *transport
}

// SoraGenerateRequest is the input to sora.Generate.
type SoraGenerateRequest struct {
	// Video generation model.
	Model string
	// Text description of the video to generate.
	Prompt string
	// Duration in seconds.
	Duration int
	// Video orientation (landscape or portrait).
	Orientation string
	// Output size preset.
	Size string
	// URL of a character reference image.
	CharacterURL string
	// Start frame index for character compositing.
	CharacterStart int
	// End frame index for character compositing.
	CharacterEnd int
	// List of reference image URLs.
	ImageURLs []string
	// Model version.
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
	body["model"] = r.Model
	body["prompt"] = r.Prompt
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
	if r.ImageURLs != nil {
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
