package acedatacloud

import (
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestMidjourneyProviderSerializesPollableAndNonPollableRequests(t *testing.T) {
	type call struct {
		path string
		body map[string]any
	}
	var calls []call

	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		defer r.Body.Close()
		var body map[string]any
		_ = json.NewDecoder(r.Body).Decode(&body)
		calls = append(calls, call{path: r.URL.Path, body: body})
		w.Header().Set("Content-Type", "application/json")
		_, _ = w.Write([]byte(`{"task_id":"task-1","data":[]}`))
	}))
	defer server.Close()

	client, err := NewClient(WithAPIToken("t"), WithBaseURL(server.URL))
	if err != nil {
		t.Fatalf("NewClient: %v", err)
	}

	async := false
	handle, err := client.Midjourney().Imagine(context.Background(), MidjourneyImagineRequest{
		Prompt: "A cat",
		Async:  &async,
	})
	if err != nil {
		t.Fatalf("Imagine: %v", err)
	}
	describe, err := client.Midjourney().Describe(context.Background(), MidjourneyDescribeRequest{
		ImageURL: "https://example.com/cat.png",
	})
	if err != nil {
		t.Fatalf("Describe: %v", err)
	}

	if handle == nil || handle.ID != "task-1" {
		t.Fatalf("Imagine handle = %+v, want id task-1", handle)
	}
	if got, _ := describe["task_id"].(string); got != "task-1" {
		t.Fatalf("Describe task_id = %q, want task-1", got)
	}
	if len(calls) != 2 {
		t.Fatalf("got %d calls, want 2", len(calls))
	}
	if calls[0].path != "/midjourney/imagine" {
		t.Fatalf("first path = %s, want /midjourney/imagine", calls[0].path)
	}
	if got, _ := calls[0].body["prompt"].(string); got != "A cat" {
		t.Fatalf("imagine prompt = %q, want A cat", got)
	}
	if got, ok := calls[0].body["async"].(bool); !ok || got {
		t.Fatalf("imagine async = %#v, want false", calls[0].body["async"])
	}
	if calls[1].path != "/midjourney/describe" {
		t.Fatalf("second path = %s, want /midjourney/describe", calls[1].path)
	}
	if got, _ := calls[1].body["image_url"].(string); got != "https://example.com/cat.png" {
		t.Fatalf("describe image_url = %q, want expected URL", got)
	}
}
