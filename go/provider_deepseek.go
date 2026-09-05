// Code generated from the platform OpenAPI spec. DO NOT EDIT.
// Regenerate with: python scripts/generate_providers.py

package acedatacloud

import "context"

// Deepseek is the deepseek provider client.
type Deepseek struct {
	t *transport
}

// DeepseekCompletionsRequest is the input to deepseek.Completions.
type DeepseekCompletionsRequest struct {
	// Deepseek Chat Completions Model
	Model string
	// Deepseek Chat Completions Messages 4
	Messages []map[string]any
	// Deepseek Chat Completions N
	N float64
	// Deepseek Chat Completions Stream
	Stream bool
	// Deepseek Chat Completions Max Tokens
	MaxTokens float64
	// Deepseek Chat Completions Temperature
	Temperature float64
	// Deepseek Chat Completions Response Format 4
	ResponseFormat any
	// Deepseek Chat Completions Top P
	TopP float64
	// Deepseek Chat Completions Frequency Penalty
	FrequencyPenalty float64
	// Deepseek Chat Completions Presence Penalty
	PresencePenalty float64
	// Deepseek Chat Completions Seed
	Seed int
	// Deepseek Chat Completions Stop 3
	Stop any
	// Deepseek Chat Completions Max Completion Tokens
	MaxCompletionTokens int
	// Deepseek Chat Completions Logprobs
	Logprobs bool
	// Deepseek Chat Completions Top Logprobs
	TopLogprobs int
	// Deepseek Chat Completions Stream Options
	StreamOptions map[string]any
	// Deepseek Chat Completions Parallel Tool Calls
	ParallelToolCalls bool
	// Deepseek Chat Completions User
	User string
	// Deepseek Chat Completions Reasoning Effort
	ReasoningEffort string
	// Deepseek Chat Completions Service Tier
	ServiceTier string
	// Deepseek Chat Completions Store
	Store bool
	// Deepseek Chat Completions Metadata
	Metadata map[string]any
	// Deepseek Chat Completions Logit Bias
	LogitBias map[string]any
	// Deepseek Chat Completions Modalities
	Modalities []string
	// Deepseek Chat Completions Audio
	Audio map[string]any
	// Deepseek Chat Completions Prediction 3
	Prediction map[string]any
	// Deepseek Chat Completions Web Search Options
	WebSearchOptions map[string]any
	// Deepseek Chat Completions Tools
	Tools []map[string]any
	// Deepseek Chat Completions Tool Choice 3
	ToolChoice any
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r DeepseekCompletionsRequest) toBody() map[string]any {
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
	if r.ResponseFormat != nil {
		body["response_format"] = r.ResponseFormat
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
	if r.Stop != nil {
		body["stop"] = r.Stop
	}
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
	if r.ToolChoice != nil {
		body["tool_choice"] = r.ToolChoice
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

// Completions Deepseek Chat Completions
func (c *Deepseek) Completions(ctx context.Context, req DeepseekCompletionsRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/deepseek/chat/completions",
		Body:   req.toBody(),
	})
}
