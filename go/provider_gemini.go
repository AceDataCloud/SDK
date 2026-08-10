package acedatacloud

import (
	"context"
)

type Gemini struct{ t *transport }

type GeminiChatRequest struct {
	Model    string
	Messages []map[string]any
	Stream   bool
	Extra    map[string]any
}

func (r GeminiChatRequest) toBody() map[string]any {
	body := map[string]any{"model": r.Model, "messages": r.Messages}
	if r.Stream {
		body["stream"] = true
	}
	for key, value := range r.Extra {
		if _, exists := body[key]; !exists {
			body[key] = value
		}
	}
	return body
}

type GeminiChat struct{ t *transport }
type GeminiChatCompletions struct{ t *transport }

func (g *Gemini) Chat() *GeminiChat { return &GeminiChat{t: g.t} }
func (g *GeminiChat) Completions() *GeminiChatCompletions {
	return &GeminiChatCompletions{t: g.t}
}

func (g *GeminiChatCompletions) Create(ctx context.Context, req GeminiChatRequest) (map[string]any, error) {
	body := req.toBody()
	delete(body, "stream")
	return g.t.do(ctx, requestOpts{Method: "POST", Path: "/gemini/chat/completions", Body: body})
}

func (g *GeminiChatCompletions) CreateStream(ctx context.Context, req GeminiChatRequest) (<-chan map[string]any, <-chan error) {
	req.Stream = true
	return streamDecode(g.t, "/gemini/chat/completions", req.toBody())
}

type GeminiContentRequest struct {
	Contents []map[string]any
	Extra    map[string]any
}

func (r GeminiContentRequest) toBody() map[string]any {
	body := map[string]any{"contents": r.Contents}
	for key, value := range r.Extra {
		if _, exists := body[key]; !exists {
			body[key] = value
		}
	}
	return body
}

func (g *Gemini) GenerateContent(ctx context.Context, model string, req GeminiContentRequest) (map[string]any, error) {
	return g.t.do(ctx, requestOpts{
		Method: "POST", Path: "/v1beta/models/" + model + ":generateContent", Body: req.toBody(),
	})
}

func (g *Gemini) StreamGenerateContent(
	ctx context.Context, model string, req GeminiContentRequest,
) (<-chan map[string]any, <-chan error) {
	return streamDecode(g.t, "/v1beta/models/"+model+":streamGenerateContent", req.toBody())
}

type GeminiVideosRequest struct {
	Prompt      string
	Model       string
	AspectRatio string
	Resolution  string
	ImageURLs   []string
	VideoURLs   []string
	Async       *bool
	CallbackURL string
}

func (r GeminiVideosRequest) toBody() map[string]any {
	body := map[string]any{
		"prompt":       r.Prompt,
		"model":        "omni-flash",
		"aspect_ratio": "16:9",
		"resolution":   "720p",
		"async":        true,
	}
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

func (g *Gemini) Videos(ctx context.Context, req GeminiVideosRequest) (*TaskHandle, error) {
	result, err := g.t.do(ctx, requestOpts{Method: "POST", Path: "/gemini/videos", Body: req.toBody()})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/gemini/tasks", g.t, result), nil
}
