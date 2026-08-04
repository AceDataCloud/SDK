package acedatacloud

import (
	"context"
	"encoding/json"
	"io"
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestGemini_VideosGenerateAppliesSpecDefaults(t *testing.T) {
	var gotPath string
	var gotBody map[string]any
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		gotPath = r.URL.Path
		raw, _ := io.ReadAll(r.Body)
		_ = json.Unmarshal(raw, &gotBody)
		w.Header().Set("Content-Type", "application/json")
		_, _ = w.Write([]byte(`{"task_id":"task-gemini"}`))
	}))
	defer srv.Close()

	c, _ := NewClient(WithAPIToken("t"), WithBaseURL(srv.URL))
	handle, err := c.Gemini().Videos().Generate(context.Background(), GeminiVideoRequest{
		Prompt: "a kitten in a garden",
	})
	if err != nil {
		t.Fatalf("Generate: %v", err)
	}
	if gotPath != "/gemini/videos" {
		t.Fatalf("bad path: %s", gotPath)
	}
	if gotBody["model"] != "omni-flash" || gotBody["aspect_ratio"] != "16:9" || gotBody["resolution"] != "720p" {
		t.Fatalf("missing spec defaults: %+v", gotBody)
	}
	if gotBody["async"] != true {
		t.Fatalf("expected async default true: %+v", gotBody)
	}
	if handle == nil || handle.ID != "task-gemini" {
		t.Fatalf("expected handle with id=task-gemini, got %+v", handle)
	}
}

func TestGemini_VideosGenerateRejectsMultipleReferenceVideos(t *testing.T) {
	c, _ := NewClient(WithAPIToken("t"))
	_, err := c.Gemini().Videos().Generate(context.Background(), GeminiVideoRequest{
		Prompt:    "x",
		VideoURLs: []string{"https://example.com/a.mp4", "https://example.com/b.mp4"},
	})
	if err == nil {
		t.Fatal("expected an error for more than one reference video")
	}
}

func TestGemini_NativeGenerateContentPutsModelInPath(t *testing.T) {
	var gotPath string
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		gotPath = r.URL.Path
		w.Header().Set("Content-Type", "application/json")
		_, _ = w.Write([]byte(`{"candidates":[]}`))
	}))
	defer srv.Close()

	c, _ := NewClient(WithAPIToken("t"), WithBaseURL(srv.URL))
	_, err := c.Gemini().GenerateContent(context.Background(), GeminiGenerateContentRequest{
		Model:    "gemini-2.5-flash",
		Contents: []map[string]any{{"role": "user", "parts": []map[string]any{{"text": "hi"}}}},
	})
	if err != nil {
		t.Fatalf("GenerateContent: %v", err)
	}
	if gotPath != "/v1beta/models/gemini-2.5-flash:generateContent" {
		t.Fatalf("bad path: %s", gotPath)
	}
}

func TestGemini_ChatCompletionsPath(t *testing.T) {
	var gotPath string
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		gotPath = r.URL.Path
		w.Header().Set("Content-Type", "application/json")
		_, _ = w.Write([]byte(`{"id":"chat-1"}`))
	}))
	defer srv.Close()

	c, _ := NewClient(WithAPIToken("t"), WithBaseURL(srv.URL))
	_, err := c.Gemini().Chat().Completions().Create(context.Background(), GeminiChatRequest{
		Model:    "gemini-3.0-pro",
		Messages: []map[string]any{{"role": "user", "content": "hi"}},
	})
	if err != nil {
		t.Fatalf("Create: %v", err)
	}
	if gotPath != "/gemini/chat/completions" {
		t.Fatalf("bad path: %s", gotPath)
	}
}

func TestGemini_TasksEndpointRegistered(t *testing.T) {
	if serviceTaskEndpoints["gemini"] != "/gemini/tasks" {
		t.Fatalf("gemini tasks endpoint missing: %v", serviceTaskEndpoints["gemini"])
	}
}
