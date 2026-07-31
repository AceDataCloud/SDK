// Code generated from the platform OpenAPI spec. DO NOT EDIT.
// Regenerate with: python scripts/generate_providers.py

package acedatacloud

import "context"

// Midjourney is the midjourney provider client.
type Midjourney struct {
	t *transport
}

// MidjourneyImagineRequest is the input to Midjourney.Imagine.
type MidjourneyImagineRequest struct {
	Prompt         string
	Action         string
	Mode           string
	ImageID        string
	Mask           string
	Timeout        float64
	Translation    bool
	SplitImages    bool
	Version        string
	HD             bool
	Quality        string
	StyleReference bool
	Moodboard      bool
	// Async submits without blocking; poll the returned handle. Defaults true.
	Async *bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r MidjourneyImagineRequest) toBody() map[string]any {
	body := map[string]any{}
	if r.Prompt != "" {
		body["prompt"] = r.Prompt
	}
	if r.Action != "" {
		body["action"] = r.Action
	}
	if r.Mode != "" {
		body["mode"] = r.Mode
	}
	if r.ImageID != "" {
		body["image_id"] = r.ImageID
	}
	if r.Mask != "" {
		body["mask"] = r.Mask
	}
	if r.Timeout != 0 {
		body["timeout"] = r.Timeout
	}
	if r.Translation {
		body["translation"] = r.Translation
	}
	if r.SplitImages {
		body["split_images"] = r.SplitImages
	}
	if r.Version != "" {
		body["version"] = r.Version
	}
	if r.HD {
		body["hd"] = r.HD
	}
	if r.Quality != "" {
		body["quality"] = r.Quality
	}
	if r.StyleReference {
		body["style_reference"] = r.StyleReference
	}
	if r.Moodboard {
		body["moodboard"] = r.Moodboard
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

// Imagine submits a Midjourney image generation request.
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

// MidjourneyEditsRequest is the input to Midjourney.Edits.
type MidjourneyEditsRequest struct {
	Prompt      string
	Action      string
	Mode        string
	ImageURL    string
	Mask        string
	SplitImages bool
	Async       *bool
	CallbackURL string
	Extra       map[string]any
}

func (r MidjourneyEditsRequest) toBody() map[string]any {
	body := map[string]any{}
	if r.Prompt != "" {
		body["prompt"] = r.Prompt
	}
	if r.Action != "" {
		body["action"] = r.Action
	}
	if r.Mode != "" {
		body["mode"] = r.Mode
	}
	if r.ImageURL != "" {
		body["image_url"] = r.ImageURL
	}
	if r.Mask != "" {
		body["mask"] = r.Mask
	}
	if r.SplitImages {
		body["split_images"] = r.SplitImages
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

// Edits submits a Midjourney image editing request.
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

// MidjourneyVideosRequest is the input to Midjourney.Videos.
type MidjourneyVideosRequest struct {
	Action      string
	Mode        string
	Resolution  string
	Prompt      string
	VideoID     string
	VideoIndex  float64
	Loop        bool
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
	if r.Loop {
		body["loop"] = r.Loop
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

// Videos submits a Midjourney video generation request.
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
