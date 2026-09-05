package acedatacloud

import "testing"

func TestSunoLatestDocsContract(t *testing.T) {
	mp3 := (SunoMp3Request{
		AudioID: "audio-1",
	}).toBody()
	if mp3["audio_id"] != "audio-1" || mp3["async"] != true {
		t.Fatalf("unexpected Suno MP3 body: %#v", mp3)
	}

	generate := (SunoGenerateRequest{
		Prompt:                   "a short prompt",
		LyricPrompt:              "write a chorus",
		ReplaceSectionResultMode: "candidates",
	}).toBody()
	if generate["prompt"] != "a short prompt" ||
		generate["lyric_prompt"] != "write a chorus" ||
		generate["replace_section_result_mode"] != "candidates" {
		t.Fatalf("unexpected Suno generate body: %#v", generate)
	}

	upload := (SunoUploadRequest{
		AudioURL: "https://cdn.example.com/ref.mp3",
		Mode:     "enhanced",
		Name:     "Reference",
	}).toBody()
	if upload["mode"] != "enhanced" || upload["name"] != "Reference" {
		t.Fatalf("unexpected Suno upload body: %#v", upload)
	}
}
