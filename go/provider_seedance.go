// Code generated from the platform OpenAPI spec. DO NOT EDIT.
// Regenerate with: python scripts/generate_providers.py

package acedatacloud

import "context"


// Seedance is the seedance provider client.
type Seedance struct {
	t *transport
}

// SeedanceGenerateRequest is the input to seedance.Generate.
type SeedanceGenerateRequest struct {
	// Model ID for video generation
	Model string
	// Input content for video generation. Each entry must include one of `text`, `image_url`, `audio_url`, or `video
	Content []any
	// The random seed used for reproducible generation has a value range from -1 to 4294967295; -1 indicates randomn
	Seed int
	// Aspect ratio of the generated video
	Ratio string
	// The frame count for generating a video must meet 25 + 4n (such as 29, 33, 37... 289). Either duration or frame
	Frames int
	// The duration of the generated video, in seconds. Either duration or frames can be specified; if both are speci
	Duration int
	// Whether to add a watermark to the generated video.
	Watermark bool
	// Video resolution. The default value depends on the model used: most models default to 720p, while the lite mod
	Resolution string
	// Is the camera position fixed during the generation process?
	Camerafixed bool
	// Whether to generate audio from video. The `doubao-seedance-1-5-pro-251215` and `doubao-seedance-2-0` series mo
	GenerateAudio bool
	// Whether to return the last frame of the generated video.
	ReturnLastFrame bool
	// Task timeout threshold, unit in seconds
	ExecutionExpiresAfter int
	// Async submits without blocking; poll the returned handle. Defaults true.
	Async *bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r SeedanceGenerateRequest) toBody() map[string]any {
	body := map[string]any{}
	body["model"] = r.Model
	body["content"] = r.Content
	if r.Seed != 0 {
		body["seed"] = r.Seed
	}
	if r.Ratio != "" {
		body["ratio"] = r.Ratio
	} else {
		body["ratio"] = "16:9"
	}
	if r.Frames != 0 {
		body["frames"] = r.Frames
	}
	if r.Duration != 0 {
		body["duration"] = r.Duration
	}
	body["watermark"] = r.Watermark
	if r.Resolution != "" {
		body["resolution"] = r.Resolution
	}
	body["camerafixed"] = r.Camerafixed
	body["generate_audio"] = r.GenerateAudio
	body["return_last_frame"] = r.ReturnLastFrame
	if r.ExecutionExpiresAfter != 0 {
		body["execution_expires_after"] = r.ExecutionExpiresAfter
	} else {
		body["execution_expires_after"] = 172800
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

// Generate ByteDance Seedance video generation API. Supports doubao-seedance-1-0-pro-250528, doubao-seedance-1-0-pro-fast-251015, doubao-seedance-1-5-pro-251215,
func (c *Seedance) Generate(ctx context.Context, req SeedanceGenerateRequest) (*TaskHandle, error) {
	result, err := c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/seedance/videos",
		Body:   req.toBody(),
	})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/seedance/tasks", c.t, result), nil
}
