package acedatacloud

import (
	"context"
	"encoding/base64"
	"encoding/json"
	"io"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"time"
)

func TestNewClient_RequiresTokenOrHandler(t *testing.T) {
	t.Setenv("ACEDATACLOUD_API_TOKEN", "")
	_, err := NewClient()
	if err == nil {
		t.Fatal("expected error when no token and no payment handler")
	}
	if _, ok := err.(*AuthenticationError); !ok {
		t.Fatalf("expected AuthenticationError, got %T", err)
	}
}

func TestNewClient_WithToken(t *testing.T) {
	c, err := NewClient(WithAPIToken("test-token"))
	if err != nil {
		t.Fatalf("NewClient: %v", err)
	}
	if c.OpenAI() == nil || c.Chat() == nil || c.Captcha() == nil || c.Images() == nil || c.Tasks() == nil {
		t.Fatal("resources must be non-nil")
	}
}

func TestCaptchaEndpoints(t *testing.T) {
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		switch r.URL.Path {
		case "/captcha/recognition/hcaptcha":
			_, _ = w.Write([]byte(`{"task_id":"captcha-recognition-task"}`))
		case "/captcha/token/hcaptcha":
			_, _ = w.Write([]byte(`{"task_id":"captcha-token-task"}`))
		case "/captcha/tasks":
			_, _ = w.Write([]byte(`{"status":"succeeded"}`))
		default:
			t.Fatalf("unexpected path: %s", r.URL.Path)
		}
	}))
	defer srv.Close()

	c, _ := NewClient(WithAPIToken("t"), WithBaseURL(srv.URL))
	if _, err := c.Captcha().Recognition().HCaptcha(context.Background(), CaptchaRecognitionHCaptchaRequest{
		Queries:  []string{"cat", "dog"},
		Question: "Choose cats",
		Async:    true,
	}); err != nil {
		t.Fatalf("Recognition HCaptcha: %v", err)
	}
	if _, err := c.Captcha().Token().HCaptcha(context.Background(), CaptchaTokenHCaptchaRequest{
		WebsiteKey: "site-key",
		WebsiteURL: "https://accounts.hcaptcha.com/demo",
		Async:      true,
	}); err != nil {
		t.Fatalf("Token HCaptcha: %v", err)
	}
	if _, err := c.Captcha().Tasks().Retrieve(context.Background(), "task-1", nil); err != nil {
		t.Fatalf("Tasks Retrieve: %v", err)
	}
}

func TestChatCompletions_Create(t *testing.T) {
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/v1/chat/completions" {
			t.Errorf("unexpected path %s", r.URL.Path)
		}
		if r.Header.Get("Authorization") != "Bearer token-abc" {
			t.Errorf("missing auth header")
		}
		var body map[string]any
		_ = json.NewDecoder(r.Body).Decode(&body)
		if body["model"] != "gpt-4o-mini" {
			t.Errorf("bad model: %v", body["model"])
		}
		w.Header().Set("Content-Type", "application/json")
		_, _ = w.Write([]byte(`{"id":"c1","choices":[{"message":{"role":"assistant","content":"hi"}}]}`))
	}))
	defer srv.Close()

	c, _ := NewClient(WithAPIToken("token-abc"), WithBaseURL(srv.URL))
	res, err := c.OpenAI().Chat().Completions().Create(context.Background(), ChatCompletionRequest{
		Model:    "gpt-4o-mini",
		Messages: []map[string]any{{"role": "user", "content": "hi"}},
	})
	if err != nil {
		t.Fatalf("Create: %v", err)
	}
	if res["id"] != "c1" {
		t.Fatalf("bad response: %+v", res)
	}
}

func TestTransport_RetriesOn503(t *testing.T) {
	attempts := 0
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		attempts++
		if attempts < 2 {
			w.WriteHeader(503)
			_, _ = w.Write([]byte(`{"error":{"code":"unknown","message":"busy"}}`))
			return
		}
		w.Header().Set("Content-Type", "application/json")
		_, _ = w.Write([]byte(`{"ok":true}`))
	}))
	defer srv.Close()

	c, _ := NewClient(WithAPIToken("t"), WithBaseURL(srv.URL), WithMaxRetries(3))
	res, err := c.OpenAI().Chat().Completions().Create(context.Background(), ChatCompletionRequest{
		Model:    "m",
		Messages: []map[string]any{{"role": "user", "content": "x"}},
	})
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if res["ok"] != true {
		t.Fatalf("bad response: %+v", res)
	}
	if attempts != 2 {
		t.Fatalf("expected 2 attempts, got %d", attempts)
	}
}

