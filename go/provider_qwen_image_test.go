package acedatacloud

import "testing"

func TestQwenImageRequestUsesCurrentContract(t *testing.T) {
	body := (QwenImageGenerateRequest{
		Model:            "qwen-image-3.0-pro",
		Prompt:           "A watercolor city",
		ImageURLs:        []string{"https://cdn.example.com/reference.png"},
		N:                2,
		Size:             "1536x1024",
		PromptExtend:     true,
		PromptExtendMode: "agent",
		EnableThinking:   true,
		NegativePrompt:   "text",
		Seed:             42,
		Watermark:        true,
	}).toBody()

	if body["model"] != "qwen-image-3.0-pro" || body["prompt"] != "A watercolor city" {
		t.Fatalf("required Qwen Image fields drifted: %#v", body)
	}
	if body["prompt_extend_mode"] != "agent" || body["seed"] != 42 || body["watermark"] != true {
		t.Fatalf("optional Qwen Image fields drifted: %#v", body)
	}
	if body["async"] != true {
		t.Fatalf("Qwen Image requests must default to async: %#v", body)
	}
}

func TestQwenImageRequestAppliesScalarDefaults(t *testing.T) {
	body := (QwenImageGenerateRequest{
		Model:  "qwen-image-3.0",
		Prompt: "A lighthouse",
	}).toBody()

	if body["n"] != 1 || body["prompt_extend_mode"] != "direct" || body["watermark"] != false {
		t.Fatalf("unexpected Qwen Image defaults: %#v", body)
	}
}
