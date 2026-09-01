package acedatacloud

import "context"

// GeminiChatCompletionRequest is the input to GeminiChatCompletions.
type GeminiChatCompletionRequest struct {
	Model    string           `json:"model"`
	Messages []map[string]any `json:"messages"`
	Stream   bool             `json:"stream,omitempty"`
	Extra    map[string]any   `json:"-"`
}

func (r GeminiChatCompletionRequest) toBody() map[string]any {
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

// GeminiVideoRequest is the input to GeminiVideo.
type GeminiVideoRequest struct {
	Prompt      string
	Model       string
	AspectRatio string
	Resolution  string
	ImageURLs   []string
	VideoURLs   []string
	Async       *bool
	CallbackURL string
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
	if r.Async != nil {
		body["async"] = *r.Async
	}
	if r.CallbackURL != "" {
		body["callback_url"] = r.CallbackURL
	}
	return body
}

// GeminiResource groups Gemini endpoints.
type GeminiResource struct{ t *transport }

// ChatCompletions calls POST /gemini/chat/completions.
func (g *GeminiResource) ChatCompletions(ctx context.Context, req GeminiChatCompletionRequest) (map[string]any, error) {
	return g.t.do(ctx, requestOpts{Method: "POST", Path: "/gemini/chat/completions", Body: req.toBody()})
}

// GenerateContent calls Gemini's native generateContent endpoint.
func (g *GeminiResource) GenerateContent(ctx context.Context, model string, contents []map[string]any, extra map[string]any) (map[string]any, error) {
	body := map[string]any{"contents": contents}
	for k, v := range extra {
		body[k] = v
	}
	return g.t.do(ctx, requestOpts{Method: "POST", Path: "/v1beta/models/" + model + ":generateContent", Body: body})
}

// StreamGenerateContent calls Gemini's native streamGenerateContent endpoint.
func (g *GeminiResource) StreamGenerateContent(ctx context.Context, model string, contents []map[string]any, extra map[string]any) (map[string]any, error) {
	body := map[string]any{"contents": contents}
	for k, v := range extra {
		body[k] = v
	}
	return g.t.do(ctx, requestOpts{Method: "POST", Path: "/v1beta/models/" + model + ":streamGenerateContent", Body: body})
}

// GenerateVideo submits a Gemini video request and returns its task handle.
func (g *GeminiResource) GenerateVideo(ctx context.Context, req GeminiVideoRequest) (*TaskHandle, error) {
	result, err := g.t.do(ctx, requestOpts{Method: "POST", Path: "/gemini/videos", Body: req.toBody()})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/gemini/tasks", g.t, result), nil
}

// Tasks calls POST /gemini/tasks.
func (g *GeminiResource) Tasks(ctx context.Context, id string, ids []string, action string) (map[string]any, error) {
	if action == "" {
		action = "retrieve"
	}
	body := map[string]any{"action": action}
	if id != "" {
		body["id"] = id
	}
	if ids != nil {
		body["ids"] = ids
	}
	return g.t.do(ctx, requestOpts{Method: "POST", Path: "/gemini/tasks", Body: body})
}
