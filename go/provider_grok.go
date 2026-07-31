package acedatacloud

import "context"

// Grok is the grok provider client.
type Grok struct {
	t *transport
}

// GrokChatCompletionsRequest is the input to grok.ChatCompletions.
type GrokChatCompletionsRequest struct {
	// Chat model name (e.g. grok-4, grok-3).
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
	MaxTokens float64
	// Maximum completion tokens.
	MaxCompletionTokens int
	// Frequency penalty.
	FrequencyPenalty float64
	// Presence penalty.
	PresencePenalty float64
	// Number of completions to generate.
	N float64
	// Stop sequences.
	Stop any
	// Reproducibility seed.
	Seed int
	// Return log probabilities.
	Logprobs bool
	// Number of top log-prob tokens to return.
	TopLogprobs int
	// Streaming options.
	StreamOptions map[string]any
	// Whether to enable parallel tool calls.
	ParallelToolCalls bool
	// End-user identifier.
	User string
	// Reasoning effort level.
	ReasoningEffort string
	// Service tier.
	ServiceTier string
	// Store the conversation.
	Store bool
	// Metadata key-value pairs.
	Metadata map[string]any
	// Logit bias adjustments.
	LogitBias map[string]any
	// Output modalities.
	Modalities []any
	// Audio output settings.
	Audio map[string]any
	// Predicted output.
	Prediction map[string]any
	// Web search options.
	WebSearchOptions map[string]any
	// Tools available to the model.
	Tools []any
	// Tool choice.
	ToolChoice any
	// Response format.
	ResponseFormat map[string]any
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r GrokChatCompletionsRequest) toBody() map[string]any {
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
	if r.MaxCompletionTokens != 0 {
		body["max_completion_tokens"] = r.MaxCompletionTokens
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
	if r.Logprobs {
		body["logprobs"] = r.Logprobs
	}
	if r.TopLogprobs != 0 {
		body["top_logprobs"] = r.TopLogprobs
	}
	if r.StreamOptions != nil {
		body["stream_options"] = r.StreamOptions
	}
	if r.ParallelToolCalls {
		body["parallel_tool_calls"] = r.ParallelToolCalls
	}
	if r.User != "" {
		body["user"] = r.User
	}
	if r.ReasoningEffort != "" {
		body["reasoning_effort"] = r.ReasoningEffort
	}
	if r.ServiceTier != "" {
		body["service_tier"] = r.ServiceTier
	}
	if r.Store {
		body["store"] = r.Store
	}
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

// ChatCompletions submits a Grok chat completion request.
func (c *Grok) ChatCompletions(ctx context.Context, req GrokChatCompletionsRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/grok/chat/completions",
		Body:   req.toBody(),
	})
}

// GrokVideosGenerateRequest is the input to grok.VideosGenerate.
type GrokVideosGenerateRequest struct {
	// Text prompt describing the video.
	Prompt string
	// Video generation model.
	Model string
	// Reference image URL.
	ImageURL string
	// Additional reference image URLs.
	ReferenceImageURLs []string
	// Output aspect ratio.
	AspectRatio string
	// Output resolution (480p, 720p, 1080p).
	Resolution string
	// Duration in seconds.
	Duration int
	// Async submits without blocking; poll the returned handle. Defaults true.
	Async *bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r GrokVideosGenerateRequest) toBody() map[string]any {
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
	if r.ReferenceImageURLs != nil {
		body["reference_image_urls"] = r.ReferenceImageURLs
	}
	if r.AspectRatio != "" {
		body["aspect_ratio"] = r.AspectRatio
	}
	if r.Resolution != "" {
		body["resolution"] = r.Resolution
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

// VideosGenerate submits a Grok video generation request.
func (c *Grok) VideosGenerate(ctx context.Context, req GrokVideosGenerateRequest) (*TaskHandle, error) {
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
