package acedatacloud

import "testing"

func TestSunoUploadSerializesCurrentOptions(t *testing.T) {
	body := (SunoUploadRequest{
		AudioURL:    "https://cdn.example.com/reference.wav",
		Mode:        "enhanced",
		Name:        "Reference",
		CallbackURL: "https://example.com/callback",
	}).toBody()

	expected := map[string]any{
		"audio_url":    "https://cdn.example.com/reference.wav",
		"mode":         "enhanced",
		"name":         "Reference",
		"callback_url": "https://example.com/callback",
	}
	for key, value := range expected {
		if body[key] != value {
			t.Fatalf("expected %s=%q, got %#v", key, value, body[key])
		}
	}
}

func TestSunoUploadUsesSpecDefaultMode(t *testing.T) {
	body := (SunoUploadRequest{AudioURL: "https://cdn.example.com/reference.wav"}).toBody()
	if body["mode"] != "standard" {
		t.Fatalf("expected mode=standard, got %#v", body["mode"])
	}
}
