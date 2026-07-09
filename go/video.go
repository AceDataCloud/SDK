package acedatacloud

import "context"

// VideoGenerateRequest is the input to videos.generate.
type VideoGenerateRequest struct {
	// Prompt is the required text prompt.
	Prompt string
	// Provider selects the backend: "sora", "luma", "veo", "kling",
	// "hailuo", "seedance", "wan", "pika", "pixverse", "happyhorse".
	Provider string
	// Model is optional — provider-specific model identifier.
	Model string
	// ImageURL is optional reference image for image-to-video.
	ImageURL string
	// CallbackURL optionally receives the task completion webhook.
	CallbackURL string
	// Async, when true, returns a task_id without requiring a CallbackURL.
	Async bool
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r VideoGenerateRequest) toBody() map[string]any {
	body := map[string]any{"prompt": r.Prompt}
	if r.Model != "" {
		body["model"] = r.Model
	}
	if r.ImageURL != "" {
		body["image_url"] = r.ImageURL
	}
	if r.CallbackURL != "" {
		body["callback_url"] = r.CallbackURL
	}
	if r.Async {
		body["async"] = true
	}
	for k, v := range r.Extra {
		if _, exists := body[k]; !exists {
			body[k] = v
		}
	}
	return body
}

// VideoResource groups video-generation endpoints.
type VideoResource struct{ t *transport }

// Generate enqueues a video-generation task. It returns a TaskHandle for
// polling when the server responds asynchronously, or the direct result
// map when the server produced the video synchronously.
func (v *VideoResource) Generate(ctx context.Context, req VideoGenerateRequest) (*TaskHandle, map[string]any, error) {
	provider := req.Provider
	if provider == "" {
		provider = "sora"
	}
	result, err := v.t.do(ctx, requestOpts{Method: "POST", Path: "/" + provider + "/videos", Body: req.toBody()})
	if err != nil {
		return nil, nil, err
	}
	taskID, _ := result["task_id"].(string)
	if taskID == "" {
		return nil, result, nil
	}
	handle := &TaskHandle{ID: taskID, pollEndpoint: endpointFor(provider), transport: v.t}
	return handle, result, nil
}
