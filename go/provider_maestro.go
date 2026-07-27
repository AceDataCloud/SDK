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
	// Output languages, e.g. ["zh-cn", "en"]. The first is the primary language; each additional one reuses the visu
	Langs []string
	// Optional visual-style preset — expressed through typography, palette, motion, image treatment and pacing. Orth
	Style string
	// Optional narration voice — the **timbre** of the voiceover, independent of language. `auto` (default) lets the
	Voice string
	// generate = a new video. remix / edit / extend = iterate on a previous video (require `ref_task_id`).
	Action string
	// Output aspect ratio (hint — the agent may follow the prompt).
	Aspect string
	// Production tier, a multiplier on the duration-based price. `draft` = a fast rough cut for previewing the idea
	Quality string
	// Target video length in seconds (1–600, i.e. up to 10 minutes). Billed by duration: credits ≈ 0.85 × duration ×
	Duration int
	// How to route the video — a hint; the AI director still decides the final structure. `auto` (default) = the dir
	Scenario string
	// Optional reference media (image / video / audio URLs) the agent can use — e.g. a product shot or logo to featu
	FileURLs []string
	// Required when `action` is remix / edit / extend: the task_id of the previous video to start from.
	RefTaskID string
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r MaestroGenerateRequest) toBody() map[string]any {
	body := map[string]any{}
	body["prompt"] = r.Prompt
	body["langs"] = r.Langs
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
	for k, v := range r.Extra {
		if _, exists := body[k]; !exists {
			body[k] = v
		}
	}
	return body
}

// Generate Maestro Video Generation API
func (c *Maestro) Generate(ctx context.Context, req MaestroGenerateRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/maestro/videos",
		Body:   req.toBody(),
	})
}

// MaestroEstimatesRequest is the input to maestro.Estimates.
type MaestroEstimatesRequest struct {
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r MaestroEstimatesRequest) toBody() map[string]any {
	body := map[string]any{}
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

// Estimates Call /maestro/estimates.
func (c *Maestro) Estimates(ctx context.Context, req MaestroEstimatesRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{
		Method: "POST",
		Path:   "/maestro/estimates",
		Body:   req.toBody(),
	})
}
