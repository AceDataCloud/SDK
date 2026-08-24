package acedatacloud

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"mime/multipart"
	"net/http"
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

// AudioSpeechRequest is the input to OpenAI audio.speech.create.
type AudioSpeechRequest struct {
	Model          string         `json:"model,omitempty"`
	Input          string         `json:"input"`
	Voice          string         `json:"voice,omitempty"`
	ResponseFormat string         `json:"response_format,omitempty"`
	Speed          *float64       `json:"speed,omitempty"`
	Extra          map[string]any `json:"-"`
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

// OpenAIResource groups the OpenAI-compatible endpoints.
type OpenAIResource struct {
	t *transport
}

// Chat returns the chat sub-namespace.
func (o *OpenAIResource) Chat() *OpenAIChat { return &OpenAIChat{t: o.t} }

// Models returns the models sub-namespace.
func (o *OpenAIResource) Models() *OpenAIModels { return &OpenAIModels{t: o.t} }

// Responses returns the responses sub-namespace.
func (o *OpenAIResource) Responses() *OpenAIResponses { return &OpenAIResponses{t: o.t} }

// Audio returns the audio sub-namespace.
func (o *OpenAIResource) Audio() *OpenAIAudio { return &OpenAIAudio{t: o.t} }

// Realtime returns the realtime sub-namespace.
func (o *OpenAIResource) Realtime() *OpenAIRealtime { return &OpenAIRealtime{t: o.t} }

// OpenAIChat exposes “/v1/chat/completions“.
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

// OpenAIModels exposes “/openai/models“.
type OpenAIModels struct{ t *transport }

// List returns available OpenAI-compatible models.
func (m *OpenAIModels) List(ctx context.Context) (map[string]any, error) {
	return m.t.do(ctx, requestOpts{Method: "GET", Path: "/openai/models"})
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

// OpenAIAudio exposes “/v1/audio/*“.
type OpenAIAudio struct{ t *transport }

// Speech returns the speech sub-namespace.
func (a *OpenAIAudio) Speech() *OpenAIAudioSpeech { return &OpenAIAudioSpeech{t: a.t} }

// Transcriptions returns the transcriptions sub-namespace.
func (a *OpenAIAudio) Transcriptions() *OpenAIAudioTranscriptions {
	return &OpenAIAudioTranscriptions{t: a.t}
}

// OpenAIAudioSpeech exposes audio.speech.create.
type OpenAIAudioSpeech struct{ t *transport }

// Create returns the generated audio bytes.
func (s *OpenAIAudioSpeech) Create(ctx context.Context, req AudioSpeechRequest) ([]byte, error) {
	return doRaw(ctx, s.t, http.MethodPost, "/v1/audio/speech", req.toBody(), "")
}

// OpenAIAudioTranscriptions exposes audio.transcriptions.create.
type OpenAIAudioTranscriptions struct{ t *transport }

// Create transcribes audio using a multipart/form-data request.
func (tr *OpenAIAudioTranscriptions) Create(ctx context.Context, req AudioTranscriptionRequest) (map[string]any, error) {
	return doTranscription(ctx, tr.t, req)
}

// OpenAIRealtime exposes “/v1/realtime“.
type OpenAIRealtime struct{ t *transport }

// Connect calls the realtime endpoint.
func (r *OpenAIRealtime) Connect(ctx context.Context) (map[string]any, error) {
	return r.t.do(ctx, requestOpts{Method: "GET", Path: "/v1/realtime"})
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

func doRaw(ctx context.Context, t *transport, method, path string, body any, contentType string) ([]byte, error) {
	var bodyBytes []byte
	if body != nil {
		var err error
		bodyBytes, err = json.Marshal(body)
		if err != nil {
			return nil, fmt.Errorf("marshal body: %w", err)
		}
	}
	req, err := http.NewRequestWithContext(ctx, method, t.opts.baseURL+path, bytes.NewReader(bodyBytes))
	if err != nil {
		return nil, fmt.Errorf("build request: %w", err)
	}
	for k, v := range t.headers {
		req.Header.Set(k, v)
	}
	if contentType != "" {
		req.Header.Set("Content-Type", contentType)
	}
	resp, err := t.httpClient.Do(req)
	if err != nil {
		return nil, &TransportError{&APIError{Message: err.Error()}}
	}
	defer resp.Body.Close()
	respBody, _ := io.ReadAll(resp.Body)
	if resp.StatusCode >= 400 {
		parsed := map[string]any{}
		if err := json.Unmarshal(respBody, &parsed); err != nil {
			parsed = map[string]any{"error": map[string]any{"code": "unknown", "message": string(respBody)}}
		}
		return nil, mapError(resp.StatusCode, parsed)
	}
	return respBody, nil
}

func doTranscription(ctx context.Context, t *transport, req AudioTranscriptionRequest) (map[string]any, error) {
	var body bytes.Buffer
	writer := multipart.NewWriter(&body)
	filename := req.Filename
	if filename == "" {
		filename = "audio"
	}
	part, err := writer.CreateFormFile("file", filename)
	if err != nil {
		return nil, err
	}
	if _, err := part.Write(req.File); err != nil {
		return nil, err
	}
	writeFormField(writer, "model", req.Model)
	writeFormField(writer, "language", req.Language)
	writeFormField(writer, "prompt", req.Prompt)
	writeFormField(writer, "response_format", req.ResponseFormat)
	if req.Temperature != nil {
		writeFormField(writer, "temperature", fmt.Sprintf("%v", *req.Temperature))
	}
	if req.Stream != nil {
		writeFormField(writer, "stream", fmt.Sprintf("%t", *req.Stream))
	}
	for _, item := range req.TimestampGranularities {
		writeFormField(writer, "timestamp_granularities[]", item)
	}
	for _, item := range req.Languages {
		writeFormField(writer, "languages[]", item)
	}
	for _, item := range req.Keywords {
		writeFormField(writer, "keywords[]", item)
	}
	for k, v := range req.Extra {
		writeFormField(writer, k, fmt.Sprintf("%v", v))
	}
	if err := writer.Close(); err != nil {
		return nil, err
	}
	raw, err := doRawBody(ctx, t, http.MethodPost, "/v1/audio/transcriptions", body.Bytes(), writer.FormDataContentType())
	if err != nil {
		return nil, err
	}
	parsed := map[string]any{}
	if len(strings.TrimSpace(string(raw))) == 0 {
		return parsed, nil
	}
	if err := json.Unmarshal(raw, &parsed); err != nil {
		return nil, fmt.Errorf("parse response: %w", err)
	}
	return parsed, nil
}

func writeFormField(writer *multipart.Writer, key, value string) {
	if value != "" {
		_ = writer.WriteField(key, value)
	}
}

func doRawBody(ctx context.Context, t *transport, method, path string, body []byte, contentType string) ([]byte, error) {
	req, err := http.NewRequestWithContext(ctx, method, t.opts.baseURL+path, bytes.NewReader(body))
	if err != nil {
		return nil, fmt.Errorf("build request: %w", err)
	}
	for k, v := range t.headers {
		req.Header.Set(k, v)
	}
	if contentType != "" {
		req.Header.Set("Content-Type", contentType)
	}
	resp, err := t.httpClient.Do(req)
	if err != nil {
		return nil, &TransportError{&APIError{Message: err.Error()}}
	}
	defer resp.Body.Close()
	respBody, _ := io.ReadAll(resp.Body)
	if resp.StatusCode >= 400 {
		parsed := map[string]any{}
		if err := json.Unmarshal(respBody, &parsed); err != nil {
			parsed = map[string]any{"error": map[string]any{"code": "unknown", "message": string(respBody)}}
		}
		return nil, mapError(resp.StatusCode, parsed)
	}
	return respBody, nil
}
