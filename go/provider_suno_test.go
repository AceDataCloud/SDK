package acedatacloud

import "testing"

func TestSunoLatestRequestContract(t *testing.T) {
	generateBody := (SunoGenerateRequest{
		Prompt:                   "A song about winter",
		LyricPrompt:              "Write lyrics about snow",
		ReplaceSectionResultMode: "candidates",
	}).toBody()
	if generateBody["prompt"] != "A song about winter" ||
		generateBody["lyric_prompt"] != "Write lyrics about snow" ||
		generateBody["replace_section_result_mode"] != "candidates" {
		t.Fatalf("unexpected Suno generate body: %#v", generateBody)
	}

	voxBody := (SunoVoxRequest{AudioID: "audio-1", VocalStart: 1.5, VocalEnd: 8}).toBody()
	if voxBody["vocal_start"] != 1.5 || voxBody["vocal_end"] != float64(8) {
		t.Fatalf("unexpected Suno vox body: %#v", voxBody)
	}

	uploadBody := (SunoUploadRequest{
		AudioURL: "https://cdn.example.com/song.mp3",
		Mode:     "enhanced",
		Name:     "Reference",
	}).toBody()
	if uploadBody["mode"] != "enhanced" || uploadBody["name"] != "Reference" {
		t.Fatalf("unexpected Suno upload body: %#v", uploadBody)
	}
}
