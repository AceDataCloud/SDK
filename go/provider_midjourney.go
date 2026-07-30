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
	Mask           string
	Mode           string
	Action         string
	Prompt         string
	Timeout        float64
	ImageID        string
	Translation    *bool
	SplitImages    *bool
	Version        string
	HD             *bool
	Quality        string
	StyleReference *bool
	Moodboard      *bool
	Async          *bool
	CallbackURL    string
	Extra          map[string]any
}

func (r MidjourneyImagineRequest) toBody() map[string]any {
	body := map[string]any{}
	if r.Mask != "" {
		body["mask"] = r.Mask
	}
	if r.Mode != "" {
		body["mode"] = r.Mode
	}
	if r.Action != "" {
		body["action"] = r.Action
	}
	if r.Prompt != "" {
		body["prompt"] = r.Prompt
	}
	if r.Timeout != 0 {
		body["timeout"] = r.Timeout
	}
	if r.ImageID != "" {
		body["image_id"] = r.ImageID
	}
	if r.Translation != nil {
		body["translation"] = *r.Translation
	}
	if r.SplitImages != nil {
		body["split_images"] = *r.SplitImages
	}
	if r.Version != "" {
		body["version"] = r.Version
	}
	if r.HD != nil {
		body["hd"] = *r.HD
	}
	if r.Quality != "" {
		body["quality"] = r.Quality
	}
	if r.StyleReference != nil {
		body["style_reference"] = *r.StyleReference
	}
	if r.Moodboard != nil {
		body["moodboard"] = *r.Moodboard
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

// Imagine calls /midjourney/imagine.
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
	ImageID     string
	CallbackURL string
	Extra       map[string]any
}

func (r MidjourneySeedRequest) toBody() map[string]any {
	body := map[string]any{"image_id": r.ImageID}
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

// Seed calls /midjourney/seed.
func (c *Midjourney) Seed(ctx context.Context, req MidjourneySeedRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/midjourney/seed",
		Body:   req.toBody(),
	})
}

// MidjourneyEditsRequest is the input to midjourney.Edits.
type MidjourneyEditsRequest struct {
	Mask        string
	Mode        string
	Action      string
	Prompt      string
	ImageURL    string
	SplitImages *bool
	Async       *bool
	CallbackURL string
	Extra       map[string]any
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
	}
	if r.Prompt != "" {
		body["prompt"] = r.Prompt
	}
	if r.ImageURL != "" {
		body["image_url"] = r.ImageURL
	}
	if r.SplitImages != nil {
		body["split_images"] = *r.SplitImages
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

// Edits calls /midjourney/edits.
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

// MidjourneyVideosRequest is the input to midjourney.Videos.
type MidjourneyVideosRequest struct {
	Action      string
	Mode        string
	Resolution  string
	Prompt      string
	VideoID     string
	VideoIndex  float64
	Loop        *bool
	ImageURL    string
	EndImageURL string
	Async       *bool
	CallbackURL string
	Extra       map[string]any
}

func (r MidjourneyVideosRequest) toBody() map[string]any {
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
	if r.Loop != nil {
		body["loop"] = *r.Loop
	}
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

// Videos calls /midjourney/videos.
func (c *Midjourney) Videos(ctx context.Context, req MidjourneyVideosRequest) (*TaskHandle, error) {
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
	ImageURL    string
	CallbackURL string
	Extra       map[string]any
}

func (r MidjourneyDescribeRequest) toBody() map[string]any {
	body := map[string]any{"image_url": r.ImageURL}
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

// Describe calls /midjourney/describe.
func (c *Midjourney) Describe(ctx context.Context, req MidjourneyDescribeRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/midjourney/describe",
		Body:   req.toBody(),
	})
}

// MidjourneyShortenRequest is the input to midjourney.Shorten.
type MidjourneyShortenRequest struct {
	Prompt      string
	CallbackURL string
	Extra       map[string]any
}

func (r MidjourneyShortenRequest) toBody() map[string]any {
	body := map[string]any{"prompt": r.Prompt}
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

// Shorten calls /midjourney/shorten.
func (c *Midjourney) Shorten(ctx context.Context, req MidjourneyShortenRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/midjourney/shorten",
		Body:   req.toBody(),
	})
}

// MidjourneyTranslateRequest is the input to midjourney.Translate.
type MidjourneyTranslateRequest struct {
	Content     string
	CallbackURL string
	Extra       map[string]any
}

func (r MidjourneyTranslateRequest) toBody() map[string]any {
	body := map[string]any{"content": r.Content}
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

// Translate calls /midjourney/translate.
func (c *Midjourney) Translate(ctx context.Context, req MidjourneyTranslateRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/midjourney/translate",
		Body:   req.toBody(),
	})
}
