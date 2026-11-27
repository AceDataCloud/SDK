package acedatacloud

import "context"

// FaceResource groups face transformation endpoints (“/face/*“).
type FaceResource struct{ t *transport }

func (f *FaceResource) call(ctx context.Context, action string, body map[string]any) (map[string]any, error) {
	return f.t.do(ctx, requestOpts{Method: "POST", Path: "/face/" + action, Body: body})
}

// Analyze detects face keypoints for the image at imageURL. Extra is
// merged into the request body for forward-compatible fields.
func (f *FaceResource) Analyze(ctx context.Context, imageURL string, extra map[string]any) (map[string]any, error) {
	return f.call(ctx, "analyze", withImage(imageURL, extra))
}

// Beautify beautifies a portrait.
func (f *FaceResource) Beautify(ctx context.Context, imageURL string, extra map[string]any) (map[string]any, error) {
	return f.call(ctx, "beautify", withImage(imageURL, extra))
}

// ChangeAge ages or de-ages a face.
func (f *FaceResource) ChangeAge(ctx context.Context, imageURL string, extra map[string]any) (map[string]any, error) {
	return f.call(ctx, "change-age", withImage(imageURL, extra))
}

// ChangeGender swaps the perceived gender of a face.
func (f *FaceResource) ChangeGender(ctx context.Context, imageURL string, extra map[string]any) (map[string]any, error) {
	return f.call(ctx, "change-gender", withImage(imageURL, extra))
}

// DetectLive runs liveness detection.
func (f *FaceResource) DetectLive(ctx context.Context, imageURL string, extra map[string]any) (map[string]any, error) {
	return f.call(ctx, "detect-live", withImage(imageURL, extra))
}

// Swap replaces the face in target with the face from source.
func (f *FaceResource) Swap(ctx context.Context, sourceImageURL, targetImageURL string, extra map[string]any) (map[string]any, error) {
	body := map[string]any{"source_image_url": sourceImageURL, "target_image_url": targetImageURL}
	for k, v := range extra {
		if _, ok := body[k]; !ok {
			body[k] = v
		}
	}
	return f.call(ctx, "swap", body)
}

// Cartoon creates a cartoon avatar from a portrait.
func (f *FaceResource) Cartoon(ctx context.Context, imageURL string, extra map[string]any) (map[string]any, error) {
	return f.call(ctx, "cartoon", withImage(imageURL, extra))
}

func withImage(imageURL string, extra map[string]any) map[string]any {
	body := map[string]any{"image_url": imageURL}
	for k, v := range extra {
		if _, ok := body[k]; !ok {
			body[k] = v
		}
	}
	return body
}
