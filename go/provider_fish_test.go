package acedatacloud

import "testing"

func TestFishOmitsUnsetNormalize(t *testing.T) {
	body := FishGenerateRequest{Text: "Hello"}.toBody()
	if _, ok := body["normalize"]; ok {
		t.Fatalf("zero-value request leaked normalize=false: %#v", body)
	}
}

func TestFishSerializesExplicitNormalize(t *testing.T) {
	body := FishGenerateRequest{Text: "Hello", Normalize: boolPtr(false)}.toBody()
	if body["normalize"] != false {
		t.Fatalf("expected explicit normalize=false, got %#v", body)
	}
}
