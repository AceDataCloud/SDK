package acedatacloud

import "context"

// Claude is the claude provider client.
type Claude struct{ t *transport }

// ClaudeModel names a Claude model accepted by the API.
type ClaudeModel string

const (
	ClaudeFable5           ClaudeModel = "claude-fable-5"
	ClaudeOpus5            ClaudeModel = "claude-opus-5"
	ClaudeOpus48           ClaudeModel = "claude-opus-4-8"
	ClaudeSonnet5          ClaudeModel = "claude-sonnet-5"
	ClaudeSonnet46         ClaudeModel = "claude-sonnet-4-6"
	ClaudeOpus47           ClaudeModel = "claude-opus-4-7"
	ClaudeOpus46           ClaudeModel = "claude-opus-4-6"
	ClaudeOpus4520251101   ClaudeModel = "claude-opus-4-5-20251101"
	ClaudeHaiku4520251001  ClaudeModel = "claude-haiku-4-5-20251001"
	ClaudeSonnet4520250929 ClaudeModel = "claude-sonnet-4-5-20250929"
	ClaudeOpus4120250805   ClaudeModel = "claude-opus-4-1-20250805"
	ClaudeSonnet420250514  ClaudeModel = "claude-sonnet-4-20250514"
	ClaudeOpus420250514    ClaudeModel = "claude-opus-4-20250514"
	Claude37Sonnet20250219 ClaudeModel = "claude-3-7-sonnet-20250219"
	Claude35Sonnet20241022 ClaudeModel = "claude-3-5-sonnet-20241022"
	Claude35Haiku20241022  ClaudeModel = "claude-3-5-haiku-20241022"
	Claude35Sonnet20240620 ClaudeModel = "claude-3-5-sonnet-20240620"
	Claude3Haiku20240307   ClaudeModel = "claude-3-haiku-20240307"
	Claude3Sonnet20240229  ClaudeModel = "claude-3-sonnet-20240229"
	Claude3Opus20240229    ClaudeModel = "claude-3-opus-20240229"
)

// ClaudeChat returns the OpenAI-compatible Claude chat namespace.
func (c *Claude) Chat() *ClaudeChat { return &ClaudeChat{t: c.t} }

// ClaudeMessages returns the native Claude Messages namespace.
func (c *Claude) Messages() *ClaudeMessages { return &ClaudeMessages{t: c.t} }

type ClaudeChat struct{ t *transport }

func (c *ClaudeChat) Completions() *ClaudeChatCompletions { return &ClaudeChatCompletions{t: c.t} }

type ClaudeChatCompletions struct{ t *transport }

// ClaudeChatCompletionRequest is the input to claude.chat.completions.create.
type ClaudeChatCompletionRequest struct {
	Model               ClaudeModel
	Messages            []map[string]any
	N                   float64
	Stream              bool
	MaxTokens           float64
	Temperature         *float64
	ResponseFormat      any
	TopP                *float64
	FrequencyPenalty    *float64
	PresencePenalty     *float64
	Seed                int
	Stop                any
	MaxCompletionTokens int
	Logprobs            *bool
	TopLogprobs         int
	StreamOptions       map[string]any
	ParallelToolCalls   *bool
	User                string
	ReasoningEffort     string
	ServiceTier         string
	Store               *bool
	Metadata            map[string]any
	LogitBias           map[string]any
	Modalities          []any
	Audio               map[string]any
	Prediction          map[string]any
	WebSearchOptions    map[string]any
	Tools               []any
	ToolChoice          any
	Extra               map[string]any
}

