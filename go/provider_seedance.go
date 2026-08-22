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
	// $t(seedance_videos_model)
	Model string
	// $t(seedance_videos)
	Content []map[string]any
	// $t(seedance_videos_resolution)
	Resolution string
	// $t(seedance_videos_ratio)
	Ratio string
	// $t(seedance_videos_duration)
	Duration int
	// $t(seedance_videos_frames)
	Frames int
	// $t(seedance_videos_seed)
	Seed int
	// $t(seedance_videos_camerafixed)
	Camerafixed bool
	// $t(seedance_videos_watermark)
	Watermark bool
	// $t(seedance_videos_generate_audio)
	GenerateAudio bool
	// $t(seedance_videos_return_last_frame)
	ReturnLastFrame bool
	// $t(seedance_videos_execution_expires_after)
	ExecutionExpiresAfter int
	// $t(seedance_videos_omni_reference_task_type)
	OmniReferenceTaskType string
	// $t(seedance_videos_output_format)
	OutputFormat string
	// $t(seedance_videos_tools)
	Tools []map[string]any
	// $t(seedance_videos_priority)
	Priority int
	// $t(seedance_videos_safety_identifier)
	SafetyIdentifier string
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
	if r.Resolution != "" {
		body["resolution"] = r.Resolution
	}
	if r.Ratio != "" {
		body["ratio"] = r.Ratio
	} else {
		body["ratio"] = "16:9"
	}
	if r.Duration != 0 {
		body["duration"] = r.Duration
	}
	if r.Frames != 0 {
		body["frames"] = r.Frames
	}
	if r.Seed != 0 {
		body["seed"] = r.Seed
	}
	body["camerafixed"] = r.Camerafixed
	body["watermark"] = r.Watermark
	body["generate_audio"] = r.GenerateAudio
	body["return_last_frame"] = r.ReturnLastFrame
	if r.ExecutionExpiresAfter != 0 {
		body["execution_expires_after"] = r.ExecutionExpiresAfter
	} else {
		body["execution_expires_after"] = 172800
	}
	if r.OmniReferenceTaskType != "" {
		body["omni_reference_task_type"] = r.OmniReferenceTaskType
	}
	if r.OutputFormat != "" {
		body["output_format"] = r.OutputFormat
	}
	if r.Tools != nil {
		body["tools"] = r.Tools
	}
	if r.Priority != 0 {
		body["priority"] = r.Priority
	} else {
		body["priority"] = 0
	}
	if r.SafetyIdentifier != "" {
		body["safety_identifier"] = r.SafetyIdentifier
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

// Generate Call /seedance/videos.
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
