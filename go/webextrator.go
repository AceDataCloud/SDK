package acedatacloud

import "context"

// WebExtratorResource groups web extraction endpoints.
type WebExtratorResource struct{ t *transport }

func (w *WebExtratorResource) Extract(ctx context.Context, url string, extra map[string]any) (map[string]any, error) {
	body := withExtra(map[string]any{"url": url}, extra)
	return w.t.do(ctx, requestOpts{Method: "POST", Path: "/webextrator/extract", Body: body})
}

func (w *WebExtratorResource) Render(ctx context.Context, url string, extra map[string]any) (map[string]any, error) {
	body := withExtra(map[string]any{"url": url}, extra)
	return w.t.do(ctx, requestOpts{Method: "POST", Path: "/webextrator/render", Body: body})
}

func withExtra(body map[string]any, extra map[string]any) map[string]any {
	for k, v := range extra {
		if _, ok := body[k]; !ok {
			body[k] = v
		}
	}
	return body
}
