package acedatacloud

import "context"

// Veo is the Veo provider client.
type Veo struct {
	t *transport
}

type VeoModel string

const (
	VeoModelVeo3                 VeoModel = "veo3"
	VeoModelVeo3Fast             VeoModel = "veo3-fast"
	VeoModelVeo31Fast            VeoModel = "veo31-fast"
	VeoModelVeo31                VeoModel = "veo31"
	VeoModelVeo31FastIngredients VeoModel = "veo31-fast-ingredients"
)

type VeoResolution string

const (
	VeoResolution4K    VeoResolution = "4k"
	VeoResolution1080P VeoResolution = "1080p"
	VeoResolutionGIF   VeoResolution = "gif"
)

type VeoAction string

const (
	VeoActionTextToVideo        VeoAction = "text2video"
	VeoActionImageToVideo       VeoAction = "image2video"
	VeoActionIngredientsToVideo VeoAction = "ingredients2video"
	VeoActionGet1080P           VeoAction = "get1080p"
)

type VeoAspectRatio string

const (
	VeoAspectRatio16x9 VeoAspectRatio = "16:9"
	VeoAspectRatio9x16 VeoAspectRatio = "9:16"
)

// VeoGenerateRequest is the input to Veo.Generate.
type VeoGenerateRequest struct {
	Action      VeoAction
	Prompt      string
	Model       VeoModel
	Resolution  VeoResolution
	VideoID     string
	Translation *bool
	AspectRatio VeoAspectRatio
	ImageURLs   []string
	CallbackURL string
	// Async submits without blocking; poll the returned handle. Defaults true.
	Async *bool
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r VeoGenerateRequest) toBody() map[string]any {
	body := map[string]any{}
	if r.Action != "" {
		body["action"] = string(r.Action)
	}
	if r.Prompt != "" {
		body["prompt"] = r.Prompt
	}
	if r.Model != "" {
		body["model"] = string(r.Model)
	}
	if r.Resolution != "" {
		body["resolution"] = string(r.Resolution)
	}
	if r.VideoID != "" {
		body["video_id"] = r.VideoID
	}
	if r.Translation != nil {
		body["translation"] = *r.Translation
	}
	if r.AspectRatio != "" {
		body["aspect_ratio"] = string(r.AspectRatio)
	}
	if r.ImageURLs != nil {
		body["image_urls"] = r.ImageURLs
	}
	if r.CallbackURL != "" {
		body["callback_url"] = r.CallbackURL
	}
	body["async"] = true
	if r.Async != nil {
		body["async"] = *r.Async
	}
	for k, v := range r.Extra {
		if _, exists := body[k]; !exists {
			body[k] = v
		}
	}
	return body
}

// Generate creates a Veo video task.
func (c *Veo) Generate(ctx context.Context, req VeoGenerateRequest) (*TaskHandle, error) {
	result, err := c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/veo/videos",
		Body:   req.toBody(),
	})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/veo/tasks", c.t, result), nil
}
