package acedatacloud

import "testing"

func TestQwenImageDefaultsMatchSpec(t *testing.T) {
	body := (QwenImageGenerateRequest{
		Model:  "qwen-image-3.0",
		Prompt: "a cat",
	}).toBody()

	if body["async"] != false {
		t.Fatalf("expected async default false, got %#v", body["async"])
	}
	if body["prompt_extend"] != true {
		t.Fatalf("expected prompt_extend default true, got %#v", body["prompt_extend"])
	}
	if body["enable_thinking"] != true {
		t.Fatalf("expected enable_thinking default true, got %#v", body["enable_thinking"])
	}
}

func TestQwenImageExplicitBooleansOverrideDefaults(t *testing.T) {
	promptExtend := false
	enableThinking := false
	async := true
	body := (QwenImageGenerateRequest{
		Model:          "qwen-image-3.0",
		Prompt:         "a cat",
		PromptExtend:   &promptExtend,
		EnableThinking: &enableThinking,
		Async:          &async,
	}).toBody()

	if body["prompt_extend"] != false || body["enable_thinking"] != false || body["async"] != true {
		t.Fatalf("explicit booleans not preserved: %#v", body)
	}
}
