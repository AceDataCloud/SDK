package acedatacloud

import (
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestGeminiVideoUsesDefaults(t *testing.T) {
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/gemini/videos" {
			t.Fatalf("unexpected path %s", r.URL.Path)
		}
		var body map[string]any
		_ = json.NewDecoder(r.Body).Decode(&body)
		if body["model"] != "omni-flash" || body["aspect_ratio"] != "16:9" || body["resolution"] != "720p" || body["async"] != true {
			t.Fatalf("unexpected body: %+v", body)
		}
		_, _ = w.Write([]byte(`{"task_id":"gemini-task"}`))
	}))
	defer srv.Close()

	c, _ := NewClient(WithAPIToken("t"), WithBaseURL(srv.URL))
	task, err := c.Gemini().GenerateVideo(context.Background(), GeminiVideoRequest{Prompt: "A cat"})
	if err != nil || task.ID != "gemini-task" {
		t.Fatalf("GenerateVideo = %#v, %v", task, err)
	}
}
