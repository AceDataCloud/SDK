package acedatacloud

import "testing"

func TestMidjourneyVideoRequestUsesDocumentedFields(t *testing.T) {
	body := (MidjourneyGenerateRequest{
		Action:    "generate",
		Mode:      "fast",
		Resolution: "720p",
		Prompt:    "a cat",
		ImageURL:  "https://example.com/cat.png",
	}).toBody()

	if body["action"] != "generate" || body["resolution"] != "720p" {
		t.Fatalf("unexpected Midjourney request: %#v", body)
	}
	if body["image_url"] != "https://example.com/cat.png" || body["async"] != true {
		t.Fatalf("Midjourney request drift: %#v", body)
	}
}
