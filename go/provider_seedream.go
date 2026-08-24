// Code generated from the platform OpenAPI spec. DO NOT EDIT.
// Regenerate with: python scripts/generate_providers.py

package acedatacloud

import "context"

// Seedream is the seedream provider client.
type Seedream struct {
	t *transport
}

// SeedreamGenerateRequest is the input to seedream.Generate.
type SeedreamGenerateRequest struct {
	// Seedream Images Model
	Model string
	// Seedream Images Prompt
	Prompt string
	// Seedream Images Image
	Image []string
	// Seedream Images Size
	Size string
	// Seedream Images Sequential Image Generation
	SequentialImageGeneration string
	// Seedream Images Sequential Image Generation Options
	SequentialImageGenerationOptions map[string]any
	// Seedream Images Stream
	Stream bool
	// Seedream Images Response Format
	ResponseFormat string
	// Seedream Images Watermark
	Watermark bool
	// Seedream Images Output Format
	OutputFormat string
	// Seedream Images Tools
	Tools []map[string]any
	// Seedream Images Optimize Prompt Options
	OptimizePromptOptions map[string]any
	// Async submits without blocking; poll the returned handle. Defaults true.
	Async *bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r SeedreamGenerateRequest) toBody() map[string]any {
	body := map[string]any{}
	body["model"] = r.Model
	body["prompt"] = r.Prompt
	if r.Image != nil {
		body["image"] = r.Image
	}
	if r.Size != "" {
		body["size"] = r.Size
	}
	if r.SequentialImageGeneration != "" {
		body["sequential_image_generation"] = r.SequentialImageGeneration
	}
	if r.SequentialImageGenerationOptions != nil {
		body["sequential_image_generation_options"] = r.SequentialImageGenerationOptions
	}
	body["stream"] = r.Stream
	if r.ResponseFormat != "" {
		body["response_format"] = r.ResponseFormat
	}
	body["watermark"] = r.Watermark
	if r.OutputFormat != "" {
		body["output_format"] = r.OutputFormat
	}
	if r.Tools != nil {
		body["tools"] = r.Tools
	}
	if r.OptimizePromptOptions != nil {
		body["optimize_prompt_options"] = r.OptimizePromptOptions
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

// Generate Seedream Images
func (c *Seedream) Generate(ctx context.Context, req SeedreamGenerateRequest) (*TaskHandle, error) {
	result, err := c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/seedream/images",
		Body:   req.toBody(),
	})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/seedream/tasks", c.t, result), nil
}
