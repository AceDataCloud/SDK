// Code generated from the platform OpenAPI spec. DO NOT EDIT.
// Regenerate with: python scripts/generate_providers.py

package acedatacloud

import "context"

// Suno is the suno provider client.
type Suno struct {
	t *transport
}

// SunoGenerateRequest is the input to suno.Generate.
type SunoGenerateRequest struct {
	// Lyrics for generating music under custom mode (`custom` is `true`). `chirp-v3-5` and `chirp-v4` have a maximum
	Lyric string
	// The model used for generating music has a default value of `chirp-v4`.
	Model string
	// Music style description. `chirp-v3-5` and `chirp-v4` up to 200 characters; `chirp-v4-5` and above (including `
	Style string
	// Music Title (Custom Mode). `chirp-v3-5` and `chirp-v4` up to 80 characters; `chirp-v4-5` and above (including
	Title string
	// Types of operations for generating music. `generate`: Generate audio based on prompts; `extend`: Continue gene
	Action string
	// Whether to enable the custom mode flag. If `true`, the audio will be generated based on the lyrics; otherwise,
	Custom bool
	// The prompt words for generating music in inspiration mode (when `custom` is set to `false`) must not exceed 50
	Prompt string
	// Audio ID used for generating additional audio based on existing audio. This field is required when `action` is
	AudioID string
	// Target length of the generated track in seconds, given as an integer, typically between 10 and 360. It is main
	Duration int
	// The "Weirdness" advanced parameter in the Suno official custom mode has a value range of 0 to 1, with higher v
	Weirdness float64
	// A list of reference audio URLs for inspiration, requiring 1 to 4 publicly accessible audio addresses. This fie
	AudioURLs []string
	// Generate the singer Persona ID used when creating songs based on the unique style characteristics of the speci
	PersonaID string
	// Continue generating from the specified time point (seconds) of the existing audio. For example, 213.5 means to
	ContinueAt float64
	// Add the end time of the sample for the uploaded audio, which must be less than the total duration of the song.
	SamplesEnd float64
	// The weight of the uploaded reference audio, with a value range from 0 to 1, where a higher value indicates gre
	AudioWeight float64
	// Pure accompaniment mode (no lyrics), default is `false`. When set to `true`, the lyrics filled in above will b
	Instrumental bool
	// Prompts for automatically generating lyrics, effective only when `custom` is `true` and `lyric` is empty.
	LyricPrompt string
	// Voice gender preference, selectable values are `'m'` (male voice) or `'f'` (female voice). Models `chirp-v4-5`
	VocalGender string
	// Add a default start time for the uploaded audio sample, with a default value of 0.
	SamplesStart float64
	// Styles of description that are not desired in music generation.
	NegativeTags string
	// The "Style Influence" advanced parameter in the Suno official custom mode has a value range of 0 to 1, with hi
	StyleInfluence float64
	// Audio ID list for mixing and mashup. This field is required when `action` is `mashup`.
	MashupAudioIDs []string
	// Add the end time of the AI voice to the uploaded audio, which must be less than the total duration of the song
	OverpaintingEnd float64
	// Add the end time for the AI accompaniment to the uploaded audio, which must be less than the total duration of
	UnderpaintingEnd float64
	// Set the default start time for the AI voice of the uploaded audio to 0.
	OverpaintingStart float64
	// `variation_category` only supports version v5 and above, with only three optional values: `high`, `normal`, `s
	VariationCategory string
	// When `action` is `replace_section`, specify the end time (in seconds) of the segment to be replaced.
	ReplaceSectionEnd float64
	// Set the default start time for the AI accompaniment added to the uploaded audio, with a default value of 0.
	UnderpaintingStart float64
	// When `action` is `replace_section`, specify the start time (in seconds) of the segment to be replaced.
	ReplaceSectionStart float64
	// Async submits without blocking; poll the returned handle. Defaults true.
	Async *bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r SunoGenerateRequest) toBody() map[string]any {
	body := map[string]any{}
	if r.Lyric != "" {
		body["lyric"] = r.Lyric
	}
	if r.Model != "" {
		body["model"] = r.Model
	} else {
		body["model"] = "chirp-v5-5"
	}
	if r.Style != "" {
		body["style"] = r.Style
	}
	if r.Title != "" {
		body["title"] = r.Title
	}
	if r.Action != "" {
		body["action"] = r.Action
	} else {
		body["action"] = "generate"
	}
	body["custom"] = r.Custom
	body["prompt"] = r.Prompt
	if r.AudioID != "" {
		body["audio_id"] = r.AudioID
	}
	if r.Duration != 0 {
		body["duration"] = r.Duration
	}
	if r.Weirdness != 0 {
		body["weirdness"] = r.Weirdness
	}
	body["audio_urls"] = r.AudioURLs
	if r.PersonaID != "" {
		body["persona_id"] = r.PersonaID
	}
	if r.ContinueAt != 0 {
		body["continue_at"] = r.ContinueAt
	}
	if r.SamplesEnd != 0 {
		body["samples_end"] = r.SamplesEnd
	}
	if r.AudioWeight != 0 {
		body["audio_weight"] = r.AudioWeight
	}
	body["instrumental"] = r.Instrumental
	if r.LyricPrompt != "" {
		body["lyric_prompt"] = r.LyricPrompt
	}
	if r.VocalGender != "" {
		body["vocal_gender"] = r.VocalGender
	}
	if r.SamplesStart != 0 {
		body["samples_start"] = r.SamplesStart
	}
	if r.NegativeTags != "" {
		body["negative_tags"] = r.NegativeTags
	}
	if r.StyleInfluence != 0 {
		body["style_influence"] = r.StyleInfluence
	}
	if r.MashupAudioIDs != nil {
		body["mashup_audio_ids"] = r.MashupAudioIDs
	}
	if r.OverpaintingEnd != 0 {
		body["overpainting_end"] = r.OverpaintingEnd
	}
	if r.UnderpaintingEnd != 0 {
		body["underpainting_end"] = r.UnderpaintingEnd
	}
	if r.OverpaintingStart != 0 {
		body["overpainting_start"] = r.OverpaintingStart
	}
	if r.VariationCategory != "" {
		body["variation_category"] = r.VariationCategory
	}
	if r.ReplaceSectionEnd != 0 {
		body["replace_section_end"] = r.ReplaceSectionEnd
	}
	if r.UnderpaintingStart != 0 {
		body["underpainting_start"] = r.UnderpaintingStart
	}
	if r.ReplaceSectionStart != 0 {
		body["replace_section_start"] = r.ReplaceSectionStart
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

// Generate Suno AI music generation API, generates 2 songs per request with extension support.
func (c *Suno) Generate(ctx context.Context, req SunoGenerateRequest) (*TaskHandle, error) {
	result, err := c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/suno/audios",
		Body:   req.toBody(),
	})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/suno/tasks", c.t, result), nil
}

