package acedatacloud

import "testing"

func TestSeedance25RequestUsesPublicFields(t *testing.T) {
	req := SeedanceGenerateRequest{
		Model:                 "doubao-seedance-2-5-260628",
		Content:               []map[string]any{{"type": "text", "text": "Extend the scene"}},
		Duration:              30,
		Camerafixed:           true,
		OmniReferenceTaskType: "extend",
		OutputFormat:          "mov",
		Tools:                 []map[string]any{{"type": "web_search"}},
	}
	body := req.toBody()
	if body["model"] != req.Model || body["omni_reference_task_type"] != "extend" || body["output_format"] != "mov" {
		t.Fatalf("unexpected Seedance 2.5 body: %#v", body)
	}
	if body["camerafixed"] != true || body["camera_fixed"] != nil {
		t.Fatalf("camera field drift: %#v", body)
	}
}

func TestSeedance20OmitsSeedance25Defaults(t *testing.T) {
	body := (SeedanceGenerateRequest{
		Model:   "doubao-seedance-2-0-260128",
		Content: []map[string]any{{"type": "text", "text": "A scene"}},
	}).toBody()
	if _, exists := body["output_format"]; exists {
		t.Fatalf("2.0 request unexpectedly contains output_format: %#v", body)
	}
}
