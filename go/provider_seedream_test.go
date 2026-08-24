package acedatacloud

import (
	"reflect"
	"testing"
)

func TestSeedreamRetiredParametersAreRemoved(t *testing.T) {
	requestType := reflect.TypeOf(SeedreamGenerateRequest{})

	if _, exists := requestType.FieldByName("Seed"); exists {
		t.Fatal("Seedream request still exposes retired Seed field")
	}
	if _, exists := requestType.FieldByName("GuidanceScale"); exists {
		t.Fatal("Seedream request still exposes retired GuidanceScale field")
	}
}
