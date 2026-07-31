// Code generated from the platform OpenAPI spec. DO NOT EDIT.
// Regenerate with: python scripts/generate_providers.py

package acedatacloud

import "context"

// Qrart is the qrart provider client.
type Qrart struct {
	t *transport
}

// QrartGenerateRequest is the input to Qrart.Generate.
type QrartGenerateRequest struct {
	// QR code content type.
	Type string
	// Art style prompt.
	Prompt string
	// Error correction level.
	ECL string
	// QR code weight.
	QRW float64
	// Random seed.
	Seed int
	// Number of diffusion steps.
	Steps int
	// Style preset.
	Preset string
	// Whether to use raw URL.
	RawURL bool
	// Rotation angle.
	Rotate int
	// QR code content.
	Content string
	// Pattern style.
	Pattern string
	// Logo position.
	Position string
	// Sub-marker style.
	SubMarker string
	// Pixel style.
	PixelStyle string
	// Aspect ratio.
	AspectRatio string
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
	if r.ECL != "" {
		body["ecl"] = r.ECL
	}
	if r.QRW != 0 {
		body["qrw"] = r.QRW
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
	if r.RawURL {
		body["rawurl"] = r.RawURL
	}
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

// Generate Art QR Code generation API — generates a styled QR code image.
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