func TestTransport_MapErrorNon401(t *testing.T) {
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(429)
		_, _ = w.Write([]byte(`{"error":{"code":"too_many_requests","message":"slow down"},"trace_id":"abc"}`))
	}))
	defer srv.Close()

	c, _ := NewClient(WithAPIToken("t"), WithBaseURL(srv.URL), WithMaxRetries(0))
	_, err := c.OpenAI().Chat().Completions().Create(context.Background(), ChatCompletionRequest{
		Model:    "m",
		Messages: []map[string]any{{"role": "user", "content": "x"}},
	})
	if err == nil {
		t.Fatal("expected error")
	}
	rl, ok := err.(*RateLimitError)
	if !ok {
		t.Fatalf("expected RateLimitError, got %T: %v", err, err)
	}
	if rl.TraceID() != "abc" {
		t.Errorf("missing trace_id: %+v", rl)
	}
}

func TestTransport_MapErrorWithStringBody(t *testing.T) {
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(402)
		_, _ = w.Write([]byte(`{"error":"insufficient payment"}`))
	}))
	defer srv.Close()

	// No payment handler, so 402 is raised as a plain error.
	c, _ := NewClient(WithAPIToken("t"), WithBaseURL(srv.URL), WithMaxRetries(0))
	_, err := c.OpenAI().Chat().Completions().Create(context.Background(), ChatCompletionRequest{
		Model:    "m",
		Messages: []map[string]any{{"role": "user", "content": "x"}},
	})
	if err == nil {
		t.Fatal("expected error")
	}
	apiErr, ok := err.(*APIError)
	if !ok {
		t.Fatalf("expected *APIError, got %T: %v", err, err)
	}
	if apiErr.Message != "insufficient payment" {
		t.Errorf("bad message: %q", apiErr.Message)
	}
}

func TestPaymentHandler_OnSecond402ThenSuccess(t *testing.T) {
	hit := 0
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		hit++
		if hit == 1 {
			if r.Header.Get("X-Payment") != "" {
				t.Errorf("first request should not have X-Payment")
			}
			w.Header().Set("Content-Type", "application/json")
			w.WriteHeader(402)
			_, _ = w.Write([]byte(`{"x402Version":2,"accepts":[{"network":"base","scheme":"exact","payTo":"0xabc","asset":"0xusdc","maxAmountRequired":"100"}]}`))
			return
		}
		if got := r.Header.Get("X-Payment"); got != "fake-envelope" {
			t.Errorf("expected X-Payment=fake-envelope, got %q", got)
		}
		w.Header().Set("Content-Type", "application/json")
		_, _ = w.Write([]byte(`{"paid":true}`))
	}))
	defer srv.Close()

	var received PaymentContext
	handler := PaymentHandlerFunc(func(ctx context.Context, pctx PaymentContext) (PaymentResult, error) {
		received = pctx
		return PaymentResult{Headers: map[string]string{"X-Payment": "fake-envelope"}}, nil
	})

	c, _ := NewClient(WithBaseURL(srv.URL), WithPaymentHandler(handler))
	res, err := c.OpenAI().Chat().Completions().Create(context.Background(), ChatCompletionRequest{
		Model:    "m",
		Messages: []map[string]any{{"role": "user", "content": "x"}},
	})
	if err != nil {
		t.Fatalf("Create: %v", err)
	}
	if res["paid"] != true {
		t.Fatalf("bad response: %+v", res)
	}
	if len(received.Accepts) != 1 || received.Accepts[0]["network"] != "base" {
		t.Fatalf("payment context not propagated: %+v", received)
	}
	if hit != 2 {
		t.Fatalf("expected 2 hits, got %d", hit)
	}
}

func TestPaymentHandler_ParsesPaymentRequiredHeader(t *testing.T) {
	var calls int
	required := `{"x402Version":2,"accepts":[{"network":"eip155:8453","scheme":"exact","amount":"1"}]}`
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		calls++
		if calls == 1 {
			w.Header().Set("PAYMENT-REQUIRED", base64.StdEncoding.EncodeToString([]byte(required)))
			w.WriteHeader(http.StatusPaymentRequired)
			_, _ = w.Write([]byte(`{"error":"payment required"}`))
			return
		}
		if got := r.Header.Get("PAYMENT-SIGNATURE"); got != "signed-payment" {
			t.Fatalf("expected PAYMENT-SIGNATURE, got %q", got)
		}
		_, _ = w.Write([]byte(`{"ok":true}`))
	}))
	defer srv.Close()

	handler := PaymentHandlerFunc(func(_ context.Context, pctx PaymentContext) (PaymentResult, error) {
		if got := pctx.Accepts[0]["network"]; got != "eip155:8453" {
			t.Fatalf("expected canonical network, got %v", got)
		}
		return PaymentResult{Headers: map[string]string{"PAYMENT-SIGNATURE": "signed-payment"}}, nil
	})
	c, _ := NewClient(WithBaseURL(srv.URL), WithPaymentHandler(handler))

	if _, err := c.transport.do(
		context.Background(),
		requestOpts{Method: http.MethodGet, Path: "/paid"},
	); err != nil {
		t.Fatal(err)
	}
	if calls != 2 {
		t.Fatalf("expected two calls, got %d", calls)
	}
}

