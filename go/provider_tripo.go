// Code generated from the platform OpenAPI spec. DO NOT EDIT.
// Regenerate with: python scripts/generate_providers.py

package acedatacloud

import "context"

// Tripo is the tripo provider client.
type Tripo struct {
	t *transport
}

// TripoGenerateRequest is the input to tripo.Generate.
type TripoGenerateRequest struct {
	// optional
	Action string
	// optional
	Model string
	// optional
	Texture string
	// optional
	Prompt string
	// Public PNG or JPEG up to 20 MiB.
	ImageURL string
	// Front, left, back, right. Front and at least one other image are required. Use null to skip an optional view.
	ImageURLs []*string
	// optional
	IdempotencyKey string
	// Async submits without blocking; poll the returned handle. Defaults true.
	Async *bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r TripoGenerateRequest) toBody() map[string]any {
	body := map[string]any{}
	if r.Action != "" {
		body["action"] = r.Action
	} else {
		body["action"] = "generate"
	}
	if r.Model != "" {
		body["model"] = r.Model
	} else {
		body["model"] = "v3.1-20260211"
	}
	if r.Texture != "" {
		body["texture"] = r.Texture
	} else {
		body["texture"] = "standard"
	}
	if r.Prompt != "" {
		body["prompt"] = r.Prompt
	}
	if r.ImageURL != "" {
		body["image_url"] = r.ImageURL
	}
	if r.ImageURLs != nil {
		body["image_urls"] = r.ImageURLs
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

// Generate Tripo Generations
func (c *Tripo) Generate(ctx context.Context, req TripoGenerateRequest) (*TaskHandle, error) {
	result, err := c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/tripo/generations",
		Body:   req.toBody(),
		ExtraHeaders: func() map[string]string {
			headers := map[string]string{}
			if req.IdempotencyKey != "" {
				headers["Idempotency-Key"] = req.IdempotencyKey
			}
			return headers
		}(),
	})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/tripo/tasks", c.t, result), nil
}

// TripoModelsRequest is the input to tripo.Models.
type TripoModelsRequest struct {
	// required
	Action string
	// Public HTTPS URL to a supported model file up to 150 MiB.
	ModelURL string
	// optional
	ModelID string
	// optional
	Model string
	// optional
	TextureQuality string
	// optional
	TextureAlignment string
	// optional
	TextureSeed *int
	// optional
	Pbr *bool
	// optional
	Bake *bool
	// optional
	Delight *bool
	// optional
	PartNames []string
	// optional
	Compress string
	// optional
	Prompt string
	// Public PNG or JPEG up to 20 MiB.
	ImageURL string
	// Front, left, back, right. Front and at least one other image are required. Use null to skip an optional view.
	ImageURLs []*string
	// Public PNG or JPEG up to 20 MiB.
	StyleImageURL string
	// optional
	Format string
	// optional
	Quad *bool
	// optional
	ForceSymmetry *bool
	// optional
	FlattenBottom *bool
	// optional
	PackUv *bool
	// optional
	ExportVertexColors *bool
	// optional
	PivotToCenterBottom *bool
	// optional
	WithAnimation *bool
	// optional
	AnimateInPlace *bool
	// optional
	FaceLimit *int
	// optional
	FlattenBottomThreshold *float64
	// optional
	TextureSize *int
	// optional
	TextureFormat string
	// optional
	ScaleFactor *float64
	// optional
	ExportOrientation string
	// optional
	FbxPreset string
	// optional
	TexturePackaging string
	// optional
	IdempotencyKey string
	// Async submits without blocking; poll the returned handle. Defaults true.
	Async *bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r TripoModelsRequest) toBody() map[string]any {
	body := map[string]any{}
	body["action"] = r.Action
	if r.ModelURL != "" {
		body["model_url"] = r.ModelURL
	}
	if r.ModelID != "" {
		body["model_id"] = r.ModelID
	}
	if r.Model != "" {
		body["model"] = r.Model
	}
	if r.TextureQuality != "" {
		body["texture_quality"] = r.TextureQuality
	}
	if r.TextureAlignment != "" {
		body["texture_alignment"] = r.TextureAlignment
	}
	if r.TextureSeed != nil {
		body["texture_seed"] = *r.TextureSeed
	}
	if r.Pbr != nil {
		body["pbr"] = *r.Pbr
	}
	if r.Bake != nil {
		body["bake"] = *r.Bake
	}
	if r.Delight != nil {
		body["delight"] = *r.Delight
	}
	if r.PartNames != nil {
		body["part_names"] = r.PartNames
	}
	if r.Compress != "" {
		body["compress"] = r.Compress
	}
	if r.Prompt != "" {
		body["prompt"] = r.Prompt
	}
	if r.ImageURL != "" {
		body["image_url"] = r.ImageURL
	}
	if r.ImageURLs != nil {
		body["image_urls"] = r.ImageURLs
	}
	if r.StyleImageURL != "" {
		body["style_image_url"] = r.StyleImageURL
	}
	if r.Format != "" {
		body["format"] = r.Format
	}
	if r.Quad != nil {
		body["quad"] = *r.Quad
	}
	if r.ForceSymmetry != nil {
		body["force_symmetry"] = *r.ForceSymmetry
	}
	if r.FlattenBottom != nil {
		body["flatten_bottom"] = *r.FlattenBottom
	}
	if r.PackUv != nil {
		body["pack_uv"] = *r.PackUv
	}
	if r.ExportVertexColors != nil {
		body["export_vertex_colors"] = *r.ExportVertexColors
	}
	if r.PivotToCenterBottom != nil {
		body["pivot_to_center_bottom"] = *r.PivotToCenterBottom
	}
	if r.WithAnimation != nil {
		body["with_animation"] = *r.WithAnimation
	}
	if r.AnimateInPlace != nil {
		body["animate_in_place"] = *r.AnimateInPlace
	}
	if r.FaceLimit != nil {
		body["face_limit"] = *r.FaceLimit
	}
	if r.FlattenBottomThreshold != nil {
		body["flatten_bottom_threshold"] = *r.FlattenBottomThreshold
	}
	if r.TextureSize != nil {
		body["texture_size"] = *r.TextureSize
	}
	if r.TextureFormat != "" {
		body["texture_format"] = r.TextureFormat
	}
	if r.ScaleFactor != nil {
		body["scale_factor"] = *r.ScaleFactor
	}
	if r.ExportOrientation != "" {
		body["export_orientation"] = r.ExportOrientation
	}
	if r.FbxPreset != "" {
		body["fbx_preset"] = r.FbxPreset
	}
	if r.TexturePackaging != "" {
		body["texture_packaging"] = r.TexturePackaging
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

// Models Tripo Models
func (c *Tripo) Models(ctx context.Context, req TripoModelsRequest) (*TaskHandle, error) {
	result, err := c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/tripo/models",
		Body:   req.toBody(),
		ExtraHeaders: func() map[string]string {
			headers := map[string]string{}
			if req.IdempotencyKey != "" {
				headers["Idempotency-Key"] = req.IdempotencyKey
			}
			return headers
		}(),
	})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/tripo/tasks", c.t, result), nil
}

