// Code generated from the platform OpenAPI spec. DO NOT EDIT.
// Regenerate with: python scripts/generate_providers.py

package acedatacloud

import "context"

// Tiktok is the tiktok provider client.
type Tiktok struct {
	t *transport
}

// TiktokPostsRequest is the input to tiktok.Posts.
type TiktokPostsRequest struct {
	// Tiktok Posts Cursor
	Cursor string
	// Tiktok Posts User Id
	UserID string
	// Tiktok Posts Unique Id
	UniqueID string
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r TiktokPostsRequest) toBody() map[string]any {
	body := map[string]any{}
	if r.Cursor != "" {
		body["cursor"] = r.Cursor
	}
	if r.UserID != "" {
		body["user_id"] = r.UserID
	}
	if r.UniqueID != "" {
		body["unique_id"] = r.UniqueID
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

// Posts Get a TikTok user's work based on their unique id.
func (c *Tiktok) Posts(ctx context.Context, req TiktokPostsRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/tiktok/posts",
		Body:   req.toBody(),
	})
}

// TiktokSearchRequest is the input to tiktok.Search.
type TiktokSearchRequest struct {
	// Tiktok Search Type
	Type string
	// Tiktok Search Keywords
	Keywords string
	// Tiktok Search Cursor
	Cursor int
	// Tiktok Search Region
	Region string
	// Tiktok Search Sort Type
	SortType int
	// Tiktok Search Publish Time
	PublishTime int
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r TiktokSearchRequest) toBody() map[string]any {
	body := map[string]any{}
	body["type"] = r.Type
	body["keywords"] = r.Keywords
	if r.Cursor != 0 {
		body["cursor"] = r.Cursor
	}
	if r.Region != "" {
		body["region"] = r.Region
	}
	if r.SortType != 0 {
		body["sort_type"] = r.SortType
	}
	if r.PublishTime != 0 {
		body["publish_time"] = r.PublishTime
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

// Search Search TikTok users and video resources by keyword.
func (c *Tiktok) Search(ctx context.Context, req TiktokSearchRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/tiktok/search",
		Body:   req.toBody(),
	})
}

// TiktokUserRequest is the input to tiktok.User.
type TiktokUserRequest struct {
	// Tiktok User Cursor
	Cursor string
	// Tiktok User User Id
	UserID string
	// Tiktok User Unique Id
	UniqueID string
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r TiktokUserRequest) toBody() map[string]any {
	body := map[string]any{}
	if r.Cursor != "" {
		body["cursor"] = r.Cursor
	}
	if r.UserID != "" {
		body["user_id"] = r.UserID
	}
	if r.UniqueID != "" {
		body["unique_id"] = r.UniqueID
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

// User Get user details based on a TikTok user's unique id.
func (c *Tiktok) User(ctx context.Context, req TiktokUserRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/tiktok/user",
		Body:   req.toBody(),
	})
}

// TiktokVideoRequest is the input to tiktok.Video.
type TiktokVideoRequest struct {
	// Tiktok Video Video Url
	VideoURL string
	// Tiktok Video Original Quality
	OriginalQuality int
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r TiktokVideoRequest) toBody() map[string]any {
	body := map[string]any{}
	body["video_url"] = r.VideoURL
	if r.OriginalQuality != 0 {
		body["original_quality"] = r.OriginalQuality
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

// Video Follow the link to the video on TikTok for more details.
func (c *Tiktok) Video(ctx context.Context, req TiktokVideoRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/tiktok/video",
		Body:   req.toBody(),
	})
}