func TestPaymentHandler_ParsesPaymentRequiredHeaderForStream(t *testing.T) {
	var calls int
	required := `{"x402Version":2,"accepts":[{"network":"eip155:8453","scheme":"exact","amount":"1"}]}`
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		calls++
		if calls == 1 {
			w.Header().Set("PAYMENT-REQUIRED", base64.StdEncoding.EncodeToString([]byte(required)))
			w.WriteHeader(http.StatusPaymentRequired)
			return
		}
		if got := r.Header.Get("PAYMENT-SIGNATURE"); got != "signed-payment" {
			t.Fatalf("expected PAYMENT-SIGNATURE, got %q", got)
		}
		w.Header().Set("Content-Type", "text/event-stream")
		_, _ = w.Write([]byte("data: {\"id\":\"chunk-1\"}\n\ndata: [DONE]\n\n"))
	}))
	defer srv.Close()

	handler := PaymentHandlerFunc(func(_ context.Context, pctx PaymentContext) (PaymentResult, error) {
		if got := pctx.Accepts[0]["network"]; got != "eip155:8453" {
			t.Fatalf("expected canonical network, got %v", got)
		}
		return PaymentResult{Headers: map[string]string{"PAYMENT-SIGNATURE": "signed-payment"}}, nil
	})
	c, _ := NewClient(WithBaseURL(srv.URL), WithPaymentHandler(handler))

	chunks, errors := c.OpenAI().Chat().Completions().CreateStream(context.Background(), ChatCompletionRequest{
		Model: "test", Messages: []map[string]any{{"role": "user", "content": "hi"}},
	})
	var received []map[string]any
	for chunk := range chunks {
		received = append(received, chunk)
	}
	for err := range errors {
		if err != nil {
			t.Fatal(err)
		}
	}
	if calls != 2 || len(received) != 1 || received[0]["id"] != "chunk-1" {
		t.Fatalf("unexpected stream result calls=%d chunks=%+v", calls, received)
	}
}

func TestTaskHandle_WaitCompletes(t *testing.T) {
	calls := 0
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		calls++
		b, _ := io.ReadAll(r.Body)
		if !strings.Contains(string(b), `"id":"t123"`) {
			t.Errorf("bad body: %s", b)
		}
		w.Header().Set("Content-Type", "application/json")
		if calls < 3 {
			_, _ = w.Write([]byte(`{"response":{"status":"processing"}}`))
			return
		}
		_, _ = w.Write([]byte(`{"response":{"status":"succeeded","url":"https://cdn.example/f.png"}}`))
	}))
	defer srv.Close()

	c, _ := NewClient(WithAPIToken("t"), WithBaseURL(srv.URL))
	res, err := c.Tasks().Wait(context.Background(), "suno", "t123", 10*time.Millisecond, 2*time.Second)
	if err != nil {
		t.Fatalf("Wait: %v", err)
	}
	resp := res["response"].(map[string]any)
	if resp["status"] != "succeeded" {
		t.Fatalf("bad status: %+v", resp)
	}
	if calls != 3 {
		t.Fatalf("expected 3 polls, got %d", calls)
	}
}

func TestImages_GenerateReturnsTaskHandle(t *testing.T) {
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		if r.URL.Path == "/nano-banana/images" {
			_, _ = w.Write([]byte(`{"task_id":"img-1"}`))
			return
		}
		if r.URL.Path == "/nano-banana/tasks" {
			_, _ = w.Write([]byte(`{"response":{"status":"succeeded","url":"https://cdn/x.png"}}`))
			return
		}
		t.Errorf("unexpected path %s", r.URL.Path)
	}))
	defer srv.Close()

	c, _ := NewClient(WithAPIToken("t"), WithBaseURL(srv.URL))
	handle, _, err := c.Images().Generate(context.Background(), ImageGenerateRequest{
		Prompt:   "a cat",
		Provider: "nano-banana",
	})
	if err != nil {
		t.Fatalf("Generate: %v", err)
	}
	if handle == nil || handle.ID != "img-1" {
		t.Fatalf("expected task handle with id=img-1, got %+v", handle)
	}
	res, err := handle.Wait(context.Background(), 5*time.Millisecond, 1*time.Second)
	if err != nil {
		t.Fatalf("Wait: %v", err)
	}
	resp := res["response"].(map[string]any)
	if resp["url"] != "https://cdn/x.png" {
		t.Fatalf("bad url: %+v", resp)
	}
}

