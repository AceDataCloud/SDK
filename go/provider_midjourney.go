// Code generated from the platform OpenAPI spec. DO NOT EDIT.
// Regenerate with: python scripts/generate_providers.py

package acedatacloud

import "context"

// Midjourney is the midjourney provider client.
type Midjourney struct {
	t *transport
}

// MidjourneyImagineRequest is the input to midjourney.Imagine.
type MidjourneyImagineRequest struct {
	// optional
	Mask string
	// optional
	Mode string
	// optional
	Action string
	// optional
	Prompt string
	// optional
	Timeout float64
	// optional
	ImageID string
	// optional
	Translation bool
	// optional
	SplitImages bool
	// optional
	Version string
	// optional
	Hd bool
	// optional
	Quality string
	// optional
	StyleReference bool
	// optional
	Moodboard bool
	// Async submits without blocking; poll the returned handle. Defaults true.
	Async *bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r MidjourneyImagineRequest) toBody() map[string]any {
	body := map[string]any{}
	if r.Mask != "" {
		body["mask"] = r.Mask
	}
	if r.Mode != "" {
		body["mode"] = r.Mode
	} else {
		body["mode"] = "fast"
	}
	if r.Action != "" {
		body["action"] = r.Action
	} else {
		body["action"] = "generate"
	}
	if r.Prompt != "" {
		body["prompt"] = r.Prompt
	}
	if r.Timeout != 0 {
		body["timeout"] = r.Timeout
	} else {
		body["timeout"] = 480
	}
	if r.ImageID != "" {
		body["image_id"] = r.ImageID
	}
	body["translation"] = r.Translation
	body["split_images"] = r.SplitImages
	if r.Version != "" {
		body["version"] = r.Version
	}
	body["hd"] = r.Hd
	if r.Quality != "" {
		body["quality"] = r.Quality
	} else {
		body["quality"] = "1"
	}
	body["style_reference"] = r.StyleReference
	body["moodboard"] = r.Moodboard
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

// Imagine Midjourney Imagine
func (c *Midjourney) Imagine(ctx context.Context, req MidjourneyImagineRequest) (*TaskHandle, error) {
	result, err := c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/midjourney/imagine",
		Body:   req.toBody(),
	})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/midjourney/tasks", c.t, result), nil
}

// MidjourneySeedRequest is the input to midjourney.Seed.
type MidjourneySeedRequest struct {
	// required
	ImageID string
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r MidjourneySeedRequest) toBody() map[string]any {
	body := map[string]any{}
	body["image_id"] = r.ImageID
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

// Seed Midjourney Seed
func (c *Midjourney) Seed(ctx context.Context, req MidjourneySeedRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/midjourney/seed",
		Body:   req.toBody(),
	})
}

// MidjourneyEditsRequest is the input to midjourney.Edits.
type MidjourneyEditsRequest struct {
	// optional
	Mask string
	// optional
	Mode string
	// optional
	Action string
	// optional
	Prompt string
	// optional
	ImageURL string
	// optional
	SplitImages bool
	// Async submits without blocking; poll the returned handle. Defaults true.
	Async *bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r MidjourneyEditsRequest) toBody() map[string]any {
	body := map[string]any{}
	if r.Mask != "" {
		body["mask"] = r.Mask
	}
	if r.Mode != "" {
		body["mode"] = r.Mode
	}
	if r.Action != "" {
		body["action"] = r.Action
	} else {
		body["action"] = "generate"
	}
	if r.Prompt != "" {
		body["prompt"] = r.Prompt
	}
	if r.ImageURL != "" {
		body["image_url"] = r.ImageURL
	}
	body["split_images"] = r.SplitImages
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

// Edits Midjourney Edits
func (c *Midjourney) Edits(ctx context.Context, req MidjourneyEditsRequest) (*TaskHandle, error) {
	result, err := c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/midjourney/edits",
		Body:   req.toBody(),
	})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/midjourney/tasks", c.t, result), nil
}

