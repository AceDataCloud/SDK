// Code generated from the platform OpenAPI spec. DO NOT EDIT.
// Regenerate with: python scripts/generate_providers.py

package acedatacloud

import "context"

// QwenImage is the qwen-image provider client.
type QwenImage struct {
	t *transport
}

// QwenImageGenerateRequest is the input to qwen_image.Generate.
type QwenImageGenerateRequest struct {
	// $t(qwen_image_images_model)
	Model string
	// $t(qwen_image_images_prompt)
	Prompt string
	// $t(qwen_image_images_image_urls)
	ImageURLs []string
	// $t(qwen_image_images_n)
	N int
	// $t(qwen_image_images_size)
	Size string
	// $t(qwen_image_images_prompt_extend)
	PromptExtend bool
	// $t(qwen_image_images_prompt_extend_mode)
	PromptExtendMode string
	// $t(qwen_image_images_enable_thinking)
	EnableThinking bool
	// $t(qwen_image_images_negative_prompt)
	NegativePrompt string
	// $t(qwen_image_images_seed)
	Seed int
	// $t(qwen_image_images_watermark)
	Watermark bool
	// Async submits without blocking; poll the returned handle. Defaults false.
	Async *bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r QwenImageGenerateRequest) toBody() map[string]any {
	body := map[string]any{}
	body["model"] = r.Model
	body["prompt"] = r.Prompt
	if r.ImageURLs != nil {
		body["image_urls"] = r.ImageURLs
	}
	if r.N != 0 {
		body["n"] = r.N
	} else {
		body["n"] = 1
	}
	if r.Size != "" {
		body["size"] = r.Size
	}
	body["prompt_extend"] = r.PromptExtend
	if r.PromptExtendMode != "" {
		body["prompt_extend_mode"] = r.PromptExtendMode
	} else {
		body["prompt_extend_mode"] = "direct"
	}
	body["enable_thinking"] = r.EnableThinking
	if r.NegativePrompt != "" {
		body["negative_prompt"] = r.NegativePrompt
	}
	if r.Seed != 0 {
		body["seed"] = r.Seed
	}
	body["watermark"] = r.Watermark
	body["async"] = false
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

// Generate Call /qwen-image/images.
func (c *QwenImage) Generate(ctx context.Context, req QwenImageGenerateRequest) (*TaskHandle, error) {
	result, err := c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/qwen-image/images",
		Body:   req.toBody(),
	})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/qwen-image/tasks", c.t, result), nil
}
