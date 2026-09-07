package acedatacloud

import "testing"

func TestSunoGenerationAndUploadUseCurrentContract(t *testing.T) {
	generation := (SunoGenerateRequest{Prompt: "a song", LyricPrompt: "write lyrics"}).toBody()
	if generation["replace_section_result_mode"] != "full_song" {
		t.Fatalf("missing documented default: %#v", generation)
	}

	upload := (SunoUploadRequest{AudioURL: "https://example.com/audio.mp3", Name: "reference"}).toBody()
	if upload["mode"] != "standard" || upload["name"] != "reference" {
		t.Fatalf("unexpected upload body: %#v", upload)
	}
}

func TestSunoMp3RequestIsAsync(t *testing.T) {
	body := (SunoMp3Request{AudioID: "audio-1"}).toBody()
	if body["audio_id"] != "audio-1" || body["async"] != true {
		t.Fatalf("unexpected MP3 body: %#v", body)
	}
}
