package acedatacloud

import "testing"

func boolPtr(v bool) *bool { return &v }

func TestQwenImageGenerateSerializesSpecDefaults(t *testing.T) {
	body := (QwenImageGenerateRequest{
		Model:  "qwen-image-3.0-pro",
		Prompt: "a cat",
	}).toBody()

	if body["model"] != "qwen-image-3.0-pro" || body["prompt"] != "a cat" {
		t.Fatalf("unexpected qwen-image body: %#v", body)
	}
	if body["n"] != 1 || body["prompt_extend"] != true || body["prompt_extend_mode"] != "direct" || body["enable_thinking"] != true || body["watermark"] != false || body["async"] != true {
		t.Fatalf("qwen-image defaults drifted: %#v", body)
	}
}

func TestQwenImageGenerateCanDisableDefaultTrueBooleans(t *testing.T) {
	body := (QwenImageGenerateRequest{
		Model:          "qwen-image-3.0",
		Prompt:         "a cat",
		PromptExtend:   boolPtr(false),
		EnableThinking: boolPtr(false),
	}).toBody()

	if body["prompt_extend"] != false || body["enable_thinking"] != false {
		t.Fatalf("explicit false booleans were not serialized: %#v", body)
	}
}
