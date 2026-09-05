// Code generated from the platform OpenAPI spec. DO NOT EDIT.
// Regenerate with: python scripts/generate_providers.py

package acedatacloud

import "context"

// Fish is the fish provider client.
type Fish struct {
	t *transport
}

// FishGenerateRequest is the input to fish.Generate.
type FishGenerateRequest struct {
	// Text content to be synthesized. Required, must be a non-empty string.
	Text string
	// Top-p nucleus sampling parameter, controls output diversity.
	TopP float64
	// Output audio format, default is `mp3`.
	Format string
	// Delay mode. The upstream rejects null values, and defaults to `normal` when omitted.
	Latency string
	// Rhythm coverage parameters, forwarded as is to upstream (such as speech rate, volume, etc.).
	Prosody map[string]any
	// Is the input text subjected to text normalization processing by the upstream?
	Normalize *bool
	// One-shot voice clone reference; cannot be combined with reference_id.
	References []map[string]any
	// MP3 bitrate when `format=mp3`.
	Mp3Bitrate int
	// Output the audio sampling rate (e.g., 16000, 22050, 44100).
	SampleRate int
	// Sampling temperature (0.0–1.0). The higher the value, the more diverse the output; the lower the value, the mo
	Temperature float64
	// The chunk length passed to the upstream synthesizer.
	ChunkLength int
	// Saved/public voice ID; cannot be combined with references.
	ReferenceID any
	// Maximum number of new tokens generated.
	MaxNewTokens int
	// Minimum block length.
	MinChunkLength int
	// The repetition penalty coefficient applied during the generation process.
	RepetitionPenalty float64
	// optional
	Model string
	// Async submits without blocking; poll the returned handle. Defaults true.
	Async *bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r FishGenerateRequest) toBody() map[string]any {
	body := map[string]any{}
	body["text"] = r.Text
	if r.TopP != 0 {
		body["top_p"] = r.TopP
	}
	if r.Format != "" {
		body["format"] = r.Format
	}
	if r.Latency != "" {
		body["latency"] = r.Latency
	}
	if r.Prosody != nil {
		body["prosody"] = r.Prosody
	}
	if r.Normalize != nil {
		body["normalize"] = *r.Normalize
	}
	if r.References != nil {
		body["references"] = r.References
	}
	if r.Mp3Bitrate != 0 {
		body["mp3_bitrate"] = r.Mp3Bitrate
	}
	if r.SampleRate != 0 {
		body["sample_rate"] = r.SampleRate
	}
	if r.Temperature != 0 {
		body["temperature"] = r.Temperature
	}
	if r.ChunkLength != 0 {
		body["chunk_length"] = r.ChunkLength
	}
	if r.ReferenceID != nil {
		body["reference_id"] = r.ReferenceID
	}
	if r.MaxNewTokens != 0 {
		body["max_new_tokens"] = r.MaxNewTokens
	}
	if r.MinChunkLength != 0 {
		body["min_chunk_length"] = r.MinChunkLength
	}
	if r.RepetitionPenalty != 0 {
		body["repetition_penalty"] = r.RepetitionPenalty
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

// Generate Fish Audio text-to-speech API — convert text into natural speech using a chosen voice model.
func (c *Fish) Generate(ctx context.Context, req FishGenerateRequest) (*TaskHandle, error) {
	result, err := c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/fish/tts",
		Body:   req.toBody(),
		ExtraHeaders: func() map[string]string {
			headers := map[string]string{}
			if req.Model != "" {
				headers["model"] = req.Model
			}
			return headers
		}(),
	})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/fish/tasks", c.t, result), nil
}

// FishModelRequest is the input to fish.Model.
type FishModelRequest struct {
	// Name of the voice model.
	Title string
	// The HTTP(S) URL of the audio file for cloning must be a single URL string. This interface does not support mul
	Voices string
	// Tags used for retrieval in public repositories (optional).
	Tags []string
	// Reference text corresponding to the audio sample (optional).
	Texts []string
	// The visibility of the model is set to `private` by default.
	Visibility string
	// HTTP(S) URL of the voice model cover image (optional).
	CoverImage string
	// Description of the voice model (optional).
	Description string
	// If it is `true`, the upstream service will generate a sample voice after the training is completed.
	GenerateSample bool
	// If it is `true`, the upstream service will perform quality enhancement processing on the audio samples before
	EnhanceAudioQuality bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r FishModelRequest) toBody() map[string]any {
	body := map[string]any{}
	body["title"] = r.Title
	body["voices"] = r.Voices
	if r.Tags != nil {
		body["tags"] = r.Tags
	}
	if r.Texts != nil {
		body["texts"] = r.Texts
	}
	if r.Visibility != "" {
		body["visibility"] = r.Visibility
	}
	if r.CoverImage != "" {
		body["cover_image"] = r.CoverImage
	}
	if r.Description != "" {
		body["description"] = r.Description
	}
	body["generate_sample"] = r.GenerateSample
	body["enhance_audio_quality"] = r.EnhanceAudioQuality
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

// Model Fish Audio model creation API — upload reference audio to create a custom voice-clone model.
func (c *Fish) Model(ctx context.Context, req FishModelRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/fish/model",
		Body:   req.toBody(),
	})
}
