package acedatacloud

import "context"

// TwResource groups X/Twitter data endpoints.
type TwResource struct{ t *transport }

func (x *TwResource) Posts(ctx context.Context, userID string, extra map[string]any) (map[string]any, error) {
	body := withExtra(map[string]any{"user_id": userID}, extra)
	return x.t.do(ctx, requestOpts{Method: "POST", Path: "/x/posts", Body: body})
}

func (x *TwResource) Users(ctx context.Context, username string, extra map[string]any) (map[string]any, error) {
	body := withExtra(map[string]any{"username": username}, extra)
	return x.t.do(ctx, requestOpts{Method: "POST", Path: "/x/users", Body: body})
}

func (x *TwResource) Retweets(ctx context.Context, keyword string, extra map[string]any) (map[string]any, error) {
	body := withExtra(map[string]any{"keyword": keyword}, extra)
	return x.t.do(ctx, requestOpts{Method: "POST", Path: "/x/retweets", Body: body})
}
