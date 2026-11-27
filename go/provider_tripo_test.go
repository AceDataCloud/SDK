package acedatacloud

import (
	"reflect"
	"testing"
)

func TestTripoActionOptions(t *testing.T) {
	req := TripoModelsRequest{Action: "import", ModelURL: "https://example.org/a.glb"}
	got := req.toBody()
	if !reflect.DeepEqual(got, map[string]any{"action": "import", "model_url": req.ModelURL, "async": true}) {
		t.Fatalf("import payload: %#v", got)
	}
	flag := false
	req = TripoModelsRequest{Action: "texture", ModelID: "asset", Pbr: &flag}
	if value, ok := req.toBody()["pbr"]; !ok || value != false {
		t.Fatal("lost explicit pbr=false")
	}
	front, back := "https://example.org/front.png", "https://example.org/back.png"
	views := TripoGenerateRequest{ImageURLs: []*string{&front, nil, &back}}
	if !reflect.DeepEqual(views.toBody()["image_urls"], views.ImageURLs) {
		t.Fatal("multiview slots changed")
	}
}
