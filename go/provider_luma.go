// Code generated from the platform OpenAPI spec. DO NOT EDIT.
// Regenerate with: python scripts/generate_providers.py

package acedatacloud

import "context"


// Luma is the luma provider client.
type Luma struct {
	t *transport
}

// LumaGenerateRequest is the input to luma.Generate.
type LumaGenerateRequest struct {
	// Whether to enable loop playback for the generated video.
	Loop bool
	// Operation type. Use `generate` when creating a video for the first time, and use `extend` when continuing an e
	Action string
	// Text prompts for generating videos.
	Prompt string
	// The timeout for the API return data (unit: seconds).
	Timeout float64
	// The unique identifier of the generated video used for the continuation operation (`extend`). If both are speci
	VideoID string
	// The original video URL used for the extend operation (`extend`). If `video_id` is specified at the same time, 
	VideoURL string
	// Whether to enable automatic optimization enhancement for the input prompt text, suitable for use when unsure h
	Enhancement bool
	// Generate the aspect ratio of the video, for example `16:9`.
	AspectRatio string
	// The URL of the ending frame image, which will be used as the last frame of the generated video.
	EndImageURL string
	// The URL of the starting frame image, which will be used as the first frame of the generated video.
	StartImageURL string
	// Async submits without blocking; poll the returned handle. Defaults true.
	Async *bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r LumaGenerateRequest) toBody() map[string]any {
	body := map[string]any{}
	body["loop"] = r.Loop
	if r.Action != "" {
		body["action"] = r.Action
	} else {
		body["action"] = "generate"
	}
	if r.Prompt != "" {
		body["prompt"] = r.Prompt
	} else {
		body["prompt"] = "Astronauts shuttle from space to volcano"
	}
	if r.Timeout != 0 {
		body["timeout"] = r.Timeout
	} else {
		body["timeout"] = 300
	}
	if r.VideoID != "" {
		body["video_id"] = r.VideoID
	}
	if r.VideoURL != "" {
		body["video_url"] = r.VideoURL
	}
	body["enhancement"] = r.Enhancement
	if r.AspectRatio != "" {
		body["aspect_ratio"] = r.AspectRatio
	}
	if r.EndImageURL != "" {
		body["end_image_url"] = r.EndImageURL
	} else {
		body["end_image_url"] = "https://cdn.acedata.cloud/0iad3k.png"
	}
	if r.StartImageURL != "" {
		body["start_image_url"] = r.StartImageURL
	} else {
		body["start_image_url"] = "https://cdn.acedata.cloud/r9vsv9.png"
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

// Generate Generate videos based on prompt and image frames
func (c *Luma) Generate(ctx context.Context, req LumaGenerateRequest) (*TaskHandle, error) {
	result, err := c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/luma/videos",
		Body:   req.toBody(),
	})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/luma/tasks", c.t, result), nil
}
