package acedatacloud

import "testing"

func TestWanGenerateSerializesNewVideoFields(t *testing.T) {
	body := (WanGenerateRequest{
		Model:     "wan3.0-video",
		Media:     []map[string]any{{"type": "image", "url": "https://cdn.example.com/frame.png"}},
		Ratio:     "16:9",
		Seed:      42,
		Watermark: true,
	}).toBody()

	if body["model"] != "wan3.0-video" || body["action"] != "text2video" || body["ratio"] != "16:9" || body["seed"] != 42 || body["watermark"] != true || body["async"] != true {
		t.Fatalf("wan body drifted: %#v", body)
	}
	if _, exists := body["prompt"]; exists {
		t.Fatalf("prompt is no longer required and should be omitted when empty: %#v", body)
	}
	media, ok := body["media"].([]map[string]any)
	if !ok || len(media) != 1 || media[0]["url"] != "https://cdn.example.com/frame.png" {
		t.Fatalf("media field missing: %#v", body)
	}
}
