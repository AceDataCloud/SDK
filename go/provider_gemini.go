package acedatacloud

import (
	"context"
	"net/url"
)

type GeminiChatModel string

const (
	GeminiChatModelGemini31Pro              GeminiChatModel = "gemini-3.1-pro"
	GeminiChatModelGemini30Pro              GeminiChatModel = "gemini-3.0-pro"
	GeminiChatModelGemini35Flash            GeminiChatModel = "gemini-3.5-flash"
	GeminiChatModelGemini3FlashPreview      GeminiChatModel = "gemini-3-flash-preview"
	GeminiChatModelGemini25Pro              GeminiChatModel = "gemini-2.5-pro"
	GeminiChatModelGemini25Flash            GeminiChatModel = "gemini-2.5-flash"
	GeminiChatModelGemini25FlashLite        GeminiChatModel = "gemini-2.5-flash-lite"
	GeminiChatModelGemini20Flash            GeminiChatModel = "gemini-2.0-flash"
	GeminiChatModelGemini31FlashLitePreview GeminiChatModel = "gemini-3.1-flash-lite-preview"
)

type GeminiContentModel string

const (
	GeminiContentModelGemini20Flash            GeminiContentModel = "gemini-2.0-flash"
	GeminiContentModelGemini25Flash            GeminiContentModel = "gemini-2.5-flash"
	GeminiContentModelGemini25FlashLite        GeminiContentModel = "gemini-2.5-flash-lite"
	GeminiContentModelGemini25Pro              GeminiContentModel = "gemini-2.5-pro"
	GeminiContentModelGemini3FlashPreview      GeminiContentModel = "gemini-3-flash-preview"
	GeminiContentModelGemini35Flash            GeminiContentModel = "gemini-3.5-flash"
	GeminiContentModelGemini30Pro              GeminiContentModel = "gemini-3.0-pro"
	GeminiContentModelGemini31Pro              GeminiContentModel = "gemini-3.1-pro"
	GeminiContentModelGemini31FlashLitePreview GeminiContentModel = "gemini-3.1-flash-lite-preview"
	GeminiContentModelGemini31FlashImage       GeminiContentModel = "gemini-3.1-flash-image"
	GeminiContentModelGemini25FlashImage       GeminiContentModel = "gemini-2.5-flash-image"
	GeminiContentModelGemini3ProImage          GeminiContentModel = "gemini-3-pro-image"
)

type GeminiVideoModel string

const GeminiVideoModelOmniFlash GeminiVideoModel = "omni-flash"

// Gemini is the gemini provider client.
type Gemini struct{ t *transport }

type GeminiChatCompletionRequest struct {
	Model               GeminiChatModel
	Messages            []map[string]any
	Stream              bool
	N                   float64
	MaxTokens           float64
	Temperature         *float64
	ResponseFormat      any
	TopP                *float64
	FrequencyPenalty    *float64
	PresencePenalty     *float64
	Seed                *int
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
	Tools               []map[string]any
	ToolChoice          any
	Extra               map[string]any
}

