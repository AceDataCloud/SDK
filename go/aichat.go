package acedatacloud

import "context"

// AiChatResource groups AceDataCloud AI chat endpoints.
type AiChatResource struct{ t *transport }

// AiChatCreateRequest is the input to /aichat/conversations.
type AiChatCreateRequest struct {
	Model      string
	Question   string
	ID         string
	Preset     string
	Stateful   *bool
	References []string
	Extra      map[string]any
}

func (r AiChatCreateRequest) toBody() map[string]any {
	body := map[string]any{
		"model":    r.Model,
		"question": r.Question,
	}
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
	for k, v := range r.Extra {
		if _, exists := body[k]; !exists {
			body[k] = v
		}
	}
	return body
}

// Create starts a conversation through /aichat/conversations.
func (r *AiChatResource) Create(ctx context.Context, req AiChatCreateRequest) (map[string]any, error) {
	return r.t.do(ctx, requestOpts{Method: "POST", Path: "/aichat/conversations", Body: req.toBody()})
}

// AiChatV2CreateRequest is the input to /aichat2/conversations.
type AiChatV2CreateRequest struct {
	Model             string
	Action            string
	ID                string
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
	Offset            *int
	Limit             *int
	Extra             map[string]any
}

func (r AiChatV2CreateRequest) toBody() map[string]any {
	body := map[string]any{"model": r.Model}
	if r.Action != "" {
		body["action"] = r.Action
	}
	if r.ID != "" {
		body["id"] = r.ID
	}
	if r.Question != "" {
		body["question"] = r.Question
	}
	if r.Message != nil {
		body["message"] = r.Message
	}
	if r.Stateful != nil {
		body["stateful"] = *r.Stateful
	}
	if r.References != nil {
		body["references"] = r.References
	}
	if r.Preset != "" {
		body["preset"] = r.Preset
	}
	if r.MaxTurns != 0 {
		body["max_turns"] = r.MaxTurns
	}
	if r.Async != nil {
		body["async"] = *r.Async
	}
	if r.CallbackURL != "" {
		body["callback_url"] = r.CallbackURL
	}
	if r.AllowedSkills != nil {
		body["allowed_skills"] = r.AllowedSkills
	}
	if r.AllowedMCPServers != nil {
		body["allowed_mcp_servers"] = r.AllowedMCPServers
	}
	if r.UnattendedPolicy != nil {
		body["unattended_policy"] = r.UnattendedPolicy
	}
	if r.ToolResults != nil {
		body["tool_results"] = r.ToolResults
	}
	if r.Messages != nil {
		body["messages"] = r.Messages
	}
	if r.Title != "" {
		body["title"] = r.Title
	}
	if r.UserID != "" {
		body["user_id"] = r.UserID
	}
	if r.ApplicationID != "" {
		body["application_id"] = r.ApplicationID
	}
	if r.ModelGroup != "" {
		body["model_group"] = r.ModelGroup
	}
	if r.Offset != nil {
		body["offset"] = *r.Offset
	}
	if r.Limit != nil {
		body["limit"] = *r.Limit
	}
	for k, v := range r.Extra {
		if _, exists := body[k]; !exists {
			body[k] = v
		}
	}
	return body
}

// CreateV2 starts or manages a conversation through /aichat2/conversations.
func (r *AiChatResource) CreateV2(ctx context.Context, req AiChatV2CreateRequest) (map[string]any, error) {
	return r.t.do(ctx, requestOpts{Method: "POST", Path: "/aichat2/conversations", Body: req.toBody()})
}