// MidjourneyGenerateRequest is the input to midjourney.Generate.
type MidjourneyGenerateRequest struct {
	// optional
	Action string
	// optional
	Mode string
	// optional
	Resolution string
	// optional
	Prompt string
	// optional
	VideoID string
	// optional
	VideoIndex float64
	// optional
	Loop bool
	// optional
	ImageURL string
	// optional
	EndImageURL string
	// Async submits without blocking; poll the returned handle. Defaults true.
	Async *bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r MidjourneyGenerateRequest) toBody() map[string]any {
	body := map[string]any{}
	if r.Action != "" {
		body["action"] = r.Action
	}
	if r.Mode != "" {
		body["mode"] = r.Mode
	}
	if r.Resolution != "" {
		body["resolution"] = r.Resolution
	}
	if r.Prompt != "" {
		body["prompt"] = r.Prompt
	}
	if r.VideoID != "" {
		body["video_id"] = r.VideoID
	}
	if r.VideoIndex != 0 {
		body["video_index"] = r.VideoIndex
	}
	body["loop"] = r.Loop
	if r.ImageURL != "" {
		body["image_url"] = r.ImageURL
	}
	if r.EndImageURL != "" {
		body["end_image_url"] = r.EndImageURL
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

// Generate Midjourney Videos
func (c *Midjourney) Generate(ctx context.Context, req MidjourneyGenerateRequest) (*TaskHandle, error) {
	result, err := c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/midjourney/videos",
		Body:   req.toBody(),
	})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/midjourney/tasks", c.t, result), nil
}

// MidjourneyDescribeRequest is the input to midjourney.Describe.
type MidjourneyDescribeRequest struct {
	// required
	ImageURL string
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r MidjourneyDescribeRequest) toBody() map[string]any {
	body := map[string]any{}
	body["image_url"] = r.ImageURL
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

// Describe Midjourney Describe
func (c *Midjourney) Describe(ctx context.Context, req MidjourneyDescribeRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/midjourney/describe",
		Body:   req.toBody(),
	})
}

// MidjourneyShortenRequest is the input to midjourney.Shorten.
type MidjourneyShortenRequest struct {
	// required
	Prompt string
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r MidjourneyShortenRequest) toBody() map[string]any {
	body := map[string]any{}
	body["prompt"] = r.Prompt
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

// Shorten Midjourney Shorten
func (c *Midjourney) Shorten(ctx context.Context, req MidjourneyShortenRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/midjourney/shorten",
		Body:   req.toBody(),
	})
}

// MidjourneyTranslateRequest is the input to midjourney.Translate.
type MidjourneyTranslateRequest struct {
	// required
	Content string
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r MidjourneyTranslateRequest) toBody() map[string]any {
	body := map[string]any{}
	body["content"] = r.Content
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

// Translate Midjourney Translate
func (c *Midjourney) Translate(ctx context.Context, req MidjourneyTranslateRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/midjourney/translate",
		Body:   req.toBody(),
	})
}

// MidjourneyTasksRequest is the input to midjourney.Tasks.
type MidjourneyTasksRequest struct {
	// optional
	Action string
	// optional
	ID string
	// optional
	TraceID string
	// optional
	IDs []string
	// optional
	TraceIDs []string
	// optional
	Offset int
	// optional
	Limit int
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r MidjourneyTasksRequest) toBody() map[string]any {
	body := map[string]any{}
	if r.Action != "" {
		body["action"] = r.Action
	} else {
		body["action"] = "retrieve"
	}
	if r.ID != "" {
		body["id"] = r.ID
	}
	if r.TraceID != "" {
		body["trace_id"] = r.TraceID
	}
	if r.IDs != nil {
		body["ids"] = r.IDs
	}
	if r.TraceIDs != nil {
		body["trace_ids"] = r.TraceIDs
	}
	if r.Offset != 0 {
		body["offset"] = r.Offset
	} else {
		body["offset"] = 0
	}
	if r.Limit != 0 {
		body["limit"] = r.Limit
	} else {
		body["limit"] = 12
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

// Tasks Midjourney Tasks
func (c *Midjourney) Tasks(ctx context.Context, req MidjourneyTasksRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/midjourney/tasks",
		Body:   req.toBody(),
	})
}
