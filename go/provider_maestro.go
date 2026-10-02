// Code generated from the platform OpenAPI spec. DO NOT EDIT.
// Regenerate with: python scripts/generate_providers.py

package acedatacloud

import "context"

// Maestro is the maestro provider client.
type Maestro struct {
	t *transport
}

// MaestroGenerateRequest is the input to maestro.Generate.
type MaestroGenerateRequest struct {
	// Natural-language brief describing the video to produce (the topic, what to show, tone, audience). The agent de
	Prompt string
	// Production action. generate creates a new video; remix/edit/extend require ref_task_id.
	Action string
	// Required when `action` is remix / edit / extend: the task_id of the previous video to start from.
	RefTaskID string
	// Optional reference media (image / video / audio URLs) the agent can use — e.g. a product shot or logo to featu
	FileURLs []string
	// Output languages, up to 4. The first is primary; each additional delivered language is billed +6 credits.
	Langs []string
	// Required output aspect ratio. All videos render at 1080p/30fps.
	Aspect string
	// Target video length in seconds, from 5 to 300. Successful jobs are billed by actual delivered duration, never
	Duration int
	// Production route: auto, narrated, captions, avatar, or drama. captions requires source video in file_urls; ava
	Scenario string
	// Optional visual-style preset — expressed through typography, palette, motion, image treatment and pacing. Orth
	Style string
	// Optional narration voice — the **timbre** of the voiceover, independent of language. `auto` (default) lets the
	Voice string
	// Async submits without blocking; poll the returned handle. Defaults true.
	Async *bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r MaestroGenerateRequest) toBody() map[string]any {
	body := map[string]any{}
	body["prompt"] = r.Prompt
	if r.Action != "" {
		body["action"] = r.Action
	} else {
		body["action"] = "generate"
	}
	if r.RefTaskID != "" {
		body["ref_task_id"] = r.RefTaskID
	}
	if r.FileURLs != nil {
		body["file_urls"] = r.FileURLs
	}
	body["langs"] = r.Langs
	if r.Aspect != "" {
		body["aspect"] = r.Aspect
	} else {
		body["aspect"] = "9:16"
	}
	if r.Duration != 0 {
		body["duration"] = r.Duration
	} else {
		body["duration"] = 30
	}
	if r.Scenario != "" {
		body["scenario"] = r.Scenario
	} else {
		body["scenario"] = "auto"
	}
	if r.Style != "" {
		body["style"] = r.Style
	} else {
		body["style"] = "auto"
	}
	if r.Voice != "" {
		body["voice"] = r.Voice
	} else {
		body["voice"] = "auto"
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

// Generate Maestro Videos
func (c *Maestro) Generate(ctx context.Context, req MaestroGenerateRequest) (*TaskHandle, error) {
	result, err := c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/maestro/videos",
		Body:   req.toBody(),
	})
	if err != nil {
		return nil, err
	}
	return newTaskHandle(taskIDFrom(result), "/maestro/tasks", c.t, result), nil
}
