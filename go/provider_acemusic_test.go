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
		if body["async"] != true || body["prompt"] != "folk" {
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

func TestAceMusicTaskFilterSerialization(t *testing.T) {
	body := (AcemusicTasksRequest{Action: "list", Type: "audios", Limit: 10, Offset: 20, CreatedAtMin: 100, CreatedAtMax: 200}).toBody()
	for _, key := range []string{"page", "page_size"} {
		if _, ok := body[key]; ok {
			t.Fatalf("unexpected default %s: %v", key, body)
		}
	}
	if body["limit"] != 10 || body["offset"] != 20 || body["type"] != "audios" || body["created_at_min"] != float64(100) {
		t.Fatalf("wrong filters %v", body)
	}
	paged := (AcemusicTasksRequest{Action: "list", Page: 2, PageSize: 5}).toBody()
	if paged["page"] != 2 || paged["page_size"] != 5 {
		t.Fatalf("wrong page %v", paged)
	}
}

func TestAceMusicReferenceActionSerialization(t *testing.T) {
	cases := []AcemusicGenerateRequest{
		{Action: "upload", AudioURL: "https://example.com/reference.mp3"},
		{Action: "cover", AudioID: "track-a", Lyric: "Verse", Style: "Folk"},
		{Action: "mashup", MashupAudioIDs: []string{"a", "b"}, Lyric: "Verse", Style: "Folk", AudioInfluence: 80},
	}
	for _, request := range cases {
		body := request.toBody()
		for _, name := range []string{"model", "custom"} {
			if _, exists := body[name]; exists {
				t.Fatalf("%s injected %s: %v", request.Action, name, body)
			}
		}
		if body["action"] != request.Action || body["async"] != true {
			t.Fatalf("wrong body %v", body)
		}
		if request.Action == "upload" && body["audio_url"] != request.AudioURL {
			t.Fatal(body)
		}
		if request.Action == "cover" && body["audio_id"] != request.AudioID {
			t.Fatal(body)
		}
		if request.Action == "mashup" && len(body["mashup_audio_ids"].([]string)) != 2 {
			t.Fatal(body)
		}
	}
}
