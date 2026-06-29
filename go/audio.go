package acedatacloud

import "context"

// AudioGenerateRequest is the input to audio.generate.
type AudioGenerateRequest struct {
	// Prompt is the required text prompt (or text-to-speech text for fish).
	Prompt string
	// Provider selects the backend: "suno", "producer", "fish".
	Provider string
	// Model is optional — provider-specific model identifier.
	Model string
	// Tags is optional style tags (suno/producer).
	Tags string
	// CallbackURL optionally receives the task completion webhook.
	CallbackURL string
	// Async, when true, returns a task_id without requiring a CallbackURL.
	Async bool
	// Extra fields merged into the request body.
	Extra map[string]any
}

// AudioResource groups audio/music generation endpoints.
type AudioResource struct{ t *transport }

// Generate enqueues an audio task. It returns a TaskHandle for polling
// when the server responds asynchronously, or the direct result map when
// the server produced the audio synchronously.
func (a *AudioResource) Generate(ctx context.Context, req AudioGenerateRequest) (*TaskHandle, map[string]any, error) {
	provider := req.Provider
	if provider == "" {
		provider = "suno"
	}
	var (
		body     map[string]any
		endpoint string
		headers  map[string]string
	)
	if provider == "fish" {
		body = map[string]any{"text": req.Prompt}
		endpoint = "/fish/tts"
		// Fish selects the voice model via a header, not the body.
		if req.Model != "" {
			headers = map[string]string{"model": req.Model}
		}
	} else {
		body = map[string]any{"prompt": req.Prompt}
		if req.Tags != "" {
			body["tags"] = req.Tags
		}
		if req.Model != "" {
			body["model"] = req.Model
		}
		endpoint = "/" + provider + "/audios"
	}
	if req.CallbackURL != "" {
		body["callback_url"] = req.CallbackURL
	}
	if req.Async {
		body["async"] = true
	}
	for k, v := range req.Extra {
		if _, exists := body[k]; !exists {
			body[k] = v
		}
	}
	result, err := a.t.do(ctx, requestOpts{Method: "POST", Path: endpoint, Body: body, ExtraHeaders: headers})
	if err != nil {
		return nil, nil, err
	}
	taskID, _ := result["task_id"].(string)
	if taskID == "" {
		return nil, result, nil
	}
	handle := &TaskHandle{ID: taskID, pollEndpoint: endpointFor(provider), transport: a.t}
	return handle, result, nil
}
