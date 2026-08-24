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
	// Producer Upload Audio Url
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

// Upload Producer Upload
func (c *Producer) Upload(ctx context.Context, req ProducerUploadRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/producer/upload",
		Body:   req.toBody(),
	})
}

// ProducerVideosRequest is the input to producer.Videos.
type ProducerVideosRequest struct {
	// Producer Videos Audio Id
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

// Videos Producer Videos
func (c *Producer) Videos(ctx context.Context, req ProducerVideosRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/producer/videos",
		Body:   req.toBody(),
	})
}

// ProducerWavRequest is the input to producer.Wav.
type ProducerWavRequest struct {
	// Producer Wav Audio Id
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

// Wav Producer Wav
func (c *Producer) Wav(ctx context.Context, req ProducerWavRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/producer/wav",
		Body:   req.toBody(),
	})
}

// ProducerGenerateRequest is the input to producer.Generate.
type ProducerGenerateRequest struct {
	// Producer Audios Lyric
	Lyric string
	// Producer Audios Action
	Action string
	// Producer Audios Prompt
	Prompt string
	// Producer Audios Model
	Model string
	// Producer Audios Title
	Title string
	// Producer Audios Custom
	Custom bool
	// Producer Audios Audio Id
	AudioID string
	// Producer Audios Continue At
	ContinueAt float64
	// Producer Audios Seed
	Seed string
	// Producer Audios Instrumental
	Instrumental bool
	// Producer Audios Sound Strength
	SoundStrength float64
	// Producer Audios Lyrics Strength
	LyricsStrength float64
	// Producer Audios Weirdness
	Weirdness float64
	// Producer Audios Replace Section End
	ReplaceSectionEnd float64
	// Producer Audios Replace Section Start
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
	if r.ContinueAt != 0 {
		body["continue_at"] = r.ContinueAt
	} else {
		body["continue_at"] = false
	}
	if r.Seed != "" {
		body["seed"] = r.Seed
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
	if r.Weirdness != 0 {
		body["weirdness"] = r.Weirdness
	} else {
		body["weirdness"] = false
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

// Generate Producer Audios
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
	// Producer Lyrics Prompt
	Prompt string
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

// Lyrics Producer Lyrics
func (c *Producer) Lyrics(ctx context.Context, req ProducerLyricsRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/producer/lyrics",
		Body:   req.toBody(),
	})
}
