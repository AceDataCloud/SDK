package acedatacloud

import "testing"

func TestSearchRequestSerializesDefaultsAndFilters(t *testing.T) {
	body, err := (SearchRequest{
		Query:     "SDK examples",
		Country:   "US",
		Language:  "en",
		Range:     SearchRangeQDRWeek,
		ImageSize: SearchImageSize10MP,
	}).toBody()
	if err != nil {
		t.Fatal(err)
	}

	if body["page"] != 1 || body["number"] != 10 || body["type"] != "search" {
		t.Fatalf("SERP defaults drifted: %#v", body)
	}
	if body["range"] != "qdr:w" || body["image_size"] != "10mp" {
		t.Fatalf("SERP filters drifted: %#v", body)
	}
}

func TestSearchRequestRejectsInvalidValues(t *testing.T) {
	tests := []SearchRequest{
		{Query: "   "},
		{Query: "test", Page: -1},
		{Query: "test", Number: 101},
		{Query: "test", Language: "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"},
		{Query: "test", Range: SearchRange("invalid")},
		{Query: "test", ImageSize: SearchImageSize("huge")},
	}

	for _, req := range tests {
		if _, err := req.toBody(); err == nil {
			t.Fatalf("expected validation error for %#v", req)
		}
	}
}
