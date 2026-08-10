package acedatacloud

import "context"

// GeminiModel is a supported Gemini chat model.
type GeminiModel string

const (
	Gemini31Pro              GeminiModel = "gemini-3.1-pro"
	Gemini30Pro              GeminiModel = "gemini-3.0-pro"
	Gemini36Flash            GeminiModel = "gemini-3.6-flash"
	Gemini35Flash            GeminiModel = "gemini-3.5-flash"
	Gemini3FlashPreview      GeminiModel = "gemini-3-flash-preview"
	Gemini25Pro              GeminiModel = "gemini-2.5-pro"
	Gemini25Flash            GeminiModel = "gemini-2.5-flash"
	Gemini25FlashLite        GeminiModel = "gemini-2.5-flash-lite"
	Gemini20Flash            GeminiModel = "gemini-2.0-flash"
	Gemini31FlashLitePreview GeminiModel = "gemini-3.1-flash-lite-preview"
)

// GeminiResource provides Gemini's chat, content, and video APIs.
type GeminiResource struct{ t *transport }

// GeminiChatCompletionRequest is the input to GeminiChatCompletion.
type GeminiChatCompletionRequest struct {
	Model    GeminiModel
	Messages []map[string]any
	Stream   bool
	Extra    map[string]any
}

// ChatCompletion creates a Gemini chat completion.
func (g *GeminiResource) ChatCompletion(ctx context.Context, req GeminiChatCompletionRequest) (map[string]any, error) {
	body := map[string]any{"model": req.Model, "messages": req.Messages}
	if req.Stream {
		body["stream"] = true
	}
	for k, v := range req.Extra {
		if _, exists := body[k]; !exists {
			body[k] = v
		}
	}
	return g.t.do(ctx, requestOpts{Method: "POST", Path: "/gemini/chat/completions", Body: body})
}

// GenerateContent invokes Gemini's generateContent API.
func (g *GeminiResource) GenerateContent(ctx context.Context, model string, contents []map[string]any, extra map[string]any) (map[string]any, error) {
	body := map[string]any{"contents": contents}
	for k, v := range extra {
		body[k] = v
	}
	return g.t.do(ctx, requestOpts{Method: "POST", Path: "/v1beta/models/" + model + ":generateContent", Body: body})
}

// GeminiVideoRequest is the input to Gemini video generation.
type GeminiVideoRequest struct {
	Prompt, Model, AspectRatio, Resolution, CallbackURL string
	ImageURLs, VideoURLs                                []string
	Async                                               *bool
}

func (r GeminiVideoRequest) toBody() map[string]any {
	body := map[string]any{"prompt": r.Prompt, "model": "omni-flash", "aspect_ratio": "16:9", "resolution": "720p", "async": true}
	if r.Model != "" {
		body["model"] = r.Model
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
	if r.CallbackURL != "" {
		body["callback_url"] = r.CallbackURL
	}
	if r.Async != nil {
		body["async"] = *r.Async
	}
	return body
}

// Generate submits a Gemini video task.
func (g *GeminiResource) Generate(ctx context.Context, req GeminiVideoRequest) (*TaskHandle, error) {
	result, err := g.t.do(ctx, requestOpts{Method: "POST", Path: "/gemini/videos", Body: req.toBody()})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/gemini/tasks", g.t, result), nil
}
