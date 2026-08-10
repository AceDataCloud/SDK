package acedatacloud

import "context"

// TiktokResource groups TikTok data endpoints.
type TiktokResource struct{ t *transport }

func (t *TiktokResource) Posts(ctx context.Context, body map[string]any) (map[string]any, error) {
	return t.t.do(ctx, requestOpts{Method: "POST", Path: "/tiktok/posts", Body: body})
}

func (t *TiktokResource) Search(ctx context.Context, body map[string]any) (map[string]any, error) {
	return t.t.do(ctx, requestOpts{Method: "POST", Path: "/tiktok/search", Body: body})
}

func (t *TiktokResource) User(ctx context.Context, body map[string]any) (map[string]any, error) {
	return t.t.do(ctx, requestOpts{Method: "POST", Path: "/tiktok/user", Body: body})
}

func (t *TiktokResource) Video(ctx context.Context, videoURL string, extra map[string]any) (map[string]any, error) {
	body := withExtra(map[string]any{"video_url": videoURL}, extra)
	return t.t.do(ctx, requestOpts{Method: "POST", Path: "/tiktok/video", Body: body})
}
