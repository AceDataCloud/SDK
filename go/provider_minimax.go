package acedatacloud

import "context"

type MinimaxModel string

const MinimaxModelH3 MinimaxModel = "MiniMax-H3"

type MinimaxContentType string

const (
	MinimaxContentText     MinimaxContentType = "text"
	MinimaxContentImageURL MinimaxContentType = "image_url"
	MinimaxContentVideoURL MinimaxContentType = "video_url"
	MinimaxContentAudioURL MinimaxContentType = "audio_url"
)

type MinimaxContentRole string

const (
	MinimaxRoleFirstFrame     MinimaxContentRole = "first_frame"
	MinimaxRoleLastFrame      MinimaxContentRole = "last_frame"
	MinimaxRoleReferenceImage MinimaxContentRole = "reference_image"
	MinimaxRoleReferenceVideo MinimaxContentRole = "reference_video"
	MinimaxRoleReferenceAudio MinimaxContentRole = "reference_audio"
)

type MinimaxResolution string

const (
	MinimaxResolution768P MinimaxResolution = "768P"
	MinimaxResolution2K   MinimaxResolution = "2K"
)

type MinimaxRatio string

const (
	MinimaxRatioAdaptive MinimaxRatio = "adaptive"
	MinimaxRatio21x9     MinimaxRatio = "21:9"
	MinimaxRatio16x9     MinimaxRatio = "16:9"
	MinimaxRatio4x3      MinimaxRatio = "4:3"
	MinimaxRatio1x1      MinimaxRatio = "1:1"
	MinimaxRatio3x4      MinimaxRatio = "3:4"
	MinimaxRatio9x16     MinimaxRatio = "9:16"
)

// Minimax is the minimax provider client.
type Minimax struct {
	t *transport
}

type MinimaxMediaURL struct {
	URL string `json:"url"`
}

type MinimaxContentItem struct {
	Type     MinimaxContentType `json:"type"`
	Text     string             `json:"text,omitempty"`
	ImageURL *MinimaxMediaURL   `json:"image_url,omitempty"`
	VideoURL *MinimaxMediaURL   `json:"video_url,omitempty"`
	AudioURL *MinimaxMediaURL   `json:"audio_url,omitempty"`
	Role     MinimaxContentRole `json:"role,omitempty"`
}

// MinimaxGenerateRequest is the input to minimax.Generate.
type MinimaxGenerateRequest struct {
	Model         MinimaxModel
	Content       []MinimaxContentItem
	Resolution    MinimaxResolution
	Duration      int
	Ratio         MinimaxRatio
	CallbackURL   string
	AIGCWatermark *bool
	// Async is accepted for parity with async generation providers; MiniMax always returns a task.
	Async *bool
}

func (r MinimaxGenerateRequest) toBody() map[string]any {
	body := map[string]any{
		"model":      string(r.Model),
		"content":    r.Content,
		"resolution": string(r.Resolution),
		"duration":   r.Duration,
	}
	if r.Ratio != "" {
		body["ratio"] = string(r.Ratio)
	}
	if r.CallbackURL != "" {
		body["callback_url"] = r.CallbackURL
	}
	if r.AIGCWatermark != nil {
		body["aigc_watermark"] = *r.AIGCWatermark
	}
	return body
}

// Generate calls the Minimax Videos API.
func (c *Minimax) Generate(ctx context.Context, req MinimaxGenerateRequest) (*TaskHandle, error) {
	result, err := c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/minimax/videos",
		Body:   req.toBody(),
	})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/minimax/tasks", c.t, result), nil
}
