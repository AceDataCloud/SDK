package acedatacloud

import (
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestFishGenerateRequestUsesCurrentContract(t *testing.T) {
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.Header.Get("model") != "s2.1-pro" {
			t.Errorf("unexpected model header: %q", r.Header.Get("model"))
		}
		var body map[string]any
		_ = json.NewDecoder(r.Body).Decode(&body)
		if body["format"] != "pcm" || body["mp3_bitrate"] != float64(192) || body["async"] != true {
			t.Errorf("unexpected Fish request body: %#v", body)
		}
		_, _ = w.Write([]byte(`{"task_id":"task-fish"}`))
	}))
	defer srv.Close()
	c, _ := NewClient(WithAPIToken("t"), WithBaseURL(srv.URL))
	if _, err := c.Fish().Generate(context.Background(), FishGenerateRequest{
		Text:       "Hello",
		Format:     "pcm",
		Mp3Bitrate: 192,
		Model:      "s2.1-pro",
	}); err != nil {
		t.Fatalf("Fish Generate: %v", err)
	}
}
