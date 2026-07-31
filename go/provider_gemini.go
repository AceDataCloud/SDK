package acedatacloud

import "context"

// Gemini is the gemini provider client.
type Gemini struct {
	t *transport
}

// GeminiChatCompletionsRequest is the input to gemini.ChatCompletions.
type GeminiChatCompletionsRequest struct {
	// Chat model name.
	Model string
	// Conversation messages.
	Messages []map[string]any
	// Enable streaming.
	Stream bool
	// Sampling temperature.
	Temperature float64
	// Top-p nucleus sampling.
	TopP float64
	// Maximum tokens in the response.
	MaxTokens int
	// Frequency penalty.
	FrequencyPenalty float64
	// Presence penalty.
	PresencePenalty float64
	// Number of completions to generate.
	N int
	// Stop sequences.
	Stop any
	// Reproducibility seed.
	Seed int
	// Tools available to the model.
	Tools []any
	// Tool choice.
	ToolChoice any
	// Response format.
	ResponseFormat map[string]any
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r GeminiChatCompletionsRequest) toBody() map[string]any {
	body := map[string]any{}
	body["model"] = r.Model
	body["messages"] = r.Messages
	if r.Stream {
		body["stream"] = r.Stream
	}
	if r.Temperature != 0 {
		body["temperature"] = r.Temperature
	}
	if r.TopP != 0 {
		body["top_p"] = r.TopP
	}
	if r.MaxTokens != 0 {
		body["max_tokens"] = r.MaxTokens
	}
	if r.FrequencyPenalty != 0 {
		body["frequency_penalty"] = r.FrequencyPenalty
	}
	if r.PresencePenalty != 0 {
		body["presence_penalty"] = r.PresencePenalty
	}
	if r.N != 0 {
		body["n"] = r.N
	}
	if r.Stop != nil {
		body["stop"] = r.Stop
	}
	if r.Seed != 0 {
		body["seed"] = r.Seed
	}
	if r.Tools != nil {
		body["tools"] = r.Tools
	}
	if r.ToolChoice != nil {
		body["tool_choice"] = r.ToolChoice
	}
	if r.ResponseFormat != nil {
		body["response_format"] = r.ResponseFormat
	}
	for k, v := range r.Extra {
		if _, exists := body[k]; !exists {
			body[k] = v
		}
	}
	return body
}

// ChatCompletions submits a Gemini chat completion request.
func (c *Gemini) ChatCompletions(ctx context.Context, req GeminiChatCompletionsRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/gemini/chat/completions",
		Body:   req.toBody(),
	})
}

// GeminiVideosGenerateRequest is the input to gemini.VideosGenerate.
type GeminiVideosGenerateRequest struct {
	// Text prompt.
	Prompt string
	// Video generation model.
	Model string
	// Reference image URL.
	ImageURL string
	// Aspect ratio of the output.
	AspectRatio string
	// Duration in seconds.
	Duration int
	// Async submits without blocking; poll the returned handle. Defaults true.
	Async *bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r GeminiVideosGenerateRequest) toBody() map[string]any {
	body := map[string]any{}
	if r.Prompt != "" {
		body["prompt"] = r.Prompt
	}
	if r.Model != "" {
		body["model"] = r.Model
	}
	if r.ImageURL != "" {
		body["image_url"] = r.ImageURL
	}
	if r.AspectRatio != "" {
		body["aspect_ratio"] = r.AspectRatio
	}
	if r.Duration != 0 {
		body["duration"] = r.Duration
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

// VideosGenerate submits a Gemini video generation request.
func (c *Gemini) VideosGenerate(ctx context.Context, req GeminiVideosGenerateRequest) (*TaskHandle, error) {
	result, err := c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/gemini/videos",
		Body:   req.toBody(),
	})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/gemini/tasks", c.t, result), nil
}

// GeminiGenerateContentRequest is the input to gemini.GenerateContent.
type GeminiGenerateContentRequest struct {
	// Native Gemini model name (e.g. gemini-2.0-flash).
	Model string
	// Request contents following the Gemini native content schema.
	Contents []map[string]any
	// Generation config.
	GenerationConfig map[string]any
	// Safety settings.
	SafetySettings []map[string]any
	// System instruction.
	SystemInstruction map[string]any
	// Tools available to the model.
	Tools []any
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r GeminiGenerateContentRequest) toBody() map[string]any {
	body := map[string]any{}
	body["contents"] = r.Contents
	if r.GenerationConfig != nil {
		body["generationConfig"] = r.GenerationConfig
	}
	if r.SafetySettings != nil {
		body["safetySettings"] = r.SafetySettings
	}
	if r.SystemInstruction != nil {
		body["system_instruction"] = r.SystemInstruction
	}
	if r.Tools != nil {
		body["tools"] = r.Tools
	}
	for k, v := range r.Extra {
		if _, exists := body[k]; !exists {
			body[k] = v
		}
	}
	return body
}

// GenerateContent calls the native Gemini generateContent endpoint.
func (c *Gemini) GenerateContent(ctx context.Context, model string, req GeminiGenerateContentRequest) (map[string]any, error) {
	req.Model = model
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/v1beta/models/" + model + ":generateContent",
		Body:   req.toBody(),
	})
}
