package acedatacloud

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestUnifiedProtocols(t *testing.T) {
	cases := []struct{ protocol, path, model string }{
		{"completions", "/v1/chat/completions", "gemini-4-argon"},
		{"completions", "/v1/chat/completions", "gpt-4o-image"},
		{"responses", "/v1/responses", "gpt-5-pro"},
		{"messages", "/v1/messages", "claude-sonnet-5-5"},
		{"messages", "/v1/messages", "claude-opus-5-5"},
	}
	for _, tc := range cases {
		for _, streaming := range []bool{false, true} {
			t.Run(fmt.Sprintf("%s/%s/stream=%v", tc.protocol, tc.model, streaming), func(t *testing.T) {
				calls := 0
				server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
					calls++
					if r.URL.Path != tc.path || r.Method != http.MethodPost {
						t.Errorf("unexpected route: %s %s", r.Method, r.URL.Path)
					}
					if r.Header.Get("Authorization") != "Bearer test-token" || r.Header.Get("x-api-key") != "" {
						t.Error("expected Bearer authentication only")
					}
					var body map[string]any
					if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
						t.Error(err)
					}
					if body["model"] != tc.model {
						t.Errorf("model changed: %#v", body)
					}
					if streaming && body["stream"] != true {
						t.Errorf("stream flag missing: %#v", body)
					}
					if !streaming {
						if _, exists := body["stream"]; exists {
							t.Error("non-streaming request has stream flag")
						}
					}
					if tc.protocol == "responses" {
						if body["input"] != "Fixture" {
							t.Error("input changed")
						}
					} else {
						if body["max_tokens"] != float64(12) || body["messages"] == nil {
							t.Error("message parameters changed")
						}
					}
					if streaming {
						w.Header().Set("Content-Type", "text/event-stream")
						fmt.Fprintf(w, "data: {\"model\":%q,\"type\":\"fixture\"}\n\n", tc.model)
					} else {
						w.Header().Set("Content-Type", "application/json")
						fmt.Fprintf(w, "{\"model\":%q,\"type\":\"fixture\"}", tc.model)
					}
				}))
				defer server.Close()
				client, err := NewClient(WithAPIToken("test-token"), WithBaseURL(server.URL), WithMaxRetries(0))
				if err != nil {
					t.Fatal(err)
				}
				ctx := context.Background()
				messages := []map[string]any{{"role": "user", "content": "Fixture"}}
				var result map[string]any
				var events <-chan map[string]any
				var errors <-chan error
				switch tc.protocol {
				case "completions":
					req := ChatCompletionRequest{Model: tc.model, Messages: messages, MaxTokens: 12}
					if streaming {
						events, errors = client.Chat().Completions().CreateStream(ctx, req)
					} else {
						result, err = client.Chat().Completions().Create(ctx, req)
					}
				case "responses":
					req := ResponsesRequest{Model: tc.model, Input: "Fixture"}
					if streaming {
						events, errors = client.Responses().CreateStream(ctx, req)
					} else {
						result, err = client.Responses().Create(ctx, req)
					}
				case "messages":
					req := MessagesRequest{Model: tc.model, Messages: messages, MaxTokens: 12}
					if streaming {
						events, errors = client.Chat().Messages().CreateStream(ctx, req)
					} else {
						result, err = client.Chat().Messages().Create(ctx, req)
					}
				}
				if err != nil {
					t.Fatal(err)
				}
				if streaming {
					count := 0
					for event := range events {
						result = event
						count++
					}
					for err := range errors {
						if err != nil {
							t.Fatal(err)
						}
					}
					if count != 1 {
						t.Errorf("expected one event, got %d", count)
					}
				}
				if result["model"] != tc.model || calls != 1 {
					t.Errorf("unexpected result/call count: %#v / %d", result, calls)
				}
			})
		}
	}
}
