package acedatacloud

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"mime/multipart"
	"strconv"
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

// Audio returns the audio sub-namespace.
func (o *OpenAIResource) Audio() *OpenAIAudio { return &OpenAIAudio{t: o.t} }

// Models returns the models sub-namespace.
func (o *OpenAIResource) Models() *OpenAIModels { return &OpenAIModels{t: o.t} }

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

// SpeechRequest is the input to OpenAI audio.Speech.
type SpeechRequest struct {
	Input          string         `json:"input"`
	Model          string         `json:"model,omitempty"`
	Voice          string         `json:"voice,omitempty"`
	ResponseFormat string         `json:"response_format,omitempty"`
	Speed          *float64       `json:"speed,omitempty"`
	Extra          map[string]any `json:"-"`
}

func (r SpeechRequest) toBody() map[string]any {
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

// TranscriptionRequest is the input to OpenAI audio.Transcriptions.Create.
//
// File holds the audio payload uploaded as multipart/form-data.
type TranscriptionRequest struct {
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

	// Extra fields are appended to the form as strings.
	Extra map[string]string
}

// OpenAIAudio exposes “/v1/audio/*“.
type OpenAIAudio struct{ t *transport }

// Transcriptions returns the transcriptions sub-namespace.
func (a *OpenAIAudio) Transcriptions() *OpenAITranscriptions { return &OpenAITranscriptions{t: a.t} }

// Speech synthesizes speech and returns the raw audio bytes.
func (a *OpenAIAudio) Speech(ctx context.Context, req SpeechRequest) ([]byte, error) {
	body, err := json.Marshal(req.toBody())
	if err != nil {
		return nil, fmt.Errorf("marshal body: %w", err)
	}
	return a.t.doRaw(ctx, "POST", "/v1/audio/speech", "application/json", body)
}

// OpenAITranscriptions exposes “/v1/audio/transcriptions“.
type OpenAITranscriptions struct{ t *transport }

// Create transcribes an audio file.
//
// A “response_format“ other than json/verbose_json answers with plain text,
// which is returned under the “text“ key so the result shape stays stable.
func (tr *OpenAITranscriptions) Create(ctx context.Context, req TranscriptionRequest) (map[string]any, error) {
	if len(req.File) == 0 {
		return nil, &ValidationError{&APIError{Message: "File is required", ErrCode: "bad_request"}}
	}

	buf := &bytes.Buffer{}
	writer := multipart.NewWriter(buf)
	filename := req.Filename
	if filename == "" {
		filename = "audio.mp3"
	}
	part, err := writer.CreateFormFile("file", filename)
	if err != nil {
		return nil, fmt.Errorf("build form: %w", err)
	}
	if _, err := part.Write(req.File); err != nil {
		return nil, fmt.Errorf("build form: %w", err)
	}

	fields := []struct{ name, value string }{
		{"model", req.Model},
		{"language", req.Language},
		{"prompt", req.Prompt},
		{"response_format", req.ResponseFormat},
	}
	for _, field := range fields {
		if field.value == "" {
			continue
		}
		if err := writer.WriteField(field.name, field.value); err != nil {
			return nil, fmt.Errorf("build form: %w", err)
		}
	}
	if req.Temperature != nil {
		if err := writer.WriteField("temperature", strconv.FormatFloat(*req.Temperature, 'f', -1, 64)); err != nil {
			return nil, fmt.Errorf("build form: %w", err)
		}
	}
	if req.Stream != nil {
		if err := writer.WriteField("stream", strconv.FormatBool(*req.Stream)); err != nil {
			return nil, fmt.Errorf("build form: %w", err)
		}
	}
	repeated := []struct {
		name   string
		values []string
	}{
		{"timestamp_granularities[]", req.TimestampGranularities},
		{"languages[]", req.Languages},
		{"keywords[]", req.Keywords},
	}
	for _, group := range repeated {
		for _, value := range group.values {
			if err := writer.WriteField(group.name, value); err != nil {
				return nil, fmt.Errorf("build form: %w", err)
			}
		}
	}
	for name, value := range req.Extra {
		if err := writer.WriteField(name, value); err != nil {
			return nil, fmt.Errorf("build form: %w", err)
		}
	}
	if err := writer.Close(); err != nil {
		return nil, fmt.Errorf("build form: %w", err)
	}

	raw, err := tr.t.doRaw(ctx, "POST", "/v1/audio/transcriptions", writer.FormDataContentType(), buf.Bytes())
	if err != nil {
		return nil, err
	}
	parsed := map[string]any{}
	if err := json.Unmarshal(raw, &parsed); err != nil {
		return map[string]any{"text": string(raw)}, nil
	}
	return parsed, nil
}

// OpenAIModels exposes “/openai/models“.
type OpenAIModels struct{ t *transport }

// List returns the models the token may call.
func (m *OpenAIModels) List(ctx context.Context) (map[string]any, error) {
	return m.t.do(ctx, requestOpts{Method: "GET", Path: "/openai/models"})
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
