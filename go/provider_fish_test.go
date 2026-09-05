package acedatacloud

import "testing"

func TestFishModelQueryDefaultsAndExplicitFalse(t *testing.T) {
	body := FishModelRequest{
		PageSize: 20,
		Self:     boolPtr(false),
		Tag:      "demo",
	}.toQuery()

	if got := body.Get("page_size"); got != "20" {
		t.Fatalf("expected page_size=20, got %q", got)
	}
	if got := body.Get("page_number"); got != "1" {
		t.Fatalf("expected default page_number=1, got %q", got)
	}
	if got := body.Get("self"); got != "false" {
		t.Fatalf("expected explicit self=false, got %q", got)
	}
	if got := body.Get("tag"); got != "demo" {
		t.Fatalf("expected tag=demo, got %q", got)
	}
}
