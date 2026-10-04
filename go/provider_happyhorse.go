// Code generated from the platform OpenAPI spec. DO NOT EDIT.
// Regenerate with: python scripts/generate_providers.py

package acedatacloud

import "context"

// Happyhorse is the happyhorse provider client.
type Happyhorse struct {
	t *transport
}

// HappyhorseGenerateRequest is the input to happyhorse.Generate.
type HappyhorseGenerateRequest struct {
	// Happyhorse Videos Action
	Action string
	// Happyhorse Videos Model
	Model string
	// Happyhorse Videos Prompt
	Prompt string
	// Happyhorse Videos Image Url
	ImageURL string
	// Happyhorse Videos Image Urls
	ImageURLs []string
	// Happyhorse Videos Video Url
	VideoURL string
	// Happyhorse Videos Resolution
	Resolution string
	// Happyhorse Videos Ratio
	Ratio string
	// Happyhorse Videos Duration
	Duration int
	// Happyhorse Videos Watermark
	Watermark bool
	// Happyhorse Videos Audio Setting
	AudioSetting string
	// Happyhorse Videos Seed
	Seed int
	// Async submits without blocking; poll the returned handle. Defaults true.
	Async *bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r HappyhorseGenerateRequest) toBody() map[string]any {
	body := map[string]any{}
	if r.Action != "" {
		body["action"] = r.Action
	} else {
		body["action"] = "generate"
	}
	if r.Model != "" {
		body["model"] = r.Model
	} else {
		body["model"] = "happyhorse-1.1-t2v"
	}
	if r.Prompt != "" {
		body["prompt"] = r.Prompt
	}
	if r.ImageURL != "" {
		body["image_url"] = r.ImageURL
	}
	if r.ImageURLs != nil {
		body["image_urls"] = r.ImageURLs
	}
	if r.VideoURL != "" {
		body["video_url"] = r.VideoURL
	}
	if r.Resolution != "" {
		body["resolution"] = r.Resolution
	} else {
		body["resolution"] = "1080P"
	}
	if r.Ratio != "" {
		body["ratio"] = r.Ratio
	} else {
		body["ratio"] = "16:9"
	}
	if r.Duration != 0 {
		body["duration"] = r.Duration
	} else {
		body["duration"] = 5
	}
	body["watermark"] = r.Watermark
	if r.AudioSetting != "" {
		body["audio_setting"] = r.AudioSetting
	} else {
		body["audio_setting"] = "auto"
	}
	if r.Seed != 0 {
		body["seed"] = r.Seed
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

// Generate Happyhorse Videos
func (c *Happyhorse) Generate(ctx context.Context, req HappyhorseGenerateRequest) (*TaskHandle, error) {
	result, err := c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/happyhorse/videos",
		Body:   req.toBody(),
	})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/happyhorse/tasks", c.t, result), nil
}
