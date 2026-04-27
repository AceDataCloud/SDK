package acedatacloud

import "context"

// ImageGenerateRequest is the input to images.generate.
type ImageGenerateRequest struct {
	// Prompt is the required text prompt.
	Prompt string
	// Provider selects the backend. Common values: "nano-banana",
	// "midjourney", "flux", "seedream".
	Provider string
	// Model is optional — provider-specific model identifier.
	Model string
	// NegativePrompt is optional.
	NegativePrompt string
	// ImageURL is optional reference image.
	ImageURL string
	// CallbackURL optionally receives the task completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r ImageGenerateRequest) toBody() map[string]any {
	body := map[string]any{"prompt": r.Prompt}
	if r.Model != "" {
		body["model"] = r.Model
	}
	if r.NegativePrompt != "" {
		body["negative_prompt"] = r.NegativePrompt
	}
	if r.ImageURL != "" {
		body["image_url"] = r.ImageURL
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

// ImagesResource groups image-generation endpoints.
type ImagesResource struct{ t *transport }

// Generate enqueues an image-generation task. It returns a TaskHandle
// (for polling) when the server responds asynchronously, or the direct
// result map when the server produced the image synchronously.
//
// If both a TaskHandle and a direct result are in-scope, prefer the
// TaskHandle when ``req.Provider != ""`` and the server returned a
// ``task_id``.
func (i *ImagesResource) Generate(ctx context.Context, req ImageGenerateRequest) (*TaskHandle, map[string]any, error) {
	provider := req.Provider
	if provider == "" {
		provider = "nano-banana"
	}
	endpoint := "/" + provider + "/images"
	if provider == "midjourney" {
		endpoint = "/midjourney/imagine"
	}
	body := req.toBody()
	result, err := i.t.do(ctx, requestOpts{Method: "POST", Path: endpoint, Body: body})
	if err != nil {
		return nil, nil, err
	}
	taskID, _ := result["task_id"].(string)
	if taskID == "" {
		return nil, result, nil
	}
	handle := &TaskHandle{
		ID:           taskID,
		pollEndpoint: "/" + provider + "/tasks",
		transport:    i.t,
	}
	return handle, result, nil
}
