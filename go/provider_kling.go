// Code generated from the platform OpenAPI spec. DO NOT EDIT.
// Regenerate with: python scripts/generate_providers.py

package acedatacloud

import "context"

// Kling is the kling provider client.
type Kling struct {
	t *transport
}

// KlingMotionRequest is the input to kling.Motion.
type KlingMotionRequest struct {
	// Kling Motion Mode
	Mode string
	// Kling Motion Image Url
	ImageURL string
	// Kling Motion Video Url
	VideoURL string
	// Kling Motion Character Orientation
	CharacterOrientation string
	// Kling Motion Model Name
	ModelName string
	// Kling Motion Keep Original Sound
	KeepOriginalSound string
	// Kling Motion Watermark Info
	WatermarkInfo map[string]any
	// Kling Motion Prompt
	Prompt string
	// Async submits without blocking; poll the returned handle. Defaults true.
	Async *bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r KlingMotionRequest) toBody() map[string]any {
	body := map[string]any{}
	body["mode"] = r.Mode
	body["image_url"] = r.ImageURL
	body["video_url"] = r.VideoURL
	body["character_orientation"] = r.CharacterOrientation
	if r.ModelName != "" {
		body["model_name"] = r.ModelName
	}
	if r.KeepOriginalSound != "" {
		body["keep_original_sound"] = r.KeepOriginalSound
	}
	if r.WatermarkInfo != nil {
		body["watermark_info"] = r.WatermarkInfo
	}
	if r.Prompt != "" {
		body["prompt"] = r.Prompt
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

// Motion Kling Motion
func (c *Kling) Motion(ctx context.Context, req KlingMotionRequest) (*TaskHandle, error) {
	result, err := c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/kling/motion",
		Body:   req.toBody(),
	})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/kling/tasks", c.t, result), nil
}

// KlingGenerateRequest is the input to kling.Generate.
type KlingGenerateRequest struct {
	// Kling Videos Action
	Action string
	// Kling Videos Mode
	Mode string
	// Kling Videos Model
	Model string
	// Kling Videos Prompt
	Prompt string
	// Kling Videos Duration
	Duration float64
	// Kling Videos Generate Audio
	GenerateAudio bool
	// Kling Videos Video Id
	VideoID string
	// Kling Videos Cfg Scale
	CfgScale float64
	// Kling Videos Aspect Ratio
	AspectRatio string
	// Kling Videos End Image Url
	EndImageURL string
	// Kling Videos Camera Control
	CameraControl map[string]any
	// Kling Videos Image List
	ImageList []map[string]any
	// Kling Videos Video List
	VideoList []map[string]any
	// Kling Videos Negative Prompt
	NegativePrompt string
	// Kling Videos Start Image Url
	StartImageURL string
	// Kling Videos Multi Shot
	MultiShot bool
	// Kling Videos Shot Type
	ShotType string
	// Kling Videos Multi Prompt
	MultiPrompt []map[string]any
	// Kling Videos Element List
	ElementList []map[string]any
	// Kling Videos Voice List
	VoiceList []map[string]any
	// Async submits without blocking; poll the returned handle. Defaults true.
	Async *bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r KlingGenerateRequest) toBody() map[string]any {
	body := map[string]any{}
	body["action"] = r.Action
	if r.Mode != "" {
		body["mode"] = r.Mode
	} else {
		body["mode"] = "std"
	}
	if r.Model != "" {
		body["model"] = r.Model
	} else {
		body["model"] = "kling-v1"
	}
	if r.Prompt != "" {
		body["prompt"] = r.Prompt
	}
	if r.Duration != 0 {
		body["duration"] = r.Duration
	} else {
		body["duration"] = 5
	}
	body["generate_audio"] = r.GenerateAudio
	if r.VideoID != "" {
		body["video_id"] = r.VideoID
	}
	if r.CfgScale != 0 {
		body["cfg_scale"] = r.CfgScale
	}
	if r.AspectRatio != "" {
		body["aspect_ratio"] = r.AspectRatio
	}
	if r.EndImageURL != "" {
		body["end_image_url"] = r.EndImageURL
	}
	if r.CameraControl != nil {
		body["camera_control"] = r.CameraControl
	}
	if r.ImageList != nil {
		body["image_list"] = r.ImageList
	}
	if r.VideoList != nil {
		body["video_list"] = r.VideoList
	}
	if r.NegativePrompt != "" {
		body["negative_prompt"] = r.NegativePrompt
	}
	if r.StartImageURL != "" {
		body["start_image_url"] = r.StartImageURL
	}
	body["multi_shot"] = r.MultiShot
	if r.ShotType != "" {
		body["shot_type"] = r.ShotType
	}
	if r.MultiPrompt != nil {
		body["multi_prompt"] = r.MultiPrompt
	}
	if r.ElementList != nil {
		body["element_list"] = r.ElementList
	}
	if r.VoiceList != nil {
		body["voice_list"] = r.VoiceList
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

// Generate Kling Videos
func (c *Kling) Generate(ctx context.Context, req KlingGenerateRequest) (*TaskHandle, error) {
	result, err := c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/kling/videos",
		Body:   req.toBody(),
	})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/kling/tasks", c.t, result), nil
}

