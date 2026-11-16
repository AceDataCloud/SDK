// Code generated from the platform OpenAPI spec. DO NOT EDIT.
// Regenerate with: python scripts/generate_providers.py

package acedatacloud

import "context"

// Acemusic is the acemusic provider client.
type Acemusic struct {
	t *transport
}

// AcemusicGenerateRequest is the input to acemusic.Generate.
type AcemusicGenerateRequest struct {
	// optional
	Action string
	// optional
	Model string
	// optional
	Custom bool
	// Creation idea. Required when custom is false.
	Prompt string
	// Custom lyrics. Required when custom is true.
	Lyric string
	// Musical style for custom creation.
	Style string
	// optional
	Title string
	// optional
	IdempotencyKey string
	// Async submits without blocking; poll the returned handle. Defaults true.
	Async *bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r AcemusicGenerateRequest) toBody() map[string]any {
	body := map[string]any{}
	if r.Action != "" {
		body["action"] = r.Action
	} else {
		body["action"] = "generate"
	}
	if r.Model != "" {
		body["model"] = r.Model
	} else {
		body["model"] = "acemusic-v1.1"
	}
	body["custom"] = r.Custom
	if r.Prompt != "" {
		body["prompt"] = r.Prompt
	}
	if r.Lyric != "" {
		body["lyric"] = r.Lyric
	}
	if r.Style != "" {
		body["style"] = r.Style
	}
	if r.Title != "" {
		body["title"] = r.Title
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
	return body
}

// Generate ACE Music Audios
func (c *Acemusic) Generate(ctx context.Context, req AcemusicGenerateRequest) (*TaskHandle, error) {
	result, err := c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/acemusic/audios",
		Body:   req.toBody(),
		ExtraHeaders: func() map[string]string {
			headers := map[string]string{}
			if req.IdempotencyKey != "" {
				headers["Idempotency-Key"] = req.IdempotencyKey
			}
			return headers
		}(),
	})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/acemusic/tasks", c.t, result), nil
}

// AcemusicLyricsRequest is the input to acemusic.Lyrics.
type AcemusicLyricsRequest struct {
	// required
	Prompt string
	// optional
	Style string
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r AcemusicLyricsRequest) toBody() map[string]any {
	body := map[string]any{}
	body["prompt"] = r.Prompt
	if r.Style != "" {
		body["style"] = r.Style
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

// Lyrics ACE Music Lyrics
func (c *Acemusic) Lyrics(ctx context.Context, req AcemusicLyricsRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/acemusic/lyrics",
		Body:   req.toBody(),
	})
}

// AcemusicTasksRequest is the input to acemusic.Tasks.
type AcemusicTasksRequest struct {
	// required
	Action string
	// optional
	ID string
	// optional
	IDs []string
	// optional
	Page int
	// optional
	PageSize int
	// Optional history type filter.
	Type string
	// Alternative history page size; use page/page_size or limit/offset consistently.
	Limit int
	// optional
	Offset int
	// Inclusive creation-time lower bound, Unix seconds.
	CreatedAtMin float64
	// Inclusive creation-time upper bound, Unix seconds.
	CreatedAtMax float64
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r AcemusicTasksRequest) toBody() map[string]any {
	body := map[string]any{}
	body["action"] = r.Action
	if r.ID != "" {
		body["id"] = r.ID
	}
	if r.IDs != nil {
		body["ids"] = r.IDs
	}
	if r.Page != 0 {
		body["page"] = r.Page
	}
	if r.PageSize != 0 {
		body["page_size"] = r.PageSize
	}
	if r.Type != "" {
		body["type"] = r.Type
	}
	if r.Limit != 0 {
		body["limit"] = r.Limit
	}
	if r.Offset != 0 {
		body["offset"] = r.Offset
	}
	if r.CreatedAtMin != 0 {
		body["created_at_min"] = r.CreatedAtMin
	}
	if r.CreatedAtMax != 0 {
		body["created_at_max"] = r.CreatedAtMax
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

// Tasks ACE Music Tasks
func (c *Acemusic) Tasks(ctx context.Context, req AcemusicTasksRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/acemusic/tasks",
		Body:   req.toBody(),
	})
}
