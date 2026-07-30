package acedatacloud

import (
	"reflect"
	"testing"
)

func TestFishGenerateRequestMatchesCurrentSpec(t *testing.T) {
	if _, ok := reflect.TypeOf(FishGenerateRequest{}).FieldByName("OpusBitrate"); ok {
		t.Fatal("FishGenerateRequest should not expose the removed OpusBitrate field")
	}

	body := FishGenerateRequest{
		Text:   "hello",
		Format: "pcm",
		Extra: map[string]any{
			"opus_bitrate": 64,
			"opusBitrate":  64,
		},
	}.toBody()

	if _, ok := body["opus_bitrate"]; ok {
		t.Fatal("fish request body should not include removed opus_bitrate")
	}
	if _, ok := body["opusBitrate"]; ok {
		t.Fatal("fish request body should not include removed opusBitrate")
	}
	if got := body["format"]; got != "pcm" {
		t.Fatalf("format = %v, want pcm", got)
	}
}
