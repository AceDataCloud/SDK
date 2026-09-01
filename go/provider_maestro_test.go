package acedatacloud

import "testing"

func TestMaestroGenerateRequestUsesCurrentContract(t *testing.T) {
	body := (MaestroGenerateRequest{
		Prompt:   "Launch video",
		Duration: 300,
		Scenario: "drama",
	}).toBody()

	if _, exists := body["quality"]; exists {
		t.Fatalf("obsolete quality field present: %#v", body)
	}
	if body["duration"] != 300 || body["scenario"] != "drama" {
		t.Fatalf("unexpected Maestro request body: %#v", body)
	}
}
