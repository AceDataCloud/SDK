package acedatacloud

import (
	"context"
	"encoding/json"
	"net/url"
	"strings"
)

// ChatCompletionRequest is the input to OpenAI chat.completions.create.
//
// The struct exposes the common fields explicitly and an “Extra“ map
// for forward-compatible fields (tools, response_format, etc.).
type ChatCompletionRequest struct {
	Model       string           `json:"model"`
	Messages    []map[string]any `json:"messages"`
	Stream      bool             `json:"stream,omitempty"`
	MaxTokens   int              `json:"max_tokens,omitempty"`
	Temperature *float64         `json:"temperature,omitempty"`
	TopP        *float64         `json:"top_p,omitempty"`

	// Extra is merged into the request body. Keys here take precedence
	// over nothing — they are only added if the explicit field is zero.
	Extra map[string]any `json:"-"`
}

func (r ChatCompletionRequest) toBody() map[string]any {
	body := map[string]any{
		"model":    r.Model,
		"messages": r.Messages,
	}
	if r.Stream {
		body["stream"] = true
	}
	if r.MaxTokens > 0 {
		body["max_tokens"] = r.MaxTokens
	}
	if r.Temperature != nil {
		body["temperature"] = *r.Temperature
	}
	if r.TopP != nil {
		body["top_p"] = *r.TopP
	}
	for k, v := range r.Extra {
		if _, exists := body[k]; !exists {
			body[k] = v
		}
	}
	return body
}

// ResponsesRequest is the input to OpenAI responses.create.
type ResponsesRequest struct {
	Model  string         `json:"model"`
	Input  any            `json:"input"`
	Stream bool           `json:"stream,omitempty"`
	Extra  map[string]any `json:"-"`
}

func (r ResponsesRequest) toBody() map[string]any {
	body := map[string]any{"model": r.Model, "input": r.Input}
	if r.Stream {
		body["stream"] = true
	}
	for k, v := range r.Extra {
		if _, exists := body[k]; !exists {
			body[k] = v
		}
	}
	return body
}

// OpenAIResource groups the OpenAI-compatible endpoints.
type OpenAIResource struct {
	t *transport
}

// Chat returns the chat sub-namespace.
func (o *OpenAIResource) Chat() *OpenAIChat { return &OpenAIChat{t: o.t} }

// Responses returns the responses sub-namespace.
func (o *OpenAIResource) Responses() *OpenAIResponses { return &OpenAIResponses{t: o.t} }

// Models returns the models sub-namespace.
func (o *OpenAIResource) Models() *OpenAIModels { return &OpenAIModels{t: o.t} }

// Audio returns the audio sub-namespace.
func (o *OpenAIResource) Audio() *OpenAIAudio { return &OpenAIAudio{t: o.t} }

// Realtime returns the realtime sub-namespace.
func (o *OpenAIResource) Realtime() *OpenAIRealtime { return &OpenAIRealtime{t: o.t} }

// OpenAIChat exposes “/openai/chat/completions“.
type OpenAIChat struct{ t *transport }

// Completions returns the completions sub-namespace.
func (c *OpenAIChat) Completions() *OpenAIChatCompletions { return &OpenAIChatCompletions{t: c.t} }

// OpenAIChatCompletions exposes chat.completions.create.
type OpenAIChatCompletions struct{ t *transport }

// Create performs a blocking (non-streaming) chat completion.
func (c *OpenAIChatCompletions) Create(ctx context.Context, req ChatCompletionRequest) (map[string]any, error) {
	body := req.toBody()
	delete(body, "stream")
	return c.t.do(ctx, requestOpts{Method: "POST", Path: "/openai/chat/completions", Body: body})
}

// CreateStream performs a streaming chat completion and returns a
// channel of decoded chunks (each a “map[string]any“ parsed from a
// single SSE “data:“ line).
func (c *OpenAIChatCompletions) CreateStream(ctx context.Context, req ChatCompletionRequest) (<-chan map[string]any, <-chan error) {
	req.Stream = true
	return streamDecode(c.t, "/openai/chat/completions", req.toBody())
}

// OpenAIResponses exposes “/openai/responses“.
type OpenAIResponses struct{ t *transport }

// Create performs a blocking responses.create.
func (r *OpenAIResponses) Create(ctx context.Context, req ResponsesRequest) (map[string]any, error) {
	body := req.toBody()
	delete(body, "stream")
	return r.t.do(ctx, requestOpts{Method: "POST", Path: "/openai/responses", Body: body})
}

// CreateStream performs a streaming responses.create.
func (r *OpenAIResponses) CreateStream(ctx context.Context, req ResponsesRequest) (<-chan map[string]any, <-chan error) {
	req.Stream = true
	return streamDecode(r.t, "/openai/responses", req.toBody())
}

// OpenAIModels exposes “/openai/models“.
type OpenAIModels struct{ t *transport }

// List returns the available OpenAI-compatible models.
func (m *OpenAIModels) List(ctx context.Context) (map[string]any, error) {
	return m.t.do(ctx, requestOpts{Method: "GET", Path: "/openai/models"})
}

