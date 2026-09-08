package acedatacloud

import "testing"

func TestLocalizationTranslateAcceptsMarkdownInput(t *testing.T) {
	body := LocalizationTranslateRequest{
		Input:     "# Title",
		Locale:    "de",
		Extension: "md",
	}.toBody()
	if body["input"] != "# Title" || body["locale"] != "de" || body["extension"] != "md" {
		t.Fatalf("unexpected localization body: %#v", body)
	}
}
