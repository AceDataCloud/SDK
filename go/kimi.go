package acedatacloud

import "context"

type Kimi struct{ t *transport }

type KimiChatRequest struct {
	Model    string
	Messages []map[string]any
	Stream   bool
	Extra    map[string]any
}

func (r KimiChatRequest) toBody() map[string]any {
	body := map[string]any{"model": r.Model, "messages": r.Messages}
	if r.Stream {
		body["stream"] = true
	}
	for key, value := range r.Extra {
		if _, exists := body[key]; !exists {
			body[key] = value
		}
	}
	return body
}

type KimiChat struct{ t *transport }
type KimiChatCompletions struct{ t *transport }

func (k *Kimi) Chat() *KimiChat { return &KimiChat{t: k.t} }
func (k *KimiChat) Completions() *KimiChatCompletions {
	return &KimiChatCompletions{t: k.t}
}

func (k *KimiChatCompletions) Create(ctx context.Context, req KimiChatRequest) (map[string]any, error) {
	body := req.toBody()
	delete(body, "stream")
	return k.t.do(ctx, requestOpts{Method: "POST", Path: "/kimi/chat/completions", Body: body})
}

func (k *KimiChatCompletions) CreateStream(ctx context.Context, req KimiChatRequest) (<-chan map[string]any, <-chan error) {
	req.Stream = true
	return streamDecode(k.t, "/kimi/chat/completions", req.toBody())
}
