package acedatacloud

import "testing"

func TestWan30RequestUsesNewPublicFields(t *testing.T) {
	body := (WanGenerateRequest{
		Model:     "wan3.0-video",
		Media:     []map[string]any{{"type": "image", "url": "https://cdn.example.com/frame.png"}},
		Ratio:     "9:16",
		Seed:      42,
		Watermark: true,
	}).toBody()

	if body["model"] != "wan3.0-video" || body["action"] != "text2video" {
		t.Fatalf("Wan 3.0 model/default action drifted: %#v", body)
	}
	if body["ratio"] != "9:16" || body["seed"] != 42 || body["watermark"] != true {
		t.Fatalf("Wan 3.0 options drifted: %#v", body)
	}
	if _, exists := body["prompt"]; exists {
		t.Fatalf("Wan prompt should be optional: %#v", body)
	}
}
