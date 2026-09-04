// Code generated from the platform OpenAPI spec. DO NOT EDIT.
// Regenerate with: python scripts/generate_providers.py

package acedatacloud

import (
	"context"
	"fmt"
	"net/url"
	"strings"
)

// Gemini is the gemini provider client.
type Gemini struct {
	t *transport
}

// GeminiCompletionsRequest is the input to gemini.Completions.
type GeminiCompletionsRequest struct {
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

func (r GeminiCompletionsRequest) toBody() map[string]any {
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
	body["response_format"] = r.ResponseFormat
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

// Completions Gemini Chat Completions
func (c *Gemini) Completions(ctx context.Context, req GeminiCompletionsRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/gemini/chat/completions",
		Body:   req.toBody(),
	})
}

// GeminiModelGeneratecontentRequest is the input to gemini.Model_Generatecontent.
type GeminiModelGeneratecontentRequest struct {
	// V1Beta Models Model Generatecontent Contents
	Contents []map[string]any
	// required
	Model string
	// V1Beta Models Model Generatecontent Systeminstruction
	Systeminstruction map[string]any
	// V1Beta Models Model Generatecontent Generationconfig
	Generationconfig map[string]any
	// V1Beta Models Model Generatecontent Tools
	Tools []map[string]any
	// V1Beta Models Model Generatecontent Toolconfig
	Toolconfig map[string]any
	// V1Beta Models Model Generatecontent Safetysettings
	Safetysettings []map[string]any
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r GeminiModelGeneratecontentRequest) toBody() map[string]any {
	body := map[string]any{}
	body["contents"] = r.Contents
	if r.Systeminstruction != nil {
		body["systemInstruction"] = r.Systeminstruction
	}
	if r.Generationconfig != nil {
		body["generationConfig"] = r.Generationconfig
	}
	if r.Tools != nil {
		body["tools"] = r.Tools
	}
	if r.Toolconfig != nil {
		body["toolConfig"] = r.Toolconfig
	}
	if r.Safetysettings != nil {
		body["safetySettings"] = r.Safetysettings
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

// ModelGeneratecontent Gemini Generate Content
func (c *Gemini) ModelGeneratecontent(ctx context.Context, req GeminiModelGeneratecontentRequest) (map[string]any, error) {
	path := "/v1beta/models/{model}:generateContent"
	path = strings.ReplaceAll(path, "{model}", url.PathEscape(fmt.Sprint(req.Model)))
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   path,
		Body:   req.toBody(),
	})
}

// GeminiModelStreamgeneratecontentRequest is the input to gemini.Model_Streamgeneratecontent.
type GeminiModelStreamgeneratecontentRequest struct {
	// V1Beta Models Model Generatecontent Contents
	Contents []map[string]any
	// required
	Model string
	// V1Beta Models Model Generatecontent Systeminstruction
	Systeminstruction map[string]any
	// V1Beta Models Model Generatecontent Generationconfig
	Generationconfig map[string]any
	// V1Beta Models Model Generatecontent Tools
	Tools []map[string]any
	// V1Beta Models Model Generatecontent Toolconfig
	Toolconfig map[string]any
	// V1Beta Models Model Generatecontent Safetysettings
	Safetysettings []map[string]any
	// optional
	Alt string
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r GeminiModelStreamgeneratecontentRequest) toBody() map[string]any {
	body := map[string]any{}
	body["contents"] = r.Contents
	if r.Systeminstruction != nil {
		body["systemInstruction"] = r.Systeminstruction
	}
	if r.Generationconfig != nil {
		body["generationConfig"] = r.Generationconfig
	}
	if r.Tools != nil {
		body["tools"] = r.Tools
	}
	if r.Toolconfig != nil {
		body["toolConfig"] = r.Toolconfig
	}
	if r.Safetysettings != nil {
		body["safetySettings"] = r.Safetysettings
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

func (r GeminiModelStreamgeneratecontentRequest) toQuery() url.Values {
	query := url.Values{}
	if r.Alt != "" {
		query.Set("alt", fmt.Sprint(r.Alt))
	}
	return query
}

// ModelStreamgeneratecontent Gemini Stream Generate Content
func (c *Gemini) ModelStreamgeneratecontent(ctx context.Context, req GeminiModelStreamgeneratecontentRequest) (map[string]any, error) {
	path := "/v1beta/models/{model}:streamGenerateContent"
	path = strings.ReplaceAll(path, "{model}", url.PathEscape(fmt.Sprint(req.Model)))
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   path,
		Body:   req.toBody(),
		Query:  req.toQuery(),
	})
}

// GeminiGenerateRequest is the input to gemini.Generate.
type GeminiGenerateRequest struct {
	// Gemini Videos Prompt
	Prompt string
	// Gemini Videos Model
	Model string
	// Gemini Videos Aspect Ratio
	AspectRatio string
	// Gemini Videos Resolution
	Resolution string
	// Gemini Videos Image Urls
	ImageURLs []string
	// Gemini Videos Video Urls
	VideoURLs []string
	// Async submits without blocking; poll the returned handle. Defaults true.
	Async *bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r GeminiGenerateRequest) toBody() map[string]any {
	body := map[string]any{}
	body["prompt"] = r.Prompt
	if r.Model != "" {
		body["model"] = r.Model
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

// Generate Gemini Videos
func (c *Gemini) Generate(ctx context.Context, req GeminiGenerateRequest) (*TaskHandle, error) {
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