// SunoPersonaRequest is the input to suno.Persona.
type SunoPersonaRequest struct {
	// Names of singer styles.
	Name string
	// Used to create generated song IDs in the style of the singer.
	AudioID string
	// The end time of the vocal segment in the audio (seconds).
	VocalEnd float64
	// A textual description of the singer's style.
	Description string
	// The starting time (in seconds) of the vocal segment in the audio.
	VocalStart float64
	// Used to generate audio IDs in the style of new singers (vocal reference audio).
	VoxAudioID string
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r SunoPersonaRequest) toBody() map[string]any {
	body := map[string]any{}
	body["name"] = r.Name
	body["audio_id"] = r.AudioID
	if r.VocalEnd != 0 {
		body["vocal_end"] = r.VocalEnd
	}
	if r.Description != "" {
		body["description"] = r.Description
	}
	if r.VocalStart != 0 {
		body["vocal_start"] = r.VocalStart
	}
	if r.VoxAudioID != "" {
		body["vox_audio_id"] = r.VoxAudioID
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

// Persona Suno singer style API, set song style based on a generated song ID.
func (c *Suno) Persona(ctx context.Context, req SunoPersonaRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/suno/persona",
		Body:   req.toBody(),
	})
}

// SunoMp4Request is the input to suno.Mp4.
type SunoMp4Request struct {
	// Used to obtain the song ID for the corresponding MP4 of the song.
	AudioID string
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r SunoMp4Request) toBody() map[string]any {
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

// Mp4 Suno MP4 API, get MP4 file link via audio_id.
func (c *Suno) Mp4(ctx context.Context, req SunoMp4Request) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/suno/mp4",
		Body:   req.toBody(),
	})
}

// SunoVoicesRequest is the input to suno.Voices.
type SunoVoicesRequest struct {
	// Publicly accessible URL for audio files used to create sound. Must be in MP3 or WAV format, at least 10 second
	AudioURL string
	// Custom voice personality name.
	Name string
	// Description information for custom voice personality.
	Description string
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r SunoVoicesRequest) toBody() map[string]any {
	body := map[string]any{}
	body["audio_url"] = r.AudioURL
	if r.Name != "" {
		body["name"] = r.Name
	}
	if r.Description != "" {
		body["description"] = r.Description
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

// Voices Suno Voice Clone API. Create a custom voice persona from an uploaded audio file for voice cloning in music generation.
func (c *Suno) Voices(ctx context.Context, req SunoVoicesRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/suno/voices",
		Body:   req.toBody(),
	})
}

// SunoTimingRequest is the input to suno.Timing.
type SunoTimingRequest struct {
	// Need to obtain the audio ID for timing/caption data, which is the generated Suno song ID.
	AudioID string
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r SunoTimingRequest) toBody() map[string]any {
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

// Timing Suno timeline API, get lyrics and audio timeline of generated music.
func (c *Suno) Timing(ctx context.Context, req SunoTimingRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/suno/timing",
		Body:   req.toBody(),
	})
}

