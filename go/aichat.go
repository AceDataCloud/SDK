package acedatacloud

import "context"

// AIChat2Model is a model accepted by the v2 AI dialogue API.
type AIChat2Model string

const (
	AIChat2ModelGemini37Flash       AIChat2Model = "gemini-3.7-flash"
	AIChat2ModelGemini36Flash       AIChat2Model = "gemini-3.6-flash"
	AIChat2ModelGemini35Flash       AIChat2Model = "gemini-3.5-flash"
	AIChat2ModelGemini35FlashLite   AIChat2Model = "gemini-3.5-flash-lite"
	AIChat2ModelGemini31FlashLite   AIChat2Model = "gemini-3.1-flash-lite"
	AIChat2ModelGemini31ProPreview  AIChat2Model = "gemini-3.1-pro-preview"
	AIChat2ModelGemini3FlashPreview AIChat2Model = "gemini-3-flash-preview"
	AIChat2ModelGemini25Pro         AIChat2Model = "gemini-2.5-pro"
	AIChat2ModelGemini25Flash       AIChat2Model = "gemini-2.5-flash"
	AIChat2ModelGemini25FlashLite   AIChat2Model = "gemini-2.5-flash-lite"
)

// AIChatResource exposes the AI dialogue endpoints.
type AIChatResource struct {
	t *transport
}

// AIChatRequest is the input to AIChat.Create.
type AIChatRequest struct {
	ID         string
	Model      string
	Question   string
	Preset     string
	Stateful   *bool
	References []string
	Extra      map[string]any
}

func (r AIChatRequest) toBody() map[string]any {
	body := map[string]any{"model": r.Model, "question": r.Question}
	if r.ID != "" {
		body["id"] = r.ID
	}
	if r.Preset != "" {
		body["preset"] = r.Preset
	}
	if r.Stateful != nil {
		body["stateful"] = *r.Stateful
	}
	if r.References != nil {
		body["references"] = r.References
	}
	for key, value := range r.Extra {
		if _, exists := body[key]; !exists {
			body[key] = value
		}
	}
	return body
}

// AIChatV2Request is the input to AIChat.CreateV2.
type AIChatV2Request struct {
	Action            string
	ID                string
	Model             AIChat2Model
	Question          string
	Message           any
	Stateful          *bool
	References        []string
	Preset            string
	MaxTurns          int
	Async             *bool
	CallbackURL       string
	AllowedSkills     []string
	AllowedMCPServers []string
	UnattendedPolicy  map[string]any
	ToolResults       []map[string]any
	Messages          []map[string]any
	Title             string
	UserID            string
	ApplicationID     string
	ModelGroup        string
	Offset            int
	Limit             int
	Extra             map[string]any
}

func (r AIChatV2Request) toBody() map[string]any {
	body := map[string]any{"model": r.Model}
	optional := map[string]any{
		"action":              r.Action,
		"id":                  r.ID,
		"question":            r.Question,
		"message":             r.Message,
		"stateful":            r.Stateful,
		"references":          r.References,
		"preset":              r.Preset,
		"max_turns":           r.MaxTurns,
		"async":               r.Async,
		"callback_url":        r.CallbackURL,
		"allowed_skills":      r.AllowedSkills,
		"allowed_mcp_servers": r.AllowedMCPServers,
		"unattended_policy":   r.UnattendedPolicy,
		"tool_results":        r.ToolResults,
		"messages":            r.Messages,
		"title":               r.Title,
		"user_id":             r.UserID,
		"application_id":      r.ApplicationID,
		"model_group":         r.ModelGroup,
		"offset":              r.Offset,
		"limit":               r.Limit,
	}
	for key, value := range optional {
		switch typed := value.(type) {
		case nil:
			continue
		case string:
			if typed == "" {
				continue
			}
		case int:
			if typed == 0 {
				continue
			}
		case *bool:
			if typed == nil {
				continue
			}
			value = *typed
		case []string:
			if typed == nil {
				continue
			}
		case []map[string]any:
			if typed == nil {
				continue
			}
		case map[string]any:
			if typed == nil {
				continue
			}
		}
		body[key] = value
	}
	for key, value := range r.Extra {
		if _, exists := body[key]; !exists {
			body[key] = value
		}
	}
	return body
}

// Create sends a request to /aichat/conversations.
func (c *AIChatResource) Create(ctx context.Context, req AIChatRequest) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{Method: "POST", Path: "/aichat/conversations", Body: req.toBody()})
}

// CreateV2 sends a request to /aichat2/conversations.
func (c *AIChatResource) CreateV2(ctx context.Context, req AIChatV2Request) (map[string]any, error) {
	return c.t.do(ctx, requestOpts{Method: "POST", Path: "/aichat2/conversations", Body: req.toBody()})
}
