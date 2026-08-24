// Code generated from the platform OpenAPI spec. DO NOT EDIT.
// Regenerate with: python scripts/generate_providers.py

package acedatacloud

import "context"

// Qrart is the qrart provider client.
type Qrart struct {
	t *transport
}

// QrartGenerateRequest is the input to qrart.Generate.
type QrartGenerateRequest struct {
	// Qrart Generate Type
	Type string
	// Qrart Generate Prompt
	Prompt string
	// Qrart Generate Ecl
	Ecl string
	// Qrart Generate Qrw
	Qrw float64
	// Qrart Generate Seed
	Seed float64
	// Qrart Generate Steps
	Steps float64
	// Qrart Generate Preset
	Preset string
	// Qrart Generate Rawurl
	Rawurl bool
	// Qrart Generate Rotate
	Rotate float64
	// Qrart Generate 2
	Content string
	// Qrart Generate Pattern
	Pattern string
	// Qrart Generate Position
	Position string
	// Qrart Generate Sub Marker
	SubMarker string
	// Qrart Generate Pixel Style
	PixelStyle string
	// Qrart Generate Aspect Ratio
	AspectRatio string
	// Qrart Generate Marker Shape
	MarkerShape string
	// Qrart Generate Padding Level
	PaddingLevel float64
	// Qrart Generate Padding Noise
	PaddingNoise float64
	// Qrart Generate Content Image Url
	ContentImageURL string
	// Async submits without blocking; poll the returned handle. Defaults true.
	Async *bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r QrartGenerateRequest) toBody() map[string]any {
	body := map[string]any{}
	body["type"] = r.Type
	body["prompt"] = r.Prompt
	if r.Ecl != "" {
		body["ecl"] = r.Ecl
	}
	if r.Qrw != 0 {
		body["qrw"] = r.Qrw
	}
	if r.Seed != 0 {
		body["seed"] = r.Seed
	}
	if r.Steps != 0 {
		body["steps"] = r.Steps
	}
	if r.Preset != "" {
		body["preset"] = r.Preset
	}
	body["rawurl"] = r.Rawurl
	if r.Rotate != 0 {
		body["rotate"] = r.Rotate
	}
	if r.Content != "" {
		body["content"] = r.Content
	}
	if r.Pattern != "" {
		body["pattern"] = r.Pattern
	}
	if r.Position != "" {
		body["position"] = r.Position
	}
	if r.SubMarker != "" {
		body["sub_marker"] = r.SubMarker
	}
	if r.PixelStyle != "" {
		body["pixel_style"] = r.PixelStyle
	}
	if r.AspectRatio != "" {
		body["aspect_ratio"] = r.AspectRatio
	}
	if r.MarkerShape != "" {
		body["marker_shape"] = r.MarkerShape
	}
	if r.PaddingLevel != 0 {
		body["padding_level"] = r.PaddingLevel
	}
	if r.PaddingNoise != 0 {
		body["padding_noise"] = r.PaddingNoise
	}
	if r.ContentImageURL != "" {
		body["content_image_url"] = r.ContentImageURL
	}
	body["async"] = true
	if r.Async != nil {
		body["async"] = *r.Async
	}
	if r.CallbackURL != "" {
		body["callback_url"] = r.CallbackURL
	}
	for k, v := range r.Extra {
		if _, exists := body[k]; !exists {
			body[k] = v
		}
	}
	return body
}

// Generate Generate an QR code
func (c *Qrart) Generate(ctx context.Context, req QrartGenerateRequest) (*TaskHandle, error) {
	result, err := c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/qrart/generate",
		Body:   req.toBody(),
	})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/qrart/tasks", c.t, result), nil
}
