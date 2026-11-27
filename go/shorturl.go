package acedatacloud

import "context"

// ShortURLResource exposes the short URL endpoint (“/shorturl“).
type ShortURLResource struct{ t *transport }

// Create shortens a URL. slug is optional (pass "" for an auto slug);
// extra is merged into the request body for forward-compatible fields.
func (s *ShortURLResource) Create(ctx context.Context, url, slug string, extra map[string]any) (map[string]any, error) {
	body := map[string]any{"url": url}
	if slug != "" {
		body["slug"] = slug
	}
	for k, v := range extra {
		if _, ok := body[k]; !ok {
			body[k] = v
		}
	}
	return s.t.do(ctx, requestOpts{Method: "POST", Path: "/shorturl", Body: body})
}