// TestGetRecordsTerminalState covers the parity fix: a caller driving its own
// poll loop only ever calls Get, so Get is where completion must be recorded.
// Without it, URLs stays empty after a task has plainly finished.
func TestGetRecordsTerminalState(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		_, _ = w.Write([]byte(`{"response":{"success":true,"finished_at":"2026-07-27T09:38:41Z",
			"data":[{"image_url":"https://cdn.example.com/a.png"}]}}`))
	}))
	defer server.Close()

	c, err := NewClient(WithAPIToken("t"), WithBaseURL(server.URL))
	if err != nil {
		t.Fatalf("NewClient: %v", err)
	}
	h := newTaskHandle("task-1", "/flux/tasks", c.transport, nil)
	if h.Done() {
		t.Fatal("handle should not start complete")
	}

	if _, err := h.Get(context.Background()); err != nil {
		t.Fatalf("Get: %v", err)
	}
	if !h.Done() {
		t.Error("Get must record a terminal state")
	}
	if urls := h.URLs(); len(urls) != 1 || urls[0] != "https://cdn.example.com/a.png" {
		t.Errorf("URLs after Get = %v, want the artifact", urls)
	}
}

func TestGetLeavesRunningTaskAlone(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		_, _ = w.Write([]byte(`{"response":{"status":"processing"}}`))
	}))
	defer server.Close()

	c, _ := NewClient(WithAPIToken("t"), WithBaseURL(server.URL))
	h := newTaskHandle("task-1", "/flux/tasks", c.transport, nil)
	if _, err := h.Get(context.Background()); err != nil {
		t.Fatalf("Get: %v", err)
	}
	if h.Done() {
		t.Error("a running task must not be marked complete")
	}
}

// TestStructuredErrorIsTerminal covers the hailuo shape: success:false with an
// error object and no finished_at. Reading it as still-running makes a caller
// poll until timeout instead of surfacing the upstream's reason.
func TestStructuredErrorIsTerminal(t *testing.T) {
	state := map[string]any{
		"response": map[string]any{
			"success": false,
			"error":   map[string]any{"code": "api_error", "message": "no channel"},
		},
	}
	if got := taskStatus(state); got != "failed" {
		t.Errorf("taskStatus = %q, want failed", got)
	}
}

func TestTransientErrorKeepsWaiting(t *testing.T) {
	state := map[string]any{
		"response": map[string]any{"success": false, "error": "temporary"},
	}
	if got := taskStatus(state); got != "" {
		t.Errorf("taskStatus = %q, want empty (still running)", got)
	}
}

func TestMinimaxGenerateRequestShape(t *testing.T) {
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/minimax/videos" {
			t.Fatalf("unexpected path: %s", r.URL.Path)
		}
		var body map[string]any
		if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
			t.Fatalf("decode body: %v", err)
		}
		if body["model"] != "MiniMax-H3" || body["resolution"] != "2K" || body["duration"] != float64(5) {
			t.Fatalf("bad body: %+v", body)
		}
		if body["ratio"] != "adaptive" || body["aigc_watermark"] != false {
			t.Fatalf("missing optional fields: %+v", body)
		}
		content, ok := body["content"].([]any)
		if !ok || len(content) != 2 {
			t.Fatalf("bad content: %+v", body["content"])
		}
		w.Header().Set("Content-Type", "application/json")
		_, _ = w.Write([]byte(`{"task_id":"minimax-1"}`))
	}))
	defer srv.Close()

	c, _ := NewClient(WithAPIToken("t"), WithBaseURL(srv.URL))
	watermark := false
	handle, err := c.Minimax().Generate(context.Background(), MinimaxGenerateRequest{
		Model:      MinimaxModelH3,
		Resolution: MinimaxResolution2K,
		Duration:   5,
		Ratio:      MinimaxRatioAdaptive,
		Content: []MinimaxContentItem{
			{Type: MinimaxContentText, Text: "let the subject move naturally"},
			{
				Type:     MinimaxContentImageURL,
				ImageURL: &MinimaxMediaURL{URL: "https://cdn.example.com/frame.png"},
				Role:     MinimaxRoleFirstFrame,
			},
		},
		AIGCWatermark: &watermark,
	})
	if err != nil {
		t.Fatalf("Generate: %v", err)
	}
	if handle == nil || handle.ID != "minimax-1" {
		t.Fatalf("bad handle: %+v", handle)
	}
}
