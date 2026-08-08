package acedatacloud

import (
	"context"
	"net/url"
)

// Gemini is the gemini provider client.
type Gemini struct{ t *transport }

type GeminiChatModel string
type GeminiNativeModel string
type GeminiVideoModel string

const (
	Gemini31Pro              GeminiChatModel = "gemini-3.1-pro"
	Gemini30Pro              GeminiChatModel = "gemini-3.0-pro"
	Gemini35Flash            GeminiChatModel = "gemini-3.5-flash"
	Gemini3FlashPreview      GeminiChatModel = "gemini-3-flash-preview"
	Gemini25Pro              GeminiChatModel = "gemini-2.5-pro"
	Gemini25Flash            GeminiChatModel = "gemini-2.5-flash"
	Gemini25FlashLite        GeminiChatModel = "gemini-2.5-flash-lite"
	Gemini20Flash            GeminiChatModel = "gemini-2.0-flash"
	Gemini31FlashLitePreview GeminiChatModel = "gemini-3.1-flash-lite-preview"

	GeminiNative20Flash            GeminiNativeModel = "gemini-2.0-flash"
	GeminiNative25Flash            GeminiNativeModel = "gemini-2.5-flash"
	GeminiNative25FlashLite        GeminiNativeModel = "gemini-2.5-flash-lite"
	GeminiNative25Pro              GeminiNativeModel = "gemini-2.5-pro"
	GeminiNative3FlashPreview      GeminiNativeModel = "gemini-3-flash-preview"
	GeminiNative35Flash            GeminiNativeModel = "gemini-3.5-flash"
	GeminiNative30Pro              GeminiNativeModel = "gemini-3.0-pro"
	GeminiNative31Pro              GeminiNativeModel = "gemini-3.1-pro"
	GeminiNative31FlashLitePreview GeminiNativeModel = "gemini-3.1-flash-lite-preview"
	GeminiNative31FlashImage       GeminiNativeModel = "gemini-3.1-flash-image"
	GeminiNative25FlashImage       GeminiNativeModel = "gemini-2.5-flash-image"
	GeminiNative3ProImage          GeminiNativeModel = "gemini-3-pro-image"
	GeminiVideoOmniFlash           GeminiVideoModel  = "omni-flash"
)

func (g *Gemini) Chat() *GeminiChat     { return &GeminiChat{t: g.t} }
func (g *Gemini) Videos() *GeminiVideos { return &GeminiVideos{t: g.t} }

type GeminiChat struct{ t *transport }

func (g *GeminiChat) Completions() *GeminiChatCompletions { return &GeminiChatCompletions{t: g.t} }

type GeminiChatCompletions struct{ t *transport }

type GeminiChatCompletionRequest struct {
	Model               GeminiChatModel
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

func (r GeminiChatCompletionRequest) toBody() map[string]any {
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

func (c *GeminiChatCompletions) Create(ctx context.Context, req GeminiChatCompletionRequest) (map[string]any, error) {
	body := req.toBody()
	delete(body, "stream")
	return c.t.do(ctx, requestOpts{Method: "POST", Path: "/gemini/chat/completions", Body: body})
}

func (c *GeminiChatCompletions) CreateStream(ctx context.Context, req GeminiChatCompletionRequest) (<-chan map[string]any, <-chan error) {
	req.Stream = true
	return streamDecode(c.t, "/gemini/chat/completions", req.toBody())
}

type GeminiVideos struct{ t *transport }

type GeminiVideoRequest struct {
	Prompt      string
	Model       GeminiVideoModel
	AspectRatio string
	Resolution  string
	ImageURLs   []string
	VideoURLs   []string
	Async       *bool
	CallbackURL string
	Extra       map[string]any
}

func (r GeminiVideoRequest) toBody() map[string]any {
	body := map[string]any{"prompt": r.Prompt}
	if r.Model != "" {
		body["model"] = string(r.Model)
	} else {
		body["model"] = "omni-flash"
	}
	if r.AspectRatio != "" {
		body["aspect_ratio"] = r.AspectRatio
	} else {
		body["aspect_ratio"] = "16:9"
	}
	if r.Resolution != "" {
		body["resolution"] = r.Resolution
	} else {
		body["resolution"] = "720p"
	}
	if r.ImageURLs != nil {
		body["image_urls"] = r.ImageURLs
	}
	if r.VideoURLs != nil {
		body["video_urls"] = r.VideoURLs
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

func (v *GeminiVideos) Generate(ctx context.Context, req GeminiVideoRequest) (*TaskHandle, error) {
	result, err := v.t.do(ctx, requestOpts{Method: "POST", Path: "/gemini/videos", Body: req.toBody()})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/gemini/tasks", v.t, result), nil
}

type GeminiContentRequest struct {
	Model             GeminiNativeModel
	Contents          []map[string]any
	SystemInstruction map[string]any
	GenerationConfig  map[string]any
	Tools             []any
	ToolConfig        map[string]any
	SafetySettings    []any
	CachedContent     string
	Extra             map[string]any
}

func (r GeminiContentRequest) toBody() map[string]any {
	body := map[string]any{"contents": r.Contents}
	if r.SystemInstruction != nil {
		body["systemInstruction"] = r.SystemInstruction
	}
	if r.GenerationConfig != nil {
		body["generationConfig"] = r.GenerationConfig
	}
	if r.Tools != nil {
		body["tools"] = r.Tools
	}
	if r.ToolConfig != nil {
		body["toolConfig"] = r.ToolConfig
	}
	if r.SafetySettings != nil {
		body["safetySettings"] = r.SafetySettings
	}
	if r.CachedContent != "" {
		body["cachedContent"] = r.CachedContent
	}
	for k, v := range r.Extra {
		if _, exists := body[k]; !exists {
			body[k] = v
		}
	}
	return body
}

func (g *Gemini) GenerateContent(ctx context.Context, req GeminiContentRequest) (map[string]any, error) {
	path := "/v1beta/models/" + url.PathEscape(string(req.Model)) + ":generateContent"
	return g.t.do(ctx, requestOpts{Method: "POST", Path: path, Body: req.toBody()})
}

func (g *Gemini) StreamGenerateContent(ctx context.Context, req GeminiContentRequest) (<-chan map[string]any, <-chan error) {
	path := "/v1beta/models/" + url.PathEscape(string(req.Model)) + ":streamGenerateContent?alt=sse"
	return streamDecode(g.t, path, req.toBody())
}
