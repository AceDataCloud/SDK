package acedatacloud

import (
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestMinimaxGenerateUsesNewEndpointAndDefaults(t *testing.T) {
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/minimax/videos" {
			t.Fatalf("unexpected path %s", r.URL.Path)
		}
		var body map[string]any
		if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
			t.Fatalf("decode body: %v", err)
		}
		if body["model"] != "minimax-h3" {
			t.Fatalf("expected default model minimax-h3, got %v", body["model"])
		}
		if body["prompt"] != "a cat running" {
			t.Fatalf("expected prompt to be forwarded, got %v", body["prompt"])
		}
		w.Header().Set("Content-Type", "application/json")
		_, _ = w.Write([]byte(`{"task_id":"t-1"}`))
	}))
	defer srv.Close()

	c, _ := NewClient(WithAPIToken("t"), WithBaseURL(srv.URL))
	h, err := c.Minimax().Generate(context.Background(), MinimaxGenerateRequest{Prompt: "a cat running"})
	if err != nil {
		t.Fatalf("Generate: %v", err)
	}
	if h == nil || h.ID != "t-1" {
		t.Fatalf("expected task handle with id t-1, got %+v", h)
	}
}
