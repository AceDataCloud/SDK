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
	// Full model ID. Seedream 5.0 Pro supports single-image generation, precise editing, transparent backgrounds, an
	Model string
	// Generation or editing prompt. Optional only for Seedream 5.0 Pro layer decomposition, where omission automatic
	Prompt string
	// One reference image URL/base64 string or an array. Pro accepts up to 10 images in regular mode and exactly one
	Image any
	// Output size. Pro supports 1K/1.5K/2K or valid dimensions; decomposition also supports auto. Lite supports 2K/3
	Size string
	// Sequential image mode. auto lets supported Lite/4.x models generate a related set; disabled returns one image.
	SequentialImageGeneration string
	// Sequential image options. max_images is 1-15 and input images plus outputs must not exceed 15.
	SequentialImageGenerationOptions map[string]any
	// Stream normalized image events. Supported by Lite/4.x only and cannot be combined with async or callback_url.
	Stream *bool
	// Image response format: url or b64_json.
	ResponseFormat string
	// Whether to add the AI-generated watermark.
	Watermark bool
	// Output image format, jpeg or png. Supported by Seedream 5.0 Pro and Lite.
	OutputFormat string
	// Model tools. Seedream 5.0 Lite supports web_search.
	Tools []map[string]any
	// Prompt optimization. Pro supports standard/fast; Lite and 4.5 support standard; 4.0 supports standard/fast.
	OptimizePromptOptions map[string]any
	// Seedream 5.0 Pro layer decomposition. Requires exactly one PNG/JPEG and returns one base image plus up to 16 t
	LayerDecomposition *bool
	// Seedream 5.0 Pro background mode. transparent requires one transparent PNG input and PNG output; opaque produc
	Background string
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
	if r.Prompt != "" {
		body["prompt"] = r.Prompt
	}
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
	if r.Stream != nil {
		body["stream"] = *r.Stream
	}
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
	if r.LayerDecomposition != nil {
		body["layer_decomposition"] = *r.LayerDecomposition
	}
	if r.Background != "" {
		body["background"] = r.Background
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

// Generate Call /seedream/images.
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
