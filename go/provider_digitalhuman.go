// Code generated from the platform OpenAPI spec. DO NOT EDIT.
// Regenerate with: python scripts/generate_providers.py

package acedatacloud

import (
	"context"
	"fmt"
)


// Digitalhuman is the digitalhuman provider client.
type Digitalhuman struct {
	t *transport
}

// DigitalhumanGenerateRequest is the input to digitalhuman.Generate.
type DigitalhumanGenerateRequest struct {
	// Public URL of the source face video (preferred). One of video_url/image_url required.
	VideoURL string
	// Spoken text -> TTS (requires voice_id).
	Text string
	// Audio tempo multiplier.
	Speed float64
	// Diffusion steps (LatentSync).
	Steps int
	// latentsync = quality (default); heygem = fast tier.
	Engine string
	// Lip-sync strength (LatentSync). Lower loosens sync.
	Guidance float64
	// Apply the mouth-seam reduction blend.
	SeamFix bool
	// A cloned voice from POST /digital-human/voices.
	VoiceID string
	// Public URL of the driving audio (.wav/.mp3/.m4a). OR supply text(+voice_id).
	AudioURL string
	// Public URL of a source face photo (photo-driven path).
	ImageURL string
	// optional
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
	if r.Text != "" {
		body["text"] = r.Text
	} else {
		body["text"] = "\u5927\u5bb6\u597d\uff0c\u8fd9\u662f\u79bb\u7ebf\u751f\u6210\u7684\u6570\u5b57\u4eba\u3002"
	}
	if r.Speed != 0 {
		body["speed"] = r.Speed
	} else {
		body["speed"] = 1.0
	}
	if r.Steps != 0 {
		body["steps"] = r.Steps
	} else {
		body["steps"] = 40
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
	body["seam_fix"] = r.SeamFix
	if r.VoiceID != "" {
		body["voice_id"] = r.VoiceID
	}
	if r.AudioURL != "" {
		body["audio_url"] = r.AudioURL
	}
	if r.ImageURL != "" {
		body["image_url"] = r.ImageURL
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

func (r DigitalhumanGenerateRequest) validate() error {
	if r.VideoURL == "" && r.ImageURL == "" {
		return fmt.Errorf("video_url or image_url is required")
	}
	return nil
}

// Generate Digital Human video generation API — turn a portrait plus audio or text into a talking-head video.
func (c *Digitalhuman) Generate(ctx context.Context, req DigitalhumanGenerateRequest) (*TaskHandle, error) {
	if err := req.validate(); err != nil {
		return nil, err
	}
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

// Voices Digital Human voice-clone API — upload an audio sample to clone a custom voice for speech synthesis.
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
