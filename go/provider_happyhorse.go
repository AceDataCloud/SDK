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
	// Random seed, range 0–2147483647.
	Seed int
	// HappyHorse model name. Different actions only support the corresponding model family.
	Model string
	// Output video aspect ratio. Text-to-video and reference image-to-video support this parameter; the first frame
	Ratio string
	// Operation types. `generate` is for generating video from text, `image_to_video` is for generating video from t
	Action string
	// Text prompt words. Text-to-video, reference image to video, and video editing scenarios are required.
	Prompt string
	// Output video duration (seconds), value range 3–15. The output duration of `video_edit` is determined by the in
	Duration int
	// The input image URL for the first frame of the video. Only used by `image_to_video`.
	ImageURL string
	// URL of the video to be edited. For `video_edit` use only.
	VideoURL string
	// Whether to add the HappyHorse watermark. Default is off.
	Watermark bool
	// Reference image URL array. `reference_to_video` supports 1–9 images, `video_edit` supports 0–5 images.
	ImageURLs []string
	// Output video resolution, optional 720P or 1080P.
	Resolution string
	// Audio strategy for video editing. `auto` is determined by the model, `origin` retains the original audio of th
	AudioSetting string
	// Async submits without blocking; poll the returned handle. Defaults true.
	Async *bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r HappyhorseGenerateRequest) toBody() map[string]any {
	body := map[string]any{}
	if r.Seed != 0 {
		body["seed"] = r.Seed
	}
	if r.Model != "" {
		body["model"] = r.Model
	} else {
		body["model"] = "happyhorse-1.1-t2v"
	}
	if r.Ratio != "" {
		body["ratio"] = r.Ratio
	} else {
		body["ratio"] = "16:9"
	}
	if r.Action != "" {
		body["action"] = r.Action
	} else {
		body["action"] = "generate"
	}
	if r.Prompt != "" {
		body["prompt"] = r.Prompt
	} else {
		body["prompt"] = "A cinematic white horse lifts its head, the mane moves gently in the sunrise wind, slow camera push in, warm film lighting"
	}
	if r.Duration != 0 {
		body["duration"] = r.Duration
	} else {
		body["duration"] = 5
	}
	if r.ImageURL != "" {
		body["image_url"] = r.ImageURL
	} else {
		body["image_url"] = "https://cdn.acedata.cloud/b1c82e4937.png"
	}
	if r.VideoURL != "" {
		body["video_url"] = r.VideoURL
	} else {
		body["video_url"] = "https://platform2.cdn.acedata.cloud/happyhorse/27837f92-d1c1-4db4-ad9a-4e6e81d9f6c1.mp4"
	}
	body["watermark"] = r.Watermark
	if r.ImageURLs != nil {
		body["image_urls"] = r.ImageURLs
	}
	if r.Resolution != "" {
		body["resolution"] = r.Resolution
	} else {
		body["resolution"] = "1080P"
	}
	if r.AudioSetting != "" {
		body["audio_setting"] = r.AudioSetting
	} else {
		body["audio_setting"] = "auto"
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

// Generate Call /happyhorse/videos.
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
