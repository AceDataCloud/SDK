package acedatacloud

import "testing"

func TestMaestroGenerateRequestDefaults(t *testing.T) {
	body := (MaestroGenerateRequest{Prompt: "a video"}).toBody()

	if body["quality"] != string(MaestroQualityStandard) || body["scenario"] != string(MaestroScenarioAuto) {
		t.Fatalf("unexpected Maestro defaults: %#v", body)
	}
	if body["async"] != true {
		t.Fatalf("expected async submission: %#v", body)
	}
	langs, ok := body["langs"].([]string)
	if !ok || len(langs) != 1 || langs[0] != "zh-cn" {
		t.Fatalf("unexpected language default: %#v", body["langs"])
	}
}

func TestMaestroGenerateRequestRequiresReferenceTask(t *testing.T) {
	err := (MaestroGenerateRequest{Prompt: "a video", Action: MaestroActionEdit}).validate()
	if err == nil {
		t.Fatal("expected edit request without ref_task_id to fail validation")
	}
}
