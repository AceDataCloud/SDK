// Code generated from the platform OpenAPI spec. DO NOT EDIT.
// Regenerate with: python scripts/generate_providers.py

package acedatacloud

import "context"

// Grok is the grok provider client.
type Grok struct {
	t *transport
}

// GrokCompletionsRequest is the input to grok.Completions.
type GrokCompletionsRequest struct {
	// Grok Chat Completions Model
	Model string
	// Grok Chat Completions Messages 4
	Messages []map[string]any
	// Grok Chat Completions N
	N float64
	// Grok Chat Completions Stream
	Stream bool
	// Grok Chat Completions Max Tokens
	MaxTokens float64
	// Grok Chat Completions Temperature
	Temperature float64
	// Grok Chat Completions Top P
	TopP float64
	// Grok Chat Completions Frequency Penalty
	FrequencyPenalty float64
	// Grok Chat Completions Presence Penalty
	PresencePenalty float64
	// Grok Chat Completions Seed
	Seed int
	// Grok Chat Completions Stop 3
	Stop any
	// Grok Chat Completions Max Completion Tokens
	MaxCompletionTokens int
	// Grok Chat Completions Logprobs
	Logprobs bool
	// Grok Chat Completions Top Logprobs
	TopLogprobs int
	// Grok Chat Completions Stream Options
	StreamOptions map[string]any
	// Grok Chat Completions Parallel Tool Calls
	ParallelToolCalls bool
	// Grok Chat Completions User
	User string
	// Grok Chat Completions Reasoning Effort
	ReasoningEffort string
	// Grok Chat Completions Service Tier
	ServiceTier string
	// Grok Chat Completions Store
	Store bool
	// Grok Chat Completions Metadata
	Metadata map[string]any
	// Grok Chat Completions Logit Bias
	LogitBias map[string]any
	// Grok Chat Completions Modalities
	Modalities []string
	// Grok Chat Completions Audio
	Audio map[string]any
	// Grok Chat Completions Prediction 3
	Prediction map[string]any
	// Grok Chat Completions Web Search Options
	WebSearchOptions map[string]any
	// Grok Chat Completions Tools
	Tools []map[string]any
	// Grok Chat Completions Tool Choice 3
	ToolChoice any
	// Grok Chat Completions Response Format 4
	ResponseFormat any
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r GrokCompletionsRequest) toBody() map[string]any {
	body := map[string]any{}
	body["model"] = r.Model
	body["messages"] = r.Messages
	if r.N != 0 {
		body["n"] = r.N
	} else {
		body["n"] = 1
	}
	body["stream"] = r.Stream
	if r.MaxTokens != 0 {
		body["max_tokens"] = r.MaxTokens
	}
	if r.Temperature != 0 {
		body["temperature"] = r.Temperature
	} else {
		body["temperature"] = 1
	}
	if r.TopP != 0 {
		body["top_p"] = r.TopP
	} else {
		body["top_p"] = 1
	}
	if r.FrequencyPenalty != 0 {
		body["frequency_penalty"] = r.FrequencyPenalty
	} else {
		body["frequency_penalty"] = 0
	}
	if r.PresencePenalty != 0 {
		body["presence_penalty"] = r.PresencePenalty
	} else {
		body["presence_penalty"] = 0
	}
	if r.Seed != 0 {
		body["seed"] = r.Seed
	}
	body["stop"] = r.Stop
	if r.MaxCompletionTokens != 0 {
		body["max_completion_tokens"] = r.MaxCompletionTokens
	}
	body["logprobs"] = r.Logprobs
	if r.TopLogprobs != 0 {
		body["top_logprobs"] = r.TopLogprobs
	}
	if r.StreamOptions != nil {
		body["stream_options"] = r.StreamOptions
	}
	body["parallel_tool_calls"] = r.ParallelToolCalls
	if r.User != "" {
		body["user"] = r.User
	}
	if r.ReasoningEffort != "" {
		body["reasoning_effort"] = r.ReasoningEffort
	} else {
		body["reasoning_effort"] = "medium"
	}
	if r.ServiceTier != "" {
		body["service_tier"] = r.ServiceTier
	} else {
		body["service_tier"] = "auto"
	}
	body["store"] = r.Store
	if r.Metadata != nil {
		body["metadata"] = r.Metadata
	}
	if r.LogitBias != nil {
		body["logit_bias"] = r.LogitBias
	}
	if r.Modalities != nil {
		body["modalities"] = r.Modalities
	}
	if r.Audio != nil {
		body["audio"] = r.Audio
	}
	if r.Prediction != nil {
		body["prediction"] = r.Prediction
	}
	if r.WebSearchOptions != nil {
		body["web_search_options"] = r.WebSearchOptions
	}
	if r.Tools != nil {
		body["tools"] = r.Tools
	}
	body["tool_choice"] = r.ToolChoice
	body["response_format"] = r.ResponseFormat
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

// Completions Grok Chat Completions
func (c *Grok) Completions(ctx context.Context, req GrokCompletionsRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/grok/chat/completions",
		Body:   req.toBody(),
	})
}

// GrokGenerateRequest is the input to grok.Generate.
type GrokGenerateRequest struct {
	// Grok Videos Prompt
	Prompt string
	// Grok Videos Model
	Model string
	// Grok Videos Image Url
	ImageURL string
	// Grok Videos Reference Image Urls
	ReferenceImageURLs []string
	// Grok Videos Aspect Ratio
	AspectRatio string
	// Grok Videos Resolution
	Resolution string
	// Grok Videos Duration
	Duration int
	// Async submits without blocking; poll the returned handle. Defaults true.
	Async *bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r GrokGenerateRequest) toBody() map[string]any {
	body := map[string]any{}
	if r.Prompt != "" {
		body["prompt"] = r.Prompt
	}
	if r.Model != "" {
		body["model"] = r.Model
	} else {
		body["model"] = "grok-imagine-video-1.5-fast:reverse"
	}
	if r.ImageURL != "" {
		body["image_url"] = r.ImageURL
	}
	if r.ReferenceImageURLs != nil {
		body["reference_image_urls"] = r.ReferenceImageURLs
	}
	if r.AspectRatio != "" {
		body["aspect_ratio"] = r.AspectRatio
	}
	if r.Resolution != "" {
		body["resolution"] = r.Resolution
	} else {
		body["resolution"] = "480p"
	}
	if r.Duration != 0 {
		body["duration"] = r.Duration
	} else {
		body["duration"] = 6
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

// Generate Grok Videos
func (c *Grok) Generate(ctx context.Context, req GrokGenerateRequest) (*TaskHandle, error) {
	result, err := c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/grok/videos",
		Body:   req.toBody(),
	})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/grok/tasks", c.t, result), nil
}
