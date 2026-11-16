package acedatacloud

import (
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestAceMusicGenerationContract(t *testing.T) {
	calls := 0
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		calls++
		if r.URL.Path != "/acemusic/audios" || r.Header.Get("Idempotency-Key") != "stable" {
			t.Errorf("wrong request: %s %v", r.URL.Path, r.Header)
		}
		var body map[string]any
		if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
			t.Fatal(err)
		}
		if body["model"] != "acemusic-v1.1" || body["async"] != true || body["prompt"] != "folk" {
			t.Errorf("wrong payload: %v", body)
		}
		w.Header().Set("Content-Type", "application/json")
		_, _ = w.Write([]byte(`{"task_id":"original"}`))
	}))
	defer server.Close()
	client, err := NewClient(WithAPIToken("token"), WithBaseURL(server.URL))
	if err != nil {
		t.Fatal(err)
	}
	task, err := client.Acemusic().Generate(context.Background(), AcemusicGenerateRequest{Prompt: "folk", IdempotencyKey: "stable"})
	if err != nil || task == nil || task.ID != "original" || calls != 1 {
		t.Fatalf("unexpected result %v %v %d", task, err, calls)
	}
}

func TestAceMusicPartialFailureIsTerminal(t *testing.T) {
	state := map[string]any{"state": "processing", "response": map[string]any{"data": []any{map[string]any{"state": "succeeded", "audio_url": "https://cdn.acedata.cloud/one.mp3"}}}}
	if taskStatus(state) != "" {
		t.Fatal("individual song completed pending group")
	}
	state["state"] = "partial_failed"
	if taskStatus(state) != "failed" {
		t.Fatal("partial group was not terminal")
	}
}
