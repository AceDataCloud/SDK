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
	// Models used for generating images. If not specified, the default is `doubao-seedream-5.0-lite`. `doubao-seedre
	Model string
	// Prompts for generating images.
	Prompt string
	// Generate a random seed for image generation. The supported range is [-1, 2147483647], with a default value of
	Seed int
	// Generate image dimensions or aspect ratios. Supports preset options (`1K`/`2K`/`3K`/`4K`), or explicit `<width
	Size string
	// Reference image links for image editing are required, supporting accessible http/https URLs, or base64 encoded
	Image []string
	// List of tools that can be called by the model. Currently, only `web_search` is supported. Applicable only to `
	Tools []any
	// Whether to return all images in a streaming manner, default is `false`. Only supports `doubao-seedream-5.0-lit
	Stream bool
	// Whether to add AI-generated watermark, default is `true`.
	Watermark bool
	// The output image file format is `jpeg` by default. Only `doubao-seedream-5.0-pro` and `doubao-seedream-5.0-lit
	OutputFormat string
	// Prompt word weight, the larger the value, the more relevant the generated result is to the prompt word. Only s
	GuidanceScale any
	// The response format defaults to `url`, and also supports `b64_json`.
	ResponseFormat string
	// Optional prompt word optimization configuration. Only supports `doubao-seedream-5.0-lite`, `doubao-seedream-4.
	OptimizePromptOptions map[string]any
	// The default value is `disabled`. Setting it to `auto` allows the model to generate a set of stylistically cohe
	SequentialImageGeneration string
	// Adjustable parameters for batch image generation. Effective only when `sequential_image_generation=auto`. Only
	SequentialImageGenerationOptions map[string]any
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
	if r.Seed != 0 {
		body["seed"] = r.Seed
	}
	if r.Size != "" {
		body["size"] = r.Size
	}
	if r.Image != nil {
		body["image"] = r.Image
	}
	if r.Tools != nil {
		body["tools"] = r.Tools
	}
	body["stream"] = r.Stream
	body["watermark"] = r.Watermark
	if r.OutputFormat != "" {
		body["output_format"] = r.OutputFormat
	}
	body["guidance_scale"] = r.GuidanceScale
	if r.ResponseFormat != "" {
		body["response_format"] = r.ResponseFormat
	}
	if r.OptimizePromptOptions != nil {
		body["optimize_prompt_options"] = r.OptimizePromptOptions
	}
	if r.SequentialImageGeneration != "" {
		body["sequential_image_generation"] = r.SequentialImageGeneration
	}
	if r.SequentialImageGenerationOptions != nil {
		body["sequential_image_generation_options"] = r.SequentialImageGenerationOptions
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

// Generate ByteDance Seedream high-quality image generation and editing API. Supports text-to-image models doubao-seedream-3-0-t2i-250415, doubao-seedream-4-0-25
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
