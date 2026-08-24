package acedatacloud

import "context"

// GLMResource exposes GLM chat completions.
type GLMResource struct{ t *transport }

// Chat returns the GLM chat namespace.
func (g *GLMResource) Chat() *GLMChat { return &GLMChat{t: g.t} }

// GLMChat exposes /glm/chat/completions.
type GLMChat struct{ t *transport }

// Completions returns the completions sub-namespace.
func (c *GLMChat) Completions() *GLMChatCompletions { return &GLMChatCompletions{t: c.t} }

// GLMChatCompletions exposes glm chat.completions.create.
type GLMChatCompletions struct{ t *transport }

// GLMChatCompletionRequest is the input to glm.chat.completions.create.
type GLMChatCompletionRequest struct {
	Model               string
	Messages            []map[string]any
	N                   *float64
	Stream              bool
	MaxTokens           *float64
	Temperature         *float64
	ResponseFormat      map[string]any
	TopP                *float64
	FrequencyPenalty    *float64
	PresencePenalty     *float64
	Seed                *int
	Stop                any
	MaxCompletionTokens *int
	Logprobs            *bool
	TopLogprobs         *int
	StreamOptions       map[string]any
	ParallelToolCalls   *bool
	User                string
	ReasoningEffort     string
	ServiceTier         string
	Store               *bool
	Metadata            map[string]string
	LogitBias           map[string]int
	Modalities          []string
	Audio               map[string]any
	Prediction          map[string]any
	WebSearchOptions    map[string]any
	Tools               []map[string]any
	ToolChoice          any
	Extra               map[string]any
}

func (r GLMChatCompletionRequest) toBody() map[string]any {
	body := map[string]any{
		"model":    r.Model,
		"messages": r.Messages,
	}
	if r.N != nil {
		body["n"] = *r.N
	}
	if r.Stream {
		body["stream"] = true
	}
	if r.MaxTokens != nil {
		body["max_tokens"] = *r.MaxTokens
	}
	if r.Temperature != nil {
		body["temperature"] = *r.Temperature
	}
	if r.ResponseFormat != nil {
		body["response_format"] = r.ResponseFormat
	}
	if r.TopP != nil {
		body["top_p"] = *r.TopP
	}
	if r.FrequencyPenalty != nil {
		body["frequency_penalty"] = *r.FrequencyPenalty
	}
	if r.PresencePenalty != nil {
		body["presence_penalty"] = *r.PresencePenalty
	}
	if r.Seed != nil {
		body["seed"] = *r.Seed
	}
	if r.Stop != nil {
		body["stop"] = r.Stop
	}
	if r.MaxCompletionTokens != nil {
		body["max_completion_tokens"] = *r.MaxCompletionTokens
	}
	if r.Logprobs != nil {
		body["logprobs"] = *r.Logprobs
	}
	if r.TopLogprobs != nil {
		body["top_logprobs"] = *r.TopLogprobs
	}
	if r.StreamOptions != nil {
		body["stream_options"] = r.StreamOptions
	}
	if r.ParallelToolCalls != nil {
		body["parallel_tool_calls"] = *r.ParallelToolCalls
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
	if r.Store != nil {
		body["store"] = *r.Store
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

// Create performs a blocking (non-streaming) GLM chat completion.
func (c *GLMChatCompletions) Create(ctx context.Context, req GLMChatCompletionRequest) (map[string]any, error) {
	body := req.toBody()
	delete(body, "stream")
	return c.t.do(ctx, requestOpts{Method: "POST", Path: "/glm/chat/completions", Body: body})
}

// CreateStream performs a streaming GLM chat completion.
func (c *GLMChatCompletions) CreateStream(ctx context.Context, req GLMChatCompletionRequest) (<-chan map[string]any, <-chan error) {
	req.Stream = true
	return streamDecode(c.t, "/glm/chat/completions", req.toBody())
}
