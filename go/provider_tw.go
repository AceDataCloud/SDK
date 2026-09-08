// Code generated from the platform OpenAPI spec. DO NOT EDIT.
// Regenerate with: python scripts/generate_providers.py

package acedatacloud

import "context"

// Tw is the tw provider client.
type Tw struct {
	t *transport
}

// TwCommentsRequest is the input to tw.Comments.
type TwCommentsRequest struct {
	// X Comments Note Id
	NoteID string
	// X Comments Cursor
	Cursor string
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r TwCommentsRequest) toBody() map[string]any {
	body := map[string]any{}
	body["note_id"] = r.NoteID
	if r.Cursor != "" {
		body["cursor"] = r.Cursor
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

// Comments Get all the comment information for a tweet by entering the id of the tweet.
func (c *Tw) Comments(ctx context.Context, req TwCommentsRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/x/comments",
		Body:   req.toBody(),
	})
}

// TwSearchRequest is the input to tw.Search.
type TwSearchRequest struct {
	// X Search Keyword
	Keyword string
	// X Search Cursor
	Cursor string
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r TwSearchRequest) toBody() map[string]any {
	body := map[string]any{}
	body["keyword"] = r.Keyword
	if r.Cursor != "" {
		body["cursor"] = r.Cursor
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

// Search Find chronological tweets by keyword.
func (c *Tw) Search(ctx context.Context, req TwSearchRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/x/search",
		Body:   req.toBody(),
	})
}

// TwPostsRequest is the input to tw.Posts.
type TwPostsRequest struct {
	// X Posts User Id
	UserID string
	// X Posts Cursor
	Cursor string
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r TwPostsRequest) toBody() map[string]any {
	body := map[string]any{}
	body["user_id"] = r.UserID
	if r.Cursor != "" {
		body["cursor"] = r.Cursor
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

// Posts Get all the post information for a tweet by entering the user_id of the tweet.
func (c *Tw) Posts(ctx context.Context, req TwPostsRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/x/posts",
		Body:   req.toBody(),
	})
}

// TwUsersRequest is the input to tw.Users.
type TwUsersRequest struct {
	// X Users Username
	Username string
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r TwUsersRequest) toBody() map[string]any {
	body := map[string]any{}
	body["username"] = r.Username
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

// Users Get user details by Twitter username.
func (c *Tw) Users(ctx context.Context, req TwUsersRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/x/users",
		Body:   req.toBody(),
	})
}

// TwRetweetsRequest is the input to tw.Retweets.
type TwRetweetsRequest struct {
	// X Retweets Post Id
	NoteID string
	// X Retweets Cursor
	Cursor string
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r TwRetweetsRequest) toBody() map[string]any {
	body := map[string]any{}
	body["note_id"] = r.NoteID
	if r.Cursor != "" {
		body["cursor"] = r.Cursor
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

// Retweets Find retweets of a tweet.
func (c *Tw) Retweets(ctx context.Context, req TwRetweetsRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/x/retweets",
		Body:   req.toBody(),
	})
}
