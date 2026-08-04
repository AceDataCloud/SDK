package acedatacloud

import (
	"context"
	"errors"
	"net/url"
)

// GeminiResource groups the Gemini endpoints: the OpenAI-compatible chat
// surface, the async video endpoint, and Google's native v1beta calls.
type GeminiResource struct {
	t *transport
}

const (
	geminiChatPath   = "/gemini/chat/completions"
	geminiVideosPath = "/gemini/videos"
	geminiTasksPath  = "/gemini/tasks"
)

// Chat returns the chat sub-namespace.
func (g *GeminiResource) Chat() *GeminiChat { return &GeminiChat{t: g.t} }

// Videos returns the video-generation sub-namespace.
func (g *GeminiResource) Videos() *GeminiVideos { return &GeminiVideos{t: g.t} }

// GeminiChatRequest is the input to gemini.Chat().Completions().Create.
type GeminiChatRequest struct {
	Model    string           `json:"model"`
	Messages []map[string]any `json:"messages"`
	Stream   bool             `json:"stream,omitempty"`
	// Extra is merged into the request body for fields the SDK does not model.
	Extra map[string]any `json:"-"`
}

func (r GeminiChatRequest) toBody() map[string]any {
	body := map[string]any{"model": r.Model, "messages": r.Messages}
	if r.Stream {
		body["stream"] = true
	}
	for k, v := range r.Extra {
		if _, exists := body[k]; !exists {
			body[k] = v
		}
	}
	return body
}

// GeminiChat exposes "/gemini/chat/completions".
type GeminiChat struct{ t *transport }

// Completions returns the completions sub-namespace.
func (c *GeminiChat) Completions() *GeminiCompletions { return &GeminiCompletions{t: c.t} }

// GeminiCompletions performs chat completion calls.
type GeminiCompletions struct{ t *transport }

// Create performs a blocking chat completion.
func (c *GeminiCompletions) Create(ctx context.Context, req GeminiChatRequest) (map[string]any, error) {
	body := req.toBody()
	delete(body, "stream")
	return c.t.do(ctx, requestOpts{Method: "POST", Path: geminiChatPath, Body: body})
}

// CreateStream performs a streaming chat completion.
func (c *GeminiCompletions) CreateStream(ctx context.Context, req GeminiChatRequest) (<-chan map[string]any, <-chan error) {
	req.Stream = true
	return streamDecode(c.t, geminiChatPath, req.toBody())
}

// GeminiVideoRequest is the input to gemini.Videos().Generate.
type GeminiVideoRequest struct {
	// Prompt describing the video to generate.
	Prompt string
	// Model defaults to "omni-flash".
	Model string
	// AspectRatio is "16:9" or "9:16"; defaults to "16:9".
	AspectRatio string
	// Resolution is "720p" or "1080p"; defaults to "720p".
	Resolution string
	// ImageURLs are reference images.
	ImageURLs []string
	// VideoURLs accepts at most one reference video.
	VideoURLs []string
	// Async submits without blocking; poll the returned handle. Defaults true.
	Async *bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r GeminiVideoRequest) toBody() (map[string]any, error) {
	if len(r.VideoURLs) > 1 {
		return nil, errors.New("acedatacloud: VideoURLs accepts at most 1 video URL")
	}
	body := map[string]any{"prompt": r.Prompt}
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
	return body, nil
}

// GeminiVideos exposes "/gemini/videos".
type GeminiVideos struct{ t *transport }

// Generate submits a video generation task and returns a pollable handle.
func (v *GeminiVideos) Generate(ctx context.Context, req GeminiVideoRequest) (*TaskHandle, error) {
	body, err := req.toBody()
	if err != nil {
		return nil, err
	}
	result, err := v.t.do(ctx, requestOpts{Method: "POST", Path: geminiVideosPath, Body: body})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), geminiTasksPath, v.t, result), nil
}

// GeminiGenerateContentRequest is the input to the native v1beta calls.
type GeminiGenerateContentRequest struct {
	// Model is interpolated into the request path.
	Model string
	// Contents is the native Gemini conversation payload.
	Contents []map[string]any
	// Extra fields (generationConfig, tools, systemInstruction, ...).
	Extra map[string]any
}

func (r GeminiGenerateContentRequest) toBody() map[string]any {
	body := map[string]any{"contents": r.Contents}
	for k, v := range r.Extra {
		if _, exists := body[k]; !exists {
			body[k] = v
		}
	}
	return body
}

func geminiNativePath(model string, stream bool) string {
	action := "generateContent"
	if stream {
		action = "streamGenerateContent"
	}
	return "/v1beta/models/" + url.PathEscape(model) + ":" + action
}

// GenerateContent calls "POST /v1beta/models/{model}:generateContent".
func (g *GeminiResource) GenerateContent(ctx context.Context, req GeminiGenerateContentRequest) (map[string]any, error) {
	if req.Model == "" {
		return nil, errors.New("acedatacloud: Model is required")
	}
	return g.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   geminiNativePath(req.Model, false),
		Body:   req.toBody(),
	})
}

// StreamGenerateContent calls "POST /v1beta/models/{model}:streamGenerateContent".
func (g *GeminiResource) StreamGenerateContent(ctx context.Context, req GeminiGenerateContentRequest) (<-chan map[string]any, <-chan error) {
	if req.Model == "" {
		errCh := make(chan error, 1)
		errCh <- errors.New("acedatacloud: Model is required")
		close(errCh)
		out := make(chan map[string]any)
		close(out)
		return out, errCh
	}
	return streamDecode(g.t, geminiNativePath(req.Model, true), req.toBody())
}
