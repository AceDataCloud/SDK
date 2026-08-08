package acedatacloud

import (
	"context"
	"fmt"
)

type MinimaxModel string

const MinimaxModelH3 MinimaxModel = "MiniMax-H3"

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

type MinimaxContentType string

const (
	MinimaxContentText     MinimaxContentType = "text"
	MinimaxContentImageURL MinimaxContentType = "image_url"
	MinimaxContentVideoURL MinimaxContentType = "video_url"
	MinimaxContentAudioURL MinimaxContentType = "audio_url"
)

type MinimaxContentRole string

const (
	MinimaxContentFirstFrame     MinimaxContentRole = "first_frame"
	MinimaxContentLastFrame      MinimaxContentRole = "last_frame"
	MinimaxContentReferenceImage MinimaxContentRole = "reference_image"
	MinimaxContentReferenceVideo MinimaxContentRole = "reference_video"
	MinimaxContentReferenceAudio MinimaxContentRole = "reference_audio"
)

type MinimaxMediaURL struct {
	URL string `json:"url"`
}

type MinimaxContent struct {
	Type     MinimaxContentType `json:"type"`
	Text     string             `json:"text,omitempty"`
	ImageURL *MinimaxMediaURL   `json:"image_url,omitempty"`
	VideoURL *MinimaxMediaURL   `json:"video_url,omitempty"`
	AudioURL *MinimaxMediaURL   `json:"audio_url,omitempty"`
	Role     MinimaxContentRole `json:"role,omitempty"`
}

// Minimax is the MiniMax H3 video generation client.
type Minimax struct {
	t *transport
}

// MinimaxGenerateRequest is the input to Minimax.Generate.
type MinimaxGenerateRequest struct {
	Model         MinimaxModel
	Content       []MinimaxContent
	Resolution    MinimaxResolution
	Duration      int
	Ratio         MinimaxRatio
	AIGCWatermark bool
	// Async is accepted for parity with the other SDKs. MiniMax tasks are always asynchronous.
	Async       *bool
	CallbackURL   string
}

func (r MinimaxGenerateRequest) validate() error {
	if r.Duration < 4 || r.Duration > 15 {
		return fmt.Errorf("duration must be between 4 and 15 seconds")
	}
	if len(r.Content) == 0 {
		return fmt.Errorf("content must contain at least one item")
	}
	for _, item := range r.Content {
		switch item.Type {
		case MinimaxContentText, MinimaxContentImageURL, MinimaxContentVideoURL, MinimaxContentAudioURL:
		default:
			return fmt.Errorf("each content item must have a valid type")
		}
	}
	return nil
}

func (r MinimaxGenerateRequest) toBody() map[string]any {
	body := map[string]any{
		"model":          r.Model,
		"content":        r.Content,
		"resolution":     r.Resolution,
		"duration":       r.Duration,
		"aigc_watermark": r.AIGCWatermark,
	}
	if r.Ratio != "" {
		body["ratio"] = r.Ratio
	}
	if r.CallbackURL != "" {
		body["callback_url"] = r.CallbackURL
	}
	return body
}

// Generate submits a MiniMax H3 video generation task.
func (c *Minimax) Generate(ctx context.Context, req MinimaxGenerateRequest) (*TaskHandle, error) {
	if err := req.validate(); err != nil {
		return nil, err
	}
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
