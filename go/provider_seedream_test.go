package acedatacloud

import "testing"

func TestSeedreamGenerateRequestSerializesCurrentSchema(t *testing.T) {
	body := (SeedreamGenerateRequest{
		Model:                            "doubao-seedream-5-0-pro-260628",
		Prompt:                           "a cat",
		Image:                            []string{"https://example.com/reference.png"},
		SequentialImageGeneration:        "auto",
		SequentialImageGenerationOptions: map[string]any{"max_images": 2},
		ResponseFormat:                   "b64_json",
		Tools:                            []any{map[string]any{"type": "web_search"}},
	}).toBody()

	if body["sequential_image_generation"] != "auto" {
		t.Fatalf("unexpected sequential_image_generation: %v", body["sequential_image_generation"])
	}
	if body["response_format"] != "b64_json" {
		t.Fatalf("unexpected response_format: %v", body["response_format"])
	}
	if _, ok := body["seed"]; ok {
		t.Fatal("deprecated seed must not be serialized")
	}
	if _, ok := body["guidance_scale"]; ok {
		t.Fatal("deprecated guidance_scale must not be serialized")
	}
}
