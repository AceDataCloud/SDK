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
	// Seedance Videos Model
	Model string
	// Seedance Videos
	Content []map[string]any
	// Seedance Videos Resolution
	Resolution string
	// Seedance Videos Ratio
	Ratio string
	// Seedance Videos Duration
	Duration int
	// Seedance Videos Frames
	Frames int
	// Seedance Videos Seed
	Seed int
	// Seedance Videos Camerafixed
	Camerafixed bool
	// Seedance Videos Watermark
	Watermark bool
	// Seedance Videos Generate Audio
	GenerateAudio bool
	// Seedance Videos Return Last Frame
	ReturnLastFrame bool
	// Seedance Videos Execution Expires After
	ExecutionExpiresAfter int
	// Seedance Videos Omni Reference Task Type
	OmniReferenceTaskType string
	// Seedance Videos Output Format
	OutputFormat string
	// Seedance Videos Tools
	Tools []map[string]any
	// Seedance Videos Priority
	Priority int
	// Seedance Videos Safety Identifier
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

// Generate Seedance Videos
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
