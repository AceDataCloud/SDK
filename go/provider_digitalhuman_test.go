package acedatacloud

import (
	"context"
	"testing"
)

func TestDigitalhumanGenerateRequest_ToBodyAllowsImageURLWithoutVideoURL(t *testing.T) {
	body := (DigitalhumanGenerateRequest{
		ImageURL: "https://cdn.example.com/avatar.jpg",
	}).toBody()

	if got := body["image_url"]; got != "https://cdn.example.com/avatar.jpg" {
		t.Fatalf("expected image_url to be serialized, got %#v", got)
	}
	if _, ok := body["video_url"]; ok {
		t.Fatalf("video_url must be omitted when only image_url is provided: %#v", body)
	}
}

func TestDigitalhumanGenerate_RequiresVideoOrImageURL(t *testing.T) {
	client := &Digitalhuman{}

	_, err := client.Generate(context.Background(), DigitalhumanGenerateRequest{})
	if err == nil {
		t.Fatal("expected validation error")
	}
	if got := err.Error(); got != "video_url or image_url is required" {
		t.Fatalf("unexpected error: %v", err)
	}
}
