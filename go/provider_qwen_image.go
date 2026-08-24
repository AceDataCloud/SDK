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
	// Qwen Image Images Model
	Model string
	// Qwen Image Images Prompt
	Prompt string
	// Qwen Image Images Image Urls
	ImageURLs []string
	// Qwen Image Images N
	N int
	// Qwen Image Images Size
	Size string
	// Qwen Image Images Prompt Extend
	PromptExtend bool
	// Qwen Image Images Prompt Extend Mode
	PromptExtendMode string
	// Qwen Image Images Enable Thinking
	EnableThinking bool
	// Qwen Image Images Negative Prompt
	NegativePrompt string
	// Qwen Image Images Seed
	Seed int
	// Qwen Image Images Watermark
	Watermark bool
	// Async submits without blocking; poll the returned handle. Defaults true.
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

// Generate Qwen Image Images
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
