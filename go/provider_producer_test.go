package acedatacloud

import "testing"

func TestProducerLyricsPromptIsString(t *testing.T) {
	body := (ProducerLyricsRequest{Prompt: "Write a summer chorus"}).toBody()

	if body["prompt"] != "Write a summer chorus" {
		t.Fatalf("unexpected Producer lyrics body: %#v", body)
	}
}
