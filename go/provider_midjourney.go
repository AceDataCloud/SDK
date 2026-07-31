package acedatacloud

import "context"

// Midjourney is the midjourney provider client.
type Midjourney struct {
	t *transport
}

// MidjourneyImagineRequest is the input to midjourney.Imagine.
type MidjourneyImagineRequest struct {
	// Prompt describing the image to generate.
	Prompt string
	// ID of an existing Midjourney image to remix.
	ImageID string
	// Inpainting mask URL.
	Mask string
	// Processing mode (fast, relax, turbo).
	Mode string
	// Action type.
	Action string
	// Timeout in seconds.
	Timeout float64
	// Enable prompt auto-translation.
	Translation bool
	// Split the output into individual images.
	SplitImages bool
	// Midjourney version string.
	Version string
	// Enable HD quality.
	HD bool
	// Output quality preset.
	Quality string
	// Enable style reference mode.
	StyleReference bool
	// Enable moodboard mode.
	Moodboard bool
	// Async submits without blocking; poll the returned handle.
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
	if r.ImageID != "" {
		body["image_id"] = r.ImageID
	}
	if r.Mask != "" {
		body["mask"] = r.Mask
	}
	if r.Mode != "" {
		body["mode"] = r.Mode
	}
	if r.Action != "" {
		body["action"] = r.Action
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

// MidjourneyEditsRequest is the input to midjourney.Edits.
type MidjourneyEditsRequest struct {
	// Prompt for the edit.
	Prompt string
	// Image URL to edit.
	ImageURL string
	// Inpainting mask URL.
	Mask string
	// Processing mode (fast, relax, turbo).
	Mode string
	// Action type.
	Action string
	// Split the output into individual images.
	SplitImages bool
	// Async submits without blocking; poll the returned handle.
	Async *bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r MidjourneyEditsRequest) toBody() map[string]any {
	body := map[string]any{}
	if r.Prompt != "" {
		body["prompt"] = r.Prompt
	}
	if r.ImageURL != "" {
		body["image_url"] = r.ImageURL
	}
	if r.Mask != "" {
		body["mask"] = r.Mask
	}
	if r.Mode != "" {
		body["mode"] = r.Mode
	}
	if r.Action != "" {
		body["action"] = r.Action
	}
	if r.SplitImages {
		body["split_images"] = r.SplitImages
	}
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

// MidjourneyVideosRequest is the input to midjourney.Videos.
type MidjourneyVideosRequest struct {
	// Video action (generate, extend).
	Action string
	// Processing mode (fast, turbo).
	Mode string
	// Output resolution (480p, 720p).
	Resolution string
	// Text prompt.
	Prompt string
	// Source image/video ID.
	VideoID string
	// Panel index to animate.
	VideoIndex float64
	// Loop the video.
	Loop bool
	// Reference start image URL.
	ImageURL string
	// Reference end image URL.
	EndImageURL string
	// Async submits without blocking; poll the returned handle.
	Async *bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
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

// Seed retrieves the generation seed for a Midjourney image.
func (c *Midjourney) Seed(ctx context.Context, imageID string) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/midjourney/seed",
		Body:   map[string]any{"image_id": imageID},
	})
}

// Describe generates a prompt description for a Midjourney image.
func (c *Midjourney) Describe(ctx context.Context, imageURL string) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/midjourney/describe",
		Body:   map[string]any{"image_url": imageURL},
	})
}

// Shorten condenses a Midjourney prompt.
func (c *Midjourney) Shorten(ctx context.Context, prompt string) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/midjourney/shorten",
		Body:   map[string]any{"prompt": prompt},
	})
}

// Translate translates content for use in a Midjourney prompt.
func (c *Midjourney) Translate(ctx context.Context, content string) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/midjourney/translate",
		Body:   map[string]any{"content": content},
	})
}
