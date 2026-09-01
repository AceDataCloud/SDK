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
	// Fish Tts Text
	Text string
	// Fish Tts Reference Id
	ReferenceID string
	// Fish Tts Format
	Format string
	// Fish Tts Sample Rate
	SampleRate int
	// Fish Tts Mp3 Bitrate
	Mp3Bitrate int
	// Fish Tts Latency
	Latency string
	// Fish Tts Chunk Length
	ChunkLength int
	// Fish Tts Min Chunk Length
	MinChunkLength int
	// Fish Tts Temperature
	Temperature float64
	// Fish Tts Top P
	TopP float64
	// Fish Tts Repetition Penalty
	RepetitionPenalty float64
	// Fish Tts Max New Tokens
	MaxNewTokens int
	// Fish Tts Normalize
	Normalize bool
	// Fish Tts Prosody
	Prosody map[string]any
	// Fish Tts References
	References []map[string]any
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
	if r.ReferenceID != "" {
		body["reference_id"] = r.ReferenceID
	}
	if r.Format != "" {
		body["format"] = r.Format
	}
	if r.SampleRate != 0 {
		body["sample_rate"] = r.SampleRate
	}
	if r.Mp3Bitrate != 0 {
		body["mp3_bitrate"] = r.Mp3Bitrate
	}
	if r.Latency != "" {
		body["latency"] = r.Latency
	}
	if r.ChunkLength != 0 {
		body["chunk_length"] = r.ChunkLength
	}
	if r.MinChunkLength != 0 {
		body["min_chunk_length"] = r.MinChunkLength
	}
	if r.Temperature != 0 {
		body["temperature"] = r.Temperature
	}
	if r.TopP != 0 {
		body["top_p"] = r.TopP
	}
	if r.RepetitionPenalty != 0 {
		body["repetition_penalty"] = r.RepetitionPenalty
	}
	if r.MaxNewTokens != 0 {
		body["max_new_tokens"] = r.MaxNewTokens
	}
	body["normalize"] = r.Normalize
	if r.Prosody != nil {
		body["prosody"] = r.Prosody
	}
	if r.References != nil {
		body["references"] = r.References
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

// Generate Fish Tts
func (c *Fish) Generate(ctx context.Context, req FishGenerateRequest) (*TaskHandle, error) {
	headers := map[string]string{}
	if req.Model != "" {
		headers["model"] = req.Model
	}
	result, err := c.t.do(ctx, requestOpts{
		Method:       "POST",
		Path:         "/fish/tts",
		Body:         req.toBody(),
		ExtraHeaders: headers,
	})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/fish/tasks", c.t, result), nil
}
