package acedatacloud

import "context"

// QrartResource groups QRArt endpoints.
type QrartResource struct{ t *transport }

func (q *QrartResource) Generate(ctx context.Context, body map[string]any) (*TaskHandle, error) {
	if body == nil {
		body = map[string]any{}
	}
	if _, ok := body["async"]; !ok {
		body["async"] = true
	}
	result, err := q.t.do(ctx, requestOpts{Method: "POST", Path: "/qrart/generate", Body: body})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/qrart/tasks", q.t, result), nil
}

func (q *QrartResource) Tasks(ctx context.Context, body map[string]any) (map[string]any, error) {
	return q.t.do(ctx, requestOpts{Method: "POST", Path: "/qrart/tasks", Body: body})
}
