package acedatacloud

import "testing"

func TestKlingRequestsUseDocumentedDefaultsAndFields(t *testing.T) {
	if body := (KlingGenerateRequest{Action: "text2video"}).toBody(); body["model"] != "kling-v1" || body["mode"] != "std" || body["duration"] != 5 {
		t.Fatalf("unexpected generate defaults: %#v", body)
	}
	if body := (KlingMotionRequest{Mode: "pro", ImageURL: "https://example.com/image", VideoURL: "https://example.com/video", CharacterOrientation: "image", ModelName: "kling-v3", WatermarkInfo: map[string]any{"enabled": true}}).toBody(); body["model_name"] != "kling-v3" || body["watermark_info"] == nil {
		t.Fatalf("motion fields not serialized: %#v", body)
	}
	if body := (KlingLipSyncRequest{Mode: "text2video"}).toBody(); body["audio_type"] != "url" || body["voice_language"] != "zh" || body["voice_speed"] != 1.0 || body["async"] != false {
		t.Fatalf("unexpected lip-sync defaults: %#v", body)
	}
	if body := (KlingTalkingPhotoRequest{ImageURL: "https://example.com/image", AudioURL: "https://example.com/audio"}).toBody(); body["model"] != "kling-v2-1-master" || body["duration"] != 5 || body["mode"] != "pro" || body["async"] != false {
		t.Fatalf("unexpected talking-photo defaults: %#v", body)
	}
}
