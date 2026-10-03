// Code generated from the platform OpenAPI spec. DO NOT EDIT.
// Regenerate with: python scripts/generate_providers.py

package acedatacloud

import "context"

// Digitalhuman is the digitalhuman provider client.
type Digitalhuman struct {
	t *transport
}

// DigitalhumanGenerateRequest is the input to digitalhuman.Generate.
type DigitalhumanGenerateRequest struct {
	// Public URL of the source face video (preferred). Supply either video_url or image_url.
	VideoURL string
	// Public URL of a source face photo (photo-driven path). Supply either video_url or image_url.
	ImageURL string
	// Public URL of the driving audio (.wav/.mp3/.m4a). OR supply text(+voice_id).
	AudioURL string
	// Spoken text -> TTS (requires voice_id).
	Text string
	// A cloned voice from POST /digital-human/voices.
	VoiceID string
	// [Deprecated] Accepted for backward compatibility but no longer changes the output or the price — every request
	Engine string
	// Lip-sync strength (LatentSync). Lower loosens sync.
	Guidance float64
	// Diffusion steps (LatentSync).
	Steps int
	// Apply the mouth-seam reduction blend.
	SeamFix bool
	// Audio tempo multiplier.
	Speed float64
	// [Deprecated] Output is always rendered at 720p.
	Resolution string
	// Async submits without blocking; poll the returned handle. Defaults true.
	Async *bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r DigitalhumanGenerateRequest) toBody() map[string]any {
	body := map[string]any{}
	if r.VideoURL != "" {
		body["video_url"] = r.VideoURL
	}
	if r.ImageURL != "" {
		body["image_url"] = r.ImageURL
	}
	if r.AudioURL != "" {
		body["audio_url"] = r.AudioURL
	}
	if r.Text != "" {
		body["text"] = r.Text
	}
	if r.VoiceID != "" {
		body["voice_id"] = r.VoiceID
	}
	if r.Engine != "" {
		body["engine"] = r.Engine
	} else {
		body["engine"] = "latentsync"
	}
	if r.Guidance != 0 {
		body["guidance"] = r.Guidance
	} else {
		body["guidance"] = 2.0
	}
	if r.Steps != 0 {
		body["steps"] = r.Steps
	} else {
		body["steps"] = 40
	}
	body["seam_fix"] = r.SeamFix
	if r.Speed != 0 {
		body["speed"] = r.Speed
	} else {
		body["speed"] = 1.0
	}
	if r.Resolution != "" {
		body["resolution"] = r.Resolution
	} else {
		body["resolution"] = "720p"
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

// Generate Digital Human Videos
func (c *Digitalhuman) Generate(ctx context.Context, req DigitalhumanGenerateRequest) (*TaskHandle, error) {
	result, err := c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/digital-human/videos",
		Body:   req.toBody(),
	})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/digital-human/tasks", c.t, result), nil
}

// DigitalhumanVoicesRequest is the input to digitalhuman.Voices.
type DigitalhumanVoicesRequest struct {
	// Public URL of a clean 10-20s voice sample.
	AudioURL string
	// optional
	Lang string
	// Optional label.
	Name string
	// Async submits without blocking; poll the returned handle. Defaults true.
	Async *bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r DigitalhumanVoicesRequest) toBody() map[string]any {
	body := map[string]any{}
	body["audio_url"] = r.AudioURL
	if r.Lang != "" {
		body["lang"] = r.Lang
	} else {
		body["lang"] = "zh"
	}
	if r.Name != "" {
		body["name"] = r.Name
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

// Voices Digital Human Voices
func (c *Digitalhuman) Voices(ctx context.Context, req DigitalhumanVoicesRequest) (*TaskHandle, error) {
	result, err := c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/digital-human/voices",
		Body:   req.toBody(),
	})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/digital-human/tasks", c.t, result), nil
}
