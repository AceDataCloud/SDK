// Code generated from the platform OpenAPI spec. DO NOT EDIT.
// Regenerate with: python scripts/generate_providers.py

package acedatacloud

import "context"

// Coding is the coding provider client.
type Coding struct {
	t *transport
}

// CodingCountTokensRequest is the input to coding.Count_Tokens.
type CodingCountTokensRequest struct {
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

func (r CodingCountTokensRequest) toBody() map[string]any {
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
func (c *Coding) CountTokens(ctx context.Context, req CodingCountTokensRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/v1/messages/count_tokens",
		Body:   req.toBody(),
	})
}

// CodingMessagesRequest is the input to coding.Messages.
type CodingMessagesRequest struct {
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

func (r CodingMessagesRequest) toBody() map[string]any {
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
func (c *Coding) Messages(ctx context.Context, req CodingMessagesRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/v1/messages",
		Body:   req.toBody(),
	})
}

// CodingCompletionsRequest is the input to coding.Completions.
type CodingCompletionsRequest struct {
	// Openai Chat Completions Model
	Model string
	// Openai Chat Completions Messages 4
	Messages []map[string]any
	// Openai Chat Completions N
	N float64
	// Openai Chat Completions Stream
	Stream bool
	// Openai Chat Completions Max Tokens
	MaxTokens float64
	// Openai Chat Completions Temperature
	Temperature float64
	// Openai Chat Completions Response Format 4
	ResponseFormat any
	// Openai Chat Completions Tools
	Tools []map[string]any
	// Openai Chat Completions Tool Choice 3
	ToolChoice any
	// Openai Chat Completions Top P
	TopP float64
	// Openai Chat Completions Frequency Penalty
	FrequencyPenalty float64
	// Openai Chat Completions Presence Penalty
	PresencePenalty float64
	// Openai Chat Completions Seed
	Seed int
	// Openai Chat Completions Stop 3
	Stop any
	// Openai Chat Completions Max Completion Tokens
	MaxCompletionTokens int
	// Openai Chat Completions Logprobs
	Logprobs bool
	// Openai Chat Completions Top Logprobs
	TopLogprobs int
	// Openai Chat Completions Stream Options
	StreamOptions map[string]any
	// Openai Chat Completions Parallel Tool Calls
	ParallelToolCalls bool
	// Openai Chat Completions User
	User string
	// Openai Chat Completions Reasoning Effort
	ReasoningEffort string
	// Openai Chat Completions Service Tier
	ServiceTier string
	// Openai Chat Completions Store
	Store bool
	// Openai Chat Completions Metadata
	Metadata map[string]any
	// Openai Chat Completions Logit Bias
	LogitBias map[string]any
	// Openai Chat Completions Modalities
	Modalities []string
	// Openai Chat Completions Audio
	Audio map[string]any
	// Openai Chat Completions Prediction 3
	Prediction map[string]any
	// Openai Chat Completions Web Search Options
	WebSearchOptions map[string]any
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r CodingCompletionsRequest) toBody() map[string]any {
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
	if r.Tools != nil {
		body["tools"] = r.Tools
	}
	if r.ToolChoice != nil {
		body["tool_choice"] = r.ToolChoice
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

// Completions Openai Chat Completions
func (c *Coding) Completions(ctx context.Context, req CodingCompletionsRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/openai/chat/completions",
		Body:   req.toBody(),
	})
}

// CodingV1ChatCompletionsRequest is the input to coding.V1_Chat_Completions.
type CodingV1ChatCompletionsRequest struct {
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

func (r CodingV1ChatCompletionsRequest) toBody() map[string]any {
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

// V1ChatCompletions Claude Chat Completions
func (c *Coding) V1ChatCompletions(ctx context.Context, req CodingV1ChatCompletionsRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/v1/chat/completions",
		Body:   req.toBody(),
	})
}

// CodingDeepseekChatCompletionsRequest is the input to coding.Deepseek_Chat_Completions.
type CodingDeepseekChatCompletionsRequest struct {
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

func (r CodingDeepseekChatCompletionsRequest) toBody() map[string]any {
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

// DeepseekChatCompletions Deepseek Chat Completions
func (c *Coding) DeepseekChatCompletions(ctx context.Context, req CodingDeepseekChatCompletionsRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/deepseek/chat/completions",
		Body:   req.toBody(),
	})
}

