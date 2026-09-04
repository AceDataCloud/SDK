package acedatacloud

import "testing"

func TestSunoMp3RequestDefaultsAsync(t *testing.T) {
	body := (SunoMp3Request{AudioID: "audio-1"}).toBody()
	if body["audio_id"] != "audio-1" {
		t.Fatalf("missing audio_id: %#v", body)
	}
	if body["async"] != true {
		t.Fatalf("mp3 requests must default async=true: %#v", body)
	}
}

func TestSunoUploadRequestDefaultsMode(t *testing.T) {
	body := (SunoUploadRequest{AudioURL: "https://cdn.example.com/a.mp3"}).toBody()
	if body["audio_url"] != "https://cdn.example.com/a.mp3" {
		t.Fatalf("missing audio_url: %#v", body)
	}
	if body["mode"] != "standard" {
		t.Fatalf("upload mode must default to standard: %#v", body)
	}
}
