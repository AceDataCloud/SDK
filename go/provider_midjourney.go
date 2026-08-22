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
	// Midjourney Imagine Mask
	Mask string
	// Midjourney Imagine Mode
	Mode string
	// Midjourney Imagine Action
	Action string
	// Midjourney Imagine Prompt
	Prompt string
	// Midjourney Imagine Timeout
	Timeout float64
	// Midjourney Imagine Image Id
	ImageID string
	// Midjourney Imagine Translation
	Translation bool
	// Midjourney Imagine Split Images
	SplitImages bool
	// Midjourney Imagine Version
	Version string
	// Midjourney Imagine Hd
	Hd bool
	// Midjourney Imagine Quality
	Quality string
	// Midjourney Imagine Style Reference
	StyleReference bool
	// Midjourney Imagine Moodboard
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
	// Midjourney Seed Image Id
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
	// Midjourney Edits Mask
	Mask string
	// Midjourney Edits Mode
	Mode string
	// Midjourney Edits Action
	Action string
	// Midjourney Edits Prompt
	Prompt string
	// Midjourney Edits Image Url
	ImageURL string
	// Midjourney Edits Split Images
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
	// Midjourney Videos Action
	Action string
	// Midjourney Videos Mode
	Mode string
	// Midjourney Videos Resolution
	Resolution string
	// Midjourney Videos Prompt
	Prompt string
	// Midjourney Videos Video Id
	VideoID string
	// Midjourney Videos Video Index
	VideoIndex float64
	// Midjourney Videos Loop
	Loop bool
	// Midjourney Videos Image Url
	ImageURL string
	// Midjourney Videos End Image Url
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
	// Midjourney Describe Image Url
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
	// Midjourney Shorten Prompt
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
	// Midjourney Translate 2
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
