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
	// Suno Audios Lyric
	Lyric string
	// Suno Audios Model
	Model string
	// Suno Audios Style
	Style string
	// Suno Audios Variation Category
	VariationCategory string
	// Suno Audios Title
	Title string
	// Suno Audios Action
	Action string
	// Suno Audios Custom
	Custom bool
	// Suno Audios Prompt
	Prompt string
	// Suno Audios Lyric Prompt
	LyricPrompt string
	// Suno Audios Audio Id
	AudioID string
	// Suno Audios Mashup Audio Ids
	MashupAudioIDs []string
	// Suno Audios Audio Urls
	AudioURLs []string
	// Suno Audios Weirdness
	Weirdness float64
	// Suno Audios Persona Id
	PersonaID string
	// Suno Audios Overpainting Start
	OverpaintingStart float64
	// Suno Audios Overpainting End
	OverpaintingEnd float64
	// Suno Audios Samples Start
	SamplesStart float64
	// Suno Audios Samples End
	SamplesEnd float64
	// Suno Audios Underpainting Start
	UnderpaintingStart float64
	// Suno Audios Underpainting End
	UnderpaintingEnd float64
	// Suno Audios Continue At
	ContinueAt float64
	// Suno Audios Instrumental
	Instrumental bool
	// Suno Audios Vocal Gender
	VocalGender string
	// Suno Audios Negative Tags
	NegativeTags string
	// Suno Audios Style Influence
	StyleInfluence float64
	// Suno Audios Audio Weight
	AudioWeight float64
	// Suno Audios Duration
	Duration int
	// Suno Audios Replace Section End
	ReplaceSectionEnd float64
	// Suno Audios Replace Section Result Mode
	ReplaceSectionResultMode string
	// Suno Audios Replace Section Start
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
	}
	if r.Style != "" {
		body["style"] = r.Style
	}
	if r.VariationCategory != "" {
		body["variation_category"] = r.VariationCategory
	}
	if r.Title != "" {
		body["title"] = r.Title
	}
	if r.Action != "" {
		body["action"] = r.Action
	}
	body["custom"] = r.Custom
	if r.Prompt != "" {
		body["prompt"] = r.Prompt
	}
	if r.LyricPrompt != "" {
		body["lyric_prompt"] = r.LyricPrompt
	}
	if r.AudioID != "" {
		body["audio_id"] = r.AudioID
	}
	if r.MashupAudioIDs != nil {
		body["mashup_audio_ids"] = r.MashupAudioIDs
	}
	if r.AudioURLs != nil {
		body["audio_urls"] = r.AudioURLs
	}
	if r.Weirdness != 0 {
		body["weirdness"] = r.Weirdness
	}
	if r.PersonaID != "" {
		body["persona_id"] = r.PersonaID
	}
	if r.OverpaintingStart != 0 {
		body["overpainting_start"] = r.OverpaintingStart
	}
	if r.OverpaintingEnd != 0 {
		body["overpainting_end"] = r.OverpaintingEnd
	}
	if r.SamplesStart != 0 {
		body["samples_start"] = r.SamplesStart
	}
	if r.SamplesEnd != 0 {
		body["samples_end"] = r.SamplesEnd
	}
	if r.UnderpaintingStart != 0 {
		body["underpainting_start"] = r.UnderpaintingStart
	}
	if r.UnderpaintingEnd != 0 {
		body["underpainting_end"] = r.UnderpaintingEnd
	}
	if r.ContinueAt != 0 {
		body["continue_at"] = r.ContinueAt
	}
	body["instrumental"] = r.Instrumental
	if r.VocalGender != "" {
		body["vocal_gender"] = r.VocalGender
	}
	if r.NegativeTags != "" {
		body["negative_tags"] = r.NegativeTags
	}
	if r.StyleInfluence != 0 {
		body["style_influence"] = r.StyleInfluence
	}
	if r.AudioWeight != 0 {
		body["audio_weight"] = r.AudioWeight
	}
	if r.Duration != 0 {
		body["duration"] = r.Duration
	}
	if r.ReplaceSectionEnd != 0 {
		body["replace_section_end"] = r.ReplaceSectionEnd
	}
	if r.ReplaceSectionResultMode != "" {
		body["replace_section_result_mode"] = r.ReplaceSectionResultMode
	} else {
		body["replace_section_result_mode"] = "full_song"
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

// Generate Suno Audios
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
	// Suno Vox Audio Id
	AudioID string
	// Suno Vox Vocal Start
	VocalStart float64
	// Suno Vox Vocal End
	VocalEnd float64
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
	body["vocal_start"] = r.VocalStart
	body["vocal_end"] = r.VocalEnd
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

// Vox Suno Vox
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

// SunoMp3Request is the input to suno.Mp3.
type SunoMp3Request struct {
	// Suno Mp3 Audio Id
	AudioID string
	// Async submits without blocking; poll the returned handle. Defaults true.
	Async *bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r SunoMp3Request) toBody() map[string]any {
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

// Mp3 Suno Mp3
func (c *Suno) Mp3(ctx context.Context, req SunoMp3Request) (*TaskHandle, error) {
	result, err := c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/suno/mp3",
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
	// Suno Lyrics Model
	Model string
	// Suno Lyrics Prompt
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

// Lyrics Suno Lyrics
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
