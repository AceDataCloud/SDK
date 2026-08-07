package acedatacloud

import (
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestMinimaxGenerate_UsesMinimaxEndpointsAndDefaults(t *testing.T) {
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/minimax/videos" {
			t.Fatalf("unexpected path %s", r.URL.Path)
		}
		var body map[string]any
		if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
			t.Fatalf("decode body: %v", err)
		}
		if body["model"] != "minimax-h3" {
			t.Fatalf("model default mismatch: %v", body["model"])
		}
		if body["ratio"] != "16:9" {
			t.Fatalf("ratio default mismatch: %v", body["ratio"])
		}
		if body["duration"] != float64(4) {
			t.Fatalf("duration default mismatch: %v", body["duration"])
		}
		if body["async"] != true {
			t.Fatalf("async default mismatch: %v", body["async"])
		}
		w.Header().Set("Content-Type", "application/json")
		_, _ = w.Write([]byte(`{"task_id":"mm-1"}`))
	}))
	defer srv.Close()

	c, err := NewClient(WithAPIToken("t"), WithBaseURL(srv.URL))
	if err != nil {
		t.Fatalf("NewClient: %v", err)
	}

	handle, err := c.Minimax().Generate(context.Background(), MinimaxGenerateRequest{})
	if err != nil {
		t.Fatalf("Generate: %v", err)
	}
	if handle == nil || handle.ID != "mm-1" {
		t.Fatalf("bad task handle: %+v", handle)
	}
}
