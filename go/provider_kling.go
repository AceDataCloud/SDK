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
	// Video generation mode, optional, enumeration values: `std` (standard mode, 720p, lower consumption) or `pro` (
	Mode string
	// Reference image URL: The characters, background, and other elements in the generated video are all based on th
	ImageURL string
	// Reference video URL: The character movements in the generated video will be consistent with this reference vid
	VideoURL string
	// Generate the orientation of characters in the video, which can be chosen to be consistent with the reference i
	CharacterOrientation string
	// Text prompts can contain both positive and negative descriptions simultaneously.
	Prompt string
	// Model name, optional, enumeration values: `kling-v2-6` or `kling-v3`. If not provided, the server's default mo
	ModelName string
	// Watermark configuration, optional. The object format is `{ "enabled": true }`. When `enabled` is set to `true`
	WatermarkInfo map[string]any
	// Whether to keep the original audio of the reference video, optional, enumeration values: `yes` (keep) or `no`
	KeepOriginalSound string
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
	if r.Prompt != "" {
		body["prompt"] = r.Prompt
	}
	if r.ModelName != "" {
		body["model_name"] = r.ModelName
	}
	if r.WatermarkInfo != nil {
		body["watermark_info"] = r.WatermarkInfo
	}
	if r.KeepOriginalSound != "" {
		body["keep_original_sound"] = r.KeepOriginalSound
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

// Motion Kling motion-control video generation API. Generates controllable-motion video clips from a reference image and motion trajectory (motion brush, etc.)
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
	// Video generation action. If the value is `text2video`, then generate a video based on the prompt.
	Action string
	// Video generation mode, optional. Supported values: `std` (high performance mode), `pro` (high quality mode), `
	Mode string
	// The model used for generating videos, with a default value of kling-v1.
	Model string
	// Prompts for generating videos. When using Omni All-Purpose Reference (model `kling-o1` or `kling-v3-omni`), yo
	Prompt string
	// Video generation duration, measured in seconds, is optional. For kling-v3/kling-v3-omni: supports flexible set
	Duration float64
	// When the action is extend, you can specify the video_id to continue the extension of that video.
	VideoID string
	// The strength of relevance of the prompt words, used to control the degree of alignment between the generated v
	CfgScale float64
	// Omni reference image list, applicable only to models `kling-o1` and `kling-v3-omni`. Array elements pass image
	ImageList []map[string]any
	// Omni reference video list, applicable only to models `kling-o1` and `kling-v3-omni`. Upload a reference video
	VideoList []map[string]any
	// Video aspect ratio, optional, enumeration values: 16:9, 9:16, 1:1. The default value is 16:9.
	AspectRatio string
	// End frame reference image URL. Valid only when `action=image2video` and `start_image_url` is not empty. Model/
	EndImageURL string
	// Contains 6 fields used to specify the movement or change of the camera in different directions. `camera_contro
	CameraControl map[string]any
	// Whether to generate audio while generating video, optional. Only `kling-v3`, `kling-v3-omni`, and `kling-v2-6`
	GenerateAudio bool
	// Optional parameters, supporting up to 200 characters, used to describe content that you do not wish to appear
	NegativePrompt string
	// You can specify the first frame reference image of the video, which is effective when the action is image2vide
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
	}
	if r.Model != "" {
		body["model"] = r.Model
	}
	if r.Prompt != "" {
		body["prompt"] = r.Prompt
	}
	if r.Duration != 0 {
		body["duration"] = r.Duration
	}
	if r.VideoID != "" {
		body["video_id"] = r.VideoID
	}
	if r.CfgScale != 0 {
		body["cfg_scale"] = r.CfgScale
	}
	if r.ImageList != nil {
		body["image_list"] = r.ImageList
	}
	if r.VideoList != nil {
		body["video_list"] = r.VideoList
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
	body["generate_audio"] = r.GenerateAudio
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

// Generate Kuaishou Kling AI video generation API. Supports text-to-video, image-to-video, and start/end frame control across kling-v1, kling-v1-6, kling-v2-mast
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
	// audio2video: Drive with audio clips; text2video: Drive with text + tone.
	Mode string
	// Text to be read aloud (required when mode is text2video, up to 120 characters).
	Text string
	// The ID of the video generated by Kling (for example, from /kling/videos image2video) must be generated within
	VideoID string
	// The tone used (required when mode is text2video).
	VoiceID string
	// The public URL for the audio drive (required when mode is audio2video).
	AudioURL string
	// The public URL of the 5-second/10-second video that matches the lip sync. Choose one between video_id.
	VideoURL string
	// Base64 of the audio file (required when audio_type is file). Supports .mp3/.wav/.m4a/.aac, not exceeding 5MB.
	AudioFile string
	// The method of providing audio (for audio2video).
	AudioType string
	// The speech rate of text2video (0.8–2.0, keep one decimal place).
	VoiceSpeed float64
	// The tone language of text2video.
	VoiceLanguage string
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
	if r.Text != "" {
		body["text"] = r.Text
	}
	if r.VideoID != "" {
		body["video_id"] = r.VideoID
	}
	if r.VoiceID != "" {
		body["voice_id"] = r.VoiceID
	}
	if r.AudioURL != "" {
		body["audio_url"] = r.AudioURL
	}
	if r.VideoURL != "" {
		body["video_url"] = r.VideoURL
	}
	if r.AudioFile != "" {
		body["audio_file"] = r.AudioFile
	}
	if r.AudioType != "" {
		body["audio_type"] = r.AudioType
	} else {
		body["audio_type"] = "url"
	}
	if r.VoiceSpeed != 0 {
		body["voice_speed"] = r.VoiceSpeed
	} else {
		body["voice_speed"] = 1.0
	}
	if r.VoiceLanguage != "" {
		body["voice_language"] = r.VoiceLanguage
	} else {
		body["voice_language"] = "zh"
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

// LipSync Kling lip-sync API — sync a character's mouth in a video to audio or text.
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
	// Public URL for audio (.mp3/.wav/.m4a/.aac, no more than 5MB), characters will lip-sync according to its conten
	AudioURL string
	// Public URL of the character photo, it is recommended to use a clear frontal photo.
	ImageURL string
	// The generation quality of photo animation stage.
	Mode string
	// The Kling model used in the photo animation stage.
	Model string
	// Optional: Action/expression prompts for the photo animation stage.
	Prompt string
	// Video duration (seconds), while also limiting the length of the audio reading.
	Duration int
	// Async submits without blocking; poll the returned handle. Defaults true.
	Async *bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r KlingTalkingPhotoRequest) toBody() map[string]any {
	body := map[string]any{}
	body["audio_url"] = r.AudioURL
	body["image_url"] = r.ImageURL
	if r.Mode != "" {
		body["mode"] = r.Mode
	} else {
		body["mode"] = "pro"
	}
	if r.Model != "" {
		body["model"] = r.Model
	} else {
		body["model"] = "kling-v2-1-master"
	}
	if r.Prompt != "" {
		body["prompt"] = r.Prompt
	}
	if r.Duration != 0 {
		body["duration"] = r.Duration
	} else {
		body["duration"] = 5
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

// TalkingPhoto Kling talking-photo API — make a still portrait speak from audio or text.
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
