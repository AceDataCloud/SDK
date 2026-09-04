package acedatacloud

import (
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestGeminiGenerateRequestUsesVideoTaskEndpoint(t *testing.T) {
	body := (GeminiGenerateRequest{Prompt: "A cinematic ocean sunrise"}).toBody()
	if body["prompt"] != "A cinematic ocean sunrise" ||
		body["model"] != "omni-flash" ||
		body["aspect_ratio"] != "16:9" ||
		body["resolution"] != "720p" ||
		body["async"] != true {
		t.Fatalf("unexpected Gemini video body: %#v", body)
	}
}

func TestGeminiGenerateContentUsesModelPathParameter(t *testing.T) {
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/v1beta/models/gemini-2.5-flash:generateContent" {
			t.Fatalf("unexpected path: %s", r.URL.Path)
		}
		var body map[string]any
		_ = json.NewDecoder(r.Body).Decode(&body)
		if _, exists := body["model"]; exists {
			t.Fatalf("path model leaked into request body: %#v", body)
		}
		_, _ = w.Write([]byte(`{"ok":true}`))
	}))
	defer srv.Close()

	c, _ := NewClient(WithAPIToken("t"), WithBaseURL(srv.URL))
	_, err := c.Gemini().ModelGeneratecontent(context.Background(), GeminiModelGeneratecontentRequest{
		Model:    "gemini-2.5-flash",
		Contents: []map[string]any{{"parts": []map[string]any{{"text": "hi"}}}},
	})
	if err != nil {
		t.Fatalf("ModelGeneratecontent: %v", err)
	}
}

func TestGeminiStreamGenerateContentUsesQueryParameter(t *testing.T) {
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/v1beta/models/gemini-2.5-flash:streamGenerateContent" {
			t.Fatalf("unexpected path: %s", r.URL.Path)
		}
		if r.URL.Query().Get("alt") != "sse" {
			t.Fatalf("unexpected query: %s", r.URL.RawQuery)
		}
		var body map[string]any
		_ = json.NewDecoder(r.Body).Decode(&body)
		if _, exists := body["alt"]; exists {
			t.Fatalf("query alt leaked into request body: %#v", body)
		}
		_, _ = w.Write([]byte(`{"ok":true}`))
	}))
	defer srv.Close()

	c, _ := NewClient(WithAPIToken("t"), WithBaseURL(srv.URL))
	_, err := c.Gemini().ModelStreamgeneratecontent(context.Background(), GeminiModelStreamgeneratecontentRequest{
		Model:    "gemini-2.5-flash",
		Contents: []map[string]any{{"parts": []map[string]any{{"text": "hi"}}}},
		Alt:      "sse",
	})
	if err != nil {
		t.Fatalf("ModelStreamgeneratecontent: %v", err)
	}
}
