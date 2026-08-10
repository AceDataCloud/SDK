package acedatacloud

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"mime/multipart"
	"net/http"
	"net/url"
	"strconv"
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

// SpeechRequest is the input to OpenAI audio.speech.
type SpeechRequest struct {
	Input          string
	Model          string
	Voice          string
	ResponseFormat string
	Speed          *float64
	Extra          map[string]any
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

// TranscriptionRequest is the input to OpenAI audio.transcriptions.
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
	Extra                  map[string]string
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

// List returns available OpenAI-compatible models.
func (m *OpenAIModels) List(ctx context.Context) (map[string]any, error) {
	return m.t.do(ctx, requestOpts{Method: "GET", Path: "/openai/models"})
}

// OpenAIAudio exposes OpenAI-compatible audio endpoints.
type OpenAIAudio struct{ t *transport }

// Speech converts text to speech and returns the audio bytes.
func (a *OpenAIAudio) Speech(ctx context.Context, req SpeechRequest) ([]byte, error) {
	return a.t.doBytes(ctx, requestOpts{Method: "POST", Path: "/v1/audio/speech", Body: req.toBody()})
}

// Transcriptions transcribes an audio file and returns the JSON or text response.
func (a *OpenAIAudio) Transcriptions(ctx context.Context, req TranscriptionRequest) (any, error) {
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
	fields := map[string]string{}
	for k, v := range req.Extra {
		fields[k] = v
	}
	if req.Model != "" {
		fields["model"] = req.Model
	}
	if req.Language != "" {
		fields["language"] = req.Language
	}
	if req.Prompt != "" {
		fields["prompt"] = req.Prompt
	}
	if req.ResponseFormat != "" {
		fields["response_format"] = req.ResponseFormat
	}
	if req.Temperature != nil {
		fields["temperature"] = strconv.FormatFloat(*req.Temperature, 'f', -1, 64)
	}
	if req.Stream != nil {
		fields["stream"] = strconv.FormatBool(*req.Stream)
	}
	for k, v := range fields {
		if err := writer.WriteField(k, v); err != nil {
			return nil, err
		}
	}
	for _, value := range req.TimestampGranularities {
		if err := writer.WriteField("timestamp_granularities[]", value); err != nil {
			return nil, err
		}
	}
	for _, value := range req.Languages {
		if err := writer.WriteField("languages[]", value); err != nil {
			return nil, err
		}
	}
	for _, value := range req.Keywords {
		if err := writer.WriteField("keywords[]", value); err != nil {
			return nil, err
		}
	}
	if err := writer.Close(); err != nil {
		return nil, err
	}

	respBody, contentType, err := a.t.doRaw(ctx, "POST", "/v1/audio/transcriptions", &body, writer.FormDataContentType())
	if err != nil {
		return nil, err
	}
	if strings.HasPrefix(contentType, "text/plain") {
		return string(respBody), nil
	}
	parsed := map[string]any{}
	if err := json.Unmarshal(respBody, &parsed); err != nil {
		return nil, err
	}
	return parsed, nil
}

// OpenAIRealtime exposes the realtime WebSocket URL helper.
type OpenAIRealtime struct{ t *transport }

// URL returns a WebSocket URL for the realtime endpoint.
func (r *OpenAIRealtime) URL(model string) (string, error) {
	if model == "" {
		model = "gpt-realtime-2.1"
	}
	base, err := url.Parse(r.t.opts.baseURL)
	if err != nil {
		return "", err
	}
	if base.Scheme == "https" {
		base.Scheme = "wss"
	} else {
		base.Scheme = "ws"
	}
	base.Path = "/v1/realtime"
	base.RawQuery = url.Values{"model": []string{model}}.Encode()
	return base.String(), nil
}

func (t *transport) doBytes(ctx context.Context, r requestOpts) ([]byte, error) {
	respBody, _, err := t.doRaw(ctx, r.Method, r.Path, mustJSONReader(r.Body), "application/json")
	return respBody, err
}

func mustJSONReader(body any) io.Reader {
	if body == nil {
		return nil
	}
	data, err := json.Marshal(body)
	if err != nil {
		return strings.NewReader("{}")
	}
	return bytes.NewReader(data)
}

func (t *transport) doRaw(ctx context.Context, method string, path string, body io.Reader, contentType string) ([]byte, string, error) {
	req, err := http.NewRequestWithContext(ctx, method, t.opts.baseURL+path, body)
	if err != nil {
		return nil, "", fmt.Errorf("build request: %w", err)
	}
	for k, v := range t.headers {
		req.Header.Set(k, v)
	}
	if contentType != "" {
		req.Header.Set("Content-Type", contentType)
	}
	resp, err := t.httpClient.Do(req)
	if err != nil {
		return nil, "", &TransportError{&APIError{Message: err.Error()}}
	}
	defer resp.Body.Close()
	respBody, _ := io.ReadAll(resp.Body)
	if resp.StatusCode >= 400 {
		parsed := map[string]any{}
		if err := json.Unmarshal(respBody, &parsed); err != nil {
			parsed = map[string]any{"error": map[string]any{"code": "unknown", "message": string(respBody)}}
		}
		return nil, "", mapError(resp.StatusCode, parsed)
	}
	return respBody, resp.Header.Get("Content-Type"), nil
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
