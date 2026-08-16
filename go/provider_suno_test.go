package acedatacloud

import "testing"

func TestSunoGenerateUsesStringPromptFields(t *testing.T) {
	body := (SunoGenerateRequest{
		Prompt:      "A song for Christmas",
		LyricPrompt: "A lyric idea",
	}).toBody()
	if body["prompt"] != "A song for Christmas" {
		t.Fatalf("prompt should be a string: %#v", body)
	}
	if body["lyric_prompt"] != "A lyric idea" {
		t.Fatalf("lyric_prompt should be a string: %#v", body)
	}
}

func TestSunoVoxAlwaysSendsVocalWindow(t *testing.T) {
	body := (SunoVoxRequest{
		AudioID:    "audio-1",
		VocalStart: 0,
		VocalEnd:   12.5,
	}).toBody()
	if body["vocal_start"] != float64(0) || body["vocal_end"] != 12.5 {
		t.Fatalf("vox request missing vocal window: %#v", body)
	}
}