func (r GeminiChatCompletionRequest) toBody() map[string]any {
	body := map[string]any{
		"model":               string(r.Model),
		"messages":            r.Messages,
		"stream":              r.Stream,
		"n":                   1.0,
		"temperature":         1.0,
		"top_p":               1.0,
		"frequency_penalty":   0.0,
		"presence_penalty":    0.0,
		"logprobs":            false,
		"parallel_tool_calls": true,
		"reasoning_effort":    "medium",
		"service_tier":        "auto",
		"store":               false,
	}
	if r.N != 0 {
		body["n"] = r.N
	}
	if r.MaxTokens != 0 {
		body["max_tokens"] = r.MaxTokens
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
	if r.MaxCompletionTokens != 0 {
		body["max_completion_tokens"] = r.MaxCompletionTokens
	}
	if r.Logprobs != nil {
		body["logprobs"] = *r.Logprobs
	}
	if r.TopLogprobs != 0 {
		body["top_logprobs"] = r.TopLogprobs
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

type GeminiGenerateContentRequest struct {
	Model             GeminiContentModel
	Contents          []map[string]any
	SystemInstruction map[string]any
	GenerationConfig  map[string]any
	Tools             []map[string]any
	ToolConfig        map[string]any
	SafetySettings    []map[string]any
	Extra             map[string]any
}

func (r GeminiGenerateContentRequest) toBody() map[string]any {
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
	for k, v := range r.Extra {
		if _, exists := body[k]; !exists {
			body[k] = v
		}
	}
	return body
}

type GeminiVideoGenerateRequest struct {
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

func (r GeminiVideoGenerateRequest) toBody() map[string]any {
	body := map[string]any{
		"prompt":       r.Prompt,
		"model":        string(GeminiVideoModelOmniFlash),
		"aspect_ratio": "16:9",
		"resolution":   "720p",
		"async":        true,
	}
	if r.Model != "" {
		body["model"] = string(r.Model)
	}
	if r.AspectRatio != "" {
		body["aspect_ratio"] = r.AspectRatio
	}
	if r.Resolution != "" {
		body["resolution"] = r.Resolution
	}
	if r.ImageURLs != nil {
		body["image_urls"] = r.ImageURLs
	}
	if r.VideoURLs != nil {
		body["video_urls"] = r.VideoURLs
	}
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

func (g *Gemini) Chat() *GeminiChat     { return &GeminiChat{t: g.t} }
func (g *Gemini) Videos() *GeminiVideos { return &GeminiVideos{t: g.t} }
func (g *Gemini) Tasks() *GeminiTasks   { return &GeminiTasks{t: g.t} }

func (g *Gemini) GenerateContent(ctx context.Context, req GeminiGenerateContentRequest) (map[string]any, error) {
	path := "/v1beta/models/" + url.PathEscape(string(req.Model)) + ":generateContent"
	return g.t.do(ctx, requestOpts{Method: "POST", Path: path, Body: req.toBody()})
}

func (g *Gemini) StreamGenerateContent(ctx context.Context, req GeminiGenerateContentRequest) (<-chan map[string]any, <-chan error) {
	path := "/v1beta/models/" + url.PathEscape(string(req.Model)) + ":streamGenerateContent?alt=sse"
	return streamDecode(g.t, path, req.toBody())
}

type GeminiChat struct{ t *transport }

func (c *GeminiChat) Completions() *GeminiChatCompletions { return &GeminiChatCompletions{t: c.t} }

type GeminiChatCompletions struct{ t *transport }

func (c *GeminiChatCompletions) Create(ctx context.Context, req GeminiChatCompletionRequest) (map[string]any, error) {
	body := req.toBody()
	body["stream"] = false
	return c.t.do(ctx, requestOpts{Method: "POST", Path: "/gemini/chat/completions", Body: body})
}

func (c *GeminiChatCompletions) CreateStream(ctx context.Context, req GeminiChatCompletionRequest) (<-chan map[string]any, <-chan error) {
	req.Stream = true
	return streamDecode(c.t, "/gemini/chat/completions", req.toBody())
}

type GeminiVideos struct{ t *transport }

func (v *GeminiVideos) Generate(ctx context.Context, req GeminiVideoGenerateRequest) (*TaskHandle, error) {
	result, err := v.t.do(ctx, requestOpts{Method: "POST", Path: "/gemini/videos", Body: req.toBody()})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/gemini/tasks", v.t, result), nil
}

type GeminiTasks struct{ t *transport }

func (t *GeminiTasks) Retrieve(ctx context.Context, id string, extra map[string]any) (map[string]any, error) {
	body := map[string]any{"action": "retrieve", "id": id}
	for k, v := range extra {
		body[k] = v
	}
	return t.t.do(ctx, requestOpts{Method: "POST", Path: "/gemini/tasks", Body: body})
}

func (t *GeminiTasks) RetrieveBatch(ctx context.Context, ids []string, extra map[string]any) (map[string]any, error) {
	body := map[string]any{"action": "retrieve_batch"}
	if ids != nil {
		body["ids"] = ids
	}
	for k, v := range extra {
		body[k] = v
	}
	return t.t.do(ctx, requestOpts{Method: "POST", Path: "/gemini/tasks", Body: body})
}
