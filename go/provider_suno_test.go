package acedatacloud

import "testing"

func TestSunoGenerateSerializesDocsSyncedParameters(t *testing.T) {
	body := SunoGenerateRequest{
		Prompt:                   "lofi beat",
		LyricPrompt:              "write a short hook",
		ReplaceSectionResultMode: "candidates",
	}.toBody()

	if body["prompt"] != "lofi beat" {
		t.Fatalf("expected prompt string, got %#v", body["prompt"])
	}
	if body["lyric_prompt"] != "write a short hook" {
		t.Fatalf("expected lyric_prompt string, got %#v", body["lyric_prompt"])
	}
	if body["replace_section_result_mode"] != "candidates" {
		t.Fatalf("expected replace_section_result_mode override, got %#v", body["replace_section_result_mode"])
	}
}

func TestSunoMp3SerializesTaskRequest(t *testing.T) {
	body := SunoMp3Request{AudioID: "audio-1"}.toBody()

	if body["audio_id"] != "audio-1" {
		t.Fatalf("expected audio_id, got %#v", body["audio_id"])
	}
	if body["async"] != true {
		t.Fatalf("expected async=true by default, got %#v", body["async"])
	}
}

func TestSunoUploadSerializesModeAndName(t *testing.T) {
	body := SunoUploadRequest{
		AudioURL: "https://cdn.example.com/in.mp3",
		Mode:     "enhanced",
		Name:     "Reference",
	}.toBody()

	if body["mode"] != "enhanced" {
		t.Fatalf("expected enhanced mode, got %#v", body["mode"])
	}
	if body["name"] != "Reference" {
		t.Fatalf("expected upload name, got %#v", body["name"])
	}
}
