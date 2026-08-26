// Code generated from the platform OpenAPI spec. DO NOT EDIT.
// Regenerate with: python scripts/generate_providers.py

package acedatacloud

import "context"

// Wan is the wan provider client.
type Wan struct {
	t *transport
}

// WanGenerateRequest is the input to wan.Generate.
type WanGenerateRequest struct {
	// $t(wan_videos_model)
	Model string
	// $t(wan_videos_audio)
	Audio bool
	// $t(wan_videos_prompt_extend)
	PromptExtend bool
	// $t(wan_videos_action)
	Action string
	// $t(wan_videos_resolution)
	Resolution string
	// $t(wan_videos_shot_type)
	ShotType string
	// $t(wan_videos_duration)
	Duration float64
	// $t(wan_videos_prompt)
	Prompt string
	// $t(wan_videos_negative_prompt)
	NegativePrompt string
	// $t(wan_videos_size)
	Size string
	// $t(wan_videos_audio_url)
	AudioURL string
	// $t(wan_videos_reference_video_urls)
	ReferenceVideoURLs []string
	// $t(wan_videos_image_url)
	ImageURL string
	// $t(wan_videos_media)
	Media []map[string]any
	// $t(wan_videos_ratio)
	Ratio string
	// $t(wan_videos_seed)
	Seed int
	// $t(wan_videos_watermark)
	Watermark bool
	// Async submits without blocking; poll the returned handle.
	Async *bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r WanGenerateRequest) toBody() map[string]any {
	body := map[string]any{}
	body["model"] = r.Model
	body["audio"] = r.Audio
	body["prompt_extend"] = r.PromptExtend
	if r.Action != "" {
		body["action"] = r.Action
	} else {
		body["action"] = "text2video"
	}
	if r.Resolution != "" {
		body["resolution"] = r.Resolution
	}
	if r.ShotType != "" {
		body["shot_type"] = r.ShotType
	}
	if r.Duration != 0 {
		body["duration"] = r.Duration
	}
	if r.Prompt != "" {
		body["prompt"] = r.Prompt
	}
	if r.NegativePrompt != "" {
		body["negative_prompt"] = r.NegativePrompt
	}
	if r.Size != "" {
		body["size"] = r.Size
	}
	if r.AudioURL != "" {
		body["audio_url"] = r.AudioURL
	}
	if r.ReferenceVideoURLs != nil {
		body["reference_video_urls"] = r.ReferenceVideoURLs
	}
	if r.ImageURL != "" {
		body["image_url"] = r.ImageURL
	}
	if r.Media != nil {
		body["media"] = r.Media
	}
	if r.Ratio != "" {
		body["ratio"] = r.Ratio
	}
	if r.Seed != 0 {
		body["seed"] = r.Seed
	}
	body["watermark"] = r.Watermark
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

// Generate Generate videos based on prompt and image frames
func (c *Wan) Generate(ctx context.Context, req WanGenerateRequest) (*TaskHandle, error) {
	result, err := c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/wan/videos",
		Body:   req.toBody(),
	})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/wan/tasks", c.t, result), nil
}
