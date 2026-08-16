package acedatacloud

import (
	"bytes"
	"context"
	"encoding/json"
	"mime/multipart"
	"net/http"
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

// OpenAIListModelsResponse is returned by OpenAI models.list.
type OpenAIListModelsResponse map[string]any

// AudioSpeechRequest is the input to OpenAI audio.speech.create.
type AudioSpeechRequest struct {
	Input          string
	Model          string
	Voice          string
	ResponseFormat string
	Speed          float64
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
	if r.Speed != 0 {
		body["speed"] = r.Speed
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
	Extra                  map[string]string
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

// OpenAIModels exposes models.list.
type OpenAIModels struct{ t *transport }

// List returns the models available through the OpenAI-compatible API.
func (m *OpenAIModels) List(ctx context.Context) (OpenAIListModelsResponse, error) {
	return m.t.do(ctx, requestOpts{Method: "GET", Path: "/openai/models"})
}

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

// OpenAIAudio exposes OpenAI-compatible audio endpoints.
type OpenAIAudio struct{ t *transport }

// Speech returns the speech sub-namespace.
func (a *OpenAIAudio) Speech() *OpenAIAudioSpeech { return &OpenAIAudioSpeech{t: a.t} }

// Transcriptions returns the transcriptions sub-namespace.
func (a *OpenAIAudio) Transcriptions() *OpenAIAudioTranscriptions {
	return &OpenAIAudioTranscriptions{t: a.t}
}

// OpenAIAudioSpeech exposes audio.speech.create.
type OpenAIAudioSpeech struct{ t *transport }

// Create synthesizes speech and returns the audio bytes.
func (s *OpenAIAudioSpeech) Create(ctx context.Context, req AudioSpeechRequest) ([]byte, error) {
	return s.t.doBytes(ctx, requestOpts{Method: "POST", Path: "/v1/audio/speech", Body: req.toBody()})
}

// OpenAIAudioTranscriptions exposes audio.transcriptions.create.
type OpenAIAudioTranscriptions struct{ t *transport }

// Create transcribes an audio file and parses the default JSON response.
func (tr *OpenAIAudioTranscriptions) Create(ctx context.Context, req AudioTranscriptionRequest) (map[string]any, error) {
	var body bytes.Buffer
	writer := multipart.NewWriter(&body)
	part, err := writer.CreateFormFile("file", req.Filename)
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
		if *req.Stream {
			fields["stream"] = "true"
		} else {
			fields["stream"] = "false"
		}
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
	return tr.t.do(ctx, requestOpts{
		Method:      http.MethodPost,
		Path:        "/v1/audio/transcriptions",
		RawBody:     body.Bytes(),
		ContentType: writer.FormDataContentType(),
	})
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