// SunoVoxRequest is the input to suno.Vox.
type SunoVoxRequest struct {
	// The source audio ID used to extract human voice, which is the unique identifier of the Suno audio segment to b
	AudioID string
	// End time point for vocal extraction (unit: seconds).
	VocalEnd float64
	// The starting time point for vocal extraction (unit: seconds).
	VocalStart float64
	// Async submits without blocking; poll the returned handle. Defaults true.
	Async *bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r SunoVoxRequest) toBody() map[string]any {
	body := map[string]any{}
	body["audio_id"] = r.AudioID
	body["vocal_end"] = r.VocalEnd
	body["vocal_start"] = r.VocalStart
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

// Vox Suno vocal/instrumental stems API. Pass an audio_id to asynchronously produce vocal-only and instrumental-only stem files for remixing and creative re
func (c *Suno) Vox(ctx context.Context, req SunoVoxRequest) (*TaskHandle, error) {
	result, err := c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/suno/vox",
		Body:   req.toBody(),
	})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/suno/tasks", c.t, result), nil
}

// SunoWavRequest is the input to suno.Wav.
type SunoWavRequest struct {
	// Used to obtain the existing audio ID of WAV format audio.
	AudioID string
	// Async submits without blocking; poll the returned handle. Defaults true.
	Async *bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r SunoWavRequest) toBody() map[string]any {
	body := map[string]any{}
	body["audio_id"] = r.AudioID
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

// Wav SUNO allows generating higher quality wav files based on the existing audio_id.
func (c *Suno) Wav(ctx context.Context, req SunoWavRequest) (*TaskHandle, error) {
	result, err := c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/suno/wav",
		Body:   req.toBody(),
	})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/suno/tasks", c.t, result), nil
}

// SunoMidiRequest is the input to suno.Midi.
type SunoMidiRequest struct {
	// The source audio ID for generating MIDI will extract MIDI content based on the existing audio.
	AudioID string
	// Async submits without blocking; poll the returned handle. Defaults true.
	Async *bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r SunoMidiRequest) toBody() map[string]any {
	body := map[string]any{}
	body["audio_id"] = r.AudioID
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

// Midi Suno MIDI API, retrieve MIDI data from generated music.
func (c *Suno) Midi(ctx context.Context, req SunoMidiRequest) (*TaskHandle, error) {
	result, err := c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/suno/midi",
		Body:   req.toBody(),
	})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/suno/tasks", c.t, result), nil
}

// SunoStyleRequest is the input to suno.Style.
type SunoStyleRequest struct {
	// Style prompts that need optimization.
	Prompt string
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r SunoStyleRequest) toBody() map[string]any {
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

// Style SUNO allows us to input prompts to generate enhanced song styles.
func (c *Suno) Style(ctx context.Context, req SunoStyleRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/suno/style",
		Body:   req.toBody(),
	})
}

// SunoLyricsRequest is the input to suno.Lyrics.
type SunoLyricsRequest struct {
	// The model used for generating lyrics has a default value of `default`, with optional values including `default
	Model string
	// Prompts for generating lyrics, describing the desired theme or style of the lyrics.
	Prompt string
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r SunoLyricsRequest) toBody() map[string]any {
	body := map[string]any{}
	body["model"] = r.Model
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

// Lyrics Suno lyrics generation API. Generates structured song lyrics from a prompt; supports the default and remi-v1 models.
func (c *Suno) Lyrics(ctx context.Context, req SunoLyricsRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/suno/lyrics",
		Body:   req.toBody(),
	})
}

// SunoMashupLyricsRequest is the input to suno.Mashup_Lyrics.
type SunoMashupLyricsRequest struct {
	// The first paragraph of lyrics content used for mixed generation.
	LyricsA string
	// The content of the second verse for mixed-generated lyrics.
	LyricsB string
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r SunoMashupLyricsRequest) toBody() map[string]any {
	body := map[string]any{}
	body["lyrics_a"] = r.LyricsA
	body["lyrics_b"] = r.LyricsB
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

// MashupLyrics Suno mashup lyrics API, merge two lyrics into a blended version.
func (c *Suno) MashupLyrics(ctx context.Context, req SunoMashupLyricsRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/suno/mashup-lyrics",
		Body:   req.toBody(),
	})
}

// SunoUploadRequest is the input to suno.Upload.
type SunoUploadRequest struct {
	// The CDN address (URL) for the custom audio file to be uploaded.
	AudioURL string
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r SunoUploadRequest) toBody() map[string]any {
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

// Upload Suno reference audio upload API, upload audio to get an audio_id for extended generation.
func (c *Suno) Upload(ctx context.Context, req SunoUploadRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/suno/upload",
		Body:   req.toBody(),
	})
}
