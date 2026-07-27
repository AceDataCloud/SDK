// Code generated from the platform OpenAPI spec. DO NOT EDIT.
// Regenerate with: python scripts/generate_providers.py

package acedatacloud

import "context"


// Producer is the producer provider client.
type Producer struct {
	t *transport
}

// ProducerUploadRequest is the input to producer.Upload.
type ProducerUploadRequest struct {
	// The CDN address for the custom audio files to be uploaded.
	AudioURL string
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r ProducerUploadRequest) toBody() map[string]any {
	body := map[string]any{}
	body["audio_url"] = r.AudioURL
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

// Upload Producer reference audio upload API, upload audio to get an audio_id for generation.
func (c *Producer) Upload(ctx context.Context, req ProducerUploadRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/producer/upload",
		Body:   req.toBody(),
	})
}

// ProducerVideosRequest is the input to producer.Videos.
type ProducerVideosRequest struct {
	// Reference audio ID.
	AudioID string
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r ProducerVideosRequest) toBody() map[string]any {
	body := map[string]any{}
	body["audio_id"] = r.AudioID
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

// Videos AceData Producer MP4 retrieval API. Pass an audio_id to receive an MP4 video download link with cover art.
func (c *Producer) Videos(ctx context.Context, req ProducerVideosRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/producer/videos",
		Body:   req.toBody(),
	})
}

// ProducerWavRequest is the input to producer.Wav.
type ProducerWavRequest struct {
	// Reference audio ID.
	AudioID string
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r ProducerWavRequest) toBody() map[string]any {
	body := map[string]any{}
	body["audio_id"] = r.AudioID
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

// Wav AceData Producer WAV (lossless) retrieval API. Pass an audio_id to receive a WAV-format download link.
func (c *Producer) Wav(ctx context.Context, req ProducerWavRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/producer/wav",
		Body:   req.toBody(),
	})
}

// ProducerGenerateRequest is the input to producer.Generate.
type ProducerGenerateRequest struct {
	// Lyrics content for generating audio.
	Lyric string
	// Types of audio generation operations. Supported values include `generate` (generate based on prompts), `cover`
	Action string
	// Prompts for generating audio should not exceed 200 characters in length.
	Prompt string
	// Random seed used for audio generation.
	Seed string
	// The model used for generating music is `FUZZ-2.0` by default.
	Model string
	// Title used for generating songs.
	Title string
	// Is it a custom mode? If `true`, the audio will be generated based on the `lyric`; otherwise, it will be genera
	Custom bool
	// The unique ID of the reference song.
	AudioID string
	// The degree of uniqueness of style can be selected between 0 and 1, with a default value of 0.5.
	Weirdness float64
	// Specify the time point (in seconds) from which to continue writing the song.
	ContinueAt float64
	// If `true`, the generated audio will only contain the accompaniment, without vocal lyrics.
	Instrumental bool
	// The impact intensity of the audio prompt words can be selected between 0.2 and 1, with a default value of 0.5.
	SoundStrength float64
	// The degree of influence of lyrics on audio generation can be selected between 0 and 1, with a default value of
	LyricsStrength float64
	// Replace the end time point of the segment (seconds).
	ReplaceSectionEnd float64
	// Replace the starting time point of the segment (seconds).
	ReplaceSectionStart float64
	// Async submits without blocking; poll the returned handle. Defaults true.
	Async *bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r ProducerGenerateRequest) toBody() map[string]any {
	body := map[string]any{}
	body["lyric"] = r.Lyric
	body["action"] = r.Action
	body["prompt"] = r.Prompt
	if r.Seed != "" {
		body["seed"] = r.Seed
	}
	if r.Model != "" {
		body["model"] = r.Model
	}
	if r.Title != "" {
		body["title"] = r.Title
	}
	body["custom"] = r.Custom
	if r.AudioID != "" {
		body["audio_id"] = r.AudioID
	}
	if r.Weirdness != 0 {
		body["weirdness"] = r.Weirdness
	} else {
		body["weirdness"] = false
	}
	if r.ContinueAt != 0 {
		body["continue_at"] = r.ContinueAt
	} else {
		body["continue_at"] = false
	}
	body["instrumental"] = r.Instrumental
	if r.SoundStrength != 0 {
		body["sound_strength"] = r.SoundStrength
	} else {
		body["sound_strength"] = false
	}
	if r.LyricsStrength != 0 {
		body["lyrics_strength"] = r.LyricsStrength
	} else {
		body["lyrics_strength"] = false
	}
	if r.ReplaceSectionEnd != 0 {
		body["replace_section_end"] = r.ReplaceSectionEnd
	} else {
		body["replace_section_end"] = false
	}
	if r.ReplaceSectionStart != 0 {
		body["replace_section_start"] = r.ReplaceSectionStart
	} else {
		body["replace_section_start"] = false
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

// Generate Producer AI music generation API, generates 1 song per request.
func (c *Producer) Generate(ctx context.Context, req ProducerGenerateRequest) (*TaskHandle, error) {
	result, err := c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/producer/audios",
		Body:   req.toBody(),
	})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/producer/tasks", c.t, result), nil
}

// ProducerLyricsRequest is the input to producer.Lyrics.
type ProducerLyricsRequest struct {
	// Prompts for generating lyrics.
	Prompt map[string]any
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r ProducerLyricsRequest) toBody() map[string]any {
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

// Lyrics Producer AI lyrics generation API, input a prompt to generate lyrics.
func (c *Producer) Lyrics(ctx context.Context, req ProducerLyricsRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/producer/lyrics",
		Body:   req.toBody(),
	})
}
