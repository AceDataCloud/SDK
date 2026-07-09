package acedatacloud

import "context"

// ImageGenerateRequest is the input to images.generate.
type ImageGenerateRequest struct {
	// Prompt is the required text prompt.
	Prompt string
	// Provider selects the backend. Common values: "nano-banana", "flux", "seedream".
	Provider string
	// Model is optional — provider-specific model identifier.
	Model string
	// NegativePrompt is optional.
	NegativePrompt string
	// Image is an optional list of reference images (e.g. for seedream image-to-image).
	Image []any
	// ImageURL is optional reference image.
	ImageURL string
	// Size is the optional output size (e.g. "1K", "2K", "4K", "adaptive" for seedream).
	Size string
	// Seed is an optional integer seed for reproducibility.
	Seed *int
	// GuidanceScale is an optional guidance scale parameter.
	GuidanceScale *float64
	// ResponseFormat is optional (e.g. "url", "b64_json").
	ResponseFormat string
	// Watermark controls whether a watermark is applied.
	Watermark *bool
	// OutputFormat is the optional output file format (e.g. "jpeg", "png").
	OutputFormat string
	// Stream controls streaming mode (seedream-specific).
	Stream *bool
	// SequentialImageGeneration controls sequential image generation mode.
	SequentialImageGeneration string
	// SequentialImageGenerationOptions holds options for sequential generation.
	SequentialImageGenerationOptions map[string]any
	// Tools is an optional list of tools (seedream-specific).
	Tools []any
	// OptimizePromptOptions holds prompt optimization options.
	OptimizePromptOptions map[string]any
	// CallbackURL optionally receives the task completion webhook.
	CallbackURL string
	// Async, when true, returns a task_id without requiring a CallbackURL;
	// poll the tasks endpoint for the result.
	Async bool
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
	if len(r.Image) > 0 {
		body["image"] = r.Image
	}
	if r.ImageURL != "" {
		body["image_url"] = r.ImageURL
	}
	if r.Size != "" {
		body["size"] = r.Size
	}
	if r.Seed != nil {
		body["seed"] = *r.Seed
	}
	if r.GuidanceScale != nil {
		body["guidance_scale"] = *r.GuidanceScale
	}
	if r.ResponseFormat != "" {
		body["response_format"] = r.ResponseFormat
	}
	if r.Watermark != nil {
		body["watermark"] = *r.Watermark
	}
	if r.OutputFormat != "" {
		body["output_format"] = r.OutputFormat
	}
	if r.Stream != nil {
		body["stream"] = *r.Stream
	}
	if r.SequentialImageGeneration != "" {
		body["sequential_image_generation"] = r.SequentialImageGeneration
	}
	if len(r.SequentialImageGenerationOptions) > 0 {
		body["sequential_image_generation_options"] = r.SequentialImageGenerationOptions
	}
	if len(r.Tools) > 0 {
		body["tools"] = r.Tools
	}
	if len(r.OptimizePromptOptions) > 0 {
		body["optimize_prompt_options"] = r.OptimizePromptOptions
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
