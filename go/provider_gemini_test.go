package acedatacloud

import "testing"

func TestGeminiGenerateRequestDefaults(t *testing.T) {
	body := (GeminiGenerateRequest{
		Prompt: "A cat running on the beach",
	}).toBody()

	if body["prompt"] != "A cat running on the beach" {
		t.Fatalf("prompt mismatch: %#v", body)
	}
	if body["model"] != "omni-flash" || body["aspect_ratio"] != "16:9" || body["resolution"] != "720p" {
		t.Fatalf("default fields drifted: %#v", body)
	}
	if body["async"] != true {
		t.Fatalf("async should default to true: %#v", body)
	}
}