// TripoAnimationsRequest is the input to tripo.Animations.
type TripoAnimationsRequest struct {
	// required
	Action string
	// optional
	ModelID string
	// Public HTTPS URL to a supported model file up to 150 MiB.
	ModelURL string
	// optional
	Model string
	// optional
	RigType string
	// optional
	Spec string
	// optional
	Format string
	// optional
	Animation string
	// optional
	Animations []string
	// optional
	ExportWithGeometry *bool
	// optional
	AnimateInPlace *bool
	// optional
	IdempotencyKey string
	// Async submits without blocking; poll the returned handle. Defaults true.
	Async *bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r TripoAnimationsRequest) toBody() map[string]any {
	body := map[string]any{}
	body["action"] = r.Action
	if r.ModelID != "" {
		body["model_id"] = r.ModelID
	}
	if r.ModelURL != "" {
		body["model_url"] = r.ModelURL
	}
	if r.Model != "" {
		body["model"] = r.Model
	}
	if r.RigType != "" {
		body["rig_type"] = r.RigType
	}
	if r.Spec != "" {
		body["spec"] = r.Spec
	}
	if r.Format != "" {
		body["format"] = r.Format
	}
	if r.Animation != "" {
		body["animation"] = r.Animation
	}
	if r.Animations != nil {
		body["animations"] = r.Animations
	}
	if r.ExportWithGeometry != nil {
		body["export_with_geometry"] = *r.ExportWithGeometry
	}
	if r.AnimateInPlace != nil {
		body["animate_in_place"] = *r.AnimateInPlace
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

// Animations Tripo Animations
func (c *Tripo) Animations(ctx context.Context, req TripoAnimationsRequest) (*TaskHandle, error) {
	result, err := c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/tripo/animations",
		Body:   req.toBody(),
		ExtraHeaders: func() map[string]string {
			headers := map[string]string{}
			if req.IdempotencyKey != "" {
				headers["Idempotency-Key"] = req.IdempotencyKey
			}
			return headers
		}(),
	})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/tripo/tasks", c.t, result), nil
}

// TripoTasksRequest is the input to tripo.Tasks.
type TripoTasksRequest struct {
	// optional
	Action string
	// optional
	ID string
	// optional
	TraceID string
	// optional
	IDs []string
	// optional
	TraceIDs []string
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r TripoTasksRequest) toBody() map[string]any {
	body := map[string]any{}
	if r.Action != "" {
		body["action"] = r.Action
	} else {
		body["action"] = "retrieve"
	}
	if r.ID != "" {
		body["id"] = r.ID
	}
	if r.TraceID != "" {
		body["trace_id"] = r.TraceID
	}
	if r.IDs != nil {
		body["ids"] = r.IDs
	}
	if r.TraceIDs != nil {
		body["trace_ids"] = r.TraceIDs
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

// Tasks Tripo tasks
func (c *Tripo) Tasks(ctx context.Context, req TripoTasksRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/tripo/tasks",
		Body:   req.toBody(),
	})
}