// CodingGlmChatCompletionsRequest is the input to coding.Glm_Chat_Completions.
type CodingGlmChatCompletionsRequest struct {
	// Glm Chat Completions Model
	Model string
	// Glm Chat Completions Messages 4
	Messages []map[string]any
	// Glm Chat Completions N
	N float64
	// Glm Chat Completions Stream
	Stream bool
	// Glm Chat Completions Max Tokens
	MaxTokens float64
	// Glm Chat Completions Temperature
	Temperature float64
	// Glm Chat Completions Response Format 4
	ResponseFormat any
	// Glm Chat Completions Top P
	TopP float64
	// Glm Chat Completions Frequency Penalty
	FrequencyPenalty float64
	// Glm Chat Completions Presence Penalty
	PresencePenalty float64
	// Glm Chat Completions Seed
	Seed int
	// Glm Chat Completions Stop 3
	Stop any
	// Glm Chat Completions Max Completion Tokens
	MaxCompletionTokens int
	// Glm Chat Completions Logprobs
	Logprobs bool
	// Glm Chat Completions Top Logprobs
	TopLogprobs int
	// Glm Chat Completions Stream Options
	StreamOptions map[string]any
	// Glm Chat Completions Parallel Tool Calls
	ParallelToolCalls bool
	// Glm Chat Completions User
	User string
	// Glm Chat Completions Reasoning Effort
	ReasoningEffort string
	// Glm Chat Completions Service Tier
	ServiceTier string
	// Glm Chat Completions Store
	Store bool
	// Glm Chat Completions Metadata
	Metadata map[string]any
	// Glm Chat Completions Logit Bias
	LogitBias map[string]any
	// Glm Chat Completions Modalities
	Modalities []string
	// Glm Chat Completions Audio
	Audio map[string]any
	// Glm Chat Completions Prediction 3
	Prediction map[string]any
	// Glm Chat Completions Web Search Options
	WebSearchOptions map[string]any
	// Glm Chat Completions Tools
	Tools []map[string]any
	// Glm Chat Completions Tool Choice 3
	ToolChoice any
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r CodingGlmChatCompletionsRequest) toBody() map[string]any {
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

// GlmChatCompletions Glm Chat Completions
func (c *Coding) GlmChatCompletions(ctx context.Context, req CodingGlmChatCompletionsRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/glm/chat/completions",
		Body:   req.toBody(),
	})
}

// CodingGeminiChatCompletionsRequest is the input to coding.Gemini_Chat_Completions.
type CodingGeminiChatCompletionsRequest struct {
	// Gemini Chat Completions Model
	Model string
	// Gemini Chat Completions Messages 4
	Messages []map[string]any
	// Gemini Chat Completions N
	N float64
	// Gemini Chat Completions Stream
	Stream bool
	// Gemini Chat Completions Max Tokens
	MaxTokens float64
	// Gemini Chat Completions Temperature
	Temperature float64
	// Gemini Chat Completions Response Format 4
	ResponseFormat any
	// Gemini Chat Completions Top P
	TopP float64
	// Gemini Chat Completions Frequency Penalty
	FrequencyPenalty float64
	// Gemini Chat Completions Presence Penalty
	PresencePenalty float64
	// Gemini Chat Completions Seed
	Seed int
	// Gemini Chat Completions Stop 3
	Stop any
	// Gemini Chat Completions Max Completion Tokens
	MaxCompletionTokens int
	// Gemini Chat Completions Logprobs
	Logprobs bool
	// Gemini Chat Completions Top Logprobs
	TopLogprobs int
	// Gemini Chat Completions Stream Options
	StreamOptions map[string]any
	// Gemini Chat Completions Parallel Tool Calls
	ParallelToolCalls bool
	// Gemini Chat Completions User
	User string
	// Gemini Chat Completions Reasoning Effort
	ReasoningEffort string
	// Gemini Chat Completions Service Tier
	ServiceTier string
	// Gemini Chat Completions Store
	Store bool
	// Gemini Chat Completions Metadata
	Metadata map[string]any
	// Gemini Chat Completions Logit Bias
	LogitBias map[string]any
	// Gemini Chat Completions Modalities
	Modalities []string
	// Gemini Chat Completions Audio
	Audio map[string]any
	// Gemini Chat Completions Prediction 3
	Prediction map[string]any
	// Gemini Chat Completions Web Search Options
	WebSearchOptions map[string]any
	// Gemini Chat Completions Tools
	Tools []map[string]any
	// Gemini Chat Completions Tool Choice 3
	ToolChoice any
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r CodingGeminiChatCompletionsRequest) toBody() map[string]any {
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

// GeminiChatCompletions Gemini Chat Completions
func (c *Coding) GeminiChatCompletions(ctx context.Context, req CodingGeminiChatCompletionsRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/gemini/chat/completions",
		Body:   req.toBody(),
	})
}