func (r ClaudeChatCompletionRequest) toBody() map[string]any {
	body := map[string]any{"model": string(r.Model), "messages": r.Messages, "stream": r.Stream}
	if r.N != 0 {
		body["n"] = r.N
	} else {
		body["n"] = 1.0
	}
	if r.MaxTokens != 0 {
		body["max_tokens"] = r.MaxTokens
	}
	if r.Temperature != nil {
		body["temperature"] = *r.Temperature
	} else {
		body["temperature"] = 1.0
	}
	if r.ResponseFormat != nil {
		body["response_format"] = r.ResponseFormat
	}
	if r.TopP != nil {
		body["top_p"] = *r.TopP
	} else {
		body["top_p"] = 1.0
	}
	if r.FrequencyPenalty != nil {
		body["frequency_penalty"] = *r.FrequencyPenalty
	} else {
		body["frequency_penalty"] = 0.0
	}
	if r.PresencePenalty != nil {
		body["presence_penalty"] = *r.PresencePenalty
	} else {
		body["presence_penalty"] = 0.0
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
	if r.Logprobs != nil {
		body["logprobs"] = *r.Logprobs
	} else {
		body["logprobs"] = false
	}
	if r.TopLogprobs != 0 {
		body["top_logprobs"] = r.TopLogprobs
	}
	if r.StreamOptions != nil {
		body["stream_options"] = r.StreamOptions
	}
	if r.ParallelToolCalls != nil {
		body["parallel_tool_calls"] = *r.ParallelToolCalls
	} else {
		body["parallel_tool_calls"] = true
	}
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
	if r.Store != nil {
		body["store"] = *r.Store
	} else {
		body["store"] = false
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
	for k, v := range r.Extra {
		if _, exists := body[k]; !exists {
			body[k] = v
		}
	}
	return body
}

func (c *ClaudeChatCompletions) Create(ctx context.Context, req ClaudeChatCompletionRequest) (map[string]any, error) {
	body := req.toBody()
	delete(body, "stream")
	return c.t.do(ctx, requestOpts{Method: "POST", Path: "/v1/chat/completions", Body: body})
}

func (c *ClaudeChatCompletions) CreateStream(ctx context.Context, req ClaudeChatCompletionRequest) (<-chan map[string]any, <-chan error) {
	req.Stream = true
	return streamDecode(c.t, "/v1/chat/completions", req.toBody())
}

type ClaudeMessages struct{ t *transport }

// ClaudeMessageRequest is the input to claude.messages.create and count_tokens.
type ClaudeMessageRequest struct {
	Model         ClaudeModel
	Messages      []map[string]any
	MaxTokens     int
	Metadata      map[string]any
	StopSequences []string
	Stream        bool
	System        string
	Temperature   *float64
	ToolChoice    map[string]any
	Tools         []any
	TopK          int
	TopP          *float64
	Thinking      any
	Extra         map[string]any
}

func (r ClaudeMessageRequest) toBody() map[string]any {
	body := map[string]any{"model": string(r.Model), "messages": r.Messages, "max_tokens": r.MaxTokens, "stream": r.Stream}
	if r.Metadata != nil {
		body["metadata"] = r.Metadata
	}
	if r.StopSequences != nil {
		body["stop_sequences"] = r.StopSequences
	}
	if r.System != "" {
		body["system"] = r.System
	}
	if r.Temperature != nil {
		body["temperature"] = *r.Temperature
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
	if r.TopP != nil {
		body["top_p"] = *r.TopP
	}
	if r.Thinking != nil {
		body["thinking"] = r.Thinking
	}
	for k, v := range r.Extra {
		if _, exists := body[k]; !exists {
			body[k] = v
		}
	}
	return body
}

func (m *ClaudeMessages) Create(ctx context.Context, req ClaudeMessageRequest) (map[string]any, error) {
	body := req.toBody()
	delete(body, "stream")
	return m.t.do(ctx, requestOpts{Method: "POST", Path: "/v1/messages", Body: body})
}

func (m *ClaudeMessages) CreateStream(ctx context.Context, req ClaudeMessageRequest) (<-chan map[string]any, <-chan error) {
	req.Stream = true
	return streamDecode(m.t, "/v1/messages", req.toBody())
}

func (m *ClaudeMessages) CountTokens(ctx context.Context, req ClaudeMessageRequest) (map[string]any, error) {
	body := req.toBody()
	delete(body, "stream")
	delete(body, "max_tokens")
	return m.t.do(ctx, requestOpts{Method: "POST", Path: "/v1/messages/count_tokens", Body: body})
}
