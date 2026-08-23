package acedatacloud

import "context"

// Kling is the Kling provider client.
type Kling struct {
	t *transport
}

// KlingGenerateRequest is the input to Kling.Generate.
type KlingGenerateRequest struct {
	Action         string
	Model          string
	Mode           string
	Prompt         string
	Duration       int
	GenerateAudio  *bool
	VideoID        string
	CfgScale       float64
	AspectRatio    string
	CallbackURL    string
	Async          *bool
	Timeout        int
	EndImageURL    string
	CameraControl  map[string]any
	ImageList      []map[string]any
	VideoList      []map[string]any
	NegativePrompt string
	StartImageURL  string
}

func (r KlingGenerateRequest) toBody() map[string]any {
	body := map[string]any{"action": r.Action, "model": r.Model, "mode": r.Mode, "duration": r.Duration}
	if r.Model == "" {
		body["model"] = "kling-v1"
	}
	if r.Mode == "" {
		body["mode"] = "std"
	}
	if r.Duration == 0 {
		body["duration"] = 5
	}
	if r.Prompt != "" {
		body["prompt"] = r.Prompt
	}
	if r.GenerateAudio != nil {
		body["generate_audio"] = *r.GenerateAudio
	}
	if r.VideoID != "" {
		body["video_id"] = r.VideoID
	}
	if r.CfgScale != 0 {
		body["cfg_scale"] = r.CfgScale
	}
	if r.AspectRatio != "" {
		body["aspect_ratio"] = r.AspectRatio
	}
	if r.CallbackURL != "" {
		body["callback_url"] = r.CallbackURL
	}
	if r.Async != nil {
		body["async"] = *r.Async
	}
	if r.Timeout != 0 {
		body["timeout"] = r.Timeout
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
	return body
}

// Generate calls /kling/videos.
func (c *Kling) Generate(ctx context.Context, req KlingGenerateRequest) (*TaskHandle, error) {
	result, err := c.t.do(ctx, requestOpts{Method: "POST", Path: "/kling/videos", Body: req.toBody()})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/kling/tasks", c.t, result), nil
}

// KlingMotionRequest is the input to Kling.Motion.
type KlingMotionRequest struct {
	Mode                 string
	ImageURL             string
	VideoURL             string
	CharacterOrientation string
	ModelName            string
	KeepOriginalSound    string
	WatermarkInfo        map[string]any
	Prompt               string
	CallbackURL          string
	Async                *bool
}

func (r KlingMotionRequest) toBody() map[string]any {
	body := map[string]any{"mode": r.Mode, "image_url": r.ImageURL, "video_url": r.VideoURL, "character_orientation": r.CharacterOrientation}
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
	if r.CallbackURL != "" {
		body["callback_url"] = r.CallbackURL
	}
	if r.Async != nil {
		body["async"] = *r.Async
	}
	return body
}

// Motion calls /kling/motion.
func (c *Kling) Motion(ctx context.Context, req KlingMotionRequest) (*TaskHandle, error) {
	result, err := c.t.do(ctx, requestOpts{Method: "POST", Path: "/kling/motion", Body: req.toBody()})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/kling/tasks", c.t, result), nil
}

// KlingLipSyncRequest is the input to Kling.LipSync.
type KlingLipSyncRequest struct {
	Mode, VideoID, VideoURL, AudioURL, AudioType, AudioFile, Text, VoiceID, VoiceLanguage, CallbackURL string
	VoiceSpeed                                                                                         float64
	Async                                                                                              *bool
}

func (r KlingLipSyncRequest) toBody() map[string]any {
	body := map[string]any{"mode": r.Mode, "audio_type": r.AudioType, "voice_language": r.VoiceLanguage, "voice_speed": r.VoiceSpeed, "async": false}
	if r.AudioType == "" {
		body["audio_type"] = "url"
	}
	if r.VoiceLanguage == "" {
		body["voice_language"] = "zh"
	}
	if r.VoiceSpeed == 0 {
		body["voice_speed"] = 1.0
	}
	if r.Async != nil {
		body["async"] = *r.Async
	}
	for key, value := range map[string]string{"video_id": r.VideoID, "video_url": r.VideoURL, "audio_url": r.AudioURL, "audio_file": r.AudioFile, "text": r.Text, "voice_id": r.VoiceID, "callback_url": r.CallbackURL} {
		if value != "" {
			body[key] = value
		}
	}
	return body
}

// LipSync calls /kling/lip-sync.
func (c *Kling) LipSync(ctx context.Context, req KlingLipSyncRequest) (*TaskHandle, error) {
	result, err := c.t.do(ctx, requestOpts{Method: "POST", Path: "/kling/lip-sync", Body: req.toBody()})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/kling/tasks", c.t, result), nil
}

// KlingTalkingPhotoRequest is the input to Kling.TalkingPhoto.
type KlingTalkingPhotoRequest struct {
	ImageURL, AudioURL, Prompt, Model, Mode, CallbackURL string
	Duration                                             int
	Async                                                *bool
}

func (r KlingTalkingPhotoRequest) toBody() map[string]any {
	body := map[string]any{"image_url": r.ImageURL, "audio_url": r.AudioURL, "model": r.Model, "duration": r.Duration, "mode": r.Mode, "async": false}
	if r.Model == "" {
		body["model"] = "kling-v2-1-master"
	}
	if r.Duration == 0 {
		body["duration"] = 5
	}
	if r.Mode == "" {
		body["mode"] = "pro"
	}
	if r.Prompt != "" {
		body["prompt"] = r.Prompt
	}
	if r.CallbackURL != "" {
		body["callback_url"] = r.CallbackURL
	}
	if r.Async != nil {
		body["async"] = *r.Async
	}
	return body
}

// TalkingPhoto calls /kling/talking-photo.
func (c *Kling) TalkingPhoto(ctx context.Context, req KlingTalkingPhotoRequest) (*TaskHandle, error) {
	result, err := c.t.do(ctx, requestOpts{Method: "POST", Path: "/kling/talking-photo", Body: req.toBody()})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/kling/tasks", c.t, result), nil
}
