// Code generated from the platform OpenAPI spec. DO NOT EDIT.
// Regenerate with: python scripts/generate_providers.py

package acedatacloud

import (
	"context"
	"fmt"
)

// Minimax is the minimax provider client.
type Minimax struct {
	t *transport
}

// MinimaxGenerateRequest is the input to minimax.Generate.
type MinimaxGenerateRequest struct {
	// Minimax Videos Model
	Model string
	// Minimax Videos Content
	Content []map[string]any
	// Minimax Videos Resolution
	Resolution string
	// Minimax Videos Duration
	Duration int
	// Minimax Videos Ratio
	Ratio string
	// Async submits without blocking; poll the returned handle. Defaults true.
	Async *bool
	// CallbackURL optionally receives the completion webhook.
	CallbackURL string
	// Extra fields merged into the request body.
	Extra map[string]any
}

func (r MinimaxGenerateRequest) toBody() map[string]any {
	body := map[string]any{}
	body["model"] = r.Model
	body["content"] = r.Content
	body["resolution"] = r.Resolution
	body["duration"] = r.Duration
	if r.Ratio != "" {
		body["ratio"] = r.Ratio
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

func validateMinimaxContentItem(item map[string]any) error {
	kind, _ := item["type"].(string)
	switch kind {
	case "text":
		text, _ := item["text"].(string)
		if text == "" {
			return fmt.Errorf("minimax.content item with type='text' requires non-empty text")
		}
		return nil
	case "image_url":
		imageURL, _ := item["image_url"].(map[string]any)
		if _, ok := imageURL["url"].(string); !ok {
			return fmt.Errorf("minimax.content item with type='image_url' requires image_url.url")
		}
		if role, ok := item["role"].(string); ok && role != "" {
			if role != "first_frame" && role != "last_frame" && role != "reference_image" {
				return fmt.Errorf("minimax.content item with type='image_url' role must be first_frame, last_frame, or reference_image")
			}
		}
		return nil
	case "video_url":
		videoURL, _ := item["video_url"].(map[string]any)
		if _, ok := videoURL["url"].(string); !ok {
			return fmt.Errorf("minimax.content item with type='video_url' requires video_url.url")
		}
		if role, _ := item["role"].(string); role != "reference_video" {
			return fmt.Errorf("minimax.content item with type='video_url' requires role='reference_video'")
		}
		return nil
	case "audio_url":
		audioURL, _ := item["audio_url"].(map[string]any)
		if _, ok := audioURL["url"].(string); !ok {
			return fmt.Errorf("minimax.content item with type='audio_url' requires audio_url.url")
		}
		if role, _ := item["role"].(string); role != "reference_audio" {
			return fmt.Errorf("minimax.content item with type='audio_url' requires role='reference_audio'")
		}
		return nil
	default:
		return fmt.Errorf("minimax.content item type must be one of: text, image_url, video_url, audio_url")
	}
}

func validateMinimaxGenerateRequest(req MinimaxGenerateRequest) error {
	if len(req.Content) == 0 {
		return fmt.Errorf("minimax.content must contain at least one item")
	}
	for _, item := range req.Content {
		if err := validateMinimaxContentItem(item); err != nil {
			return err
		}
	}
	if req.Duration < 4 || req.Duration > 15 {
		return fmt.Errorf("minimax.duration must be between 4 and 15 seconds")
	}
	return nil
}

// Generate Minimax Videos
func (c *Minimax) Generate(ctx context.Context, req MinimaxGenerateRequest) (*TaskHandle, error) {
	if err := validateMinimaxGenerateRequest(req); err != nil {
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