// CodingGrokChatCompletionsRequest is the input to coding.Grok_Chat_Completions.
type CodingGrokChatCompletionsRequest struct {
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

func (r CodingGrokChatCompletionsRequest) toBody() map[string]any {
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
	if r.ResponseFormat != nil {
		body["response_format"] = r.ResponseFormat
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

// GrokChatCompletions Grok Chat Completions
func (c *Coding) GrokChatCompletions(ctx context.Context, req CodingGrokChatCompletionsRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/grok/chat/completions",
		Body:   req.toBody(),
	})
}

// CodingKimiChatCompletionsRequest is the input to coding.Kimi_Chat_Completions.
type CodingKimiChatCompletionsRequest struct {
	// Kimi Chat Completions Model
	Model string
	// Kimi Chat Completions Messages 4
	Messages []map[string]any
	// Kimi Chat Completions N
	N int
	// Kimi Chat Completions Stream
	Stream bool
	// Kimi Chat Completions Max Tokens
	MaxTokens float64
	// Kimi Chat Completions Temperature
	Temperature float64
	// Kimi Chat Completions Response Format 4
	ResponseFormat any
	// Kimi Chat Completions Top P
	TopP float64
	// Kimi Chat Completions Frequency Penalty
	FrequencyPenalty float64
	// Kimi Chat Completions Presence Penalty
	PresencePenalty float64
	// Kimi Chat Completions Seed
	Seed int
	// Kimi Chat Completions Stop 3
	Stop any
	// Kimi Chat Completions Max Completion Tokens
	MaxCompletionTokens int
	// Kimi Chat Completions Logprobs
	Logprobs bool
	// Kimi Chat Completions Top Logprobs
	TopLogprobs int
	// Kimi Chat Completions Stream Options
	StreamOptions map[string]any
	// Kimi Chat Completions Parallel Tool Calls
	ParallelToolCalls bool
	// Kimi Chat Completions User
	User string
	// Kimi Chat Completions Reasoning Effort
	ReasoningEffort string
	// Kimi Chat Completions Service Tier
	ServiceTier string
	// Kimi Chat Completions Store
	Store bool
	// Kimi Chat Completions Metadata
	Metadata map[string]any
	// Kimi Chat Completions Logit Bias
	LogitBias map[string]any
	// Kimi Chat Completions Modalities
	Modalities []string
	// Kimi Chat Completions Audio
	Audio map[string]any
	// Kimi Chat Completions Prediction 3
	Prediction map[string]any
	// Kimi Chat Completions Web Search Options
	WebSearchOptions map[string]any
	// Kimi Chat Completions Tools
	Tools []map[string]any
	// Kimi Chat Completions Tool Choice 3
	ToolChoice any
	// Kimi Chat Completions Thinking
	Thinking map[string]any
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r CodingKimiChatCompletionsRequest) toBody() map[string]any {
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
	if r.Thinking != nil {
		body["thinking"] = r.Thinking
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

// KimiChatCompletions Kimi Chat Completions
func (c *Coding) KimiChatCompletions(ctx context.Context, req CodingKimiChatCompletionsRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/kimi/chat/completions",
		Body:   req.toBody(),
	})
}

// CodingResponsesRequest is the input to coding.Responses.
type CodingResponsesRequest struct {
	// Openai Responses Model
	Model string
	// Openai Responses Input 2
	Input any
	// Openai Responses N
	N float64
	// Openai Responses Background
	Background bool
	// Openai Responses Stream
	Stream bool
	// Openai Responses Tools
	Tools []map[string]any
	// Openai Responses Max Tokens
	MaxTokens float64
	// Openai Responses Temperature
	Temperature float64
	// Openai Responses Response Format
	ResponseFormat map[string]any
	// Openapi.Ed972A38Ecef4Fcbaf33750De42D25Dc.Tool Choice.C7B5D99A6584
	ToolChoice any
	// optional
	ParallelToolCalls bool
	// optional
	Include []string
	// optional
	Reasoning map[string]any
	// optional
	Text map[string]any
	// optional
	MaxOutputTokens int
	// optional
	Store bool
	// optional
	StreamOptions map[string]any
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r CodingResponsesRequest) toBody() map[string]any {
	body := map[string]any{}
	body["model"] = r.Model
	body["input"] = r.Input
	if r.N != 0 {
		body["n"] = r.N
	} else {
		body["n"] = 1
	}
	body["background"] = r.Background
	body["stream"] = r.Stream
	if r.Tools != nil {
		body["tools"] = r.Tools
	}
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
	if r.ToolChoice != nil {
		body["tool_choice"] = r.ToolChoice
	}
	body["parallel_tool_calls"] = r.ParallelToolCalls
	if r.Include != nil {
		body["include"] = r.Include
	}
	if r.Reasoning != nil {
		body["reasoning"] = r.Reasoning
	}
	if r.Text != nil {
		body["text"] = r.Text
	}
	if r.MaxOutputTokens != 0 {
		body["max_output_tokens"] = r.MaxOutputTokens
	}
	body["store"] = r.Store
	if r.StreamOptions != nil {
		body["stream_options"] = r.StreamOptions
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

// Responses Openai V1 Responses
func (c *Coding) Responses(ctx context.Context, req CodingResponsesRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/openai/responses",
		Body:   req.toBody(),
	})
}
