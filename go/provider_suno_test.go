package acedatacloud

import "testing"

func TestSunoRecentDocsFields(t *testing.T) {
	generate := SunoGenerateRequest{
		Prompt:                   "A song for the release",
		LyricPrompt:              "Write upbeat launch lyrics",
		ReplaceSectionResultMode: "candidates",
	}.toBody()
	if generate["prompt"] != "A song for the release" ||
		generate["lyric_prompt"] != "Write upbeat launch lyrics" ||
		generate["replace_section_result_mode"] != "candidates" {
		t.Fatalf("unexpected generate body: %#v", generate)
	}

	mp3 := SunoMp3Request{AudioID: "audio-1"}.toBody()
	if mp3["audio_id"] != "audio-1" || mp3["async"] != true {
		t.Fatalf("unexpected mp3 body: %#v", mp3)
	}

	vox := SunoVoxRequest{AudioID: "audio-1", VocalStart: 0, VocalEnd: 12.5}.toBody()
	if _, ok := vox["vocal_start"]; !ok {
		t.Fatalf("required vocal_start missing: %#v", vox)
	}
	if vox["vocal_end"] != 12.5 {
		t.Fatalf("required vocal_end missing: %#v", vox)
	}

	upload := SunoUploadRequest{
		AudioURL: "https://example.com/audio.mp3",
		Mode:     "enhanced",
		Name:     "demo",
	}.toBody()
	if upload["mode"] != "enhanced" || upload["name"] != "demo" {
		t.Fatalf("unexpected upload body: %#v", upload)
	}
}
