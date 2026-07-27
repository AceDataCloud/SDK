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
	// Models for generating videos include optional values such as `wan2.6-t2v` (text-to-video), `wan2.6-i2v` (image
	Model string
	// Operation types. `text2video` indicates text-to-video, and `image2video` indicates image-to-video.
	Action string
	// Prompts for generating videos.
	Prompt string
	// Video size specifications.
	Size string
	// Specify whether the generated video contains sound.
	Audio bool
	// Specify the duration of the video to be generated (in seconds), with optional values of `5`, `10`, or `15`.
	Duration float64
	// The URL of the audio file, the model will generate the corresponding video based on that audio.
	AudioURL string
	// The URL of the starting frame image, which will serve as the first frame of the generated video.
	ImageURL string
	// Specify the type of shots for the video, that is, whether the video consists of a single continuous shot (`sin
	ShotType string
	// Specify the resolution level for generating the video, used to adjust the video clarity (total pixel count). T
	Resolution string
	// Whether to enable intelligent rewriting of prompts. Once enabled, a large model will be used to intelligently 
	PromptExtend bool
	// Reverse prompt words, used to describe content that is not desired to appear in the video footage, can be used
	NegativePrompt string
	// An array of URLs for reference video files, used to extract the character images (and vocal tones, if any) fro
	ReferenceVideoURLs []string
	// Async submits without blocking; poll the returned handle. Defaults true.
	Async *bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r WanGenerateRequest) toBody() map[string]any {
	body := map[string]any{}
	body["model"] = r.Model
	body["action"] = r.Action
	body["prompt"] = r.Prompt
	if r.Size != "" {
		body["size"] = r.Size
	}
	body["audio"] = r.Audio
	if r.Duration != 0 {
		body["duration"] = r.Duration
	}
	if r.AudioURL != "" {
		body["audio_url"] = r.AudioURL
	}
	if r.ImageURL != "" {
		body["image_url"] = r.ImageURL
	} else {
		body["image_url"] = "https://cdn.acedata.cloud/r9vsv9.png"
	}
	if r.ShotType != "" {
		body["shot_type"] = r.ShotType
	}
	if r.Resolution != "" {
		body["resolution"] = r.Resolution
	}
	body["prompt_extend"] = r.PromptExtend
	if r.NegativePrompt != "" {
		body["negative_prompt"] = r.NegativePrompt
	} else {
		body["negative_prompt"] = "Astronauts shuttle from space to volcano"
	}
	if r.ReferenceVideoURLs != nil {
		body["reference_video_urls"] = r.ReferenceVideoURLs
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
