// Code generated from the platform OpenAPI spec. DO NOT EDIT.
// Regenerate with: python scripts/generate_providers.py

package acedatacloud

import (
	"context"
	"fmt"
)

// Maestro is the maestro provider client.
type Maestro struct {
	t *transport
}

type MaestroAction string

const (
	MaestroActionGenerate MaestroAction = "generate"
	MaestroActionRemix    MaestroAction = "remix"
	MaestroActionEdit     MaestroAction = "edit"
	MaestroActionExtend   MaestroAction = "extend"
)

type MaestroAspect string

const (
	MaestroAspectPortrait  MaestroAspect = "9:16"
	MaestroAspectLandscape MaestroAspect = "16:9"
	MaestroAspectSquare    MaestroAspect = "1:1"
)

type MaestroQuality string

const (
	MaestroQualityLite     MaestroQuality = "lite"
	MaestroQualityStandard MaestroQuality = "standard"
	MaestroQualityPro      MaestroQuality = "pro"
)

type MaestroScenario string

const (
	MaestroScenarioAuto     MaestroScenario = "auto"
	MaestroScenarioNarrated MaestroScenario = "narrated"
	MaestroScenarioCaptions MaestroScenario = "captions"
	MaestroScenarioAvatar   MaestroScenario = "avatar"
	MaestroScenarioDrama    MaestroScenario = "drama"
)

// MaestroGenerateRequest is the input to maestro.Generate.
type MaestroGenerateRequest struct {
	// Natural-language brief describing the video to produce (the topic, what to show, tone, audience). The agent de
	Prompt string
	// Output languages, e.g. ["zh-cn", "en"]. The first is the primary language; each additional one reuses the visu
	Langs []string
	// Optional visual-style preset — expressed through typography, palette, motion, image treatment and pacing. Orth
	Style string
	// Optional narration voice — the **timbre** of the voiceover, independent of language. `auto` (default) lets the
	Voice string
	// generate = a new video. remix / edit / extend = iterate on a previous video (require `ref_task_id`).
	Action MaestroAction
	// Output aspect ratio (hint — the agent may follow the prompt).
	Aspect MaestroAspect
	// Production tier, a multiplier on the duration-based price. `draft` = a fast rough cut for previewing the idea
	Quality MaestroQuality
	// Target video length in seconds (1–600, i.e. up to 10 minutes). Billed by duration: credits ≈ 0.85 × duration ×
	Duration int
	// How to route the video — a hint; the AI director still decides the final structure. `auto` (default) = the dir
	Scenario MaestroScenario
	// Optional reference media (image / video / audio URLs) the agent can use — e.g. a product shot or logo to featu
	FileURLs []string
	// Required when `action` is remix / edit / extend: the task_id of the previous video to start from.
	RefTaskID string
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Async submits without blocking; poll the returned handle. Defaults true.
	Async *bool
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r MaestroGenerateRequest) toBody() map[string]any {
	body := map[string]any{}
	body["prompt"] = r.Prompt
	if r.Langs == nil {
		body["langs"] = []string{"zh-cn"}
	} else {
		body["langs"] = r.Langs
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
	if r.Action != "" {
		body["action"] = r.Action
	} else {
		body["action"] = "generate"
	}
	if r.Aspect != "" {
		body["aspect"] = r.Aspect
	} else {
		body["aspect"] = "9:16"
	}
	if r.Quality != "" {
		body["quality"] = r.Quality
	} else {
		body["quality"] = "standard"
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
	if r.FileURLs != nil {
		body["file_urls"] = r.FileURLs
	}
	if r.RefTaskID != "" {
		body["ref_task_id"] = r.RefTaskID
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

func (r MaestroGenerateRequest) validate() error {
	action := r.Action
	if action == "" {
		action = MaestroActionGenerate
	}
	quality := r.Quality
	if quality == "" {
		quality = MaestroQualityStandard
	}
	scenario := r.Scenario
	if scenario == "" {
		scenario = MaestroScenarioAuto
	}
	duration := r.Duration
	if duration == 0 {
		duration = 30
	}
	if action != MaestroActionGenerate && action != MaestroActionRemix && action != MaestroActionEdit && action != MaestroActionExtend {
		return fmt.Errorf("action must be generate, remix, edit, or extend")
	}
	if action != MaestroActionGenerate && r.RefTaskID == "" {
		return fmt.Errorf("ref_task_id is required when action is remix, edit, or extend")
	}
	if quality != MaestroQualityLite && quality != MaestroQualityStandard && quality != MaestroQualityPro {
		return fmt.Errorf("quality must be lite, standard, or pro")
	}
	if r.Langs != nil && (len(r.Langs) == 0 || len(r.Langs) > 4) {
		return fmt.Errorf("langs must contain between 1 and 4 languages")
	}
	if duration < 5 || duration > 300 {
		return fmt.Errorf("duration must be an integer between 5 and 300")
	}
	if quality == MaestroQualityLite && (duration > 30 || (action != MaestroActionGenerate && action != MaestroActionEdit)) {
		return fmt.Errorf("lite supports generate/edit actions and durations up to 30 seconds")
	}
	if quality == MaestroQualityStandard && (duration > 120 || action == MaestroActionExtend) {
		return fmt.Errorf("standard supports generate/remix/edit actions and durations up to 120 seconds")
	}
	allowed := map[MaestroQuality]map[MaestroScenario]bool{
		MaestroQualityLite:     {MaestroScenarioAuto: true, MaestroScenarioNarrated: true, MaestroScenarioCaptions: true},
		MaestroQualityStandard: {MaestroScenarioAuto: true, MaestroScenarioNarrated: true, MaestroScenarioCaptions: true, MaestroScenarioAvatar: true},
		MaestroQualityPro:      {MaestroScenarioAuto: true, MaestroScenarioNarrated: true, MaestroScenarioCaptions: true, MaestroScenarioAvatar: true, MaestroScenarioDrama: true},
	}
	if scenario != MaestroScenarioAuto && scenario != MaestroScenarioNarrated && scenario != MaestroScenarioCaptions && scenario != MaestroScenarioAvatar && scenario != MaestroScenarioDrama {
		return fmt.Errorf("scenario must be auto, narrated, captions, avatar, or drama")
	}
	if !allowed[quality][scenario] {
		return fmt.Errorf("%s scenario requires a higher quality tier", scenario)
	}
	if (scenario == MaestroScenarioCaptions || scenario == MaestroScenarioAvatar) && len(r.FileURLs) == 0 {
		return fmt.Errorf("file_urls is required for the %s scenario", scenario)
	}
	return nil
}

// Generate Maestro Video Generation API
func (c *Maestro) Generate(ctx context.Context, req MaestroGenerateRequest) (*TaskHandle, error) {
	if err := req.validate(); err != nil {
		return nil, err
	}
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
