package acedatacloud

import "context"

// MidjourneyResource groups Midjourney endpoints.
type MidjourneyResource struct{ t *transport }

func (m *MidjourneyResource) submit(ctx context.Context, path string, body map[string]any) (*TaskHandle, error) {
	if body == nil {
		body = map[string]any{}
	}
	if _, ok := body["async"]; !ok {
		body["async"] = true
	}
	result, err := m.t.do(ctx, requestOpts{Method: "POST", Path: path, Body: body})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/midjourney/tasks", m.t, result), nil
}

func (m *MidjourneyResource) Imagine(ctx context.Context, body map[string]any) (*TaskHandle, error) {
	return m.submit(ctx, "/midjourney/imagine", body)
}

func (m *MidjourneyResource) Edits(ctx context.Context, body map[string]any) (*TaskHandle, error) {
	return m.submit(ctx, "/midjourney/edits", body)
}

func (m *MidjourneyResource) Videos(ctx context.Context, body map[string]any) (*TaskHandle, error) {
	return m.submit(ctx, "/midjourney/videos", body)
}

func (m *MidjourneyResource) Seed(ctx context.Context, imageID string, extra map[string]any) (map[string]any, error) {
	body := withExtra(map[string]any{"image_id": imageID}, extra)
	return m.t.do(ctx, requestOpts{Method: "POST", Path: "/midjourney/seed", Body: body})
}

func (m *MidjourneyResource) Describe(ctx context.Context, imageURL string, extra map[string]any) (map[string]any, error) {
	body := withExtra(map[string]any{"image_url": imageURL}, extra)
	return m.t.do(ctx, requestOpts{Method: "POST", Path: "/midjourney/describe", Body: body})
}

func (m *MidjourneyResource) Shorten(ctx context.Context, prompt string, extra map[string]any) (map[string]any, error) {
	body := withExtra(map[string]any{"prompt": prompt}, extra)
	return m.t.do(ctx, requestOpts{Method: "POST", Path: "/midjourney/shorten", Body: body})
}

func (m *MidjourneyResource) Translate(ctx context.Context, content string, extra map[string]any) (map[string]any, error) {
	body := withExtra(map[string]any{"content": content}, extra)
	return m.t.do(ctx, requestOpts{Method: "POST", Path: "/midjourney/translate", Body: body})
}

func (m *MidjourneyResource) Tasks(ctx context.Context, body map[string]any) (map[string]any, error) {
	return m.t.do(ctx, requestOpts{Method: "POST", Path: "/midjourney/tasks", Body: body})
}