// KlingLipSyncRequest is the input to kling.Lip_Sync.
type KlingLipSyncRequest struct {
	// Kling Lip Sync Mode
	Mode string
	// Kling Lip Sync Video Id
	VideoID string
	// Kling Lip Sync Video Url
	VideoURL string
	// Kling Lip Sync Audio Url
	AudioURL string
	// Kling Lip Sync Audio Type
	AudioType string
	// Kling Lip Sync Audio File
	AudioFile string
	// Kling Lip Sync Text
	Text string
	// Kling Lip Sync Voice Id
	VoiceID string
	// Kling Lip Sync Voice Language
	VoiceLanguage string
	// Kling Lip Sync Voice Speed
	VoiceSpeed float64
	// Async submits without blocking; poll the returned handle. Defaults true.
	Async *bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r KlingLipSyncRequest) toBody() map[string]any {
	body := map[string]any{}
	body["mode"] = r.Mode
	if r.VideoID != "" {
		body["video_id"] = r.VideoID
	}
	if r.VideoURL != "" {
		body["video_url"] = r.VideoURL
	}
	if r.AudioURL != "" {
		body["audio_url"] = r.AudioURL
	}
	if r.AudioType != "" {
		body["audio_type"] = r.AudioType
	} else {
		body["audio_type"] = "url"
	}
	if r.AudioFile != "" {
		body["audio_file"] = r.AudioFile
	}
	if r.Text != "" {
		body["text"] = r.Text
	}
	if r.VoiceID != "" {
		body["voice_id"] = r.VoiceID
	}
	if r.VoiceLanguage != "" {
		body["voice_language"] = r.VoiceLanguage
	} else {
		body["voice_language"] = "zh"
	}
	if r.VoiceSpeed != 0 {
		body["voice_speed"] = r.VoiceSpeed
	} else {
		body["voice_speed"] = 1.0
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

// LipSync Kling Lip Sync
func (c *Kling) LipSync(ctx context.Context, req KlingLipSyncRequest) (*TaskHandle, error) {
	result, err := c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/kling/lip-sync",
		Body:   req.toBody(),
	})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/kling/tasks", c.t, result), nil
}

// KlingTalkingPhotoRequest is the input to kling.Talking_Photo.
type KlingTalkingPhotoRequest struct {
	// Kling Talking Photo Image Url
	ImageURL string
	// Kling Talking Photo Audio Url
	AudioURL string
	// Kling Talking Photo Prompt
	Prompt string
	// Kling Talking Photo Model
	Model string
	// Kling Talking Photo Duration
	Duration int
	// Kling Talking Photo Mode
	Mode string
	// Async submits without blocking; poll the returned handle. Defaults true.
	Async *bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r KlingTalkingPhotoRequest) toBody() map[string]any {
	body := map[string]any{}
	body["image_url"] = r.ImageURL
	body["audio_url"] = r.AudioURL
	if r.Prompt != "" {
		body["prompt"] = r.Prompt
	}
	if r.Model != "" {
		body["model"] = r.Model
	} else {
		body["model"] = "kling-v2-1-master"
	}
	if r.Duration != 0 {
		body["duration"] = r.Duration
	} else {
		body["duration"] = 5
	}
	if r.Mode != "" {
		body["mode"] = r.Mode
	} else {
		body["mode"] = "pro"
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

// TalkingPhoto Kling Talking Photo
func (c *Kling) TalkingPhoto(ctx context.Context, req KlingTalkingPhotoRequest) (*TaskHandle, error) {
	result, err := c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/kling/talking-photo",
		Body:   req.toBody(),
	})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/kling/tasks", c.t, result), nil
}

// KlingGoodsStudioRequest is the input to kling.Goods_Studio.
type KlingGoodsStudioRequest struct {
	// Kling Goods Contents
	Contents []map[string]any
	// required
	Settings map[string]any
	// Kling Goods Watermark
	Watermark bool
	// Async submits without blocking; poll the returned handle. Defaults true.
	Async *bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r KlingGoodsStudioRequest) toBody() map[string]any {
	body := map[string]any{}
	body["contents"] = r.Contents
	body["settings"] = r.Settings
	body["watermark"] = r.Watermark
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

// GoodsStudio Kling Goods Summary
func (c *Kling) GoodsStudio(ctx context.Context, req KlingGoodsStudioRequest) (*TaskHandle, error) {
	result, err := c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/kling/goods-studio",
		Body:   req.toBody(),
	})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/kling/tasks", c.t, result), nil
}

// KlingVideoCommerceRequest is the input to kling.Video_Commerce.
type KlingVideoCommerceRequest struct {
	// Kling Commerce Contents
	Contents []map[string]any
	// optional
	Settings map[string]any
	// Kling Commerce Watermark
	Watermark bool
	// Async submits without blocking; poll the returned handle. Defaults true.
	Async *bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r KlingVideoCommerceRequest) toBody() map[string]any {
	body := map[string]any{}
	body["contents"] = r.Contents
	if r.Settings != nil {
		body["settings"] = r.Settings
	}
	body["watermark"] = r.Watermark
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

// VideoCommerce Kling Commerce Summary
func (c *Kling) VideoCommerce(ctx context.Context, req KlingVideoCommerceRequest) (*TaskHandle, error) {
	result, err := c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/kling/video-commerce",
		Body:   req.toBody(),
	})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/kling/tasks", c.t, result), nil
}
