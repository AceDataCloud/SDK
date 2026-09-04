package acedatacloud

import (
	"context"
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestGeminiGenerateContentUsesModelPathParameter(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/v1beta/models/gemini-3.1-flash-lite:generateContent" {
			t.Errorf("unexpected path: %s", r.URL.Path)
		}
		_, _ = w.Write([]byte(`{"success":true}`))
	}))
	defer server.Close()

	client, _ := NewClient(WithAPIToken("t"), WithBaseURL(server.URL))
	_, err := client.Gemini().ModelGeneratecontent(context.Background(), GeminiModelGeneratecontentRequest{
		Model:    "gemini-3.1-flash-lite",
		Contents: []map[string]any{{"role": "user", "parts": []map[string]any{{"text": "Hello"}}}},
	})
	if err != nil {
		t.Fatalf("Gemini request failed: %v", err)
	}
}
