package acedatacloud

import "context"

// QRart is the qrart provider client.
type QRart struct {
	t *transport
}

// QRartGenerateRequest is the input to qrart.Generate.
type QRartGenerateRequest struct {
	// Descriptive prompt for the QR code visual style.
	Prompt string
	// QR code content type (link, text, email, phone, sms).
	Type string
	// Content encoded in the QR code (URL, text, etc.).
	Content string
	// URL of an image to use as QR content.
	ContentImageURL string
	// Error correction level.
	Ecl string
	// QR code weight in the composition (0–1).
	Qrw float64
	// Random seed for reproducibility.
	Seed float64
	// Number of diffusion steps.
	Steps float64
	// Output aspect ratio.
	AspectRatio string
	// Visual style preset name.
	Preset string
	// Dot pattern variant.
	Pattern string
	// Pixel shape style.
	PixelStyle string
	// Logo position within the QR code.
	Position string
	// Corner marker shape.
	MarkerShape string
	// Inner corner marker shape.
	SubMarker string
	// Padding level (0, 5, 10, 15, 20).
	PaddingLevel int
	// Padding noise amount (0–1).
	PaddingNoise float64
	// Rotation angle (0, 90, 180, 270).
	Rotate int
	// Return a raw (non-proxied) URL.
	Rawurl bool
	// Async submits without blocking; poll the returned handle. Defaults true.
	Async *bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r QRartGenerateRequest) toBody() map[string]any {
	body := map[string]any{}
	body["prompt"] = r.Prompt
	body["type"] = r.Type
	if r.Content != "" {
		body["content"] = r.Content
	}
	if r.ContentImageURL != "" {
		body["content_image_url"] = r.ContentImageURL
	}
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
	if r.AspectRatio != "" {
		body["aspect_ratio"] = r.AspectRatio
	}
	if r.Preset != "" {
		body["preset"] = r.Preset
	}
	if r.Pattern != "" {
		body["pattern"] = r.Pattern
	}
	if r.PixelStyle != "" {
		body["pixel_style"] = r.PixelStyle
	}
	if r.Position != "" {
		body["position"] = r.Position
	}
	if r.MarkerShape != "" {
		body["marker_shape"] = r.MarkerShape
	}
	if r.SubMarker != "" {
		body["sub_marker"] = r.SubMarker
	}
	if r.PaddingLevel != 0 {
		body["padding_level"] = r.PaddingLevel
	}
	if r.PaddingNoise != 0 {
		body["padding_noise"] = r.PaddingNoise
	}
	if r.Rotate != 0 {
		body["rotate"] = r.Rotate
	}
	if r.Rawurl {
		body["rawurl"] = r.Rawurl
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

// Generate submits a QR art generation request.
func (c *QRart) Generate(ctx context.Context, req QRartGenerateRequest) (*TaskHandle, error) {
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
