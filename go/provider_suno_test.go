package acedatacloud

import "testing"

func TestSunoGenerateRequestUsesSyncedFields(t *testing.T) {
	body := (SunoGenerateRequest{
		Prompt:                   "lofi beat",
		LyricPrompt:              "winter lyrics",
		ReplaceSectionResultMode: "candidates",
	}).toBody()

	if body["prompt"] != "lofi beat" || body["lyric_prompt"] != "winter lyrics" {
		t.Fatalf("string prompt fields were not serialized: %#v", body)
	}
	if body["replace_section_result_mode"] != "candidates" {
		t.Fatalf("replace_section_result_mode was not serialized: %#v", body)
	}
}

func TestSunoMp3RequestUsesAsyncTaskBody(t *testing.T) {
	body := (SunoMp3Request{AudioID: "audio-1"}).toBody()

	if body["audio_id"] != "audio-1" || body["async"] != true {
		t.Fatalf("unexpected MP3 body: %#v", body)
	}
}
