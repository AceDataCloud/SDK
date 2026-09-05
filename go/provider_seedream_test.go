package acedatacloud

import "testing"

func boolPtr(value bool) *bool { return &value }

func TestSeedreamLayerDecompositionSerializesExplicitTrue(t *testing.T) {
	body := SeedreamGenerateRequest{
		Model:              "doubao-seedream-5-0-pro-260628",
		Image:              "https://cdn.example.com/poster.png",
		Size:               "1.5K",
		LayerDecomposition: boolPtr(true),
	}.toBody()
	if body["layer_decomposition"] != true {
		t.Fatalf("expected explicit layer_decomposition=true, got %#v", body)
	}
	if _, ok := body["prompt"]; ok {
		t.Fatalf("prompt must be omitted for automatic decomposition: %#v", body)
	}
}

func TestSeedreamLiteOmitsProOnlyOptionalBooleans(t *testing.T) {
	body := SeedreamGenerateRequest{Model: "doubao-seedream-5-0-260128", Prompt: "a cat"}.toBody()
	if _, ok := body["layer_decomposition"]; ok {
		t.Fatalf("zero-value request leaked Pro-only layer_decomposition: %#v", body)
	}
	if _, ok := body["stream"]; ok {
		t.Fatalf("zero-value request leaked stream=false: %#v", body)
	}
	if _, ok := body["watermark"]; ok {
		t.Fatalf("zero-value request leaked watermark=false: %#v", body)
	}
}

func TestSeedreamSerializesExplicitWatermark(t *testing.T) {
	body := SeedreamGenerateRequest{
		Model:     "doubao-seedream-5-0-260128",
		Watermark: boolPtr(false),
	}.toBody()
	if body["watermark"] != false {
		t.Fatalf("expected explicit watermark=false, got %#v", body)
	}
}
