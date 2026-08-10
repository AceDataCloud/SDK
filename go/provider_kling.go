package acedatacloud

import "context"

// Kling is the Kling provider client.
type Kling struct {
	t *transport
}

// KlingCameraControl configures camera movement for Kling video generation.
type KlingCameraControl struct {
	Type   string
	Config map[string]float64
}

func (c KlingCameraControl) toBody() map[string]any {
	body := map[string]any{}
	if c.Type != "" {
		body["type"] = c.Type
	}
	if c.Config != nil {
		body["config"] = c.Config
	}
	return body
}

// KlingReferenceImage is an Omni reference image.
type KlingReferenceImage struct {
	ImageURL string
	Type     string
}

func (r KlingReferenceImage) toBody() map[string]any {
	body := map[string]any{"image_url": r.ImageURL}
	if r.Type != "" {
		body["type"] = r.Type
	}
	return body
}

// KlingReferenceVideo is an Omni reference video.
type KlingReferenceVideo struct {
	VideoURL          string
	ReferType         string
	KeepOriginalSound string
}

func (r KlingReferenceVideo) toBody() map[string]any {
	body := map[string]any{"video_url": r.VideoURL}
	if r.ReferType != "" {
		body["refer_type"] = r.ReferType
	}
	if r.KeepOriginalSound != "" {
		body["keep_original_sound"] = r.KeepOriginalSound
	}
	return body
}

// KlingGenerateRequest is the input to kling.Generate.
type KlingGenerateRequest struct {
	Action         string
	Model          string
	Mode           string
	Prompt         string
	Duration       int
	GenerateAudio  *bool
	VideoID        string
	CfgScale       *float64
	AspectRatio    string
	CallbackURL    string
	Async          *bool
	EndImageURL    string
	CameraControl  *KlingCameraControl
	ImageList      []KlingReferenceImage
	VideoList      []KlingReferenceVideo
	NegativePrompt string
	StartImageURL  string
	Extra          map[string]any
}

func (r KlingGenerateRequest) toBody() map[string]any {
	body := map[string]any{"action": r.Action, "model": "kling-v1", "async": true}
	if r.Model != "" {
		body["model"] = r.Model
	}
	if r.Mode != "" {
		body["mode"] = r.Mode
	}
	if r.Prompt != "" {
		body["prompt"] = r.Prompt
	}
	if r.Duration != 0 {
		body["duration"] = r.Duration
	}
	if r.GenerateAudio != nil {
		body["generate_audio"] = *r.GenerateAudio
	}
	if r.VideoID != "" {
		body["video_id"] = r.VideoID
	}
	if r.CfgScale != nil {
		body["cfg_scale"] = *r.CfgScale
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
	if r.EndImageURL != "" {
		body["end_image_url"] = r.EndImageURL
	}
	if r.CameraControl != nil {
		body["camera_control"] = r.CameraControl.toBody()
	}
	if r.ImageList != nil {
		images := make([]map[string]any, 0, len(r.ImageList))
		for _, image := range r.ImageList {
			images = append(images, image.toBody())
		}
		body["image_list"] = images
	}
	if r.VideoList != nil {
		videos := make([]map[string]any, 0, len(r.VideoList))
		for _, video := range r.VideoList {
			videos = append(videos, video.toBody())
		}
		body["video_list"] = videos
	}
	if r.NegativePrompt != "" {
		body["negative_prompt"] = r.NegativePrompt
	}
	if r.StartImageURL != "" {
		body["start_image_url"] = r.StartImageURL
	}
	for k, v := range r.Extra {
		if _, exists := body[k]; !exists {
			body[k] = v
		}
	}
	return body
}

// Generate creates a Kling video task.
func (c *Kling) Generate(ctx context.Context, req KlingGenerateRequest) (*TaskHandle, error) {
	result, err := c.t.do(ctx, requestOpts{Method: "POST", Path: "/kling/videos", Body: req.toBody()})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/kling/tasks", c.t, result), nil
}

// KlingMotionRequest is the input to kling.Motion.
type KlingMotionRequest struct {
	ModelName            string
	Mode                 string
	KeepOriginalSound    string
	WatermarkInfo        map[string]any
	ImageURL             string
	VideoURL             string
	CharacterOrientation string
	Prompt               string
	CallbackURL          string
	Async                *bool
	Extra                map[string]any
}

func (r KlingMotionRequest) toBody() map[string]any {
	body := map[string]any{
		"mode":                  r.Mode,
		"image_url":             r.ImageURL,
		"video_url":             r.VideoURL,
		"character_orientation": r.CharacterOrientation,
		"async":                 true,
	}
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
	for k, v := range r.Extra {
		if _, exists := body[k]; !exists {
			body[k] = v
		}
	}
	return body
}

// Motion creates a Kling motion task.
func (c *Kling) Motion(ctx context.Context, req KlingMotionRequest) (*TaskHandle, error) {
	result, err := c.t.do(ctx, requestOpts{Method: "POST", Path: "/kling/motion", Body: req.toBody()})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/kling/tasks", c.t, result), nil
}

// KlingLipSyncRequest is the input to kling.LipSync.
type KlingLipSyncRequest struct {
	VideoID       string
	VideoURL      string
	Mode          string
	AudioURL      string
	AudioType     string
	AudioFile     string
	Text          string
	VoiceID       string
	VoiceLanguage string
	VoiceSpeed    float64
	CallbackURL   string
	Async         *bool
	Extra         map[string]any
}

func (r KlingLipSyncRequest) toBody() map[string]any {
	body := map[string]any{"mode": r.Mode, "audio_type": "url", "async": true}
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
	}
	if r.VoiceSpeed != 0 {
		body["voice_speed"] = r.VoiceSpeed
	}
	if r.CallbackURL != "" {
		body["callback_url"] = r.CallbackURL
	}
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

// LipSync creates a Kling lip-sync task.
func (c *Kling) LipSync(ctx context.Context, req KlingLipSyncRequest) (*TaskHandle, error) {
	result, err := c.t.do(ctx, requestOpts{Method: "POST", Path: "/kling/lip-sync", Body: req.toBody()})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/kling/tasks", c.t, result), nil
}

// KlingTalkingPhotoRequest is the input to kling.TalkingPhoto.
type KlingTalkingPhotoRequest struct {
	ImageURL    string
	AudioURL    string
	Prompt      string
	Model       string
	Duration    int
	Mode        string
	CallbackURL string
	Async       *bool
	Extra       map[string]any
}

func (r KlingTalkingPhotoRequest) toBody() map[string]any {
	body := map[string]any{"image_url": r.ImageURL, "audio_url": r.AudioURL, "async": true}
	if r.Prompt != "" {
		body["prompt"] = r.Prompt
	}
	if r.Model != "" {
		body["model"] = r.Model
	}
	if r.Duration != 0 {
		body["duration"] = r.Duration
	}
	if r.Mode != "" {
		body["mode"] = r.Mode
	}
	if r.CallbackURL != "" {
		body["callback_url"] = r.CallbackURL
	}
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

// TalkingPhoto creates a Kling talking-photo task.
func (c *Kling) TalkingPhoto(ctx context.Context, req KlingTalkingPhotoRequest) (*TaskHandle, error) {
	result, err := c.t.do(ctx, requestOpts{Method: "POST", Path: "/kling/talking-photo", Body: req.toBody()})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/kling/tasks", c.t, result), nil
}