// OpenAIAudio exposes “/v1/audio/*“.
type OpenAIAudio struct{ t *transport }

// Speech returns the speech sub-namespace.
func (a *OpenAIAudio) Speech() *OpenAIAudioSpeech { return &OpenAIAudioSpeech{t: a.t} }

// Transcriptions returns the transcriptions sub-namespace.
func (a *OpenAIAudio) Transcriptions() *OpenAIAudioTranscriptions {
	return &OpenAIAudioTranscriptions{t: a.t}
}

// AudioSpeechRequest is the input to OpenAI audio.speech.create.
type AudioSpeechRequest struct {
	Input          string
	Model          string
	Voice          string
	ResponseFormat string
	Speed          *float64
	Extra          map[string]any
}

func (r AudioSpeechRequest) toBody() map[string]any {
	body := map[string]any{"input": r.Input}
	if r.Model != "" {
		body["model"] = r.Model
	}
	if r.Voice != "" {
		body["voice"] = r.Voice
	}
	if r.ResponseFormat != "" {
		body["response_format"] = r.ResponseFormat
	}
	if r.Speed != nil {
		body["speed"] = *r.Speed
	}
	for k, v := range r.Extra {
		if _, exists := body[k]; !exists {
			body[k] = v
		}
	}
	return body
}

// OpenAIAudioSpeech exposes audio.speech.create.
type OpenAIAudioSpeech struct{ t *transport }

// Create synthesizes speech and returns the binary audio bytes.
func (s *OpenAIAudioSpeech) Create(ctx context.Context, req AudioSpeechRequest) ([]byte, error) {
	return s.t.doBytes(ctx, requestOpts{Method: "POST", Path: "/v1/audio/speech", Body: req.toBody()})
}

// AudioTranscriptionRequest is the input to OpenAI audio.transcriptions.create.
type AudioTranscriptionRequest struct {
	File                   []byte
	Filename               string
	Model                  string
	Language               string
	Prompt                 string
	ResponseFormat         string
	Temperature            *float64
	TimestampGranularities []string
	Stream                 *bool
	Languages              []string
	Keywords               []string
	Extra                  map[string]any
}

func (r AudioTranscriptionRequest) fields() map[string]any {
	fields := map[string]any{}
	for k, v := range r.Extra {
		fields[k] = v
	}
	if r.Model != "" {
		fields["model"] = r.Model
	}
	if r.Language != "" {
		fields["language"] = r.Language
	}
	if r.Prompt != "" {
		fields["prompt"] = r.Prompt
	}
	if r.ResponseFormat != "" {
		fields["response_format"] = r.ResponseFormat
	}
	if r.Temperature != nil {
		fields["temperature"] = *r.Temperature
	}
	if r.TimestampGranularities != nil {
		fields["timestamp_granularities[]"] = r.TimestampGranularities
	}
	if r.Stream != nil {
		fields["stream"] = *r.Stream
	}
	if r.Languages != nil {
		fields["languages[]"] = r.Languages
	}
	if r.Keywords != nil {
		fields["keywords[]"] = r.Keywords
	}
	return fields
}

// OpenAIAudioTranscriptions exposes audio.transcriptions.create.
type OpenAIAudioTranscriptions struct{ t *transport }

// Create transcribes audio and returns either a JSON map or text, depending on response_format.
func (tr *OpenAIAudioTranscriptions) Create(ctx context.Context, req AudioTranscriptionRequest) (any, error) {
	filename := req.Filename
	if filename == "" {
		filename = "audio"
	}
	return tr.t.doMultipart(ctx, multipartRequest{
		Path:     "/v1/audio/transcriptions",
		File:     req.File,
		Filename: filename,
		Fields:   req.fields(),
	})
}

// OpenAIRealtime exposes realtime URL construction.
type OpenAIRealtime struct{ t *transport }

// URL builds the websocket URL for the realtime endpoint.
func (r *OpenAIRealtime) URL(model string) string {
	if model == "" {
		model = "gpt-realtime"
	}
	base := strings.TrimRight(r.t.opts.baseURL, "/")
	base = strings.Replace(base, "https://", "wss://", 1)
	base = strings.Replace(base, "http://", "ws://", 1)
	values := url.Values{}
	values.Set("model", model)
	return base + "/v1/realtime?" + values.Encode()
}

// streamDecode wraps transport.stream and parses each SSE data line as JSON.
func streamDecode(t *transport, path string, body any) (<-chan map[string]any, <-chan error) {
	raw, rawErr := t.stream(context.Background(), path, body)
	out := make(chan map[string]any)
	errCh := make(chan error, 1)
	go func() {
		defer close(out)
		defer close(errCh)
		for {
			select {
			case chunk, ok := <-raw:
				if !ok {
					return
				}
				parsed := map[string]any{}
				if err := json.Unmarshal(chunk, &parsed); err == nil {
					out <- parsed
				}
			case err, ok := <-rawErr:
				if ok && err != nil {
					errCh <- err
					return
				}
				if !ok {
					return
				}
			}
		}
	}()
	return out, errCh
}
