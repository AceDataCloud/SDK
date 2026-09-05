// Code generated from the platform OpenAPI spec. DO NOT EDIT.
// Regenerate with: python scripts/generate_providers.py

package acedatacloud

import "context"

// Claude is the claude provider client.
type Claude struct {
	t *transport
}

// ClaudeCompletionsRequest is the input to claude.Completions.
type ClaudeCompletionsRequest struct {
	// V1 Chat Completions Model
	Model string
	// V1 Chat Completions Messages 4
	Messages []map[string]any
	// V1 Chat Completions N
	N float64
	// V1 Chat Completions Stream
	Stream bool
	// V1 Chat Completions Max Tokens
	MaxTokens float64
	// V1 Chat Completions Temperature
	Temperature float64
	// V1 Chat Completions Response Format 4
	ResponseFormat any
	// V1 Chat Completions Top P
	TopP float64
	// V1 Chat Completions Frequency Penalty
	FrequencyPenalty float64
	// V1 Chat Completions Presence Penalty
	PresencePenalty float64
	// V1 Chat Completions Seed
	Seed int
	// V1 Chat Completions Stop 3
	Stop any
	// V1 Chat Completions Max Completion Tokens
	MaxCompletionTokens int
	// V1 Chat Completions Logprobs
	Logprobs bool
	// V1 Chat Completions Top Logprobs
	TopLogprobs int
	// V1 Chat Completions Stream Options
	StreamOptions map[string]any
	// V1 Chat Completions Parallel Tool Calls
	ParallelToolCalls bool
	// V1 Chat Completions User
	User string
	// V1 Chat Completions Reasoning Effort
	ReasoningEffort string
	// V1 Chat Completions Service Tier
	ServiceTier string
	// V1 Chat Completions Store
	Store bool
	// V1 Chat Completions Metadata
	Metadata map[string]any
	// V1 Chat Completions Logit Bias
	LogitBias map[string]any
	// V1 Chat Completions Modalities
	Modalities []string
	// V1 Chat Completions Audio
	Audio map[string]any
	// V1 Chat Completions Prediction 3
	Prediction map[string]any
	// V1 Chat Completions Web Search Options
	WebSearchOptions map[string]any
	// V1 Chat Completions Tools
	Tools []map[string]any
	// V1 Chat Completions Tool Choice 3
	ToolChoice any
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r ClaudeCompletionsRequest) toBody() map[string]any {
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

// Completions Claude Chat Completions
func (c *Claude) Completions(ctx context.Context, req ClaudeCompletionsRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/v1/chat/completions",
		Body:   req.toBody(),
	})
}

// ClaudeMessagesRequest is the input to claude.Messages.
type ClaudeMessagesRequest struct {
	// V1 Messages Model
	Model string
	// required
	Messages []map[string]any
	// V1 Messages Max Tokens
	MaxTokens int
	// optional
	Metadata map[string]any
	// V1 Messages Stop Sequences
	StopSequences []string
	// V1 Messages Stream
	Stream bool
	// optional
	System any
	// V1 Messages Temperature
	Temperature float64
	// optional
	ToolChoice any
	// V1 Messages Tools
	Tools []map[string]any
	// V1 Messages Top K
	TopK int
	// V1 Messages Top P
	TopP float64
	// optional
	Thinking any
	// V1 Messages Output Config
	OutputConfig map[string]any
	// optional
	CacheControl map[string]any
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r ClaudeMessagesRequest) toBody() map[string]any {
	body := map[string]any{}
	body["model"] = r.Model
	body["messages"] = r.Messages
	body["max_tokens"] = r.MaxTokens
	if r.Metadata != nil {
		body["metadata"] = r.Metadata
	}
	if r.StopSequences != nil {
		body["stop_sequences"] = r.StopSequences
	}
	body["stream"] = r.Stream
	if r.System != nil {
		body["system"] = r.System
	}
	if r.Temperature != 0 {
		body["temperature"] = r.Temperature
	}
	if r.ToolChoice != nil {
		body["tool_choice"] = r.ToolChoice
	}
	if r.Tools != nil {
		body["tools"] = r.Tools
	}
	if r.TopK != 0 {
		body["top_k"] = r.TopK
	}
	if r.TopP != 0 {
		body["top_p"] = r.TopP
	}
	if r.Thinking != nil {
		body["thinking"] = r.Thinking
	}
	if r.OutputConfig != nil {
		body["output_config"] = r.OutputConfig
	}
	if r.CacheControl != nil {
		body["cache_control"] = r.CacheControl
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

// Messages Claude Messages
func (c *Claude) Messages(ctx context.Context, req ClaudeMessagesRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/v1/messages",
		Body:   req.toBody(),
	})
}

// ClaudeCountTokensRequest is the input to claude.Count_Tokens.
type ClaudeCountTokensRequest struct {
	// V1 Messages Count Tokens Model
	Model string
	// required
	Messages []map[string]any
	// optional
	System any
	// optional
	Thinking any
	// optional
	ToolChoice any
	// V1 Messages Count Tokens Tools
	Tools []map[string]any
	// optional
	CacheControl map[string]any
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r ClaudeCountTokensRequest) toBody() map[string]any {
	body := map[string]any{}
	body["model"] = r.Model
	body["messages"] = r.Messages
	if r.System != nil {
		body["system"] = r.System
	}
	if r.Thinking != nil {
		body["thinking"] = r.Thinking
	}
	if r.ToolChoice != nil {
		body["tool_choice"] = r.ToolChoice
	}
	if r.Tools != nil {
		body["tools"] = r.Tools
	}
	if r.CacheControl != nil {
		body["cache_control"] = r.CacheControl
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

// CountTokens Claude Messages Count Tokens
func (c *Claude) CountTokens(ctx context.Context, req ClaudeCountTokensRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/v1/messages/count_tokens",
		Body:   req.toBody(),
	})
}
