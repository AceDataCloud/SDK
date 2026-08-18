package acedatacloud

import "testing"

func TestMidjourneyImagineRequestUsesDocumentedDefaults(t *testing.T) {
	body := (MidjourneyImagineRequest{
		Prompt:  "a cat",
		Version: "8.2",
	}).toBody()
	if body["mode"] != "fast" || body["action"] != "generate" || body["timeout"] != 480 {
		t.Fatalf("unexpected Midjourney defaults: %#v", body)
	}
	if body["version"] != "8.2" || body["async"] != true {
		t.Fatalf("unexpected Midjourney request: %#v", body)
	}
}
